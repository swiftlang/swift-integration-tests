# Test the safety of `swift package update`.

Establish our sandbox.

```
RUN: rm -rf %t.dir
```

Create a dummy package.

```
RUN: mkdir -p %t.dir/Dep
RUN: %{swift} package -C %t.dir/Dep init --type library
RUN: git -C %t.dir/Dep init
RUN: git -C %t.dir/Dep add -A
RUN: git -C %t.dir/Dep config user.name "Test User"
RUN: git -C %t.dir/Dep config user.email "test@user.com"
RUN: git -C %t.dir/Dep commit -m "Initial commit."
RUN: git -C %t.dir/Dep tag 1.0.0
```

Create the test package.

```
RUN: mkdir -p %t.dir/Cmd
RUN: %{swift} package -C %t.dir/Cmd init --type executable
RUN: echo "import PackageDescription" >  %t.dir/Cmd/Package.swift
RUN: echo "let package = Package(" >>  %t.dir/Cmd/Package.swift
RUN: echo "  name: \"Cmd\"," >>  %t.dir/Cmd/Package.swift
RUN: echo "  dependencies: [.Package(url: \"../Dep\", Version(1,0,0))]" >>  %t.dir/Cmd/Package.swift
RUN: echo ")" >>  %t.dir/Cmd/Package.swift
```

Build the test package.

```
RUN: mkdir -p %t.dir/Cmd
RUN: %{swift} build -C %t.dir/Cmd &> %t.build-log
RUN: %{FileCheck} --check-prefix CHECK-BUILD-LOG --input-file %t.build-log %s

CHECK-BUILD-LOG: Compile Swift Module 'Cmd'
```

Validate we can run `--update`.

```
RUN: %{swift} package -C %t.dir/Cmd update
```

Modify the sources of the dependency.

```
RUN: test -f %t.dir/Cmd/Packages/Dep-1.0.0/Sources/Dep.swift
RUN: echo "INVALID CODE" >> %t.dir/Cmd/Packages/Dep-1.0.0/Sources/Dep.swift
```

Validate that `--update` errors out.

```
RUN: %{not} %{swift} package -C %t.dir/Cmd update
```

Stage the changes we made and verify it is still an error.

```
RUN: git -C %t.dir/Cmd/Packages/Dep-1.0.0 add Sources/Dep.swift
RUN: %{not} %{swift} package -C %t.dir/Cmd update
```

Validate we still have our modified source.

```
RUN: grep "INVALID CODE" %t.dir/Cmd/Packages/Dep-1.0.0/Sources/Dep.swift
```
