import re
from typing import Optional


class AbstractReplacer:
    def __init__(self, regex: re.Pattern):
        self.regex = regex

    def replace_function(self, value: str, match_start_index: int) -> Optional[str]:
        """
        Override this function to define how the replacer works.
        Returning None or the original value will not modify the target text
        """
        raise Exception("This function needs to be overwritten")

    def replace_in_text(self, text: str) -> str:
        match_list = list(self.regex.finditer(text))
        if match_list:
            # Do the replacing in reverse, since the replacing of text would otherwise mess up the following indices
            for match in reversed(match_list):
                old_value = match.group(0) # 0 = entire match
                start, end = match.span()
                new_value = self.replace_function(old_value, start)

                # new_value: None -> Not modified | a value -> will replace old value
                if new_value != None and new_value != old_value:
                    # Replace the old value with a new value
                    text = f"{text[:start]}{new_value}{text[end:]}"

        return text

