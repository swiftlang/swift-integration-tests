// swift-tools-version:4.2
import PackageDescription

let package = Package(
    name: "SwiftCMixed",
    targets: [
        .target(name: "swifty", dependencies: ["see"]),
        .target(name: "see", dependencies: []),
        .testTarget(name: "swiftyTests", dependencies: ["swifty"]),
    ]
)
