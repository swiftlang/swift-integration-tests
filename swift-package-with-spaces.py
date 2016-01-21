# Check a package with spaces.
#
# No swift-build in 2.2
# REQUIRES: disabled
#
# Make a sandbox dir.
# RUN: rm -rf %t.dir
# RUN: mkdir -p %t.dir/more\ spaces/special\ tool
# RUN: touch %t.dir/more\ spaces/special\ tool/Package.swift
# RUN: echo 'foo()' > %t.dir/more\ spaces/special\ tool/main.swift
# RUN: echo 'func foo() { print("HI") }' > %t.dir/more\ spaces/special\ tool/some\ file.swift
# RUN: %{swift} build --chdir %t.dir/more\ spaces/special\ tool -v > %t.build-log

# Check the build log.
#
# RUN: %{FileCheck} --check-prefix CHECK-BUILD-LOG --input-file %t.build-log %s
#
# CHECK-BUILD-LOG: swiftc{{.*}} -module-name specialtool {{.*}} "{{.*}}/more spaces/special tool/some file.swift"

# Verify that the tool exists and works.
#
# RUN: test -x %t.dir/more\ spaces/special\ tool/.build/debug/special\ tool
# RUN: %t.dir/more\ spaces/special\ tool/.build/debug/special\ tool > %t.out
# RUN: %{FileCheck} --check-prefix CHECK-TOOL-OUTPUT --input-file %t.out %s
#
# CHECK-TOOL-OUTPUT: HI
