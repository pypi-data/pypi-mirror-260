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
    parser.add_argument('--ex', action='store_true', help='Extend The Screen')
    parser.add_argument('--pr', action='store_true', help='Show Only On Primary Display')
    parser.add_argument('--se', action='store_true', help='Show Only On Secondary Display')
    args = parser.parse_args()
    
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)
    
    extend = args.ex
    primary = args.pr
    secondary  = args.se

    if extend:
        print("Extending the display")
        extend_display()

    if primary:
        print("Showing on Primary")
        show_on_primary()
    
    if secondary:
        print("Showing on Secondary")
        show_on_secondary()


if __name__ == "__main__":
    main()
