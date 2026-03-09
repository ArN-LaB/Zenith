import Foundation

/// Checks GitHub Releases for a newer version of Zenith.
@MainActor
final class UpdateChecker: ObservableObject {
    @Published var isChecking = false
    @Published var updateAvailable = false
    @Published var latestVersion: String? = nil
    @Published var lastError: String? = nil

    let currentVersion: String =
        Bundle.main.infoDictionary?["CFBundleShortVersionString"] as? String ?? "1.0.0"

    private var lastChecked: Date? = nil

    func check(force: Bool = false) async {
        guard !isChecking else { return }
        // Don't re-check within the same minute unless forced
        if !force, let last = lastChecked, Date().timeIntervalSince(last) < 60 { return }
        isChecking = true
        lastError = nil
        defer {
            isChecking = false
            lastChecked = Date()
        }
        do {
            var req = URLRequest(
                url: URL(string: "https://api.github.com/repos/ArN-Ld/Zenith/releases/latest")!
            )
            req.setValue("application/vnd.github+json", forHTTPHeaderField: "Accept")
            req.setValue("2022-11-28", forHTTPHeaderField: "X-GitHub-Api-Version")
            req.timeoutInterval = 10
            let (data, _) = try await URLSession.shared.data(for: req)
            struct Release: Decodable { let tag_name: String }
            let release = try JSONDecoder().decode(Release.self, from: data)
            let latest = release.tag_name.trimmingCharacters(in: CharacterSet(charactersIn: "vV"))
            latestVersion = latest
            updateAvailable = latest.compare(currentVersion, options: .numeric) == .orderedDescending
        } catch {
            lastError = error.localizedDescription
        }
    }
}
