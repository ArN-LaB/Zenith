# Changelog

All notable changes to VPN Tools for macOS are documented in this file.

---

## [1.0.0] - 2026-03-09

### Added
- Initial macOS app release.
- Menu bar icon with state-reactive SF Symbol (`bolt.shield`).
- Native SwiftUI dashboard window with golden-ratio proportions (900 × 556).
- Real-time multi-step progress pipeline: MTR latency → download speed → server ranking.
- Results table with sortable columns (server, city, distance, latency, download speed, score).
- Live log viewer with per-server event stream.
- Settings: reference location geocoder (with autocomplete), test parameters, path configuration.
- System preflight window at startup — checks `mtr`, `speedtest-cli`, `mullvad` CLI, and Python.
- Dependency auto-detection for Python, `speedtest-cli`, `mtr`, and Mullvad CLI.
- Runs [vpn-tools](https://github.com/ArN-Ld/vpn-tools) Python CLI as a bundled subprocess via `--machine-readable` JSON protocol.
- Automatic ping fallback when `mtr-packet` is not correctly configured (Homebrew SUID ownership issue — see README).
- Menu bar badge: "ping" capsule indicator when MTR falls back to ping mode.
- Dashboard "Ping mode" label in header subtitle when running in fallback mode.
- `format_mtr_results()` shows "Ping" or "MTR" label dynamically based on hop count.
- Adaptive speedtest timeout: 150 s for servers ≥ 3 000 km away.
- About panel with app version, source repository links, and dependency credits.
- App icon generated from SF Symbols with multi-resolution `.icns`.
- `build_app.sh` — self-contained release build script bundling Swift binary + Python source + vendored dependencies.
- `generate_icon.py` — reproducible icon generation via Pillow.

### Architecture
- **One-way dependency**: `vpn-tools` is a standalone CLI with no knowledge of this app. `VPN Tools.app` invokes it as a subprocess and parses its JSON output.
- `SpeedTestRunner.swift` — subprocess launch, stdin/stdout management, JSON event parsing.
- `SpeedTestViewModel.swift` — MVVM bridge, event routing, UI state machine.
- `DependencyManager.swift` — runtime dependency checks.
- `ContentView.swift` / `MenuBarView.swift` / `ResultsView.swift` / `SettingsView.swift` — SwiftUI views.

### Known Compatibility
- **macOS Homebrew mtr 0.96**: `brew install mtr` may leave `mtr-packet` with an incorrect SUID setup (owned by the installing user, not root). The app automatically uses ping fallback in this case. See [README § Requirements](README.md#requirements) for the fix.
