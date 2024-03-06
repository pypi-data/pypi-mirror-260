import os
import re
from typing import Optional
# pip dependencies
from termcolor import colored


def read_tld_list() -> list[str]:
    script_dir = os.path.dirname(os.path.realpath(__file__))
    tld_file = os.path.join(script_dir, "iana_tld_list.txt")

    with open(tld_file, "r") as f:
        tld_list = f.read().split("\n")

    # Unify entries: Remove laeding and trailing whitespaces and make them lowercase
    tld_list = [x.strip().lower() for x in tld_list]
    # Remove comments and empty lines
    tld_list = [x for x in tld_list if x and not x.startswith("#")]
    return tld_list


def get_better_tld_list() -> list[str]:
    tld_list = read_tld_list()

    if "py" in tld_list:
        # would cause false positives for python scripts. Sorry Paraguay :)
        tld_list.remove("py")
        # Add back some "common" generic second-level domain names
        tld_list += ["com.py", "coop.py", "edu.py", "mil.py", "gov.py", "org.py", "net.py", "una.py"]

    if "md" in tld_list:
        # would couse false positives for markdown files. And I never seen a Moldovan domain
        tld_list.remove("md")
        # Add back some "common" generic second-level domain names
        tld_list += ["com.md", "srl.md", "sa.md", "net.md", "org.md", "acad.md"]

    if "zip" in tld_list:
        tld_list.remove("zip") # who thought this one was a good idea?

    # let's add some common internal network names
    tld_list += ["lan", "local", "intern", "internal", "intranet", "intra", "corp"]

    # .ip is for "speedport.ip", .box for fritz.box, .htb for hack the box machines
    tld_list += ["ip", "box", "htb"]

    # and some reserved TLDs
    tld_list += ["test", "example", "invalid", "localhost"]

    # remove duplicates and order them alphabetically
    return sorted(set(tld_list))


def _build_ip_regex() -> str:
    boundary = "[^A-Za-z0-9.]"
    start_boundary = f"(?:(?<={boundary})|^)"
    end_boundary = f"(?:(?={boundary})|$)"
    byte = "(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)"
    return f"{start_boundary}{byte}(?:\\.{byte}){{3}}{end_boundary}"


def _build_hostname_regex() -> str:
    # Make sure, that we match the whole domain and fail if it is malformed (like having a . at the end)
    boundary = "[^-_~\$A-Za-z0-9.]"
    start_boundary = f"(?:(?<={boundary})|^)"
    end_boundary = f"(?:(?={boundary})|$)"
    # A part of a domain. Acn contain letters, numbers and dashes. But dashes can not be the first or last character
    part = "(?!-)[A-Za-z0-9-]{1,63}(?<!-)"
    # domain regex. May not work for some net tlds such as .accountants

    tld_list = get_better_tld_list()

    tld = "(?:" + "|".join(tld_list) + ")"
    domain_with_tld = start_boundary + f"(?:{part}\\.)+{tld}"
    # internal domains don't need a .something at the end
    internal_url_with_scheme = f"(?<=[a-zA-Z0-9]:\/\/)(?:{part}\\.)*{part}"

    # Match either an internal or a normal public domain
    combined = f"(?:{domain_with_tld}|{internal_url_with_scheme}){end_boundary}"
    return combined


IP_REGEX = re.compile(_build_ip_regex())
# Ignore case flag in needed to detect obfuscated domains like tEst.coM
HOSTNAME_REGEX = re.compile(_build_hostname_regex(), re.IGNORECASE)
HOSTNAME_OR_IP_REGEX = re.compile(f"(?:{IP_REGEX.pattern}|{HOSTNAME_REGEX.pattern})", re.IGNORECASE)
CSV_HEADER = ["file", "line_nr", "column_nr", "value", "status"]


STATUS_BADNESS_ORDER = ["ok", "error", "warn", "bad"]
def get_worst_status(status_list: list[str]) -> str:
    status_badness = [STATUS_BADNESS_ORDER.index(x) for x in status_list]
    worst_index = max(status_badness)
    return STATUS_BADNESS_ORDER[worst_index]

def determine_statuses_to_show(show: Optional[str], hide: Optional[str]):
    def split_entries(string: str) -> list[str]:
        entries = [x.strip() for x in string.split(",")]
        # remove duplicates
        entries = list(set(entries))
        for x in entries:
            if x not in STATUS_BADNESS_ORDER:
                raise Exception(f"Unknown status '{x}' in '{string}'")
        return entries

    # Check against None to correctly handle empty strings as arguments
    if show is None and hide is None:
        # Show all statuses by default
        return STATUS_BADNESS_ORDER
    elif show is None and hide:
        # Handle the hide parameter
        hide_list = split_entries(hide)
        return [status for status in STATUS_BADNESS_ORDER if status not in hide_list]
    elif hide is None and show:
        # Handle show parameter
        show_list = split_entries(show)
        return show_list
    else:
        raise Exception("Both 'show' and 'hide' are defined, but they are mutually exclusive")


class FilePathChecker:
    def __init__(self, exclude_directories: list[str], file_extensions: list[str], allow_file_extensions: bool):
        self.exclude_directories = exclude_directories
        self.file_extensions = file_extensions
        # True -> allowlist, False -> denylist
        self.allow_file_extensions = allow_file_extensions

    def should_check_dir(self, path: str) -> bool:
        for directory in self.exclude_directories:
            if os.path.samefile(directory, path):
                return False
        return True

    def should_check_file(self, path: str) -> bool:
        file_name = os.path.basename(path)
        for extension in self.file_extensions:
            if file_name.endswith(extension):
                return self.allow_file_extensions

        return not self.allow_file_extensions


_STATUS_COLORS = {
    "ok": ("green", ["bold"]),
    "error": ("yellow", ["bold"]),
    "warn": ("yellow", ["bold"]),
    "bad": ("red", ["bold"]),
}
def color_by_status(text: str, status: str, ignore_attrs: bool = False) -> str:
    color_name, attrs = _STATUS_COLORS[status]
    if ignore_attrs:
        attrs = []
    return colored(text, color_name, attrs=attrs)
