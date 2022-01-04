
# REQUIRES: platform=Linux
# RUN: rm -rf %T && mkdir -p %t
# RUN: %{python} %s '%{package_path}' '%T' '%{readelf}'

# Test that all linux libraries that we provide do not have any load
# commands that are both writeable and executable.

import argparse
import re
import sys
import subprocess

# For each library, we want to run llvm-readelf on it and verify that none of
# the flag fields say that the load commands are both writable and
# executable. Our target outputs look like this:
#
# ----
# There are 7 program headers, starting at offset 64
#
# Program Headers:
#   Type           Offset   VirtAddr           PhysAddr           FileSiz  MemSiz   Flg Align
#   PHDR           0x000040 0x0000000000000040 0x0000000000000040 0x000188 0x000188 R   0x8
#   LOAD           0x000000 0x0000000000000000 0x0000000000000000 0x9839a0 0x9839a0 R E 0x1000
#   LOAD           0x983a60 0x0000000000984a60 0x0000000000984a60 0x07ad78 0x0a3da9 RW  0x1000
#   DYNAMIC        0x9b5b88 0x00000000009b6b88 0x00000000009b6b88 0x0002f0 0x0002f0 RW  0x8
#   GNU_EH_FRAME   0x95ecd4 0x000000000095ecd4 0x000000000095ecd4 0x024ccc 0x024ccc R   0x4
#   GNU_STACK      0x000000 0x0000000000000000 0x0000000000000000 0x000000 0x000000 RW  0x0
#   GNU_RELRO      0x983a60 0x0000000000984a60 0x0000000000984a60 0x0345a0 0x0345a0 RW  0x10
# ----
#
# TODO: Evaluate if parallelism helps here. We /could/ use libdispatch to work
# in parallel over all artifacts.
class ParseState(object):
    firstLine = 0
    programHeadersLine = 1
    dataHeader = 2
    data = 3

    def __init__(self, state=None):
        if state is None:
            state = ParseState.firstLine
        self.value = state

    @property
    def regex_string(self):
        if self.value == ParseState.firstLine:
            return "There are (\d+) program headers"
        if self.value == ParseState.programHeadersLine:
            return "Program Headers:"
        if self.value == ParseState.dataHeader:
            return "\\s+Type"
        if self.value == ParseState.data:
            name = "(\w+)"
            hex_pattern = "0x[0-9a-fA-F]+"
            ws = "\s"
            col = "{}+{}".format(ws, hex_pattern)
            return "^{ws}*{name}{col}{col}{col}{col}{col} (.+) 0x".format(**
                {'ws': ws, 'name': name, 'col': col})
        raise RuntimeError('Invalid ParseState value')

    @property
    def regex(self):
        return re.compile(self.regex_string)

    @property
    def next(self):
        if self.value == ParseState.firstLine:
            return ParseState(ParseState.programHeadersLine)
        if self.value == ParseState.programHeadersLine:
            return ParseState(ParseState.dataHeader)
        if self.value == ParseState.dataHeader:
            return ParseState(ParseState.data)
        if self.value == ParseState.data:
            return self
        raise RuntimeError('Invalid ParseState value')

    def matches(self, input_string):
        return self.regex.match(input_string)

def process_library(args, lib):
    assert(len(lib) > 0)

    numberOfLines = None
    numberOfLinesSeen = 0

    print("Visiting lib: {}".format(lib))
    lines = list(reversed(subprocess.check_output([args.read_elf, "--program-headers", lib], universal_newlines=True).split("\n")[:-1]))
    p = ParseState()

    # Until we finish parsing or run out of lines to parse...
    while len(lines) > 0:
        l = lines.pop()
        print("DUMP: '{}'".format(l))
        assert(p is not None)
        curState = p

        m = curState.matches(l)
        if m is None:
            continue

        p = curState.next
        if curState.value == ParseState.firstLine:
            numberOfLines = int(m.group(1))
            continue

        if curState.value == ParseState.programHeadersLine:
            continue

        if curState.value == ParseState.dataHeader:
            continue

        if curState.value == ParseState.data:
            val = m.group(1)
            if val == "LOAD":
                flags = m.group(2)
                print("Found LOAD command! Flags: '{}'. Full match: '{}'".format(flags, l))
                if "W" in flags and "E" in flags:
                    raise RuntimeError("Found a load command that loads something executable and writeable")

            # If we haven't seen enough lines, continue.
            assert(numberOfLines is not None)
            if numberOfLinesSeen != numberOfLines - 1:
                numberOfLinesSeen += 1
                continue

            # If we have seen enough lines, be sure to not only break out
            # of the switch, but additionally break out of the whole
            # parsing loop. We could go through the rest of the output from
            # llvm-readelf, but there isn't any point.
            p = None
            break

    # If we ran out of lines to parse without finishing parsing, we failed.
    assert(p is None)
    assert(numberOfLines is not None)
    assert(numberOfLinesSeen == numberOfLines - 1)

def get_libraries(package_path):
    cmd = [
        "/usr/bin/find",
        package_path,
        "-iname",
        "*.so"
    ]
    return subprocess.check_output(cmd, universal_newlines=True).split("\n")[:-1]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('package_path')
    parser.add_argument('tmp_dir')
    parser.add_argument('read_elf')
    args = parser.parse_args()

    libraries = get_libraries(args.package_path)
    for l in libraries:

          # When linking the swiftCompilerModules to lldb, the text segment
          # gets RWE for some reason.
          # TODO: remove this workaround once rdar://87078244 is fixed
          if "liblldb.so" in l:
                continue

          process_library(args, l)
    sys.exit(0)

if __name__ == "__main__":
    main()
