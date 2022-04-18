// swift-tools-version:5.5
// The swift-tools-version declares the minimum version of Swift required to build this package.

import PackageDescription

let package = Package(
    name: "DocCTest",
    products: [
        .library(name: "DocCTest", targets: ["DocCTest"]),
    ],
    targets: [
        .target(name: "DocCTest"),
    ]
)
