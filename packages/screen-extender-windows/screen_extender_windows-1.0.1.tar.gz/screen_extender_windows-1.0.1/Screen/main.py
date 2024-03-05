import subprocess
import sys
import argparse

def extend_display():
    subprocess.run(["DisplaySwitch.exe", "/extend"])


def show_on_primary():
    subprocess.run(["DisplaySwitch.exe", "/internal"])


def show_on_secondary():
    subprocess.run(["DisplaySwitch.exe", "/external"])



def main():
    parser = argparse.ArgumentParser(description="Screen Operations")
    parser.add_argument('--option', type=int, choices=[1, 2, 3], help='1: Extend The Screen\n 2: Show Only On Primary Display, 3: Show Only On Secondary Display')
    args = parser.parse_args()

    option = args.option

    if option == 1:
        extend_display()
    elif option == 2:
        show_on_primary()
    elif option == 3:
        show_on_secondary()
    else:
        print("Invalid option")
if __name__ == "__main__":
    main()
