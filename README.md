Swift Package Tests
===================

Automated tests for validating the generated Swift snapshots behave correctly.

Usage
-----

You are expected to check this repository out as a peer of "llvm" in the
swift-project.

Run the tests using:

    sh ./litTest -sv --param package-path=/path/to/downloadable-package --param llvm-bin-dir=/usr/bin .

where the first path is the unarchived package root path and the second has LLVM
utilities like `FileCheck`.

Tests
-----

Here is a partial list of tests in the repository:

| Test Name                  | Functionality                                                    |
|----------------------------|------------------------------------------------------------------|
| basic                      | Check output of `swift --version`                                |
| example-package-dealer     | Build the example package-dealer package                         |
| repl                       | Various REPL sanity checks, notably importing Darwin and Glibc   |
| swift-build-self-host      | Use swift build to build itself                                  |
| swift-compiler             | Compile a basic swift file                                       |
| test-c-library-swiftpm     | Build a package that links a 3rd party library                   |
| test-foundation-package    | Build a package that imports Foundation                          |
| test-import-glibc          | Compile a source file importing and using Glibc                  |
| test-multi-compile         | Compile multiple source files into an executable                 |
| test-multi-compile-glibc   | Compile multiple source files importing Glibc into an executable |
| test-static-lib            | Compile multiple source files into a static library              |
| test-xctest-package        | Build a package that imports XCTest                              |
| test-swift-testing-package | Build a package that imports Swift Testing                       |


## Contributing 

Contributions to this repo are welcomed and encouraged! Please see the
[Contributing to Swift guide](https://swift.org/contributing/).

To be a truly great community, [Swift.org](https://swift.org/) needs to welcome
developers from all walks of life, with different backgrounds, and with a wide
range of experience. A diverse and friendly community will have more great
ideas, more unique perspectives, and produce more great code. We will work
diligently to make the Swift community welcoming to everyone.

To give clarity of what is expected of our members, Swift has adopted the
code of conduct defined by the Contributor Covenant. This document is used
across many open source communities, and we think it articulates our values
well. For more, see the [Code of Conduct](https://swift.org/code-of-conduct/).
