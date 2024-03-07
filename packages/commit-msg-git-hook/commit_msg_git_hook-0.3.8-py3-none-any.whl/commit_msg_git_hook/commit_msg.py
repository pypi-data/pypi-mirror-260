import json
import re
import sys

# ANSI Escape Codes
BOLD = "\033[1m"
UNDERLINE = "\033[4m"
RESET = "\033[00m"
FG_RED = "\033[31m"
FG_BLUE = "\033[34m"

CONFIG_FILE_NAME = "commit-msg.config.json"


def read_config_file(file_name: str) -> dict[str]:
    f = open(file_name)
    data = json.load(f)

    config = {
        "enabled": data["enabled"],
        "revert": data["revert"],
        "types": data["types"],
        "scopes": data["scopes"],
        "max_length": data["max_length"],
    }

    f.close()

    return config


def create_regex(config: dict[str]) -> str:
    regex = r"(^"

    if config["revert"] == True:
        regex += r'Revert ".+"$)|(^'

    regex += r"("
    regex += r"|".join(config["types"])

    regex += r")(\(("
    regex += r"|".join(config["scopes"])

    regex += r")\))?!?: \b.+$)"

    return regex


def get_commit_file_first_line() -> str:
    commit_file = sys.argv[1]

    f = open(commit_file, "r")
    first_line = f.readline()
    f.close()

    return first_line


def check_msg_empty(msg) -> None:
    if msg == "" or msg == "\n":
        exit(0)


def check_msg_length(msg, max_length) -> None:
    if len(msg) > max_length:
        print(
            f"\n{msg}",
            f"\n{BOLD}{FG_RED}[COMMIT MESSAGE TOO LONG]{RESET}",
            f"{BOLD}{FG_RED}------------------------{RESET}",
            f"{BOLD}Configured max length (first line):{RESET} {FG_BLUE}{max_length}{RESET}\n",
            sep="\n",
        )

        exit(1)


def check_msg_pattern(pattern, msg, config) -> None:
    if not re.match(pattern, msg):
        print(
            f"\n{msg}",
            f"\n{BOLD}{FG_RED}[INVALID COMMIT MESSAGE]{RESET}",
            f"{BOLD}{FG_RED}------------------------{RESET}",
            f"{BOLD}Use the Conventional Commits specification.\n{RESET}",
            f"{BOLD}Valid types:{RESET} {FG_BLUE}{config['types']}{RESET}",
            f"{BOLD}Valid scopes:{RESET} {FG_BLUE}{config['scopes']}{RESET}",
            f"\nSee the specification:\n{UNDERLINE}https://www.conventionalcommits.org/en/v1.0.0/{RESET}\n",
            sep="\n",
        )

        exit(2)


def check_msg(pattern, msg, config):
    check_msg_empty(msg)
    check_msg_length(msg, config["max_length"])
    check_msg_pattern(pattern, msg, config)


def main(msg: str = "") -> None:
    config = read_config_file(CONFIG_FILE_NAME)

    if config["enabled"] == False:
        exit(0)

    regex = create_regex(config)

    if msg == "":
        msg = get_commit_file_first_line()

    check_msg(regex, msg, config)
