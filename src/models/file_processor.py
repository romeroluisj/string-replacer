import os
import re
import random
import string
from datetime import datetime
from typing import Optional, Dict, Any, Tuple


class FileProcessorConfig:
    def __init__(self) -> None:
        self.source_file_path: str = ""
        self.find_text: str = ""
        self.replace_text: str = ""
        self.output_file_name: str = ""
        self.max_random_length: int = 10


class FileProcessor:
    def __init__(self) -> None:
        self.config = FileProcessorConfig()

    def set_source_file(self, file_path: str) -> None:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        self.config.source_file_path = file_path

    def set_find_replace_text(self, find_text: str, replace_text: str) -> None:
        self.config.find_text = find_text
        self.config.replace_text = replace_text

    def set_output_file_name(self, output_file_name: str) -> None:
        self.config.output_file_name = output_file_name

    def set_max_random_length(self, length: int) -> None:
        if length <= 0:
            raise ValueError("Length must be a positive number")
        self.config.max_random_length = length

    def generate_random_string(
        self,
        length: Optional[int] = None,
        use_uppercase: bool = True,
        use_lowercase: bool = True,
        use_numbers: bool = True,
    ) -> str:
        if length is None:
            length = self.config.max_random_length
        if length <= 0:
            raise ValueError("Length must be a positive number")
        charset = ""
        if use_uppercase:
            charset += string.ascii_uppercase
        if use_lowercase:
            charset += string.ascii_lowercase
        if use_numbers:
            charset += string.digits
        if not charset:
            raise ValueError("At least one character type must be selected")
        return "".join(random.choices(charset, k=length))

    def get_default_output_name(self) -> str:
        if not self.config.source_file_path:
            return ""
        base_name = os.path.basename(self.config.source_file_path)
        name, ext = os.path.splitext(base_name)
        # Only match underscore-separated date suffix at end
        date_pattern = r"_\d{4}_\d{2}_\d{2}$"
        m = re.search(date_pattern, name)
        if m:
            name = name[: m.start()]
        name = name.rstrip(" _")
        today = datetime.now().strftime("%Y_%m_%d")
        return f"{name}_{today}{ext}"

    def process_file(self) -> str:
        if not self.config.source_file_path:
            raise ValueError("No source file specified")
        if not self.config.output_file_name:
            raise ValueError("No output file name specified")
        try:
            with open(self.config.source_file_path, "r", encoding="utf-8") as f:
                content = f.read()
        except Exception as e:
            raise IOError(f"Error reading source file: {e}")
        if self.config.find_text:
            content = content.replace(self.config.find_text, self.config.replace_text)
        output_path = os.path.join(
            os.path.dirname(self.config.source_file_path), self.config.output_file_name
        )
        try:
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(content)
        except Exception as e:
            raise IOError(f"Error writing output file: {e}")
        return output_path

    def extract_db_passwords_from_first_line(self, content: str) -> Tuple[Optional[str], Optional[str]]:
        if not content.strip():
            return None, None
        first_line = content.split("\n")[0]
        by_match = re.search(r'BY\s+"([^"]+)"', first_line, re.IGNORECASE)
        replace_match = re.search(r'REPLACE\s+"([^"]+)"', first_line, re.IGNORECASE)
        return (by_match.group(1) if by_match else None, replace_match.group(1) if replace_match else None)

    def process_db_password_file(
        self,
        use_uppercase: bool = True,
        use_lowercase: bool = True,
        use_numbers: bool = True,
        pre_generated_password: str = None,
    ) -> str:
        if not self.config.source_file_path:
            raise ValueError("No source file specified")
        if not self.config.output_file_name:
            raise ValueError("No output file name specified")
        try:
            with open(self.config.source_file_path, "r", encoding="utf-8") as f:
                content = f.read()
        except Exception as e:
            raise IOError(f"Error reading source file: {e}")
        new_pw, cur_pw = self.extract_db_passwords_from_first_line(content)
        if not new_pw or not cur_pw:
            raise ValueError(
                "Could not find password patterns in first line. Expected 'BY \"password\"' and 'REPLACE \"password\"' patterns."
            )
        if new_pw == cur_pw:
            raise ValueError(
                f"Cannot create output file: the source file has the same password in both BY and REPLACE clauses ('{cur_pw}')."
            )
        if pre_generated_password:
            updated_new_pw = pre_generated_password
        else:
            updated_new_pw = self.generate_random_string(
                length=self.config.max_random_length,
                use_uppercase=use_uppercase,
                use_lowercase=use_lowercase,
                use_numbers=use_numbers,
            )
        updated_cur_pw = new_pw
        if updated_new_pw == updated_cur_pw:
            raise ValueError(
                f"Cannot create output file: the new password ('{updated_new_pw}') is the same as the current password ('{updated_cur_pw}')."
            )
        updated_content = content.replace(new_pw, updated_new_pw)
        updated_content = updated_content.replace(cur_pw, updated_cur_pw)
        output_path = os.path.join(
            os.path.dirname(self.config.source_file_path), self.config.output_file_name
        )
        try:
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(updated_content)
        except Exception as e:
            raise IOError(f"Error writing output file: {e}")
        return output_path

    def get_file_info(self) -> Dict[str, Any]:
        return {
            "source_file": self.config.source_file_path,
            "find_text": self.config.find_text,
            "replace_text": self.config.replace_text,
            "output_file": self.config.output_file_name,
            "max_random_length": self.config.max_random_length,
        }
