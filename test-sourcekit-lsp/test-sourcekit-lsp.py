# Canary test for sourcekit-lsp, covering interaction with swiftpm and toolchain
# language services.

# REQUIRES: have-sourcekit-lsp

# Make a sandbox dir.
# RUN: rm -rf %t.dir
# RUN: mkdir -p %t.dir
# RUN: cp -r %S/pkg %t.dir/

# RUN: env SWIFTPM_ENABLE_CLANG_INDEX_STORE=1 %{swift-build} --package-path %t.dir/pkg -Xswiftc -index-ignore-system-modules -v 2>&1 | tee %t.build-log
# RUN: %{FileCheck} --check-prefix CHECK-BUILD-LOG --input-file %t.build-log %s
# CHECK-BUILD-LOG-NOT: error:

# RUN: %{python} -u %s %{sourcekit-lsp} %t.dir/pkg | tee %t.run-log
# RUN: %{FileCheck} --input-file %t.run-log %s

from typing import Dict
import argparse
import json
import subprocess
import sys
from pathlib import Path
import re


class LspConnection:
    def __init__(self, server_path: str):
        self.request_id = 0
        self.process = subprocess.Popen(
            [server_path],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            encoding="utf-8",
        )

    def send_data(self, dict: Dict[str, object]):
        """
        Encode the given dict as JSON and send it to the LSP server with the 'Content-Length' header.
        """
        assert self.process.stdin
        body = json.dumps(dict)
        data = "Content-Length: {}\r\n\r\n{}".format(len(body), body)
        self.process.stdin.write(data)
        self.process.stdin.flush()

    def read_message_from_lsp_server(self) -> str:
        """
        Read a single message sent from the LSP server to the client.
        This can be a request reply, notification or request sent from the server to the client.
        """
        assert self.process.stdout
        # Read Content-Length: 123\r\n
        # Note: Even though the Content-Length header ends with \r\n, `readline` returns it with a single \n.
        header = self.process.stdout.readline()
        match = re.match(r"Content-Length: ([0-9]+)\n$", header)
        assert match, f"Expected Content-Length header, got '{header}'"

        # The Content-Length header is followed by an empty line
        empty_line = self.process.stdout.readline()
        assert empty_line == "\n", f"Expected empty line, got '{empty_line}'"

        # Read the actual response
        return self.process.stdout.read(int(match.group(1)))

    def read_request_reply_from_lsp_server(self, request_id: int) -> str:
        """
        Read all messages sent from the LSP server until we see a request reply.
        Assert that this request reply was for the given request_id and return it.
        """
        message = self.read_message_from_lsp_server()
        message_obj = json.loads(message)
        if "result" not in message_obj:
            # We received a message that wasn't the request reply. 
            # Log it, ignore it and wait for the next message.
            print("Received message")
            print(message)
            return self.read_request_reply_from_lsp_server(request_id)
        # We always wait for a request reply before sending the next request.
        # If we received a request reply, it should thus have the request ID of the last request that we sent.
        assert (
            message_obj["id"] == self.request_id
        ), f"Expected response for request {self.request_id}, got '{message}'"
        return message

    def send_request(self, method: str, params: Dict[str, object]) -> str:
        """
        Send a request of the given method and parameters to the LSP server and wait for the response.
        """
        self.request_id += 1

        self.send_data(
            {
                "jsonrpc": "2.0",
                "id": self.request_id,
                "method": method,
                "params": params,
            }
        )

        return self.read_request_reply_from_lsp_server(self.request_id)

    def send_notification(self, method: str, params: Dict[str, object]):
        """
        Send a notification to the LSP server. There's nothing to wait for in response
        """
        self.send_data({"jsonrpc": "2.0", "method": method, "params": params})

    def wait_for_exit(self, timeout: int) -> int:
        """
        Wait for the LSP server to terminate.
        """
        return self.process.wait(timeout)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("sourcekit_lsp")
    parser.add_argument("package")
    args = parser.parse_args()

    package_dir = Path(args.package)
    main_swift = package_dir / "Sources" / "exec" / "main.swift"
    clib_c = package_dir / "Sources" / "clib" / "clib.c"

    connection = LspConnection(args.sourcekit_lsp)
    connection.send_request(
        "initialize",
        {
            "rootPath": args.package,
            "capabilities": {},
            "initializationOptions": {
                "listenToUnitEvents": False,
            },
        },
    )

    connection.send_notification(
        "textDocument/didOpen",
        {
            "textDocument": {
                "uri": f"file://{main_swift}",
                "languageId": "swift",
                "version": 0,
                "text": main_swift.read_text(),
            }
        },
    )

    connection.send_request("workspace/_pollIndex", {})
    foo_definition_response = connection.send_request(
        "textDocument/definition",
        {
            "textDocument": {"uri": f"file://{main_swift}"},
            "position": {"line": 3, "character": 6},  ## zero-based
        },
    )
    print("foo() definition response")
    # CHECK-LABEL: foo() definition response
    print(foo_definition_response)
    # CHECK: "result":[
    # CHECK-DAG: lib.swift
    # CHECK-DAG: "line":1
    # CHECK-DAG: "character":14
    # CHECK: ]

    clib_func_definition_response = connection.send_request(
        "textDocument/definition",
        {
            "textDocument": {"uri": f"file://{main_swift}"},
            "position": {"line": 4, "character": 0},  ## zero-based
        },
    )

    print("clib_func() definition response")
    # CHECK-LABEL: clib_func() definition response
    print(clib_func_definition_response)
    # CHECK: "result":[
    # CHECK-DAG: clib.c
    # CHECK-DAG: "line":2
    # CHECK-DAG: "character":5
    # CHECK: ]

    swift_completion_response = connection.send_request(
        "textDocument/completion",
        {
            "textDocument": {"uri": f"file://{main_swift}"},
            "position": {"line": 3, "character": 6},  ## zero-based
        },
    )
    print("Swift completion response")
    # CHECK-LABEL: Swift completion response
    print(swift_completion_response)
    # CHECK: "items":[
    # CHECK-DAG: "label":"foo()"
    # CHECK-DAG: "label":"self"
    # CHECK: ]

    connection.send_notification(
        "textDocument/didOpen",
        {
            "textDocument": {
                "uri": f"file://{clib_c}",
                "languageId": "c",
                "version": 0,
                "text": clib_c.read_text(),
            }
        },
    )

    c_completion_response = connection.send_request(
        "textDocument/completion",
        {
            "textDocument": {"uri": f"file://{clib_c}"},
            "position": {"line": 2, "character": 22},  ## zero-based
        },
    )
    print("C completion response")
    # CHECK-LABEL: C completion response
    print(c_completion_response)
    # CHECK: "items":[
    # CHECK-DAG: "insertText":"clib_func"
    # Missing "clib_other" from clangd on rebranch - rdar://73762053
    # DISABLED-DAG: "insertText":"clib_other"
    # CHECK: ]

    connection.send_request("shutdown", {})
    connection.send_notification("exit", {})

    return_code = connection.wait_for_exit(timeout=1)
    if return_code == 0:
        print("OK")
    else:
        print(f"error: sourcekit-lsp exited with code {return_code}")
        sys.exit(1)
    # CHECK: OK


if __name__ == "__main__":
    main()
