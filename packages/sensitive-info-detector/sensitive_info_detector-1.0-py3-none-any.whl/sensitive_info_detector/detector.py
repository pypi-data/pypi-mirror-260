import re

from patterns import secret_patterns


def check_for_secrets(file_path):
    try:
        with open(file_path, "r") as file:
            content = file.read()
            for pattern in secret_patterns:
                if re.search(pattern, content):
                    return True
        return False

    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return False


file_path = "/home/user/assignments/assignments/sensitive_info_detector/demo.txt"
print(check_for_secrets(file_path))
