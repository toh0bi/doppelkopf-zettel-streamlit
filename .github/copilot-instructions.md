# GitHub Copilot Instructions - Doppelkopf Zettel

## Projekt-Kontext

**Projektname:** Doppelkopf Zettel  
**Typ:** Progressive Web App (PWA) für Doppelkopf-Spielverwaltung  
**Tech-Stack:** Python + Streamlit  
**Deployment:** Streamlit Community Cloud

## Entwicklungsumgebung

### Betriebssystem & Shell
- **OS:** Windows
- **Shell:** PowerShell (nicht Bash!)
- **WICHTIG:** Generiere IMMER PowerShell-Befehle, nie Bash-Befehle

### PowerShell Syntax-Regeln
✅ **Richtig (PowerShell):**
```powershell
cd frontend
...
...
```

oder mit Semikolon:
```powershell
cd frontend; npm install; npm run dev
```

❌ **Falsch (Bash):**
```bash
cd ... && ... && ..  # NICHT verwenden!
```

### Verzeichniswechsel
- Verwende `cd` oder `Set-Location`
- Keine `&&` für Befehlsketten
- Nutze `;` oder separate Befehle

### Beispiele für häufige Befehle

#### Verzeichnis erstellen
```powershell
New-Item -ItemType Directory -Force -Path "src/components"
```

#### Datei erstellen
```powershell
New-Item -ItemType File -Force -Path "src\example.py"
```



#### Mehrere Befehle
```powershell
```

## Tech-Stack Details

### frontend
- **Framework:** Streamlit (Python)

### Daten
- **Export-Format:** JSON
- **Session-ID:** Cookie-basiert (keine Backend-Persistierung)

## Code-Stil & Konventionen
tbd

### Dateistruktur
tbd

## Doppelkopf-Spiellogik

### Punkteberechnung

#### Normalspiel (2 vs 2, bei 4 Spielern)
- Gewinner je: **+X Punkte**
- Verlierer je: **-X Punkte**
- Beispiel: Eingabe "2" → Gewinner: +2/+2, Verlierer: -2/-2

#### Solo-Spiel (1 vs 3)
- **Solo gewinnt:** Solo +X×3, andere je -X
- **Solo verliert:** Solo -X×3, andere je +X
- Beispiel: Eingabe "2", Solo gewinnt → Solo: +6, andere: -2/-2/-2

#### Bei 5-6 Spielern
- Berechnung entsprechend anpassen
- Teams können unterschiedlich groß sein

### Bock-Runden (Multiplikator)
- Alle Punkte werden mit Multiplikator (2, 3, ...) multipliziert
- Automatisches Deaktivieren nach X Runden

## Wichtige Features (MVP Priorität)

### Phase 1: MVP
1. ✅ Spieler-Eingabe (4 Spieler)
2. ✅ Rundeneingabe (Gewinner + Punkte)
3. ✅ Punktetabelle
4. ✅ Streamlit Session State Speicherung
5. ✅ JSON Export

### Später (Phase 2+)
- 5-6 Spieler
- Solo-Spiele
- Grafischer Verlauf (Plotly/Altair)
- Rundenhistorie editieren
- Bock-Runden

## Naming Conventions



## Git Workflow

### Commit Messages (Deutsch)
```
feat: Spieler-Eingabe implementiert
fix: Punkteberechnung bei Solo korrigiert
refactor: ScoreBoard Komponente aufgeteilt
docs: README aktualisiert
```


## Testing & Validierung

### Wichtige Checks
- [ ] Gesamtpunktzahl ist immer 0 (Nullsummenspiel)
- [ ] Mindestens 4 Spieler erforderlich
- [ ] Punkte sind numerisch
- [ ] Session State funktioniert
- [ ] Export/Import von JSON

## Deployment

### Streamlit Community Cloud (Primär)
- **Kostenlos** für Public GitHub Repos
- **Automatisches Deployment** bei Git Push
- **Setup-Schritte:**
  1. GitHub Repository erstellen (Public)
  2. Code committen & pushen
  3. Auf https://streamlit.io/cloud anmelden
  4. Repository verbinden
  5. App deployen
- **Requirements:**
  - `requirements.txt` im Root
  - `streamlit_app.py` oder `app.py` als Einstiegspunkt
  - Secrets über Streamlit Dashboard (falls nötig)

### Alternative: AWS/Docker (später)
- Für mehr Kontrolle oder Private Hosting
- Höherer Aufwand, Kosten

## Hilfreiches

### Entwickler-Hintergrund
- Entwickler hat Erfahrung mit **Flask und Streamlit (Python)**

### Dokumentation
- Siehe `REQUIREMENTS.md` für vollständige Anforderungen
- Datenmodell ist in Requirements definiert

---

**WICHTIG:** Generiere IMMER PowerShell-Befehle, NIE Bash-Befehle!
