WARNINGS = []


def clear_warnings():
    WARNINGS.clear()


def add_warning(warning: str) -> None:
    WARNINGS.append(warning)
