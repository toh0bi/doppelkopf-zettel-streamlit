# Doppelkopf Zettel - Anforderungsdokument

## Projektübersicht

**Name:** Doppelkopf Zettel  
**Typ:** Progressive Web App (PWA)  
**Datum:** 26. Oktober 2025

Eine cookiebasierte Web-Anwendung zur Verwaltung von Doppelkopf-Spielrunden ohne Backend-Persistierung. Ähnlich wie Excalidraw funktioniert die App vollständig im Browser mit lokalem Speichern und Exportieren von Spieldaten.

---

## Kernkonzept

- **Keine Benutzerregistrierung/Login erforderlich**
- **Cookie-basierte Session-Verwaltung**
- **Lokale Datenspeicherung** im Browser
- **Export/Import-Funktionalität** für Spielstände (ähnlich Excalidraw)
- **Offenes Datenformat** (.duckdb oder alternatives offenes Format)

---

## Funktionale Anforderungen

### 1. Session-Management

#### 1.1 Neue Session starten
- [ ] Eingabe von 4-6 Spielernamen
- [ ] Validierung: Mindestens 4 Spieler erforderlich
- [ ] Cookie-basierte Session-ID Generierung
- [ ] Automatisches Speichern im Browser (localStorage/IndexedDB)

#### 1.2 Session laden
- [ ] Import einer gespeicherten Spiel-Datei
- [ ] Wiederaufnahme einer laufenden Session aus Cookie
- [ ] Drag & Drop Support für Datei-Import
- [ ] Mehrere gespeicherte Sessions verwalten können

#### 1.3 Session speichern/exportieren
- [ ] Export als .duckdb oder alternatives offenes Format (JSON, SQLite)
- [ ] Automatisches Speichern nach jeder Änderung
- [ ] Manueller Export-Button
- [ ] Dateiname mit Datum/Zeitstempel

---

### 2. Spieler-Verwaltung

- [ ] 4-6 Spieler pro Session
- [ ] Spielernamen editierbar
- [ ] Spielerfarben/Avatare zur besseren Unterscheidung (optional)
- [ ] Spieler können während des Spiels nicht entfernt werden
- [ ] Anzeige der aktuellen Punktzahl pro Spieler

---

### 3. Rundenerfassung

#### 3.1 Normale Runde
- [ ] Auswahl der Gewinner (2 Spieler beim Re-Team)
- [ ] Eingabe der Punktzahl (flexibel: 1, 2, 3, 4+ Punkte je nach Ansagen)
- [ ] Automatische Verteilung: Symmetrisch - jeder Gewinner bekommt gleich viele Punkte, jeder Verlierer verliert gleich viele
- [ ] Bestätigung der Rundeneingabe
- [ ] **Logik:** Bei 4 Spielern (2 vs 2): Gewinner je +X, Verlierer je -X
  - Beispiel: Eingabe "2 Punkte" → Gewinner: +2/+2, Verlierer: -2/-2

#### 3.2 Solo-Spiele
- [ ] Checkbox/Toggle für Solo-Spiel
- [ ] Auswahl des Solo-Spielers
- [ ] Bei Gewinn: Solo-Spieler gewinnt gegen alle anderen (1 vs 3)
- [ ] Bei Verlust: Alle anderen gewinnen gegen Solo-Spieler
- [ ] **Logik:** 
  - Solo gewinnt: Solo +X×3, andere je -X
  - Solo verliert: Solo -X×3, andere je +X
  - Beispiel: Eingabe "2 Punkte", Solo gewinnt → Solo: +6, andere: -2/-2/-2

#### 3.3 Sonderregeln
- [ ] "Nächste X Runden verdoppelt" - Multiplikator für kommende Runden
- [ ] Anzeige aktiver Sonderregeln
- [ ] Automatisches Deaktivieren nach Ablauf
- [ ] Andere Sonderregeln erweiterbar (z.B. "Bock-Runden")

#### 3.4 Rundenhistorie bearbeiten
- [ ] Vergangene Runden in Liste anzeigen
- [ ] Edit-Funktion für jede Runde
- [ ] Löschen einzelner Runden
- [ ] Neuberechnung der Gesamtpunktzahl nach Änderungen
- [ ] Undo/Redo-Funktionalität (optional)

---

### 4. Übersichten & Visualisierung

#### 4.1 Gesamtstand-Tabelle
- [ ] Live-Aktualisierung nach jeder Runde
- [ ] Sortierung nach Punktzahl (höchste zuerst)
- [ ] Anzeige der Punktedifferenz zum Führenden
- [ ] Rundenanzahl pro Spieler

#### 4.2 Grafische Auswertung
- [ ] Punkteverlauf als Liniendiagramm
- [ ] X-Achse: Rundennummer
- [ ] Y-Achse: Punktzahl
- [ ] Eine Linie pro Spieler (unterschiedliche Farben)
- [ ] Interaktive Tooltips (Rundendetails beim Hover)
- [ ] Zoom/Pan-Funktionalität (optional)

#### 4.3 Statistiken
- [ ] Gewinnrate pro Spieler
- [ ] Durchschnittliche Punkte pro Runde
- [ ] Anzahl Solo-Spiele und Erfolgsrate
- [ ] Längste Gewinn-/Verluststrähne

---

### 5. Spielabend abschließen

- [ ] "Spielabend beenden"-Button
- [ ] Finale Zusammenfassung anzeigen
- [ ] Archivierung des Spielabends
- [ ] Spielabend mit Datum/Uhrzeit versehen
- [ ] Weiterhin editierbar in der Historie
- [ ] Möglichkeit, einen neuen Spielabend mit gleichen Spielern zu starten

---

### 6. Langzeit-Historie & Auswertung

#### 6.1 Archiv vergangener Spielabende
- [ ] Liste aller beendeten Spielabende
- [ ] Filterung nach Datum/Spielern
- [ ] Detailansicht alter Spielabende
- [ ] Export einzelner oder aller Spielabende

#### 6.2 Übergreifende Statistiken
- [ ] Gesamtstatistik über alle Spielabende
- [ ] Rangliste der erfolgreichsten Spieler
- [ ] Entwicklung über Zeit
- [ ] Vergleich verschiedener Spielabende

---

## Nicht-funktionale Anforderungen

### Performance
- [ ] Schnelle Ladezeiten (< 2 Sekunden)
- [ ] Flüssige Animationen (60 FPS)
- [ ] Optimiert für Mobile und Desktop

### Usability
- [ ] Intuitive Benutzeroberfläche
- [ ] Responsive Design (Mobile-First)
- [ ] Touch-optimiert für Tablets/Smartphones
- [ ] Tastaturnavigation möglich
- [ ] Barrierefreiheit (ARIA-Labels, Kontraste)

### Datensicherheit
- [ ] Keine Daten verlassen das Gerät (außer bei manuellem Export)
- [ ] Kein Server-seitiges Tracking
- [ ] DSGVO-konform (da keine Daten gespeichert werden)

### Browser-Kompatibilität
- [ ] Chrome/Edge (neueste 2 Versionen)
- [ ] Firefox (neueste 2 Versionen)
- [ ] Safari (neueste 2 Versionen)
- [ ] Mobile Browser (iOS Safari, Chrome Mobile)

---

## Technische Architektur

### Frontend/Backend
- **Framework:** Streamlit (Python)
- **Styling:** Streamlit's native Components + Custom CSS
- **Charts:** Plotly / Altair (beide mit Streamlit kompatibel)
- **State Management:** Streamlit Session State
- **Begründung:** Streamlit ist ideal für dieses Projekt:
  - Bereits bekannt (Flask/Streamlit-Erfahrung)
  - Python-basiert, keine JavaScript-Kenntnisse nötig
  - Sehr schnelles Prototyping
  - Native Chart-Unterstützung
  - Einfaches State Management mit `st.session_state`
  - Perfekt für Daten-Apps

### Datenspeicherung
- **Browser:** Streamlit Session State (In-Memory während der Session)
- **Persistierung:** Cookies für Session-ID + lokale JSON-Dateien
- **Export-Format:** JSON (.json) - einfach, menschenlesbar, offen
  - Zusätzlich: CSV für Tabellen-Export (optional)
- **Alternative:** SQLite für lokale Datenbankfunktionalität

### Hosting & Deployment
- **Primär:** Streamlit Community Cloud (kostenlos, einfach, empfohlen!)
  - Direkte GitHub-Integration
  - Automatisches Deployment bei Git Push
  - Kostenlos für Public Repos
  - HTTPS und Custom Domains möglich
  - Secrets Management integriert
- **Alternative (später):** AWS EC2 + CloudFront (mehr Kontrolle, Kosten)
- **CI/CD:** Automatisch durch Streamlit Community Cloud

### Progressive Web App (PWA)
- [ ] Streamlit unterstützt PWA-Features limitiert
- [ ] Fokus auf responsive Web-App statt native PWA
- [ ] Mobile-optimierte UI durch Streamlit's responsive Design

---

## Datenmodell

### Session
```python
from dataclasses import dataclass
from typing import List, Dict, Optional
from datetime import datetime
from enum import Enum

class SessionStatus(Enum):
    ACTIVE = "active"
    FINISHED = "finished"

@dataclass
class Session:
    id: str                          # UUID
    created_at: datetime
    updated_at: datetime
    status: SessionStatus
    players: List['Player']
    rounds: List['Round']
    settings: 'SessionSettings'
```

### Player
```python
@dataclass
class Player:
    id: str
    name: str
    color: Optional[str] = None
    total_score: int = 0
```

### Round
```python
class RoundType(Enum):
    NORMAL = "normal"
    SOLO = "solo"

@dataclass
class Round:
    id: str
    round_number: int
    timestamp: datetime
    type: RoundType
    winners: List[str]               # Player IDs
    points: int
    multiplier: int = 1              # 1, 2, 3... (für Bock-Runden)
    is_solo: bool = False
    solo_player: Optional[str] = None  # Player ID
    scores: Dict[str, int] = None    # Score-Änderung pro Spieler
    notes: Optional[str] = None      # Optionale Notizen
    
    def __post_init__(self):
        if self.scores is None:
            self.scores = {}
```

### SessionSettings
```python
@dataclass
class SessionSettings:
    enable_bock_rounds: bool = False
    active_bock_rounds: int = 0      # Wie viele Bock-Runden noch aktiv
    points_per_win: int = 1          # Standard: 1
    solo_multiplier: int = 3         # Standard: 3
```

---

## User Stories

### Epic 1: Session-Start
**Als Spieler** möchte ich schnell eine neue Runde starten können, **damit** wir sofort mit dem Spielen beginnen können.

- User Story 1.1: Namen eingeben (4-6 Spieler)
- User Story 1.2: Session automatisch speichern
- User Story 1.3: Session später fortsetzen können

### Epic 2: Punkteerfassung
**Als Punktezähler** möchte ich nach jeder Runde schnell die Gewinner und Punkte eintragen, **damit** die Übersicht aktuell bleibt.

- User Story 2.1: Gewinner auswählen
- User Story 2.2: Punkte eingeben
- User Story 2.3: Solo-Spiel erfassen
- User Story 2.4: Sonderregeln aktivieren

### Epic 3: Auswertung
**Als Spieler** möchte ich jederzeit den aktuellen Stand sehen, **damit** ich weiß, wer führt.

- User Story 3.1: Tabelle mit Gesamtpunkten
- User Story 3.2: Grafischer Verlauf
- User Story 3.3: Rundenhistorie einsehen

### Epic 4: Datenverwaltung
**Als Nutzer** möchte ich meine Spielstände exportieren und importieren können, **damit** ich nicht abhängig vom Browser bin.

- User Story 4.1: Export als Datei
- User Story 4.2: Import einer Datei
- User Story 4.3: Mehrere Sessions verwalten

---

## UI/UX Wireframe-Ideen

### Hauptansicht (Streamlit Layout)
```
┌─────────────────────────────────────────────────┐
│  🎴 Doppelkopf Zettel                          │
│  [Export JSON] [Import JSON] [Neuer Spielabend]│
├─────────────────────────────────────────────────┤
│                                                 │
│  📊 Gesamtstand - Runde #12                    │
│  ┌─────────────────────────────────────────┐   │
│  │  Spieler    │  Punkte  │  +/-           │   │
│  ├─────────────────────────────────────────┤   │
│  │  🥇 Anna    │   +45    │  ▲ 13         │   │
│  │  🥈 Ben     │   +32    │  -            │   │
│  │  🥉 Clara   │   -12    │  ▼ 44         │   │
│  │     David   │   -18    │  ▼ 50         │   │
│  └─────────────────────────────────────────┘   │
│                                                 │
│  📈 Punkteverlauf (Plotly/Altair Chart)        │
│  ┌─────────────────────────────────────────┐   │
│  │         ╱─────Anna                      │   │
│  │     ╱───                                │   │
│  │ ───          Ben ───                    │   │
│  │         Clara ────╲                     │   │
│  │                    ╲── David            │   │
│  └─────────────────────────────────────────┘   │
│                                                 │
│  ➕ Neue Runde erfassen                         │
│  ┌─────────────────────────────────────────┐   │
│  │  Gewinner auswählen:                    │   │
│  │  ☑ Anna    ☐ Ben    ☑ Clara    ☐ David │   │
│  │                                          │   │
│  │  Punkte: [2 ▼]                          │   │
│  │                                          │   │
│  │  ☐ Solo-Spiel                           │   │
│  │  Solo-Spieler: [Bitte wählen... ▼]     │   │
│  │                                          │   │
│  │  [Runde eintragen]                      │   │
│  └─────────────────────────────────────────┘   │
│                                                 │
│  📜 Rundenhistorie (expandable)                │
│  ▼ Letzte 10 Runden anzeigen                   │
│  ┌─────────────────────────────────────────┐   │
│  │  #12: Anna, Clara (+2) vs Ben, David (-2) │
│  │  #11: Ben SOLO (+6) vs alle andere (-2)   │
│  │  #10: Ben, David (+1) vs Anna, Clara (-1) │
│  │  ...                                       │
│  └─────────────────────────────────────────┘   │
│                                                 │
└─────────────────────────────────────────────────┘
```

### Streamlit Sidebar (Navigation)
```
┌───────────────────┐
│ 🎴 Navigation     │
├───────────────────┤
│ 🏠 Aktuell       │
│ 📊 Statistiken   │
│ 📚 Historie      │
│ ⚙️ Einstellungen │
│                   │
│ Status:           │
│ ● Spielabend aktiv│
│ Spieler: 4        │
│ Runden: 12        │
└───────────────────┘
```

---

## Roadmap & Phasen

### Phase 1: MVP (Minimal Viable Product)
- [ ] 4 Spieler Unterstützung
- [ ] Basis-Rundenerfassung (Gewinner + Punkte)
- [ ] Einfache Tabelle mit Gesamtstand
- [ ] localStorage-Speicherung
- [ ] Export als JSON

**Zeitschätzung:** 2-3 Wochen

### Phase 2: Erweiterte Funktionen
- [ ] 5-6 Spieler Support
- [ ] Solo-Spiele
- [ ] Sonderregeln (Bock-Runden)
- [ ] Rundenhistorie editieren
- [ ] Grafischer Punkteverlauf

**Zeitschätzung:** 2-3 Wochen

### Phase 3: Historie & Statistiken
- [ ] Spielabende abschließen
- [ ] Archiv vergangener Spielabende
- [ ] Erweiterte Statistiken
- [ ] Langzeit-Auswertungen

**Zeitschätzung:** 2 Wochen

### Phase 4: Polish & Deployment
- [ ] Mobile-optimiertes Design perfektionieren
- [ ] **Streamlit Community Cloud Deployment**
  - [ ] GitHub Repository vorbereiten
  - [ ] requirements.txt finalisieren
  - [ ] Secrets konfigurieren (falls nötig)
  - [ ] App auf Streamlit Community Cloud deployen
  - [ ] Custom Domain einrichten (optional)
- [ ] Performance-Optimierung
- [ ] Finales Testing auf verschiedenen Geräten

**Zeitschätzung:** 1-2 Wochen

---

## Offene Fragen & Entscheidungen

### Datenformat
- **Entscheidung:** JSON (.json)
  - ✅ Einfach, menschenlesbar
  - ✅ Von jedem Tool lesbar
  - ✅ Kein zusätzliche Libraries nötig
  - ✅ Perfekt für Export/Import

### Punktesystem
- **Entscheidung:** Flexible Punkteingabe pro Runde
  - Spieler geben nach jeder Runde die Punkte ein (z.B. 1, 2, 3, 4+)
  - Unterschiedlich je nach Ansagen (Re, Kontra, Keine 90, etc.)
  - System verteilt symmetrisch auf Gewinner/Verlierer
  - **Bei 4 Spielern (2 vs 2):** Gewinner je +X, Verlierer je -X
  - **Bei Solo (1 vs 3):** Solo gewinnt: +X×3, andere je -X / Solo verliert: -X×3, andere je +X
  - **Beispiel Normalspiel:** Eingabe "2" → Gewinner: +2/+2, Verlierer: -2/-2
  - **Beispiel Solo:** Eingabe "2", Solo gewinnt → Solo: +6, andere: -2/-2/-2

### Sonderregeln
- **Frage:** Welche Sonderregeln sind wichtig?
  - Bock-Runden (Verdopplung)
  - Weitere Regeln?

### Design
- **Entscheidung:** Python + Streamlit
  - Streamlit für schnelle UI-Entwicklung
  - Plotly/Altair für interaktive Charts
  - Pandas für Datenverarbeitung
  - **Vorteil:** Nur Python-Kenntnisse erforderlich, keine JavaScript/CSS-Kenntnisse nötig
  - **Ähnlich zu Flask:** Aber mit automatischem Rendering und State Management

---

## Nächste Schritte

1. **Entscheidungen treffen** zu offenen Fragen
2. **Projektstruktur erstellen**
   - Python Virtual Environment aufsetzen
   - requirements.txt mit Dependencies (streamlit, plotly, pandas)
   - GitHub Repository initialisieren (wichtig für Streamlit Cloud!)
3. **Streamlit App initialisieren**
   - Basis-Struktur mit Sidebar
   - Session State Setup
4. **MVP Phase 1 implementieren**
   - Spieler-Eingabe
   - Rundenerfassung
   - Einfache Tabelle
5. **Deployment auf Streamlit Community Cloud**
   - Repository auf GitHub pushen
   - Mit Streamlit Community Cloud verbinden
   - App live schalten
6. **Testen & Iterieren**

---

## Anhang

### Doppelkopf Regeln (Referenz)
- 4 Spieler Standard
- Normalspiel: 2 vs 2 (Re vs Kontra)
- Solo: 1 vs 3
- **Punkte-Logik:**
  - Normalspiel: Gewinner je +X, Verlierer je -X
  - Solo gewinnt: Solo +X×3, andere je -X
  - Solo verliert: Solo -X×3, andere je +X
- Bock-Runden: Alle Punkte werden verdoppelt (Multiplikator)

### Inspirationen
- **Excalidraw:** Cookie-basiert, lokales Speichern, Export/Import
- **Streamlit Gallery:** Verschiedene Daten-Apps als Referenz
- **Notion:** Offline-First, gute UX
- **Score-keeping Apps:** Keep the Score, ScoreCount

### Python-Bibliotheken
- **Streamlit:** Web-UI Framework
- **Plotly:** Interaktive Charts
- **Pandas:** Datenverarbeitung und Tabellen
- **UUID:** Session-IDs generieren
- **JSON:** Daten Export/Import
- **Datetime:** Zeitstempel für Runden

### Deployment-Ressourcen
- **Streamlit Community Cloud:** https://streamlit.io/cloud
- **Dokumentation:** https://docs.streamlit.io/streamlit-community-cloud
- **GitHub Integration:** Automatisches Deployment bei Push

---

**Dokument-Version:** 1.0  
**Letzte Aktualisierung:** 26. Oktober 2025  
**Status:** Draft - Zur Review
