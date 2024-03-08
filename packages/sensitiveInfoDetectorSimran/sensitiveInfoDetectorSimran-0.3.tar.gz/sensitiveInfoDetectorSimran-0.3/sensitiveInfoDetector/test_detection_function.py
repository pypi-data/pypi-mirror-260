from .main import detectingInfo

classInstance = detectingInfo()


def test_sensitive_info():
    example_string = "String contains Username"
    assert classInstance.detect_secrets(example_string) == True


# Output : Test case passed


def test_no_sensitive_info():
    example_string = "String does not contain sensitive data"
    assert classInstance.detect_secrets(example_string) == False


# Output : Test case passed


def test_no_data():
    example_string = " "
    assert classInstance.detect_secrets(example_string) == False


# Output : Test case passed
