# Serial / BLE blood pressure monitor

Small desktop app (tkinter) that reads **USB‑serial cable** or **Bluetooth LE** blood-pressure frames using the same parsing logic as `bphis/application/helpers.py`. Output appears in the window and can be appended to a `.txt` file. Optionally POST each reading to an HTTP endpoint.

## Requirements

- **Python 3.10+** (3.12 / 3.13 recommended if binary wheels for dependencies matter on your OS).
- **tkinter** — included with most Windows/macOS Python builds; on Debian/Ubuntu you may need `sudo apt install python3-tk`.
- USB adapter drivers installed so the OS exposes a COM / `/dev/tty.*` port.
- For **Bluetooth**, OS Bluetooth enabled and (on Linux) permissions for BLE scanning/connecting.

## Install dependencies

From the **repository root** (`py-and`):

```bash
pip install -r serial_bp_monitor/requirements.txt
```

Or from **inside this folder**:

```bash
cd serial_bp_monitor
pip install -r requirements.txt
```

## Run the app

**Option A — from repository root**

```bash
python serial_bp_monitor/main.py
```

**Option B — from this folder**

```bash
cd serial_bp_monitor
python main.py
```

If `python` points to Python 2 on your system, use `python3` instead.

## Using the UI

### Cable (serial)

1. Open the **Cable (serial)** tab.
2. Optionally adjust **Port search** (substring matched against the OS port description, default targets Prolific adapters).
3. Click **Find port** to fill **manual port**, or type the port yourself (`COM3` on Windows, `/dev/cu.usbserial-*` or similar on macOS).
4. Confirm **Baud rate** (default **2400**, matching the original middleware).
5. Click **Connect cable**. Click again to disconnect.

### Bluetooth LE

1. Open the **Bluetooth LE** tab.
2. Set **Device name contains** (default `TM-2657`) or set **Optional fixed MAC / address** if you always use one adapter.
3. Click **Connect BLE**. Click again to disconnect.

### Output & API

- **Append readings to file** — when enabled, each decoded reading is appended to the path shown. Default log path: project folder when running from source; **`~/Library/Application Support/BPSerialMonitor/bp_readings.txt`** for the frozen **macOS** app; **next to `BPSerialMonitor.exe`** on **Windows**. Use **Browse…** to pick another file.
- **POST to Open API** — when enabled, readings are POSTed as form data to the URL (default `http://127.0.0.1/api/add-vital`), same general shape as `bphis/application/services.py`.

## Troubleshooting

- **Serial open fails** — Port in use by another app, wrong port, missing driver, or no permission (especially Linux: add user to `dialout` or equivalent).
- **Nothing appears on cable** — Wrong baud/port; verify device sends lines terminated so `readline()` returns frames.
- **BLE scan/connect fails** — Bluetooth off, device not advertising, wrong MAC/name, or OS BLE restrictions.

## Standalone installers (no Python on target machines)

The app is frozen with **[PyInstaller](https://pyinstaller.org/)**. You **must build on the same OS** you ship to (macOS `.pkg` / `.app` on a Mac, `.exe` on Windows).

### Prerequisite for building

Use a Python install that includes **tkinter** (recommended: **[python.org](https://www.python.org/downloads/)** installers). Create a virtualenv if you like; PyInstaller also expects **`requirements-packaging.txt`**.

### macOS — `.app` and `.pkg`

From **`serial_bp_monitor/`**:

```bash
chmod +x scripts/build_mac_pkg.sh
./scripts/build_mac_pkg.sh
```

Optional package metadata:

```bash
VERSION=1.2.0 ./scripts/build_mac_pkg.sh
```

Artifacts:

- **`dist/BPSerialMonitor.app`** — double‑click or drag into Applications.
- **`dist/BPSerialMonitor-<version>-macos.pkg`** — installs **`BPSerialMonitor.app`** into **`/Applications`**.

**Gatekeeper:** unsigned builds often trigger “cannot be opened” warnings. Users can **Right‑click → Open** once, or you can **code‑sign** the `.app` with an Apple Developer ID before running `pkgbuild`.

PyInstaller may download/process binaries using a cache under **`~/Library/Application Support/pyinstaller`** on macOS; the build machine needs permission to write there.

### Windows — `.exe`

From **`serial_bp_monitor/`** in **PowerShell**:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass -Force
.\scripts\build_windows.ps1
```

Artifact:

- **`dist\BPSerialMonitor.exe`** — single executable (share/copy this file).

Smart Screen / antivirus tools sometimes warn about packaged `.exe` binaries until reputation builds or until you sign the executable.

### Manual PyInstaller (either OS)

```bash
cd serial_bp_monitor
pip install -r requirements.txt -r requirements-packaging.txt
pyinstaller serial_bp_monitor.spec
```

## Project layout

| File | Purpose |
|------|---------|
| `main.py` | Tkinter UI and wiring |
| `protocol.py` | Port lookup, cable/BLE parsing, formatting |
| `workers.py` | Background serial thread and BLE asyncio loop |
| `open_api.py` | Optional HTTP POST helper |
| `requirements.txt` | Python dependencies |
| `requirements-packaging.txt` | PyInstaller (build machines only) |
| `serial_bp_monitor.spec` | PyInstaller spec ([mac `.app`] vs Windows one‑file `.exe`) |
| `scripts/build_mac_pkg.sh` | macOS: build `.app` + `.pkg` |
| `scripts/build_windows.ps1` | Windows: build `.exe` |
