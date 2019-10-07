// Check that we can debug a Swift package.
//
// REQUIRES: rdar56054057
// Make a sandbox dir.
// RUN: rm -rf %t.dir
// RUN: mkdir -p %t.dir
// RUN: cp -r %S/* %t.dir/
//
// Check the build log.
// RUN: %{swift-build} --package-path %t.dir 2>&1 | tee %t.build-log
//
// Verify that the build worked.
// RUN: test -x %t.dir/.build/debug/exec
//
// RUN: %t.dir/.build/debug/exec > %t.out
// RUN: %{FileCheck} --check-prefix CHECK-APP-OUTPUT --input-file %t.out %s
// CHECK-APP-OUTPUT: 10
// CHECK-APP-OUTPUT-NEXT: OK
//
// Try debugging the application.
// RUN: %{lldb} %t.dir/.build/debug/exec -o "b core.swift:5" -o r -o "po value" -b &> %t.lldb
// RUN: %{FileCheck} --check-prefix CHECK-LLDB-LOG --input-file %t.lldb %s
// CHECK-LLDB-LOG: (lldb) po value
// CHECK-LLDB-LOG-NEXT: 5

