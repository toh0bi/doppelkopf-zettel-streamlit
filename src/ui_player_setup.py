"""
Spieler-Setup UI-Komponente
"""
import streamlit as st
import uuid
from src.ui_cloud_session import render_cloud_session_dialog, render_load_session_dialog


def render_player_setup():
    """Rendert die Spieler-Eingabe Seite"""
    # Cloud-Load Dialog anzeigen (falls noch keine Session)
    if not st.session_state.session_started and not st.session_state.players:
        render_load_session_dialog()
    
    st.header("👥 Spieler hinzufügen")
    st.write("Bitte gib die Namen von 4-6 Spielern ein:")
    
    # Maximale Spieleranzahl erreicht?
    max_players_reached = len(st.session_state.players) >= 6
    
    if max_players_reached:
        st.warning("⚠️ Maximale Spieleranzahl erreicht (6 Spieler)")
    
    # Form für bessere Enter-Unterstützung
    with st.form(key="add_player_form", clear_on_submit=True):
        col1, col2 = st.columns([3, 1])
        
        with col1:
            player_name = st.text_input(
                "Spielername", 
                key="new_player_input",
                disabled=max_players_reached
            )
        
        with col2:
            st.write("")  # Spacer
            st.write("")  # Spacer
            submit_button = st.form_submit_button(
                "➕ Hinzufügen", 
                type="primary",
                disabled=max_players_reached
            )
        
        if submit_button:
            # Nochmal prüfen (falls zwischen Render und Submit etwas passiert ist)
            if len(st.session_state.players) >= 6:
                st.error("❌ Maximale Spieleranzahl (6) bereits erreicht!")
            elif player_name and player_name.strip():
                if player_name not in [p['name'] for p in st.session_state.players]:
                    st.session_state.players.append({
                        'id': str(uuid.uuid4()),
                        'name': player_name.strip()
                    })
                    st.success(f"✅ {player_name} hinzugefügt!")
                    st.rerun()
                else:
                    st.error("❌ Spieler existiert bereits!")
            elif not player_name or not player_name.strip():
                st.warning("⚠️ Bitte gib einen Namen ein!")
    
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
                    st.rerun()    # Session starten
    st.divider()
    
    # Cloud-Sync Dialog (nur anzeigen wenn >= 4 Spieler, also Session startbar)
    if len(st.session_state.players) >= 4:
        render_cloud_session_dialog()
    
    if len(st.session_state.players) >= 4:
        if st.button("🎮 Session starten", type="primary", use_container_width=True):
            st.session_state.session_started = True
            st.rerun()
    else:
        st.info(f"Noch {4 - len(st.session_state.players)} Spieler erforderlich (mindestens 4)")
