import platform
import json
import os

CONFIG_FILE = "commands.json"
OUTPUT_FILE = "update.sh"

def header(system: str):

    with open(OUTPUT_FILE, "w") as file:
        file.write("#!/bin/bash\n")
        file.write("# AUTOGENERATED FILE\n")
        file.write('LOGFILE="$HOME/update.log"\n')
        file.write("TMPFILE='/tmp/update_temp.log'\n")
        file.write("run () {\n")
        file.write("    command=$1\n")
        file.write("    echo 'Running $command' >> $LOGFILE\n")
        file.write("    $command >> $TMPFILE 2>&1\n")
        file.write("    if grep -q 'password' $TMPFILE; then\n")
        file.write("        echo 'Password required. Opening terminal...'\n")

        match system:
            case "linux":
                file.write("        gnome-terminal -- bash -c \"sudo $command; exec bash\"\n")
            case "darwin":
                file.write("        osascript -e 'tell application \"Terminal\" to do script \"sudo $command\"'\n")
        file.write("    fi\n")
        file.write("    cat $TMPFILE >> $LOGFILE\n")
        file.write("    rm $TMPFILE\n")
        file.write("}\n\n")
        file.write("notify(){\n")
        file.write("    TITLE=\"VW Updater\"\n")
        file.write("    MSSG=\"Update completed\"\n")
        match system:
            case "linux":
                file.write('    notify-send "$TITLE" "$MSSG"\n')
            case "darwin":
                file.write('osascript -e "display notification \"$MESSAGE\" with title \"$TITLE\"\n')
        file.write("}\n\n")



def append_commands(system: str, commands: dict):
    with open(OUTPUT_FILE, "a") as file:
        for command in commands.get(system, []):
            user_input = input(f"Do you want to include '{command['description']}: {command['command']}'? (y/n)").strip().lower()
            if user_input == "y":
                file.write(f"run \"{command['command']}\"\n")
        file.write("notify()")

def main():
    print("Generating update.sh")

    system = platform.system().lower()

    with open(CONFIG_FILE, "r") as f:
        commands = json.load(f)

    if system not in ["linux", "darwin"]:
        print("Unsupported OS, only Linux and macOS are supported. Exiting...")
        exit(1)

    print(f"{system.capitalize()} detected...")
    header(system)
    append_commands(system, commands)

    print(f"Shell script {OUTPUT_FILE} has been generated.")

    os.system(f"cat {OUTPUT_FILE}")

if __name__ == "__main__":
    main()

