import upi


def main():
    try:
        upi.menu()
    except KeyboardInterrupt:
        print(ui.RESET + "\n[ SIMULATION STOPPED ]")


if __name__ == "__main__":
    main()
