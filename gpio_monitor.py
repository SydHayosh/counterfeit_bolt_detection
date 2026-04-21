#!/usr/bin/env python3
"""
gpio_monitor.py — Continuous GPIO 2 & 3 input monitor for Raspberry Pi 5
Uses gpiod (libgpiod), the modern GPIO interface recommended for Pi 5.

Install dependency:
    sudo apt install python3-gpiod

Run:
    python3 gpio_monitor.py
"""

import gpiod
import time
import sys
from datetime import datetime

# ── Configuration ────────────────────────────────────────────────────────────
GPIO_CHIP    = "/dev/gpiochip4"   # gpiochip4 is the main chip on Pi 5
PIN_NUMBERS  = [2, 3]             # BCM GPIO pin numbers to monitor
POLL_INTERVAL_S = 0.05            # Seconds between reads (50 ms → ~20 Hz)
SHOW_UNCHANGED  = False           # Set True to print every poll, not just changes
# ─────────────────────────────────────────────────────────────────────────────


def level_label(value: int) -> str:
    return "HIGH (1)" if value else "LOW  (0)"


def main() -> None:
    print("=" * 55)
    print("  Raspberry Pi 5 — GPIO Input Monitor")
    print(f"  Chip : {GPIO_CHIP}")
    print(f"  Pins : {PIN_NUMBERS}")
    print(f"  Poll : every {POLL_INTERVAL_S * 1000:.0f} ms")
    print("  Press Ctrl+C to exit")
    print("=" * 55)

    try:
        chip = gpiod.Chip(GPIO_CHIP)
    except FileNotFoundError:
        sys.exit(
            f"[ERROR] GPIO chip '{GPIO_CHIP}' not found.\n"
            "        On Pi 5, try /dev/gpiochip4. "
            "Run 'ls /dev/gpiochip*' to list available chips."
        )

    # Request all pins as inputs
    lines = chip.get_lines(PIN_NUMBERS)
    lines.request(
        consumer="gpio_monitor",
        type=gpiod.LINE_REQ_DIR_IN,
    )

    previous_values = {pin: None for pin in PIN_NUMBERS}

    print(f"\n{'Timestamp':<26} {'Pin':<6} {'State'}")
    print("-" * 55)

    try:
        while True:
            current_values = lines.get_values()  # list matching PIN_NUMBERS order

            for pin, value in zip(PIN_NUMBERS, current_values):
                if SHOW_UNCHANGED or value != previous_values[pin]:
                    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
                    change = ""
                    if previous_values[pin] is not None and value != previous_values[pin]:
                        change = "  ← CHANGED"
                    print(f"{ts}  GPIO{pin:<3}  {level_label(value)}{change}")
                    previous_values[pin] = value

            time.sleep(POLL_INTERVAL_S)

    except KeyboardInterrupt:
        print("\n[INFO] Monitoring stopped by user.")
    finally:
        lines.release()
        chip.close()
        print("[INFO] GPIO resources released.")


if __name__ == "__main__":
    main()
