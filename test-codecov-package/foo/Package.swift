// swift-tools-version:4.2

import PackageDescription

let package = Package(
    name: "foo",
    products: [
        .library(
            name: "foo",
            targets: ["foo"]),
    ],
    targets: [
        .target(
            name: "foo",
            dependencies: []),
        .testTarget(
            name: "fooTests",
            dependencies: ["foo"]),
    ]
)
