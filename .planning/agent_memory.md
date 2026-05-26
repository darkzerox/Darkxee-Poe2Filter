# DZX Filter POE2 - Agent Memory & Context Bank

This document acts as a persistent memory and knowledge bank for future agents working on this project. It captures key design decisions, architecture details, issues faced, and their resolutions.

---

## 🧠 Session Context & Decisions

### 1. Launcher GUI Auto-Updater
- **Objective**: Create a robust automatic patch update system inside the launcher executable (`dist/DZX-PoE2-Filter-Launcher.exe`) so users do not need to download a new launcher executable for every filter update.
- **Implementation**:
  - **Threaded Check/Download**: To keep the Tkinter GUI responsive and prevent Windows from showing "Not Responding", checking and downloading updates is handled in a background daemon thread (`check_updates_thread` & `install_thread`).
  - **GitHub API Integration**: Uses standard `urllib.request` (no external `requests` package to keep the executable lightweight). Hits `https://api.github.com/repos/darkzerox/Darkxee-Poe2Filter/releases/latest` to get the latest release tag and the `dzx-poe2-filter.zip` browser download URL.
  - **Version Comparison**: The local bundled version is read from `config.json` inside the executable's temp dir. The installed version is tracked via a `.installed_version` JSON file written into the game folder.
  - **Prefix Handling**: Version strings compared are stripped of the `v` prefix (e.g., comparing `"0.5.1"` with `"0.5.1"` rather than `"v0.5.1"` with `"0.5.1"`) to prevent false update alerts.

### 2. PyInstaller Packaging (`create_release.py`)
- **Crucial Packaging Rule**: The launcher executable reads `config.json` at runtime. Therefore, `config.json` must be bundled into the root of the `.exe` temp folder (`sys._MEIPASS`).
- **Command Used**:
  ```powershell
  python -m PyInstaller --onefile --noconsole --name DZX-PoE2-Filter-Launcher --add-data "dist/filter;filters" --add-data "dzx_filter/images;dzx_filter/images" --add-data "config.json;." script/installer_gui.py
  ```
  Note the `--add-data "config.json;."` which makes it available at `sys._MEIPASS / "config.json"`.

### 3. Release Process
- Releases are fully automated and run from the local machine using `script/create_release.py`.
- It performs the following steps:
  1. Reads target version from `config.json`.
  2. Compiles filters using `script/start_build.py`.
  3. Archives filters to `dzx-poe2-filter.zip`.
  4. Compiles the executable `DZX-PoE2-Filter-Launcher.exe`.
  5. Cleans and tags git branches (`develop` and `master`).
  6. Pushes commits/tags to GitHub and creates the GitHub Release with the ZIP and EXE assets using the `gh` CLI.

---

## ⚠️ Known Gotchas & Troubleshooting

### `PermissionError: [WinError 5] Access is denied`
- **Cause**: PyInstaller fails to overwrite `dist/DZX-PoE2-Filter-Launcher.exe` because the user has the launcher open, or there are zombie background instances of the launcher still running.
- **Fix**: Run `taskkill /F /IM DZX-PoE2-Filter-Launcher.exe` to terminate any running instances before executing `script/create_release.py`.

### DPI Sizing & Fonts on Windows
- Standard Tkinter widgets can look blurry on high DPI screens.
- **Fix**: Added Windows DPI awareness calls at the bottom of `script/installer_gui.py`:
  ```python
  if sys.platform == 'win32':
      try:
          ctypes.windll.shcore.SetProcessDpiAwareness(1)
      except Exception:
          try:
              ctypes.windll.user32.SetProcessDPIAware()
          except Exception:
              pass
  ```

---

## 📅 Release Timeline

- **v0.5.2** (2026-05-26): Automatic patch check, in-memory zip download & extraction, and `.installed_version` tracking integrated.
- **v0.5.3** (2026-05-26): Adjusted logo frame height to `140` and main window height to `510` to fit the `300x113` subsampled logo without clipping. Text-based fallback centered in the header frame.
