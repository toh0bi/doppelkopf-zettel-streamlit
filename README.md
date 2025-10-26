# 🃏 Doppelkopf Zettel

Eine Progressive Web App (PWA) zur Verwaltung von Doppelkopf-Spielrunden, gebaut mit Python und Streamlit.

## Features

### ✅ Implementiert
- ✅ Spieler-Eingabe (4-6 Spieler)
- ✅ Rundeneingabe mit Re/Kontra Auswahl
- ✅ Solo-Spiele mit korrekter Punkteberechnung
- ✅ Live-Punktetabelle mit Rangliste und Solo-Anzahl
- ✅ Rundenhistorie als interaktive Tabelle mit kumulativen Punkten
- ✅ Re/Kontra und Bock-Runden Markierung
- ✅ Grafischer Punkteverlauf (Plotly)
- ✅ Erweiterte Statistiken:
  - ✅ Gewinnrate pro Spieler
  - ✅ Beste/schlechteste Pärchen
  - ✅ Durchschnittliche Punkte pro Runde und Bockrunde
  - ✅ Solo-Spiele mit Erfolgsrate
  - ✅ Längste Gewinn-/Verluststrähne
  - ✅ Re vs. Kontra Statistik
- ✅ Session State Speicherung
- ✅ JSON Export/Import

### 🔄 In Arbeit
- [ ] Rundenhistorie editierbar machen
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
- **Charts:** Plotly für interaktive Visualisierungen

## Projektstruktur

```
doppelkopf-zettel-streamlit/
├── streamlit_app.py           # Hauptanwendung
├── requirements.txt           # Python-Abhängigkeiten
├── src/
│   ├── game_logic.py         # Punkteberechnung
│   ├── session_manager.py    # Session-Verwaltung
│   ├── data_manager.py       # Export/Import
│   ├── statistics.py         # Statistik-Berechnungen
│   ├── ui_player_setup.py    # Spieler-Eingabe
│   ├── ui_new_round.py       # Rundeneingabe
│   ├── ui_overview.py        # Übersicht & Statistiken
│   ├── ui_statistics.py      # Erweiterte Statistiken
│   ├── ui_history.py         # Rundenhistorie
│   └── ui_sidebar.py         # Sidebar-Navigation
├── REQUIREMENTS.md            # Vollständige Anforderungen
└── README.md                  # Dieses Dokument
```

## Nutzung

### Session starten
1. App öffnen
2. 4-6 Spielernamen eingeben
3. "Session starten" klicken

### Runde eintragen
1. Tab "Neue Runde" öffnen
2. Punkte auswählen (Buttons 1-5 oder benutzerdefiniert)
3. Aussetzenden Spieler wählen (bei 5-6 Spielern)
4. Gewinner auswählen
   - 1 Gewinner = Solo gewonnen
   - 2 Gewinner = Normalspiel
   - 3 Gewinner = Solo verloren
5. Re/Kontra Team wählen (🟢 Re oder 🔴 Kontra)
6. Optional: Bock-Runde markieren (🎯)
7. "Runde eintragen" klicken

### Session speichern/laden
- **Exportieren:** Sidebar → "Session exportieren" → JSON-Datei herunterladen
- **Importieren:** Sidebar → "Session importieren" → JSON-Datei hochladen

## Entwicklung

### Entwickler-Notizen
- PowerShell-Befehle verwenden (Windows)
- Streamlit Session State für State Management
- Nullsummenspiel: Gesamtpunkte aller Spieler = 0

### Nächste Schritte
1. ✅ Grafischen Punkteverlauf hinzufügen
2. ✅ Re/Kontra und Bock-Runden Tracking
3. ✅ Historie als Tabelle mit kumulativen Punkten
4. ✅ Erweiterte Statistiken implementieren
5. Rundenhistorie editierbar machen
6. Spielabend archivieren

## Lizenz

MIT License

## Autor

Entwickelt mit ❤️ für Doppelkopf-Spieler
