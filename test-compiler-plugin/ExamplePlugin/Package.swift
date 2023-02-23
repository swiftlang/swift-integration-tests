// swift-tools-version: 5.7

import PackageDescription

let package = Package(
  name: "ExamplePlugin",
  platforms: [
    .macOS(.v10_15),
  ],
  dependencies: [
    .package(path: "../../../swift-syntax")
  ],
  targets: [
    .executableTarget(
      name: "ExamplePlugin",
      dependencies: [
        .product(name: "SwiftCompilerPlugin", package: "swift-syntax"),
        .product(name: "SwiftSyntax", package: "swift-syntax"),
        .product(name: "SwiftSyntaxMacros", package: "swift-syntax"),
        .product(name: "SwiftDiagnostics", package: "swift-syntax"),
      ]),
  ]
)
