// swift-tools-version:4.2
import PackageDescription

let package = Package(
    name: "Foo",
    targets: [
        .target(name: "See"),
        .target(name: "Core", dependencies: ["See"]),
        .target(name: "exec", dependencies: ["Core"]),
    ]
)
