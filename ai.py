import json
import os
import urllib.error
import urllib.request

from config import color, RED, YELLOW


def get_openrouter_key() -> str:
    api_key = os.getenv("OPENROUTER_API_KEY", "").strip()
    if api_key:
        return api_key

    api_key = "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"
    os.environ["OPENROUTER_API_KEY"] = api_key
    return api_key


def fallback_recipe_from_items(items: list[dict]) -> str:
    names = [item["nome_prodotto"].lower() for item in items]
    present = set(names)

    if "uova" in present and ("patate" in present or "cipolla" in present):
        return (
            "Titolo: Frittata semplice con patate e cipolla\n\n"
            "Perché è adatto: è facile da fare, costa poco e usa ingredienti che spesso si hanno già in casa.\n\n"
            "Tempo: circa 20 minuti\n"
            "Difficoltà: facile\n\n"
            "Cosa ti serve: uova, patate, cipolla, olio, sale e pepe.\n\n"
            "Come si fa:\n"
            "1) Taglia la cipolla e le patate a pezzetti piccoli. Mettili in padella con un filo d'olio e cuoci finché diventano morbidi.\n"
            "2) In una ciotola sbatti le uova con un pizzico di sale e pepe.\n"
            "3) Versa le uova nella padella e lascia cuocere qualche minuto. Quando è quasi pronta, gira la frittata e finisci di cuocere.\n\n"
            "Se vuoi, la puoi mangiare da sola o con un pezzo di pane."
        )
    if "pomodoro" in present and "pane" in present:
        return (
            "Titolo: Pane tostato con pomodoro\n\n"
            "Perché è adatto: è veloce, semplice e perfetto se vuoi preparare qualcosa senza stress.\n\n"
            "Tempo: circa 10 minuti\n"
            "Difficoltà: facile\n\n"
            "Cosa ti serve: pane, pomodoro, aglio, olio, sale e pepe.\n\n"
            "Come si fa:\n"
            "1) Tosta il pane in padella o in forno finché diventa dorato.\n"
            "2) Schiaccia il pomodoro in una ciotola e uniscilo all'aglio, all'olio, al sale e al pepe.\n"
            "3) Spalma il composto sul pane caldo e servi subito.\n\n"
            "Questo piatto è ottimo anche come spuntino semplice."
        )
    if "latte" in present and "uova" in present:
        return (
            "Titolo: Omelette facile\n\n"
            "Perché è adatto: è un piatto molto semplice e veloce, perfetto per chi è alle prime armi in cucina.\n\n"
            "Tempo: circa 15 minuti\n"
            "Difficoltà: facile\n\n"
            "Cosa ti serve: uova, latte, sale, pepe e un filo d'olio.\n\n"
            "Come si fa:\n"
            "1) Rompi le uova in una ciotola e unisci il latte, il sale e il pepe. Mescola bene.\n"
            "2) Versa il composto in una padella con un po' d'olio.\n"
            "3) Aspetta qualche minuto e quando si addensa, piega l'omelette e la servi subito.\n\n"
            "È ottima da sola o con un po' di pane."
        )
    return (
        "Titolo: Insalata fresca di casa\n\n"
        "Perché è adatto: è semplice da preparare, leggera e ti aiuta a usare tutto quello che hai in frigo.\n\n"
        "Tempo: circa 10 minuti\n"
        "Difficoltà: facile\n\n"
        "Cosa ti serve: ingredienti freschi presenti, olio, aceto, sale e pepe.\n\n"
        "Come si fa:\n"
        "1) Lava e taglia gli ingredienti a pezzetti piccoli.\n"
        "2) Mettili in una ciotola e condisci con olio, aceto, sale e pepe.\n"
        "3) Mescola tutto bene e servi subito.\n\n"
        "Se vuoi, puoi aggiungere anche del pane tostato o dei semi."
    )


def ask_ai_for_recipe(items: list[dict]) -> str:
    api_key = get_openrouter_key()
    if not api_key:
        return ""

    products = ", ".join(item["nome_prodotto"] for item in items)
    prompt = (
        "Sei un cuoco semplice e gentile. "
        "Fai una ricetta facile da capire anche per chi non sa cucinare, usando solo questi ingredienti: "
        f"{products}. "
        "Non fare menzioni a bambini, scadenze o contenuti sensibili. "
        "Rispondi in italiano in modo molto semplice, chiaro e senza parole complicate. "
        "Scrivi come se stesse parlando a una persona alle prime armi in cucina. "
        "Formato richiesto: "
        "Titolo: ...\n\n"
        "Perché è adatto: ...\n\n"
        "Tempo: ...\n"
        "Difficoltà: facile\n\n"
        "Cosa ti serve: ...\n\n"
        "Come si fa:\n"
        "1) ...\n"
        "2) ...\n"
        "3) ...\n\n"
        "Consiglio finale: ..."
    )

    payload = {
        "model": "meta-llama/llama-3.1-8b-instruct",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.2,
    }

    req = urllib.request.Request(
        "https://openrouter.ai/api/v1/chat/completions",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://localhost",
            "X-Title": "KitchenSync",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=60) as response:
            data = json.loads(response.read().decode("utf-8"))
            content = data["choices"][0]["message"]["content"]
            cleaned = content.strip().replace("```", "")
            lowered = cleaned.lower()
            if any(pattern in lowered for pattern in ["non posso", "bambini", "scad", "contenuti dei tuoi post", "non posso fornire"]):
                return fallback_recipe_from_items(items)
            return cleaned
    except urllib.error.HTTPError as exc:
        error_body = exc.read().decode("utf-8", errors="ignore")
        print(color(f"❌ Errore API OpenRouter: {exc.code}", RED))
        print(color(error_body[:400], YELLOW))
        return fallback_recipe_from_items(items)
    except Exception as exc:
        print(color(f"❌ Errore durante la chiamata AI: {exc}", RED))
        return fallback_recipe_from_items(items)
