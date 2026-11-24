import ui


def main():
    try:
        ui.menu()
    except KeyboardInterrupt:
        print(ui.RESET + "\n[ SIMULATION STOPPED ]")


if __name__ == "__main__":
    main()
