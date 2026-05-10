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

- **Append readings to file** — when enabled, each decoded reading is appended to the path shown (default: `serial_bp_monitor/bp_readings.txt`). Use **Browse…** to pick another file.
- **POST to Open API** — when enabled, readings are POSTed as form data to the URL (default `http://127.0.0.1/api/add-vital`), same general shape as `bphis/application/services.py`.

## Troubleshooting

- **Serial open fails** — Port in use by another app, wrong port, missing driver, or no permission (especially Linux: add user to `dialout` or equivalent).
- **Nothing appears on cable** — Wrong baud/port; verify device sends lines terminated so `readline()` returns frames.
- **BLE scan/connect fails** — Bluetooth off, device not advertising, wrong MAC/name, or OS BLE restrictions.

## Project layout

| File | Purpose |
|------|---------|
| `main.py` | Tkinter UI and wiring |
| `protocol.py` | Port lookup, cable/BLE parsing, formatting |
| `workers.py` | Background serial thread and BLE asyncio loop |
| `open_api.py` | Optional HTTP POST helper |
| `requirements.txt` | Python dependencies |
