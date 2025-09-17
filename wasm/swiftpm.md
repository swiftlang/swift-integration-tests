# SwiftPM checks for Wasm Swift SDKs

This test can only run on Linux CI as we only build Swift SDK for Wasm on Linux CI nodes.

```
REQUIRES: platform=Linux
```

1. Let's install Swift SDK for Wasm first:

```
RUN: %{swift-sdk} list | %{FileCheck} --check-prefix CHECK-SDK-LIST-BEFORE %s
CHECK-SDK-LIST-BEFORE: No Swift SDKs are currently installed.
RUN: find "%{swift-sdk-generator_srcdir}/Bundles" -mindepth 1 -maxdepth 1 | xargs %{swift-sdk} install | %{FileCheck} --check-prefix CHECK-SDK-INSTALL %s
CHECK-SDK-INSTALL: Swift SDK bundle at
CHECK-SDK-INSTALL: successfully installed as
RUN: %{swift-sdk} list | grep wasm | wc -l | %{FileCheck} --check-prefix CHECK-SDK-LIST-AFTER %s
CHECK-SDK-LIST-AFTER: 2
```

2. Creating a package from `init` template:

```
RUN: rm -rf %t.dir
RUN: mkdir -p %t.dir
RUN: cp -r %S/Hello %t.dir
```

3. Building and running prepared `"Hello, world!"` executable from the newly created package:

    a) Non-embedded Swift SDK

    ```
    RUN: %{swift-sdk} list | grep -v embedded | xargs %{swift-run} --package-path %t.dir/Hello --swift-sdk | %{FileCheck} --check-prefix CHECK-RUN-OUTPUT %s
    CHECK-RUN-OUTPUT: Hello, world!
    CHECK-RUN-OUTPUT-NEXT: Hello from WASILibc!
    ```

    b) Embedded Swift SDK

    ```
    RUN: %{swift-sdk} list | grep embedded | xargs %{swift-run} --package-path %t.dir/Hello --swift-sdk | %{FileCheck} --check-prefix CHECK-EMBEDDED-RUN-OUTPUT %s
    CHECK-EMBEDDED-RUN-OUTPUT: Hello, world!
    CHECK-EMBEDDED-RUN-OUTPUT-NEXT: Hello from WASILibc!
    ```

4. Running tests from the newly created package:

    a) Non-embedded Swift SDK

    ```
    RUN: %{swift-sdk} list | grep -v embedded | xargs %{swift-test} --package-path %t.dir/Hello --swift-sdk | %{FileCheck} --check-prefix CHECK-RUN-OUTPUT %s
    ```


5. Clean up installed Swift SDK:

```
RUN: find %{swiftpm_homedir}/ -d 1 | xargs rm -rf
RUN: %{swift-sdk} list | %{FileCheck} --check-prefix CHECK-SDK-LIST-FINAL %s
CHECK-SDK-LIST-FINAL: No Swift SDKs are currently installed.
```
