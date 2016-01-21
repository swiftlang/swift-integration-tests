# Trivial test for Swift build.
#
# No swift-build in 2.2
# REQUIRES: disabled
#
# Make a sandbox dir.
# RUN: rm -rf %t.dir
# RUN: mkdir -p %t.dir/tool
# RUN: touch %t.dir/tool/Package.swift
# RUN: echo 'print("HI")' > %t.dir/tool/main.swift
# RUN: %{swift} build --chdir %t.dir/tool -v > %t.build-log

# Check the build log.
#
# RUN: %{FileCheck} --check-prefix CHECK-BUILD-LOG --input-file %t.build-log %s
#
# CHECK-BUILD-LOG: swiftc{{.*}} -module-name tool

# Verify that the tool exists and works.
#
# RUN: test -x %t.dir/tool/.build/debug/tool
# RUN: %t.dir/tool/.build/debug/tool > %t.out
# RUN: %{FileCheck} --check-prefix CHECK-TOOL-OUTPUT --input-file %t.out %s
#
# CHECK-TOOL-OUTPUT: HI
