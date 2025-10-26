"""
Doppelkopf Zettel - Hauptanwendung
Progressive Web App für Doppelkopf-Spielverwaltung
"""

import streamlit as st
from src.session_manager import init_session_state
from src.ui_sidebar import render_sidebar
from src.ui_player_setup import render_player_setup
from src.ui_new_round import render_new_round_tab
from src.ui_overview import render_overview_tab
from src.ui_history import render_history_tab
from src.ui_statistics import render_statistics_tab

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


def main():
    """Hauptfunktion der App"""
    # Initialisiere Session State
    init_session_state()
    
    # Header
    st.markdown("<h1 class='main-header'>🃏 Doppelkopf Zettel</h1>", unsafe_allow_html=True)
    
    # Sidebar
    render_sidebar()
      # Hauptbereich
    if not st.session_state.session_started:
        # Spieler-Setup Phase
        render_player_setup()
    else:
        # Spiel-Phase mit Tabs
        tab1, tab2, tab3, tab4 = st.tabs(["📝 Neue Runde", "📊 Übersicht", "📈 Statistiken", "📜 Historie"])
        
        with tab1:
            render_new_round_tab()
        
        with tab2:
            render_overview_tab()
        
        with tab3:
            render_statistics_tab()
        
        with tab4:
            render_history_tab()


if __name__ == "__main__":
    main()
