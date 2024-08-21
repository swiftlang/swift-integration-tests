
# Test `swift package init` (library)

## Create a new package with an executable target.

```
RUN: rm -rf %t.dir
RUN: mkdir -p %t.dir/Project
RUN: %{swift-package} --package-path %t.dir/Project init --type library --enable-xctest --enable-swift-testing
RUN: %{swift-build} --package-path %t.dir/Project 2>&1 | tee %t.build-log
RUN: %{swift-test} --package-path %t.dir/Project --enable-xctest --disable-swift-testing 2>&1 | tee %t.xctest-log
RUN: %{swift-test} --package-path %t.dir/Project --disable-xctest --enable-swift-testing 2>&1 | tee %t.swift-testing-log
```

## Check the build log.

```
RUN: %{FileCheck} --check-prefix CHECK-BUILD-LOG --input-file %t.build-log %s
```

```
CHECK-BUILD-LOG: Compiling {{.*}}Project{{.*}}
```

## Check the XCTest log.

```
RUN: %{FileCheck} --check-prefix CHECK-XCTEST-LOG --input-file %t.xctest-log %s
```

```
CHECK-XCTEST-LOG: Compiling {{.*}}ProjectTests{{.*}}
CHECK-XCTEST-LOG: Test Suite 'All tests' passed
CHECK-XCTEST-LOG-NEXT: Executed 1 test
```

## Check the Swift Testing log.

```
RUN: %{FileCheck} --check-prefix CHECK-SWIFT-TESTING-LOG --input-file %t.swift-testing-log %s
```

```
CHECK-SWIFT-TESTING-LOG: Test run started.
CHECK-SWIFT-TESTING-LOG-NEXT: Test run with 1 test passed after {{.*}} seconds.
```

## Check there were no compile errors or warnings.

```
RUN: %{FileCheck} --check-prefix CHECK-NO-WARNINGS-OR-ERRORS --input-file %t.build-log %s
RUN: %{FileCheck} --check-prefix CHECK-NO-WARNINGS-OR-ERRORS --input-file %t.xctest-log %s
RUN: %{FileCheck} --check-prefix CHECK-NO-WARNINGS-OR-ERRORS --input-file %t.swift-testing-log %s
```

```
CHECK-NO-WARNINGS-OR-ERRORS-NOT: warning
CHECK-NO-WARNINGS-OR-ERRORS-NOT: error
```
