import re, os
from .config import patterns


class detectingInfo:
    def __init__(self):
        self.file_path = os.path.join(os.path.dirname(__file__), "data.txt")

    def readingData(self):
        file = open(self.file_path, "r")
        contents = file.read()
        file.close()
        value = self.detect_secrets(contents)
        return value

    def detect_secrets(self, contents):
        for pattern in patterns:
            if re.search(pattern, contents, flags=re.IGNORECASE):
                return True
        else:
            return False


if __name__ == "__main__":
    obj = detectingInfo()
    print(obj.readingData())


# Output :  True
