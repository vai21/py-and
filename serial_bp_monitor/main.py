#!/usr/bin/env python3
"""
Desktop monitor for BP cable (serial) or BLE — tkinter UI, optional log file, optional Open API.
Run from repo root: python serial_bp_monitor/main.py
"""

from __future__ import annotations

import logging
import queue
import threading
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, scrolledtext, ttk

from open_api import hit_open_api
from protocol import (
    ble_payload_for_api,
    cable_payload_for_api,
    find_com_port,
    format_ble_reading,
    format_cable_reading,
)
from workers import BleWorker, SerialCableWorker

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DEFAULT_CABLE_SEARCH = "Prolific PL2303GT"
DEFAULT_BAUD = "2400"
DEFAULT_BLE_NAME = "TM-2657"
DEFAULT_BLE_MAC = "00:09:1F:8E:2B:3A"
DEFAULT_OPEN_API = "http://127.0.0.1/api/add-vital"
OUTPUT_DEFAULT = Path(__file__).resolve().parent / "bp_readings.txt"


class SerialBpApp(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("BP serial / BLE monitor")
        self.geometry("720x560")

        self.msg_q: queue.Queue = queue.Queue()
        self.stop_serial = threading.Event()
        self.stop_ble = threading.Event()
        self.serial_worker: SerialCableWorker | None = None
        self.ble_worker: BleWorker | None = None

        self._build_ui()
        self.after(120, self._poll_queue)

    def _build_ui(self) -> None:
        nb = ttk.Notebook(self)
        nb.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)

        self.tab_cable = ttk.Frame(nb)
        self.tab_ble = ttk.Frame(nb)
        nb.add(self.tab_cable, text="Cable (serial)")
        nb.add(self.tab_ble, text="Bluetooth LE")

        # --- Cable tab
        row = 0
        ttk.Label(self.tab_cable, text="Port search (description contains):").grid(
            row=row, column=0, sticky=tk.W, padx=4, pady=2
        )
        self.var_search = tk.StringVar(value=DEFAULT_CABLE_SEARCH)
        ttk.Entry(self.tab_cable, textvariable=self.var_search, width=40).grid(
            row=row, column=1, sticky=tk.EW, padx=4, pady=2
        )
        row += 1
        ttk.Label(self.tab_cable, text="Or manual port (e.g. COM3, /dev/ttyUSB0):").grid(
            row=row, column=0, sticky=tk.W, padx=4, pady=2
        )
        self.var_manual_port = tk.StringVar(value="")
        ttk.Entry(self.tab_cable, textvariable=self.var_manual_port, width=40).grid(
            row=row, column=1, sticky=tk.EW, padx=4, pady=2
        )
        row += 1
        ttk.Label(self.tab_cable, text="Baud rate:").grid(row=row, column=0, sticky=tk.W, padx=4, pady=2)
        self.var_baud = tk.StringVar(value=DEFAULT_BAUD)
        ttk.Entry(self.tab_cable, textvariable=self.var_baud, width=12).grid(
            row=row, column=1, sticky=tk.W, padx=4, pady=2
        )
        row += 1
        bf = ttk.Frame(self.tab_cable)
        bf.grid(row=row, column=0, columnspan=2, sticky=tk.W, padx=4, pady=6)
        ttk.Button(bf, text="Find port", command=self._on_find_port).pack(side=tk.LEFT, padx=2)
        self.btn_serial_connect = ttk.Button(bf, text="Connect cable", command=self._toggle_serial)
        self.btn_serial_connect.pack(side=tk.LEFT, padx=2)
        self.tab_cable.columnconfigure(1, weight=1)

        # --- BLE tab
        row = 0
        ttk.Label(self.tab_ble, text="Device name contains:").grid(row=row, column=0, sticky=tk.W, padx=4, pady=2)
        self.var_ble_name = tk.StringVar(value=DEFAULT_BLE_NAME)
        ttk.Entry(self.tab_ble, textvariable=self.var_ble_name, width=30).grid(
            row=row, column=1, sticky=tk.W, padx=4, pady=2
        )
        row += 1
        ttk.Label(self.tab_ble, text="Optional fixed MAC / address:").grid(row=row, column=0, sticky=tk.W, padx=4, pady=2)
        self.var_ble_mac = tk.StringVar(value=DEFAULT_BLE_MAC)
        ttk.Entry(self.tab_ble, textvariable=self.var_ble_mac, width=30).grid(
            row=row, column=1, sticky=tk.W, padx=4, pady=2
        )
        row += 1
        bf2 = ttk.Frame(self.tab_ble)
        bf2.grid(row=row, column=0, columnspan=2, sticky=tk.W, padx=4, pady=6)
        self.btn_ble_connect = ttk.Button(bf2, text="Connect BLE", command=self._toggle_ble)
        self.btn_ble_connect.pack(side=tk.LEFT, padx=2)
        self.tab_ble.columnconfigure(1, weight=1)

        # --- Common options
        opt = ttk.LabelFrame(self, text="Output & API")
        opt.pack(fill=tk.X, padx=8, pady=(0, 4))

        self.var_save_file = tk.BooleanVar(value=True)
        ttk.Checkbutton(opt, text="Append readings to file", variable=self.var_save_file).grid(
            row=0, column=0, sticky=tk.W, padx=4, pady=2
        )
        self.var_log_path = tk.StringVar(value=str(OUTPUT_DEFAULT))
        ttk.Entry(opt, textvariable=self.var_log_path, width=55).grid(row=0, column=1, sticky=tk.EW, padx=4, pady=2)
        ttk.Button(opt, text="Browse…", command=self._browse_log).grid(row=0, column=2, padx=4, pady=2)

        self.var_open_api = tk.BooleanVar(value=False)
        ttk.Checkbutton(opt, text="POST to Open API", variable=self.var_open_api).grid(
            row=1, column=0, sticky=tk.W, padx=4, pady=2
        )
        self.var_api_url = tk.StringVar(value=DEFAULT_OPEN_API)
        ttk.Entry(opt, textvariable=self.var_api_url, width=55).grid(row=1, column=1, columnspan=2, sticky=tk.EW, padx=4, pady=2)
        opt.columnconfigure(1, weight=1)

        # --- Log
        lf = ttk.LabelFrame(self, text="Readings log")
        lf.pack(fill=tk.BOTH, expand=True, padx=8, pady=4)
        self.txt = scrolledtext.ScrolledText(lf, height=16, wrap=tk.WORD)
        self.txt.pack(fill=tk.BOTH, expand=True, padx=4, pady=4)

    def _browse_log(self) -> None:
        path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            initialfile=Path(self.var_log_path.get()).name,
            filetypes=[("Text", "*.txt"), ("All", "*.*")],
        )
        if path:
            self.var_log_path.set(path)

    def _append_log(self, text: str) -> None:
        self.txt.insert(tk.END, text + "\n")
        self.txt.see(tk.END)

    def _append_file(self, text: str) -> None:
        if not self.var_save_file.get():
            return
        path = Path(self.var_log_path.get()).expanduser()
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("a", encoding="utf-8") as f:
            f.write(text + "\n\n")

    def _on_find_port(self) -> None:
        term = self.var_search.get().strip()
        if not term:
            messagebox.showinfo("Find port", "Enter a search substring first.")
            return
        found = find_com_port(term)
        if not found:
            messagebox.showwarning("Find port", f"No port matched “{term}”.")
            return
        port, desc, hwid = found
        self.var_manual_port.set(port)
        messagebox.showinfo("Find port", f"{port}\n{desc}\n{hwid}")

    def _toggle_serial(self) -> None:
        if self.serial_worker and self.serial_worker.is_alive():
            self.stop_serial.set()
            self.btn_serial_connect.configure(text="Connect cable")
            self._append_log("[Cable] disconnect requested…")
            return

        self.stop_serial.clear()
        port = self.var_manual_port.get().strip()
        if not port:
            res = find_com_port(self.var_search.get().strip())
            if not res:
                messagebox.showerror("Cable", "No port: use Find port or enter manual port.")
                return
            port = res[0]
            self.var_manual_port.set(port)

        try:
            baud = int(self.var_baud.get().strip())
        except ValueError:
            messagebox.showerror("Cable", "Invalid baud rate.")
            return

        self.serial_worker = SerialCableWorker(port, baud, self.msg_q, self.stop_serial)
        self.serial_worker.start()
        self.btn_serial_connect.configure(text="Disconnect cable")

    def _toggle_ble(self) -> None:
        if self.ble_worker and self.ble_worker.is_alive():
            self.stop_ble.set()
            self.btn_ble_connect.configure(text="Connect BLE")
            self._append_log("[BLE] disconnect requested…")
            return

        self.stop_ble.clear()
        mac = self.var_ble_mac.get().strip()
        self.ble_worker = BleWorker(
            self.var_ble_name.get().strip(),
            mac if mac else None,
            self.msg_q,
            self.stop_ble,
        )
        self.ble_worker.start()
        self.btn_ble_connect.configure(text="Disconnect BLE")

    def _poll_queue(self) -> None:
        try:
            while True:
                kind, payload = self.msg_q.get_nowait()
                if kind == "error":
                    self._append_log(f"[Error] {payload}")
                elif kind == "status":
                    self._append_log(f"[Status] {payload}")
                elif kind == "cable":
                    block = format_cable_reading(payload)
                    self._append_log(block)
                    self._append_file(block)
                    if self.var_open_api.get():
                        hit_open_api(cable_payload_for_api(payload), self.var_api_url.get().strip())
                elif kind == "ble":
                    block = format_ble_reading(payload)
                    self._append_log(block)
                    self._append_file(block)
                    if self.var_open_api.get():
                        hit_open_api(ble_payload_for_api(payload), self.var_api_url.get().strip())
        except queue.Empty:
            pass
        self.after(120, self._poll_queue)

    def destroy(self) -> None:
        self.stop_serial.set()
        self.stop_ble.set()
        super().destroy()


def main() -> None:
    app = SerialBpApp()
    try:
        app.txt.configure(font=("Consolas", 10))
    except tk.TclError:
        try:
            app.txt.configure(font=("TkFixedFont", 10))
        except tk.TclError:
            pass
    app.mainloop()


if __name__ == "__main__":
    main()
