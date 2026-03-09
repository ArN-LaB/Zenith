import SwiftUI

@main
struct VPNToolsApp: App {
    @StateObject private var speedTestVM = SpeedTestViewModel()
    @StateObject private var depManager = DependencyManager()
    @Environment(\.openWindow) private var openWindow
    @AppStorage("hidePreflightAtStartup") private var hidePreflightAtStartup = false
    @AppStorage("hasCompletedFirstPreflight") private var hasCompletedFirstPreflight = false

    var body: some Scene {
        // Menu bar icon — primary interface
        MenuBarExtra {
            MenuBarView(
                openDashboard: { openWindow(id: "dashboard") }
            )
                .environmentObject(speedTestVM)
                .environmentObject(depManager)
                .task {
                    depManager.checkAll()
                    // Always show on first launch; afterwards respect user preference
                    if !hasCompletedFirstPreflight || !hidePreflightAtStartup {
                        openWindow(id: "preflight")
                        NSApp.activate(ignoringOtherApps: true)
                    }
                }
        } label: {
            Image(systemName: menuBarIcon)
                .symbolRenderingMode(.hierarchical)
        }
        .menuBarExtraStyle(.window)

        // Full dashboard window — golden ratio proportions (φ ≈ 1.618)
        Window("VPN Tools Dashboard", id: "dashboard") {
            ContentView()
                .environmentObject(speedTestVM)
                .environmentObject(depManager)
                .frame(minWidth: 700, minHeight: 433)
        }
        .defaultSize(width: 900, height: 556)

        // Startup preflight window
        Window("System Check", id: "preflight") {
            StartupPreflightView()
                .environmentObject(depManager)
        }
        .defaultSize(width: 420, height: 500)
        .defaultPosition(.center)
    }

    private var menuBarIcon: String {
        switch speedTestVM.state {
        case .idle: return "bolt.shield"
        case .running: return "bolt.shield.fill"
        case .completed: return "checkmark.shield.fill"
        case .error: return "exclamationmark.shield.fill"
        }
    }
}
