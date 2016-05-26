
# Test `swift package init` (library)

## Create a new package with an executable target.

```
RUN: rm -rf %t.dir
RUN: mkdir -p %t.dir/Project
RUN: %{swift} package --chdir %t.dir/Project init --type library
RUN: %{swift} build --chdir %t.dir/Project &> %t.build-log
RUN: %{swift} test --chdir %t.dir/Project &> %t.test-log
```

## Check the build log.

```
RUN: %{FileCheck} --check-prefix CHECK-BUILD-LOG --input-file %t.build-log %s
```

```
CHECK-BUILD-LOG: Compile Swift Module 'Project'
```

## Check the test log.

```
RUN: %{FileCheck} --check-prefix CHECK-TEST-LOG --input-file %t.test-log %s
```

```
CHECK-TEST-LOG: Compile Swift Module 'ProjectTestSuite'
CHECK-TEST-LOG: Test Suite 'All tests' passed
CHECK-TEST-LOG-NEXT: Executed 1 test
```

## Check there were no compile errors or warnings.

```
RUN: %{FileCheck} --check-prefix CHECK-NO-WARNINGS-OR-ERRORS --input-file %t.build-log %s
RUN: %{FileCheck} --check-prefix CHECK-NO-WARNINGS-OR-ERRORS --input-file %t.test-log %s
```

```
CHECK-NO-WARNINGS-OR-ERRORS-NOT: warning
CHECK-NO-WARNINGS-OR-ERRORS-NOT: error
```
