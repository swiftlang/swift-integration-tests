// swift-tools-version:5.1
import PackageDescription

let package = Package(
  name: "pkg",
  targets: [
    .target(name: "exec", dependencies: ["lib", "clib"]),
    .target(name: "lib", dependencies: []),
    .target(name: "clib", dependencies: []),
  ]
)
