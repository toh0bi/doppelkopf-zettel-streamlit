"""
Spieler-Setup UI-Komponente
"""
import streamlit as st
import uuid


def render_player_setup():
    """Rendert die Spieler-Eingabe Seite"""
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
                st.rerun()
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
                    st.rerun()
    
    # Session starten
    st.divider()
    if len(st.session_state.players) >= 4:
        if st.button("🎮 Session starten", type="primary", use_container_width=True):
            st.session_state.session_started = True
            st.rerun()
    else:
        st.info(f"Noch {4 - len(st.session_state.players)} Spieler erforderlich (mindestens 4)")
