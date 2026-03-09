// swift-tools-version: 5.9
import PackageDescription

let package = Package(
    name: "VPNTools",
    platforms: [.macOS(.v14)],
    targets: [
        .executableTarget(
            name: "VPNTools",
            path: "VPNTools",
            resources: [.process("Assets.xcassets")]
        )
    ]
)
