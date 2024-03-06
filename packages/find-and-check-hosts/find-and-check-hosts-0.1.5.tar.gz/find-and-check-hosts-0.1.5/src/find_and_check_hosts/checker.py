#!/usr/bin/env python3
from typing import Optional
#  local files
from .replacer import AbstractReplacer
from .rules import RuleConfigFile
from .patterns import IP_REGEX, HOSTNAME_OR_IP_REGEX, color_by_status, get_worst_status
# pip dependencies
from termcolor import colored



class FileChecker(AbstractReplacer):
    def __init__(self, config: RuleConfigFile, show_status_list: list[str], create_csv: bool):
        super().__init__(HOSTNAME_OR_IP_REGEX)
        self.config = config
        self.show_status_list = show_status_list
        self.create_csv = create_csv
        # Each entry is a row. Each row is a list: [file, line_nr, column_nr, value, status]
        # The line_nr and column_nr each start at 1
        self.csv_data: list[list] = []
        self.counts = {
            "ok": 0,
            "warn": 0,
            "bad": 0,
            "error": 0
        }
        self._path = ""
        self._line_nr = 0
        self._status_list: list[str] = []


    def replace_function(self, hostname_or_ip_address: str, match_start_index: int) -> Optional[str]:
        status = self.get_status(hostname_or_ip_address)
        if status in self.show_status_list:
            self._status_list.append(status)
            self.counts[status] += 1

            if self.create_csv:
                self.csv_data.append([self._path, self._line_nr, match_start_index + 1, hostname_or_ip_address, status])
            return color_by_status(hostname_or_ip_address, status)
        else:
            return None

    def show_error(self, message: str) -> None:
        if "error" in self.show_status_list:
            error_tag = color_by_status("ERROR", "error")
            print(f"[{error_tag}] {message}")
            self.counts["error"] += 1

    def check_file(self, path: str) -> None:
        try:
            with open(path, "rb") as f:
                file_data = f.read()
        except Exception:
            self.show_error(f"Failed to read file: {path}")
            return

        try:
            lines = file_data.decode().split("\n")
        except Exception:
            self.show_error(f"Binary file, failed to decode: {path}")
            return

        self._path = path

        for index, line in enumerate(lines):
            self._line_nr = index + 1
            # Remember all statuses of a line
            self._status_list = []
            colored_line = self.replace_in_text(line)

            if self._status_list:
                # The line had matches
                worst_status = get_worst_status(self._status_list)
                tag = color_by_status(worst_status.upper(), worst_status, ignore_attrs=True)
                colored_path = colored(path, "magenta")
                print(f"[{tag}] {colored_path}:{self._line_nr}\n{colored_line}\n")


    def get_status(self, match_text: str) -> str:
        if IP_REGEX.fullmatch(match_text):
            return self.config.ip_rules.get_status(match_text)
        else:
            return self.config.hostname_rules.get_status(match_text)


    def print_summary(self) -> None:
        lines = []
        for status in self.show_status_list:
            count = self.counts[status]
            if count != 0:
                colored_count = color_by_status(str(count), status)
                lines.append(f"{colored_count} {status}")

        if lines:
            tag = colored("INFO", "blue")
            print(f"[{tag}] Summary:", ", ".join(lines))


    def has_results(self) -> bool:
        # Only check the status types the user has specified
        for status in self.show_status_list:
            count = self.counts[status]
            if count != 0:
                return True

        return False
