#!/bin/bash

# KitchenSync Local Setup Script
echo "📦 Configurazione dipendenze locali per KitchenSync..."

# Crea la cartella libs se non esiste
mkdir -p libs

# Tenta di installare usando python3 -m pip (metodo più affidabile)
echo "🔄 Tentativo di installazione con python3 -m pip..."
python3 -m pip install -r requirements.txt --target ./libs

if [ $? -eq 0 ]; then
    echo "✅ Dipendenze installate correttamente in ./libs"
    echo "🚀 Ora puoi avviare l'app con: python3 gui.py"
else
    echo "🔄 Tentativo con pip3..."
    pip3 install -r requirements.txt --target ./libs

    if [ $? -eq 0 ]; then
        echo "✅ Dipendenze installate correttamente in ./libs"
        echo "🚀 Ora puoi avviare l'app con: python3 gui.py"
    else
        echo "❌ Errore: pip non trovato o non funzionante."
        echo "💡 Prova a installarlo con: sudo apt install python3-pip"
        exit 1
    fi
fi
