from pathlib import Path

CSV_FILE = Path("kitchen_sync_foods.csv")
CSV_HEADER = ["nome_prodotto", "barcode", "expiry"]

RESET = "\033[0m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
CYAN = "\033[36m"
MAGENTA = "\033[35m"
WHITE = "\033[37m"
BOLD = "\033[1m"


def color(text: str, code: str) -> str:
    return f"{code}{text}{RESET}"
