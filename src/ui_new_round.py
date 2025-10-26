"""
Neue Runde eintragen UI-Komponente
"""
import streamlit as st
from src.game_logic import add_round


def render_new_round_tab():
    """Rendert den Tab für neue Runden"""
    st.header("Neue Runde eintragen")
    num_players = len(st.session_state.players)
    
    # Initialisiere reset_flag falls nicht vorhanden
    if 'reset_round_form' not in st.session_state:
        st.session_state.reset_round_form = False
      # Initialisiere last_sitting_out falls nicht vorhanden
    if 'last_sitting_out' not in st.session_state:
        st.session_state.last_sitting_out = None
    
    # Punkteingabe mit Buttons
    st.subheader("Punkte")
    
    # Initialisiere selected_points im Session State
    if 'selected_points' not in st.session_state:
        st.session_state.selected_points = 2
    
    # 5 Buttons in 2 Reihen für bessere Mobile-Darstellung
    common_points = [1, 2, 3, 4, 5]
    
    # Erste Reihe: 1, 2, 3
    cols_row1 = st.columns(3)
    for idx, point_value in enumerate(common_points[:3]):
        with cols_row1[idx]:
            button_type = "primary" if st.session_state.selected_points == point_value else "secondary"
            if st.button(
                f"**{point_value}**",
                key=f"points_{point_value}",
                type=button_type,
                use_container_width=True
            ):
                st.session_state.selected_points = point_value
                st.rerun()
    
    # Zweite Reihe: 4, 5, [Andere]
    cols_row2 = st.columns(3)
    for idx, point_value in enumerate(common_points[3:]):
        with cols_row2[idx]:
            button_type = "primary" if st.session_state.selected_points == point_value else "secondary"
            if st.button(
                f"**{point_value}**",
                key=f"points_{point_value}",
                type=button_type,
                use_container_width=True            ):
                st.session_state.selected_points = point_value
                st.rerun()
    
    # "Andere" Option in dritter Spalte der zweiten Reihe
    with cols_row2[2]:
        use_custom = st.checkbox("Andere", help="Für negative oder höhere Punktzahlen")
    
    # Benutzerdefinierte Eingabe wenn "Andere" aktiviert
    if use_custom:
        points = st.number_input(
            "Benutzerdefinierte Punkte",
            min_value=-100,
            max_value=100,
            value=st.session_state.selected_points,
            help="Gib eine beliebige Punktzahl ein"
        )
    else:
        points = st.session_state.selected_points
    st.divider()
    
    # Gewinner-Auswahl (kombiniert mit Aussetzenden bei 5+ Spielern)
    st.subheader("Spieler & Gewinner")
      # Dynamischer Hinweistext je nach Spielerzahl
    if num_players == 4:
        st.caption("💡 1 Gewinner = Solo gewonnen | 2 Gewinner = Normalspiel | 3 Gewinner = Solo verloren")
    elif num_players >= 5:
        st.caption("💡 Wähle aus wer aussetzt und wer gewinnt | Min. 4 Spieler müssen mitspielen")
    
    winners = []
    sitting_out_players = []
    
    # Eindeutige Keys basierend auf reset_flag
    key_suffix = "_reset" if st.session_state.reset_round_form else ""
      # Bei 5+ Spielern: Erst auswählen wer aussetzt
    if num_players >= 5:
        st.markdown("**Wer setzt aus?**")
        
        # Default-Wert basierend auf Rotation
        default_sitting_index = 0  # Standard: "Niemand"
        
        if st.session_state.last_sitting_out and st.session_state.last_sitting_out != "Niemand":
            # sitting_out_index zeigt auf den NÄCHSTEN Spieler der aussetzen soll
            # +1 weil Dropdown bei Index 0 "Niemand" hat
            default_sitting_index = (st.session_state.sitting_out_index % num_players) + 1
        
        sitting_out_options = ["Niemand"] + [p['name'] for p in st.session_state.players]
        sitting_out_choice = st.selectbox(
            "Aussetzender Spieler",
            options=sitting_out_options,
            index=default_sitting_index,
            key=f"sitting_out_select{key_suffix}",
            label_visibility="collapsed"
        )
        
        if sitting_out_choice != "Niemand":
            sitting_out_players.append(sitting_out_choice)
        
        st.divider()
    
    # Gewinner-Auswahl: Einfache Checkbox-Liste
    st.markdown("**Wer gewinnt?**")
    for idx, player in enumerate(st.session_state.players):
        # Spieler setzt aus? Dann nicht anzeigen oder deaktivieren
        is_sitting_out = player['name'] in sitting_out_players
        
        if not is_sitting_out:
            is_winner = st.checkbox(
                f"✅ {player['name']}",
                key=f"winner_{player['id']}{key_suffix}"
            )
            if is_winner:
                winners.append(player['name'])
        else:
            # Ausgegraut anzeigen wenn Spieler aussetzt
            st.markdown(f"⏸️ ~~{player['name']}~~ *(setzt aus)*")
    
    # Validierung: Mindestens 4 Spieler müssen spielen
    sitting_out_player = sitting_out_players[0] if len(sitting_out_players) == 1 else None
    num_active = num_players - len(sitting_out_players)
    
    if num_players >= 5 and num_active < 4:
        st.error(f"❌ Zu viele Spieler setzen aus! Mindestens 4 Spieler müssen mitspielen. (Aktuell: {num_active})")
        sitting_out_player = None  # Reset bei Fehler    # Speichere, ob jemand aussetzt (nur wenn Validierung OK)
    if num_active >= 4:
        if sitting_out_player:
            st.session_state.last_sitting_out = sitting_out_player
            # Finde den Index des aktuell Aussetzenden für die Rotation
            for idx, player in enumerate(st.session_state.players):
                if player['name'] == sitting_out_player:
                    st.session_state.sitting_out_index = idx
                    break
        else:
            if num_players >= 5:
                st.session_state.last_sitting_out = "Niemand"
    
    st.divider()
    
    # Runde hinzufügen mit Validierung
    col_btn1, col_btn2 = st.columns([3, 1])
    
    with col_btn1:
        submit_button = st.button("✅ Runde eintragen", type="primary", use_container_width=True)
    
    with col_btn2:
        if st.button("🔄", help="Auswahl zurücksetzen"):
            # Toggle reset flag um neue Keys zu erzwingen
            st.session_state.reset_round_form = not st.session_state.reset_round_form
            st.rerun()
    
    if submit_button:
        # Nochmal validieren vor Submit
        if num_players >= 5 and num_active < 4:
            st.error("❌ Mindestens 4 Spieler müssen mitspielen!")
            return
        
        _handle_round_submission(winners, points, sitting_out_player)


def _handle_round_submission(winners, points, sitting_out_player=None):
    """Verarbeitet die Rundeneintragung"""
    
    num_winners = len(winners)
    num_players = len(st.session_state.players)
    active_players = [p['name'] for p in st.session_state.players if p['name'] != sitting_out_player]
    num_active = len(active_players)
    
    if num_winners == 0:
        st.error("❌ Bitte wähle mindestens einen Gewinner aus!")
        return
    
    # Bei 4 Spielern oder wenn jemand aussetzt: Klassische Logik (4 Spieler)
    if num_active == 4:
        if num_winners == 1:
            # Solo gewonnen (1 vs 3)
            solo_player = winners[0]
            add_round(winners, points, is_solo=True, solo_player=solo_player, sitting_out=sitting_out_player)
            st.success(f"✅ Solo-Runde eingetragen! {solo_player} gewinnt Solo mit {points:+d} Punkten")
            sleep_and_rerun()
        
        elif num_winners == 2:
            # Normalspiel (2 vs 2)
            add_round(winners, points, sitting_out=sitting_out_player)
            st.success(f"✅ Runde eingetragen! {winners[0]} & {winners[1]} gewinnen {points:+d} Punkte")
            sleep_and_rerun()
        
        elif num_winners == 3:
            # Solo verloren (1 vs 3)
            solo_player = [p for p in active_players if p not in winners][0]
            add_round(winners, points, is_solo=True, solo_player=solo_player, sitting_out=sitting_out_player)
            st.success(f"✅ Solo-Runde eingetragen! {solo_player} verliert Solo, andere gewinnen je {points:+d} Punkte")
            sleep_and_rerun()
        
        else:
            st.error(f"❌ Du hast {num_winners} Gewinner gewählt. Bei 4 aktiven Spielern: 1 (Solo gewonnen), 2 (Normal) oder 3 (Solo verloren)!")
    
    # Bei 5-6 Spielern (ohne Aussetzenden)
    else:
        if num_winners == 1:
            # Solo gewonnen
            solo_player = winners[0]
            add_round(winners, points, is_solo=True, solo_player=solo_player, sitting_out=sitting_out_player)
            st.success(f"✅ Solo-Runde eingetragen! {solo_player} gewinnt Solo mit {points:+d} Punkten")
            sleep_and_rerun()
        
        elif num_winners in [2, 3]:
            # Normalspiel bei 5-6 Spielern
            add_round(winners, points, sitting_out=sitting_out_player)
            winner_names = " & ".join(winners)
            st.success(f"✅ Runde eingetragen! {winner_names} gewinnen {points:+d} Punkte")
            sleep_and_rerun()
        
        elif num_winners == num_active - 1:
            # Solo verloren (alle außer einem gewinnen)
            solo_player = [p for p in active_players if p not in winners][0]
            add_round(winners, points, is_solo=True, solo_player=solo_player, sitting_out=sitting_out_player)
            st.success(f"✅ Solo-Runde eingetragen! {solo_player} verliert Solo, andere gewinnen je {points:+d} Punkte")
            sleep_and_rerun()
        
        else:
            st.error(f"❌ Ungültige Gewinner-Anzahl für {num_active} aktive Spieler!")

def sleep_and_rerun():
    import time
    time.sleep(2.5)
    _auto_rotate_sitting_out()
    st.rerun()


def _auto_rotate_sitting_out():
    """Rotiert automatisch zum nächsten aussetzenden Spieler (nur wenn jemand ausgesetzt hat)"""
    if len(st.session_state.players) >= 5:
        # Nur rotieren, wenn beim letzten Mal jemand ausgesetzt hat (nicht "Niemand")
        if st.session_state.last_sitting_out and st.session_state.last_sitting_out != "Niemand":
            # Erhöhe Index um 1 für nächste Runde
            st.session_state.sitting_out_index = (st.session_state.sitting_out_index + 1) % len(st.session_state.players)
            
            # Debug: Zeige welcher Spieler als nächstes dran ist
            next_player = st.session_state.players[st.session_state.sitting_out_index]['name']
            print(f"DEBUG: Rotation - Nächster Aussetzender: {next_player} (Index: {st.session_state.sitting_out_index})")
