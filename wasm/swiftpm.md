# SwiftPM checks for Wasm Swift SDKs

This test can only run on Linux CI as we only build Swift SDK for Wasm on Linux CI nodes.

```
REQUIRES: platform=Linux
```

1. Prepare the test environment:

```
RUN: rm -rf %t.dir
RUN: mkdir -p %t.dir/swift-sdks
```

2. Let's install Swift SDK for Wasm:

```
RUN: %{swift-sdk} list --swift-sdks-path %t.dir/swift-sdks | %{FileCheck} --check-prefix CHECK-SDK-LIST-BEFORE %s
CHECK-SDK-LIST-BEFORE: No Swift SDKs are currently installed.
RUN: find "%{swift-sdk-generator_srcdir}/Bundles" -mindepth 1 -maxdepth 1 | xargs %{swift-sdk} install --swift-sdks-path %t.dir/swift-sdks | %{FileCheck} --check-prefix CHECK-SDK-INSTALL %s
CHECK-SDK-INSTALL: Swift SDK bundle at
CHECK-SDK-INSTALL: successfully installed as
RUN: %{swift-sdk} list --swift-sdks-path %t.dir/swift-sdks | grep wasm | wc -l | %{FileCheck} --check-prefix CHECK-SDK-LIST-AFTER %s
CHECK-SDK-LIST-AFTER: 2
```

3. Using a prepared basic package that exercises Swift stdlib and `import WASILibc`:

```
RUN: cp -r %S/Hello %t.dir
```

4. Building and running the prepared package:

    a) Non-embedded Swift SDK

    ```
    RUN: %{swift-sdk} list --swift-sdks-path %t.dir/swift-sdks | grep -v embedded | xargs %{swift-run} --swift-sdks-path %t.dir/swift-sdks --package-path %t.dir/Hello --swift-sdk | %{FileCheck} --check-prefix CHECK-RUN-OUTPUT %s
    CHECK-RUN-OUTPUT: Hello, world!
    CHECK-RUN-OUTPUT-NEXT: Hello from WASILibc!
    ```

    b) Embedded Swift SDK

    ```
    RUN: %{swift-sdk} list --swift-sdks-path %t.dir/swift-sdks | grep embedded | xargs %{swift-run} --swift-sdks-path %t.dir/swift-sdks --package-path %t.dir/Hello --swift-sdk | %{FileCheck} --check-prefix CHECK-EMBEDDED-RUN-OUTPUT %s
    CHECK-EMBEDDED-RUN-OUTPUT: Hello, world!
    CHECK-EMBEDDED-RUN-OUTPUT-NEXT: Hello from WASILibc!
    ```

5. Building with code coverage enabled

    a) Non-embedded Swift SDK

    ```
    RUN: %{swift-sdk} list --swift-sdks-path %t.dir/swift-sdks | grep -v embedded | xargs %{swift-build} --enable-code-coverage -Xlinker -lwasi-emulated-getpid --swift-sdks-path %t.dir/swift-sdks --package-path %t.dir/Hello --swift-sdk | %{FileCheck} --check-prefix CHECK-COVERAGE-BUILD-OUTPUT %s
    CHECK-COVERAGE-BUILD-OUTPUT: Build complete!
    ```

    b) Embedded Swift SDK

    ```
    RUN: %{swift-sdk} list --swift-sdks-path %t.dir/swift-sdks | grep embedded | xargs %{swift-build} --enable-code-coverage -Xlinker -lwasi-emulated-getpid --swift-sdks-path %t.dir/swift-sdks --package-path %t.dir/Hello --swift-sdk | %{FileCheck} --check-prefix CHECK-EMBEDDED-COVERAGE-BUILD-OUTPUT %s
    CHECK-EMBEDDED-COVERAGE-BUILD-OUTPUT: Build complete!
    ```
