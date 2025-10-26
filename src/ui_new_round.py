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
    
    # 5 große Buttons für häufige Punktzahlen
    cols_points = st.columns(5)
    common_points = [1, 2, 3, 4, 5]
    
    for idx, point_value in enumerate(common_points):
        with cols_points[idx]:
            # Highlight des ausgewählten Buttons
            button_type = "primary" if st.session_state.selected_points == point_value else "secondary"
            if st.button(
                f"**{point_value}**",
                key=f"points_{point_value}",
                type=button_type,
                use_container_width=True
            ):
                st.session_state.selected_points = point_value
                st.rerun()    # Optionale benutzerdefinierte Eingabe
    col_custom1, col_custom2 = st.columns([3, 1])
    
    with col_custom2:
        use_custom = st.checkbox("Andere", help="Für negative oder höhere Punktzahlen")
    
    if use_custom:
        with col_custom1:
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
        st.caption("💡 Markiere ⏸️ für Aussetzer und ✅ für Gewinner | Min. 4 Spieler müssen mitspielen")
    
    winners = []
    sitting_out_players = []
    
    # Eindeutige Keys basierend auf reset_flag
    key_suffix = "_reset" if st.session_state.reset_round_form else ""
    
    # Kompakte Darstellung: Icon-Buttons statt großer Spalten
    for idx, player in enumerate(st.session_state.players):
        if num_players >= 5:
            # Bei 5+ Spielern: Kompakte 3-Spalten-Ansicht
            col_pause, col_name, col_win = st.columns([0.5, 2, 0.5])
            
            with col_pause:
                # Default: Basierend auf Rotation
                default_sitting = False
                if st.session_state.last_sitting_out and st.session_state.last_sitting_out != "Niemand":
                    default_sitting = (idx == st.session_state.sitting_out_index % num_players)
                
                # Checkbox mit Emoji als "Label"
                is_sitting = st.checkbox(
                    "⏸️",
                    key=f"sitting_{player['id']}{key_suffix}",
                    value=default_sitting,
                    help=f"{player['name']} setzt aus"
                )
                if is_sitting:
                    sitting_out_players.append(player['name'])
            
            with col_name:
                st.write(f"**{player['name']}**" if idx == 0 else player['name'])
            
            with col_win:
                is_sitting_out = (player['name'] in sitting_out_players)
                is_winner = st.checkbox(
                    "✅",
                    key=f"winner_{player['id']}{key_suffix}",
                    disabled=is_sitting_out,
                    help=f"{player['name']} gewinnt" if not is_sitting_out else "Kann nicht gewinnen (setzt aus)"
                )
                if is_winner and not is_sitting_out:
                    winners.append(player['name'])
        
        else:
            # Bei 4 Spielern: Nur 2 Spalten (Name + Gewinner)
            col_name, col_win = st.columns([2.5, 0.5])
            
            with col_name:
                st.write(f"**{player['name']}**" if idx == 0 else player['name'])
            
            with col_win:
                is_winner = st.checkbox(
                    "✅",
                    key=f"winner_{player['id']}{key_suffix}",
                    help=f"{player['name']} gewinnt"
                )
                if is_winner:
                    winners.append(player['name'])
    
    # Validierung: Mindestens 4 Spieler müssen spielen
    sitting_out_player = sitting_out_players[0] if len(sitting_out_players) == 1 else None
    num_active = num_players - len(sitting_out_players)
    
    if num_players >= 5 and num_active < 4:
        st.error(f"❌ Zu viele Spieler setzen aus! Mindestens 4 Spieler müssen mitspielen. (Aktuell: {num_active})")
        sitting_out_player = None  # Reset bei Fehler
      # Speichere, ob jemand aussetzt (nur wenn Validierung OK)
    if num_active >= 4:
        if sitting_out_player:
            st.session_state.last_sitting_out = sitting_out_player
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
        if st.session_state.last_sitting_out != "Niemand":
            st.session_state.sitting_out_index = (st.session_state.sitting_out_index + 1) % len(st.session_state.players)
