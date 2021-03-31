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

# RUN: %{python} -u %s %{sourcekit-lsp} %t.dir/pkg 2>&1 | tee %t.run-log
# RUN: %{FileCheck} --input-file %t.run-log %s

import argparse
import json
import os
import subprocess
import sys

class LspScript(object):
  def __init__(self):
    self.request_id = 0
    self.script = ''

  def request(self, method, params):
    body = json.dumps({
      'jsonrpc': '2.0',
      'id': self.request_id,
      'method': method,
      'params': params
    })
    self.request_id += 1
    self.script += 'Content-Length: {}\r\n\r\n{}'.format(len(body), body)

  def note(self, method, params):
    body = json.dumps({
      'jsonrpc': '2.0',
      'method': method,
      'params': params
    })
    self.script += 'Content-Length: {}\r\n\r\n{}'.format(len(body), body)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('sourcekit_lsp')
    parser.add_argument('package')
    args = parser.parse_args()

    lsp = LspScript()
    lsp.request('initialize', {
      'rootPath': args.package,
      'capabilities': {},
      'initializationOptions': {
        'listenToUnitEvents': False,
      }
    })

    main_swift = os.path.join(args.package, 'Sources', 'exec', 'main.swift')
    with open(main_swift, 'r') as f:
      main_swift_content = f.read()
    
    lsp.note('textDocument/didOpen', {
      'textDocument': {
        'uri': 'file://' + main_swift,
        'languageId': 'swift',
        'version': 0,
        'text': main_swift_content,
      }
    })

    lsp.request('workspace/_pollIndex', {})
    lsp.request('textDocument/definition', {
      'textDocument': { 'uri': 'file://' + main_swift },
      'position': { 'line': 3, 'character': 6}, ## zero-based
      })

    # CHECK: "result":[
    # CHECK-DAG: lib.swift
    # CHECK-DAG: "line":1
    # CHECK-DAG: "character":14
    # CHECK: ]

    lsp.request('textDocument/definition', {
      'textDocument': { 'uri': 'file://' + main_swift },
      'position': { 'line': 4, 'character': 0}, ## zero-based
      })

    # CHECK: "result":[
    # CHECK-DAG: clib.c
    # CHECK-DAG: "line":2
    # CHECK-DAG: "character":5
    # CHECK: ]

    lsp.request('textDocument/completion', {
      'textDocument': { 'uri': 'file://' + main_swift },
      'position': { 'line': 3, 'character': 6}, ## zero-based
      })
    # CHECK: "items":[
    # CHECK-DAG: "label":"foo()"
    # CHECK-DAG: "label":"self"
    # CHECK: ]

    clib_c = os.path.join(args.package, 'Sources', 'clib', 'clib.c')
    with open(clib_c, 'r') as f:
      clib_c_content = f.read()
    
    lsp.note('textDocument/didOpen', {
      'textDocument': {
        'uri': 'file://' + clib_c,
        'languageId': 'c',
        'version': 0,
        'text': clib_c_content,
      }
    })

    lsp.request('textDocument/completion', {
      'textDocument': { 'uri': 'file://' + clib_c },
      'position': { 'line': 2, 'character': 22}, ## zero-based
      })
    # CHECK: "items":[
    # CHECK-DAG: "insertText":"clib_func"
    # Missing "clib_other" from clangd on rebranch - rdar://73762053
    # DISABLED-DAG: "insertText":"clib_other"
    # CHECK: ]

    lsp.request('shutdown', {})
    lsp.note('exit', {})

    print('==== INPUT ====')
    print(lsp.script)
    print('')
    print('==== OUTPUT ====')

    skargs = [args.sourcekit_lsp, '--sync', '-Xclangd', '-sync']
    p = subprocess.Popen(skargs, stdin=subprocess.PIPE, stdout=subprocess.PIPE, universal_newlines=True)
    out, _ = p.communicate(lsp.script)
    print(out)
    print('')

    if p.returncode == 0:
      print('OK')
    else:
      print('error: sourcekit-lsp exited with code {}'.format(p.returncode))
      sys.exit(1)
    # CHECK: OK

if __name__ == "__main__":
    main()
