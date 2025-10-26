# 🃏 Doppelkopf Zettel

Eine Progressive Web App (PWA) zur Verwaltung von Doppelkopf-Spielrunden, gebaut mit Python und Streamlit.

## Features

### ✅ MVP (Phase 1) - Implementiert
- ✅ Spieler-Eingabe (4-6 Spieler)
- ✅ Rundeneingabe (Gewinner + Punkte)
- ✅ Solo-Spiele mit korrekter Punkteberechnung
- ✅ Live-Punktetabelle mit Rangliste
- ✅ Rundenhistorie mit Lösch-Funktion
- ✅ Session State Speicherung
- ✅ JSON Export/Import

### 🔄 Phase 2 (Geplant)
- [ ] Grafischer Punkteverlauf (Plotly/Altair)
- [ ] Erweiterte Statistiken
- [ ] Bock-Runden (Multiplikator)
- [ ] Rundenhistorie editieren
- [ ] Spielabend archivieren

## Punkteberechnung

### Normalspiel (2 vs 2)
- Gewinner je: **+X Punkte**
- Verlierer je: **-X Punkte**
- Beispiel: Eingabe "2" → Gewinner: +2/+2, Verlierer: -2/-2

### Solo-Spiel (1 vs 3)
- **Solo gewinnt:** Solo +X×3, andere je -X
- **Solo verliert:** Solo -X×3, andere je +X
- Beispiel: Eingabe "2", Solo gewinnt → Solo: +6, andere: -2/-2/-2

## Installation & Ausführung

### Lokal ausführen

```powershell
# Repository klonen
git clone <repo-url>
cd doppelkopf-zettel-streamlit

# Abhängigkeiten installieren
pip install -r requirements.txt

# App starten
streamlit run streamlit_app.py
```

Die App öffnet sich automatisch im Browser unter `http://localhost:8501`

### Deployment auf Streamlit Community Cloud

1. Repository auf GitHub pushen (Public Repo)
2. Auf [streamlit.io/cloud](https://streamlit.io/cloud) anmelden
3. "New app" klicken
4. Repository verbinden
5. `streamlit_app.py` als Main file auswählen
6. Deploy klicken

**Fertig!** Die App ist nun online verfügbar und aktualisiert sich automatisch bei Git-Pushes.

## Technologie-Stack

- **Framework:** Streamlit (Python)
- **Datenspeicherung:** Session State + JSON Export
- **Deployment:** Streamlit Community Cloud
- **Charts:** Geplant mit Plotly/Altair

## Projektstruktur

```
doppelkopf-zettel-streamlit/
├── streamlit_app.py        # Hauptanwendung
├── requirements.txt        # Python-Abhängigkeiten
├── REQUIREMENTS.md         # Vollständige Anforderungen
└── README.md              # Dieses Dokument
```

## Nutzung

### Session starten
1. App öffnen
2. 4-6 Spielernamen eingeben
3. "Session starten" klicken

### Runde eintragen
1. Tab "Neue Runde" öffnen
2. Bei Solo: Checkbox aktivieren und Solo-Spieler wählen
3. Gewinner auswählen (2 Spieler bei Normal, Solo oder andere bei Solo-Spiel)
4. Punkte eingeben
5. "Runde eintragen" klicken

### Session speichern/laden
- **Exportieren:** Sidebar → "Session exportieren" → JSON-Datei herunterladen
- **Importieren:** Sidebar → "Session importieren" → JSON-Datei hochladen

## Entwicklung

### Entwickler-Notizen
- PowerShell-Befehle verwenden (Windows)
- Streamlit Session State für State Management
- Nullsummenspiel: Gesamtpunkte aller Spieler = 0

### Nächste Schritte
1. Grafischen Punkteverlauf hinzufügen
2. Bock-Runden implementieren
3. Erweiterte Statistiken
4. Rundenhistorie editierbar machen

## Lizenz

MIT License

## Autor

Entwickelt mit ❤️ für Doppelkopf-Spieler
