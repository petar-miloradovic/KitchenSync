from datetime import datetime

from ai import ask_ai_for_recipe
from config import BLUE, BOLD, CYAN, GREEN, MAGENTA, RED, YELLOW, color
from storage import ensure_csv_file, read_food_items, write_food_items


def print_header() -> None:
    print()
    print(color("🥑 KitchenSync", BOLD + GREEN))
    print(color("Smart Pantry • Scadenze • Inventario", CYAN))
    print(color("============================================", YELLOW))


def print_menu() -> None:
    print()
    print(color("📋 MENU", BOLD + MAGENTA))
    print(f"1. {color('➕ Aggiungi alimento', GREEN)}")
    print(f"2. {color('📜 Mostra inventario', BLUE)}")
    print(f"3. {color('🗑️  Rimuovi alimento', RED)}")
    print(f"4. {color('💾 Salva/aggiorna CSV', YELLOW)}")
    print(f"5. {color('🤖 Suggerisci un piatto', GREEN)}")
    print(f"0. {color('🚪 Esci', RED)}")
    print(color("Scegli un'opzione: ", BOLD + CYAN), end="")


def read_date_input(prompt: str) -> str:
    while True:
        value = input(color(prompt, YELLOW))
        try:
            datetime.strptime(value, "%Y-%m-%d")
            return value
        except ValueError:
            print(color("⚠️ Data non valida. Usa il formato AAAA-MM-GG", RED))


def add_food_item() -> None:
    print(color("\n➕ Inserimento nuovo alimento", BOLD + GREEN))

    nome = input(color("Nome prodotto: ", CYAN)).strip()
    if not nome:
        print(color("❌ Nome prodotto obbligatorio.", RED))
        return

    barcode = input(color("Barcode: ", CYAN)).strip()
    if not barcode:
        print(color("❌ Barcode obbligatorio.", RED))
        return

    expiry = read_date_input("Data di scadenza (AAAA-MM-GG): ")

    items = read_food_items()
    items.append({
        "nome_prodotto": nome,
        "barcode": barcode,
        "expiry": expiry,
    })
    write_food_items(items)

    print(color("✅ Alimento salvato correttamente!", GREEN))
    print(color(f"   {nome} • {barcode} • {expiry}", YELLOW))


def show_inventory() -> None:
    print(color("\n📜 Inventario alimenti", BOLD + BLUE))
    items = read_food_items()

    if not items:
        print(color("😴 Nessun alimento presente.", YELLOW))
        return

    for index, item in enumerate(sorted(items, key=lambda x: x["expiry"]), start=1):
        expiry_date = datetime.strptime(item["expiry"], "%Y-%m-%d").date()
        today = datetime.now().date()

        if expiry_date < today:
            status = color("SCADUTO", RED)
        elif expiry_date == today:
            status = color("SCADENZA OGGI", YELLOW)
        elif (expiry_date - today).days <= 7:
            status = color("IN SCADENZA", MAGENTA)
        else:
            status = color("OK", GREEN)

        print(
            f"{index}. {color(item['nome_prodotto'], CYAN)} | "
            f"barcode: {color(item['barcode'], YELLOW)} | "
            f"scadenza: {color(item['expiry'], GREEN)} | {status}"
        )


def remove_food_item() -> None:
    print(color("\n🗑️ Rimozione alimento", BOLD + RED))
    items = read_food_items()

    if not items:
        print(color("😴 Nessun alimento da rimuovere.", YELLOW))
        return

    for index, item in enumerate(items, start=1):
        print(f"{index}. {item['nome_prodotto']} | {item['barcode']} | {item['expiry']}")

    choice = input(color("Inserisci il numero da rimuovere: ", CYAN)).strip()
    try:
        idx = int(choice) - 1
    except ValueError:
        print(color("❌ Selezione non valida.", RED))
        return

    if idx < 0 or idx >= len(items):
        print(color("❌ Selezione non valida.", RED))
        return

    removed = items.pop(idx)
    write_food_items(items)
    print(color(f"✅ Rimosso: {removed['nome_prodotto']}", GREEN))


def export_csv() -> None:
    items = read_food_items()
    if not items:
        print(color("😴 Nessun dato da esportare.", YELLOW))
        return

    write_food_items(items)
    print(color("💾 CSV aggiornato in: kitchen_sync_foods.csv", GREEN))


def suggest_recipe_from_inventory() -> None:
    items = read_food_items()
    if not items:
        print(color("😴 Nessun alimento disponibile per suggerire un piatto.", YELLOW))
        return

    print(color("\n🤖 Chiamata all'AI in corso...", BOLD + MAGENTA))
    recipe = ask_ai_for_recipe(items)
    if not recipe:
        return

    print(color("\n🍽️ Risposta AI", BOLD + GREEN))
    print(color(recipe, CYAN))


def run_app() -> None:
    ensure_csv_file()

    while True:
        print_menu()
        choice = input().strip()

        if choice == "1":
            add_food_item()
        elif choice == "2":
            show_inventory()
        elif choice == "3":
            remove_food_item()
        elif choice == "4":
            export_csv()
        elif choice == "5":
            suggest_recipe_from_inventory()
        elif choice == "0":
            print(color("👋 Arrivederci! KitchenSync chiude.", BOLD + GREEN))
            break
        else:
            print(color("❌ Scelta non valida. Riprova.", RED))

        print(color("\n----------------------------------------", YELLOW))
