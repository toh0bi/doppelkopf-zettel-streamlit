"""
Doppelkopf Zettel - Hauptanwendung
Progressive Web App für Doppelkopf-Spielverwaltung
"""

import streamlit as st
import streamlit.components.v1 as components
import json
from datetime import datetime
from typing import List, Dict, Optional
import uuid
import os

# Umgebungsvariable setzen um pandas Import zu überspringen
os.environ['PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION'] = 'python'

# Seitenkonfiguration
st.set_page_config(
    page_title="Doppelkopf Zettel",
    page_icon="🃏",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS für besseres Design
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #2c3e50;
        padding: 1rem 0;
    }
    .player-card {
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-weight: bold;
    }
    .winner-card {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
    }
    .score-positive {
        color: #27ae60;
        font-weight: bold;
    }
    .score-negative {
        color: #e74c3c;
        font-weight: bold;
    }
    .round-card {
        padding: 0.5rem;
        border-left: 4px solid #3498db;
        margin: 0.5rem 0;
        background-color: #f8f9fa;
    }
</style>
""", unsafe_allow_html=True)

# Session State Initialisierung
def init_session_state():
    """Initialisiert den Session State"""
    if 'session_id' not in st.session_state:
        st.session_state.session_id = str(uuid.uuid4())
    
    if 'players' not in st.session_state:
        st.session_state.players = []
    
    if 'rounds' not in st.session_state:
        st.session_state.rounds = []
    
    if 'session_started' not in st.session_state:
        st.session_state.session_started = False
    
    if 'created_at' not in st.session_state:
        st.session_state.created_at = datetime.now().isoformat()
    
    if 'auto_loaded' not in st.session_state:
        st.session_state.auto_loaded = False

def save_to_browser():
    """Speichert die aktuelle Session im Browser localStorage"""
    try:
        json_data = export_session()
        # Escaping für JavaScript
        json_escaped = json_data.replace('`', '\\`').replace('\\', '\\\\')
        
        components.html(f"""
            <script>
                try {{
                    localStorage.setItem('doppelkopf_session', `{json_escaped}`);
                    localStorage.setItem('doppelkopf_last_save', new Date().toISOString());
                    console.log('Session gespeichert in localStorage');
                }} catch (e) {{
                    console.error('Fehler beim Speichern:', e);
                }}
            </script>
        """, height=0)
    except Exception as e:
        st.error(f"Fehler beim Auto-Speichern: {e}")

def load_from_browser():
    """Lädt die Session aus dem Browser localStorage"""
    html_code = """
        <script>
            const session = localStorage.getItem('doppelkopf_session');
            const lastSave = localStorage.getItem('doppelkopf_last_save');
            
            if (session) {
                // Sende Daten an Streamlit via query parameter hack
                const data = {
                    session: session,
                    lastSave: lastSave
                };
                
                // Nutze streamlit's setComponentValue
                window.parent.postMessage({
                    type: 'streamlit:setComponentValue',
                    value: data
                }, '*');
            } else {
                window.parent.postMessage({
                    type: 'streamlit:setComponentValue',
                    value: null
                }, '*');
            }
        </script>
        <div style="display: none;">Loading...</div>
    """
    
    result = components.html(html_code, height=0)
    return result

def clear_browser_storage():
    """Löscht die gespeicherte Session aus dem Browser"""
    components.html("""
        <script>
            localStorage.removeItem('doppelkopf_session');
            localStorage.removeItem('doppelkopf_last_save');
            console.log('Session aus localStorage gelöscht');
        </script>
    """, height=0)

def calculate_scores() -> Dict[str, int]:
    """Berechnet die Gesamtpunktzahl für jeden Spieler"""
    scores = {player['name']: 0 for player in st.session_state.players}
    
    for round_data in st.session_state.rounds:
        for player_name, points in round_data['scores'].items():
            if player_name in scores:
                scores[player_name] += points
    
    return scores

def add_round(winners: List[str], points: int, is_solo: bool = False, solo_player: Optional[str] = None):
    """Fügt eine neue Runde hinzu"""
    round_data = {
        'id': str(uuid.uuid4()),
        'round_number': len(st.session_state.rounds) + 1,
        'timestamp': datetime.now().isoformat(),
        'is_solo': is_solo,
        'winners': winners,
        'points': points,
        'solo_player': solo_player,
        'scores': {}
    }
    
    # Berechne Punkteverteilung
    if is_solo and solo_player:
        # Solo-Spiel
        if solo_player in winners:
            # Solo gewinnt
            for player in st.session_state.players:
                if player['name'] == solo_player:
                    round_data['scores'][player['name']] = points * 3
                else:
                    round_data['scores'][player['name']] = -points
        else:
            # Solo verliert
            for player in st.session_state.players:
                if player['name'] == solo_player:
                    round_data['scores'][player['name']] = -points * 3
                else:
                    round_data['scores'][player['name']] = points
    else:
        # Normalspiel (2 vs 2)
        for player in st.session_state.players:
            if player['name'] in winners:
                round_data['scores'][player['name']] = points
            else:
                round_data['scores'][player['name']] = -points
    
    st.session_state.rounds.append(round_data)

def export_session():
    """Exportiert die aktuelle Session als JSON"""
    export_data = {
        'session_id': st.session_state.session_id,
        'created_at': st.session_state.created_at,
        'exported_at': datetime.now().isoformat(),
        'players': st.session_state.players,
        'rounds': st.session_state.rounds
    }
    
    return json.dumps(export_data, indent=2, ensure_ascii=False)

def import_session(json_data: str):
    """Importiert eine Session aus JSON"""
    try:
        data = json.loads(json_data)
        st.session_state.session_id = data.get('session_id', str(uuid.uuid4()))
        st.session_state.created_at = data.get('created_at', datetime.now().isoformat())
        st.session_state.players = data.get('players', [])
        st.session_state.rounds = data.get('rounds', [])
        st.session_state.session_started = len(st.session_state.players) > 0
        return True
    except Exception as e:
        st.error(f"Fehler beim Importieren: {e}")
        return False

# Hauptanwendung
def main():
    init_session_state()
    
    # Auto-Load beim ersten Aufruf
    if not st.session_state.auto_loaded:
        st.session_state.auto_loaded = True
        
        # Versuche Session aus Browser zu laden
        with st.spinner("Lade gespeicherte Session..."):
            loaded_data = load_from_browser()
            
            # Zeige Info wenn Session geladen wurde
            if loaded_data and isinstance(loaded_data, dict) and 'session' in loaded_data:
                try:
                    if import_session(loaded_data['session']):
                        last_save = loaded_data.get('lastSave', 'unbekannt')
                        st.toast(f"✅ Session wiederhergestellt (zuletzt gespeichert: {last_save})", icon="💾")
                except:
                    pass
    
    # Header
    st.markdown("<h1 class='main-header'>🃏 Doppelkopf Zettel</h1>", unsafe_allow_html=True)
      # Sidebar für Session-Management
    with st.sidebar:
        st.header("📋 Session-Verwaltung")
        
        # Status-Anzeige
        if st.session_state.session_started:
            st.success("✅ Session aktiv")
            st.caption(f"🎮 {len(st.session_state.players)} Spieler")
            st.caption(f"🎯 {len(st.session_state.rounds)} Runden")
        else:
            st.info("ℹ️ Keine aktive Session")
        
        st.divider()
        
        # Export/Import
        st.subheader("💾 Speichern/Laden")
        
        if st.session_state.session_started:
            # Auto-Save Button
            if st.button("💾 Jetzt speichern", use_container_width=True, type="primary"):
                save_to_browser()
                st.success("In Browser gespeichert!")
                st.caption("💡 Automatisches Speichern nach jeder Runde aktiv")
            
            st.divider()
            
            # Manueller Export
            json_export = export_session()
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"doppelkopf_{timestamp}.json"
            
            st.download_button(
                label="📥 Als Datei exportieren",
                data=json_export,
                file_name=filename,
                mime="application/json",
                use_container_width=True
            )
        
        uploaded_file = st.file_uploader("📤 Session importieren", type=['json'])
        if uploaded_file is not None:
            json_data = uploaded_file.read().decode('utf-8')
            if import_session(json_data):
                save_to_browser()  # Auch im Browser speichern
                st.success("Session erfolgreich importiert!")
                st.rerun()
        
        st.divider()
        
        # Neue Session starten
        if st.button("🔄 Neue Session starten", type="secondary", use_container_width=True):
            clear_browser_storage()
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
      # Hauptbereich
    if not st.session_state.session_started:
        # Spieler-Eingabe
        st.header("👥 Spieler hinzufügen")
        st.write("Bitte gib die Namen von 4-6 Spielern ein:")
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            player_name = st.text_input("Spielername", key="new_player_input")
        
        with col2:
            st.write("")  # Spacer
            st.write("")  # Spacer
            if st.button("➕ Hinzufügen", type="primary"):
                if player_name and player_name not in [p['name'] for p in st.session_state.players]:
                    st.session_state.players.append({
                        'id': str(uuid.uuid4()),
                        'name': player_name
                    })
                    save_to_browser()  # Auto-Save                    st.rerun()
                elif player_name in [p['name'] for p in st.session_state.players]:
                    st.error("Spieler existiert bereits!")
        
        # Aktuelle Spielerliste
        if st.session_state.players:
            st.subheader("Aktuelle Spieler:")
            for idx, player in enumerate(st.session_state.players):
                col1, col2 = st.columns([4, 1])
                with col1:
                    st.write(f"{idx + 1}. {player['name']}")
                with col2:
                    if st.button("❌", key=f"remove_{player['id']}"):
                        st.session_state.players = [p for p in st.session_state.players if p['id'] != player['id']]
                        save_to_browser()  # Auto-Save
                        st.rerun()
        
        # Session starten
        st.divider()
        if len(st.session_state.players) >= 4:
            if st.button("🎮 Session starten", type="primary", use_container_width=True):
                st.session_state.session_started = True
                save_to_browser()  # Auto-Save
                st.rerun()
        else:
            st.info(f"Noch {4 - len(st.session_state.players)} Spieler erforderlich (mindestens 4)")
    
    else:
        # Spielansicht
        tab1, tab2, tab3 = st.tabs(["📝 Neue Runde", "📊 Übersicht", "📜 Historie"])
        
        with tab1:
            st.header("Neue Runde eintragen")
            
            # Solo-Toggle
            is_solo = st.checkbox("Solo-Spiel")
            
            if is_solo:
                # Solo-Spieler auswählen
                solo_player = st.selectbox(
                    "Solo-Spieler",
                    [p['name'] for p in st.session_state.players]
                )
                
                # Gewinner auswählen (Solo oder andere)
                winner = st.radio(
                    "Wer hat gewonnen?",
                    [solo_player, "Die anderen Spieler"],
                    horizontal=True
                )
                
                winners = [solo_player] if winner == solo_player else [p['name'] for p in st.session_state.players if p['name'] != solo_player]
            else:
                # Normale Runde - 2 Gewinner auswählen
                st.write("Wähle die 2 Gewinner aus:")
                winners = st.multiselect(
                    "Gewinner",
                    [p['name'] for p in st.session_state.players],
                    max_selections=2
                )
            
            # Punkteingabe
            points = st.number_input("Punkte", min_value=1, max_value=10, value=2)
              # Runde hinzufügen
            if st.button("✅ Runde eintragen", type="primary", use_container_width=True):
                if is_solo:
                    add_round(winners, points, is_solo=True, solo_player=solo_player)
                    save_to_browser()  # Auto-Save
                    st.success("Solo-Runde eingetragen!")
                    st.rerun()
                elif len(winners) == 2:
                    add_round(winners, points)
                    save_to_browser()  # Auto-Save
                    st.success("Runde eingetragen!")
                    st.rerun()
                else:
                    st.error("Bitte wähle genau 2 Gewinner aus!")
        
        with tab2:
            st.header("Aktueller Spielstand")
            
            # Berechne Scores
            scores = calculate_scores()
            
            # Sortiere nach Punktzahl
            sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
            
            # Zeige Tabelle
            st.subheader("🏆 Rangliste")
            
            for idx, (player_name, score) in enumerate(sorted_scores):
                col1, col2, col3 = st.columns([1, 3, 2])
                
                with col1:
                    medal = "🥇" if idx == 0 else "🥈" if idx == 1 else "🥉" if idx == 2 else f"{idx + 1}."
                    st.write(medal)
                
                with col2:
                    st.write(f"**{player_name}**")
                
                with col3:
                    score_class = "score-positive" if score > 0 else "score-negative" if score < 0 else ""
                    st.markdown(f"<span class='{score_class}'>{score:+d} Punkte</span>", unsafe_allow_html=True)
            
            # Statistiken
            if st.session_state.rounds:
                st.divider()
                st.subheader("📈 Statistiken")
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Gespielte Runden", len(st.session_state.rounds))
                
                with col2:
                    solo_count = sum(1 for r in st.session_state.rounds if r['is_solo'])
                    st.metric("Solo-Spiele", solo_count)
                
                with col3:
                    total_points = sum(abs(sum(r['scores'].values())) for r in st.session_state.rounds)
                    st.metric("Gesamtpunkte", total_points)
        
        with tab3:
            st.header("Rundenhistorie")
            
            if st.session_state.rounds:
                # Zeige Runden in umgekehrter Reihenfolge (neueste zuerst)
                for round_data in reversed(st.session_state.rounds):
                    with st.container():
                        col1, col2 = st.columns([4, 1])
                        
                        with col1:
                            round_type = "🎯 Solo" if round_data['is_solo'] else "👥 Normal"
                            st.markdown(f"**Runde {round_data['round_number']}** - {round_type}")
                            
                            # Zeige Gewinner
                            winners_str = ", ".join(round_data['winners'])
                            st.write(f"Gewinner: {winners_str} ({round_data['points']:+d} Punkte)")
                            
                            # Zeige Score-Änderungen
                            score_details = " | ".join([f"{name}: {score:+d}" for name, score in round_data['scores'].items()])
                            st.caption(score_details)
                        with col2:
                            if st.button("🗑️", key=f"delete_{round_data['id']}"):
                                st.session_state.rounds = [r for r in st.session_state.rounds if r['id'] != round_data['id']]
                                save_to_browser()  # Auto-Save
                                st.rerun()
                        
                        st.divider()
            else:
                st.info("Noch keine Runden gespielt")

if __name__ == "__main__":
    main()
