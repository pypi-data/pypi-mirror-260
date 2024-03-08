patterns = [
    r"user[_]?name",  # Username
    r"(pass|PASS|Pass_Word|PASS_WORD)",  # Password
    r"\bsocial[_ ]*security[_ ]*number\b",  # Social Security Number
    r"\bcredit[_ ]*card[_ ]*number\b",  # Credit Card Number
    r"\bexpiration[_ ]*date\b",  # Expiration Date
    r"\bcvv\b",  # CVV
    r"\bAPI[_]?\w*",  # API
    r"\bAPI[_ ]*Key\b",  # API_KEY
    r"\bSecret[_]*Key\b",  # Secret_Key
    r"\bSecret[_]?\w*",  # Secret
    r"\b\w*Key\b",  # _Key
]
