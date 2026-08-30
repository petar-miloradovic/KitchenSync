# 🥑 KitchenSync — Smart Pantry, Expiration Tracking & Zero-Waste Recipe Engine
> **The All-in-One Intelligent Home Assistant for Waste Prevention, Smart Grocery Planning, and Effortless Meal Creation.**

---

## 🌍 Language Selection / Selezione Lingua

- [English Version](#english-version)
- [Versione Italiana](#versione-italiana)

---

<a name="english-version"></a>
# 🇬🇧 English Version

## 📌 Executive Overview
**KitchenSync** is a full-stack, cross-platform software solution designed to solve three interconnected daily friction points:
1. **Preventable Food Waste & Expiration Losses:** Millions of households throw away edible groceries simply because products are forgotten at the back of refrigerators or pantries.
2. **Daily Decision Fatigue:** The constant mental friction of deciding *"What should we cook tonight?"* given limited time, energy, and available ingredients.
3. **Inefficient Grocery Planning:** Duplicate purchases, missed essential items, and lack of shared clarity in co-living or multi-member households.

By combining **automated expiration tracking**, **dynamic recipe matching**, and **real-time collaborative shopping lists**, KitchenSync transforms daily food management into a seamless, automated, and cost-saving workflow.

---

## 💡 Core Features & Functional Architecture

### 1. 🥫 Smart Pantry & Expiration Tracking Engine
- **Bar-code & Receipt OCR Scanning:** Instantly log food items using device cameras backed by Open Food Facts API and computer vision parsing.
- **Dynamic Shelf-Life Estimation:** Automatically assigns estimated expiration windows based on item categories (e.g., Dairy, Fresh Produce, Frozen Goods, Pantry Staples).
- **Proactive Expiration Alerts:** Tiered notifications (e.g., 3 days prior, 1 day prior, day of expiration) delivered via FCM (Firebase Cloud Messaging) and push alerts.

### 2. 🍲 MealCraft AI — Dynamic Recipe Engine
- **"Zero-Waste" Expiration-First Sorting:** Prioritizes recipes that utilize ingredients reaching their expiration thresholds first.
- **Constraint-Based Matching:** Filters recipes by prep time (<15 min, 30 min, batch cooking), available appliances (Air Fryer, Microwave, Stove, Oven), and dietary preferences.
- **Step-by-Step Hands-Free Cooking Mode:** Clean UI with integrated cooking timers and wake-lock display for effortless kitchen execution.

### 3. 🛒 Household Collaborative Shopping & Budgeting
- **Real-Time WebSocket Synchronization:** Live updates across household members when items are added, checked off, or updated.
- **One-Tap Pantry Transfer:** Moving checked-off items from the shopping list directly into the virtual pantry with automated expiration tagging.
- **Shared Household Access:** Multi-user synchronization using secure QR codes or invite links.

---

## 🏗️ System Architecture & Technology Stack

```
                               ┌───────────────────────────┐
                               │   Mobile & Web Clients    │
                               │ (Flutter / React Native)  │
                               └─────────────┬─────────────┘
                                             │ HTTPS / WebSockets
                                             ▼
                               ┌───────────────────────────┐
                               │     REST & Realtime API   │
                               │  (Node.js / Express / Go) │
                               └─────────────┬─────────────┘
                                             │
      ┌──────────────────────────────────────┼──────────────────────────────────────┐
      │                                      │                                      │
      ▼                                      ▼                                      ▼
┌──────────────┐                       ┌──────────────┐                       ┌──────────────┐
│  PostgreSQL  │                       │  Meilisearch │                       │ Open Food    │
│ (Primary DB) │                       │(Recipe Index)│                       │  Facts API   │
└──────────────┘                       └──────────────┘                       └──────────────┘
```

| Layer | Recommended Technology | Technical Justification |
| :--- | :--- | :--- |
| **Frontend Mobile/Web** | Flutter / React Native | Single codebase targeting iOS, Android, and Web; fast camera integration for barcode scanning. |
| **Backend API** | Node.js (TypeScript) or Go | Asynchronous, event-driven I/O ideal for real-time WebSocket communication and rapid API response times. |
| **Primary Database** | PostgreSQL + Prisma ORM | Relational integrity for user authentication, household relations, inventory tracking, and transaction logs. |
| **Search & Matching Engine** | Meilisearch / Typesense | Sub-millisecond full-text and faceted search for matching available ingredients with recipe databases. |
| **Realtime Sync** | Supabase Realtime / Socket.io | Bi-directional WebSocket channels for instant multi-user household shopping list updates. |
| **Third-Party Data API** | Open Food Facts API | Global, open-source database containing millions of consumer product barcodes and nutritional data. |

---

## 🗄️ Database Schema (PostgreSQL DDL)

```sql
-- Database Definition for KitchenSync

CREATE TABLE households (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(100) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    household_id UUID REFERENCES households(id) ON DELETE SET NULL,
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE pantry_items (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    household_id UUID NOT NULL REFERENCES households(id) ON DELETE CASCADE,
    product_name VARCHAR(150) NOT NULL,
    barcode VARCHAR(50),
    category VARCHAR(50) DEFAULT 'General',
    quantity NUMERIC(6,2) DEFAULT 1.00,
    unit VARCHAR(20) DEFAULT 'pcs',
    location VARCHAR(30) CHECK (location IN ('Fridge', 'Freezer', 'Pantry')),
    expiration_date DATE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE recipes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title VARCHAR(150) NOT NULL,
    prep_time_minutes INT NOT NULL,
    difficulty_level VARCHAR(20) CHECK (difficulty_level IN ('Easy', 'Medium', 'Hard')),
    instructions TEXT NOT NULL,
    appliance_required VARCHAR(50)
);

CREATE TABLE recipe_ingredients (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    recipe_id UUID NOT NULL REFERENCES recipes(id) ON DELETE CASCADE,
    ingredient_name VARCHAR(100) NOT NULL,
    quantity NUMERIC(6,2),
    unit VARCHAR(20)
);

CREATE TABLE shopping_list_items (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    household_id UUID NOT NULL REFERENCES households(id) ON DELETE CASCADE,
    item_name VARCHAR(150) NOT NULL,
    is_purchased BOOLEAN DEFAULT FALSE,
    added_by_user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
```

---

## 🚀 Roadmap & Development Timeline

- [x] **Phase 1: Architecture & Data Modeling** — System design, PostgreSQL schema, wireframing.
- [ ] **Phase 2: Core Barcode & Inventory MVP** — Barcode scanning integration via Open Food Facts API and pantry CRUD.
- [ ] **Phase 3: Real-Time Sync & Notifications** — WebSocket-based shopping lists and FCM expiration notifications.
- [ ] **Phase 4: Recipe Matching Engine Integration** — Search indexing for Zero-Waste meal suggestions based on pantry state.
- [ ] **Phase 5: Beta Testing & Production Release** — User testing, security auditing, and deployment.

---

<a name="versione-italiana"></a>
# 🇮🇹 Versione Italiana

## 📌 Panoramica Esecutiva
**KitchenSync** è una soluzione software full-stack e multipiattaforma progettata per risolvere tre problematiche quotidiane interconnesse:
1. **Spreco Alimentare ed Economico Evitabile:** Miliardi di euro in generi alimentari vengono sprecati ogni anno perché i prodotti vengono dimenticati nel fondo del frigorifero o della dispensa.
2. **Fatica Decisionale Quotidiana:** Lo stress mentale nel dover decidere *"Cosa cuciniamo stasera?"* considerando tempo limitato, energie ridotte e ingredienti disponibili.
3. **Pianificazione Inefficiente della Spesa:** Acquisti duplicati, ingredienti essenziali dimenticati e mancanza di coordinamento nei nuclei familiari o tra coinquilini.

Combinando il **tracciamento automatico delle scadenze**, un **motore dinamico di raccomandazione ricette** e **liste della spesa collaborative in tempo reale**, KitchenSync trasforma la gestione del cibo in un processo automatizzato, efficiente ed economico.

---

## 💡 Funzionalità Principali e Architettura Funzionale

### 1. 🥫 Dispensa Intelligente e Tracciamento Scadenze
- **Scansione Barcode e Scontrini (OCR):** Inserimento rapido dei prodotti tramite la fotocamera dello smartphone integrata con l'API Open Food Facts e riconoscimento testo.
- **Stima Dinamica della Scadenza:** Assegnazione automatica della vita utile stimata in base alla categoria del prodotto (es. Latticini, Prodotti Freschi, Surgelati, Dispensa).
- **Notifiche Proattive di Scadenza:** Avvisi e push notification multilivello (es. 3 giorni prima, 1 giorno prima, il giorno stesso della scadenza).

### 2. 🍲 MealCraft AI — Motore Dinamico di Ricette
- **Ordinamento Anti-Spreco:** Priorità assoluta alle ricette che utilizzano ingredienti prossimi alla data di scadenza.
- **Filtri su Misura:** Selezione per tempo di preparazione (<15 min, 30 min, preparazione anticipata), elettrodomestici a disposizione (Friggitrice ad aria, Microonde, Fornelli, Forno) e preferenze alimentari.
- **Modalità Cucina Passo-Passo:** Interfaccia pulita a schermo attivo con timer di cottura integrati.

### 3. 🛒 Spesa Collaborativa per il Gruppo Domestico
- **Sincronizzazione Real-Time via WebSocket:** Aggiornamenti istantanei per tutti i membri della casa quando un articolo viene aggiunto o spuntato.
- **Trasferimento In Dispensa con Un Tap:** Gli articoli spuntati dalla lista della spesa vengono trasferiti direttamente nella dispensa virtuale con applicazione automatica della data di scadenza.
- **Accesso Condiviso Facile:** Associazione dei membri del gruppo domestico tramite codice QR o link d'invito sicuro.

---

## 🏗️ Architettura di Sistema e Stack Tecnologico

| Layer | Tecnologia Consigliata | Motivazione Tecnica |
| :--- | :--- | :--- |
| **Frontend Mobile/Web** | Flutter / React Native | Codice unico per iOS, Android e Web; integrazione nativa e veloce con la fotocamera per lo scanner barcode. |
| **Backend API** | Node.js (TypeScript) o Go | I/O asincrono orientato agli eventi, ideale per la comunicazione WebSocket in tempo reale e risposte API rapide. |
| **Database Principale** | PostgreSQL + Prisma ORM | Integrità relazionale per autenticazione utenti, gruppi domestici, inventario e log delle spese. |
| **Motore di Ricerca & Matching** | Meilisearch / Typesense | Ricerca full-text e sfaccettata ultra-veloce (<1ms) per associare gli ingredienti in dispensa alle ricette. |
| **Sincronizzazione Realtime** | Supabase Realtime / Socket.io | Canali WebSocket bidirezionali per l'aggiornamento istantaneo della lista spesa tra più utenti. |
| **API Dati Esterna** | Open Food Facts API | Database globale open-source contenente milioni di codici a barre e schede nutrizionali dei prodotti. |

---

## 🗄️ Schema del Database (PostgreSQL DDL)

```sql
-- Definizione del Database per KitchenSync

CREATE TABLE households (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(100) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    household_id UUID REFERENCES households(id) ON DELETE SET NULL,
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE pantry_items (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    household_id UUID NOT NULL REFERENCES households(id) ON DELETE CASCADE,
    product_name VARCHAR(150) NOT NULL,
    barcode VARCHAR(50),
    category VARCHAR(50) DEFAULT 'Generico',
    quantity NUMERIC(6,2) DEFAULT 1.00,
    unit VARCHAR(20) DEFAULT 'pz',
    location VARCHAR(30) CHECK (location IN ('Frigo', 'Freezer', 'Dispensa')),
    expiration_date DATE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE recipes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title VARCHAR(150) NOT NULL,
    prep_time_minutes INT NOT NULL,
    difficulty_level VARCHAR(20) CHECK (difficulty_level IN ('Facile', 'Media', 'Difficile')),
    instructions TEXT NOT NULL,
    appliance_required VARCHAR(50)
);

CREATE TABLE recipe_ingredients (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    recipe_id UUID NOT NULL REFERENCES recipes(id) ON DELETE CASCADE,
    ingredient_name VARCHAR(100) NOT NULL,
    quantity NUMERIC(6,2),
    unit VARCHAR(20)
);

CREATE TABLE shopping_list_items (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    household_id UUID NOT NULL REFERENCES households(id) ON DELETE CASCADE,
    item_name VARCHAR(150) NOT NULL,
    is_purchased BOOLEAN DEFAULT FALSE,
    added_by_user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
```

---

## 🚀 Roadmap e Fasi di Sviluppo

- [x] **Fase 1: Architettura e Modellazione Dati** — Progettazione di sistema, schema PostgreSQL, wireframe.
- [ ] **Fase 2: MVP Scanner Barcode e Inventario** — Integrazione scanner con Open Food Facts API e gestione CRUD dispensa.
- [ ] **Fase 3: Sincronizzazione Real-Time e Notifiche** — Lista spesa via WebSocket e notifiche push per prodotti in scadenza.
- [ ] **Fase 4: Integrazione Motore Ricette Anti-Spreco** — Indexing e algoritmo di ricerca per raccomandare pasti in base agli ingredienti disponibili.
- [ ] **Fase 5: Beta Test e Release in Produzione** — Test utente, audit di sicurezza e rilascio delle app negli store.

---
*Created for the KitchenSync Open Project.*
