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
    
    # Bei 5-6 Spielern: Option für aussetzenden Spieler
    sitting_out_player = None
    if num_players >= 5:
        st.subheader("Aussetzender Spieler (optional)")
        st.caption(f"📊 {num_players} Spieler registriert - Aussetzenden-Modus aktiv")
        
        col_sit1, col_sit2 = st.columns([3, 1])
        
        with col_sit1:
            # Default: Rotation basierend auf sitting_out_index
            default_sitting_out = st.session_state.players[st.session_state.sitting_out_index % num_players]['name']
            
            sitting_out_options = ["Niemand (alle spielen)"] + [p['name'] for p in st.session_state.players]
            default_index = sitting_out_options.index(default_sitting_out) if default_sitting_out in sitting_out_options else 0
            
            sitting_out_selection = st.selectbox(
                "Wer setzt aus?",
                options=sitting_out_options,
                index=default_index,
                help="Standard: Rotation nach jeder Runde. Du kannst es manuell ändern."
            )
            if sitting_out_selection != "Niemand (alle spielen)":
                sitting_out_player = sitting_out_selection
        
        with col_sit2:
            st.write("")
            st.write("")
            if st.button("♻️", help="Nächster Spieler setzt aus"):
                st.session_state.sitting_out_index = (st.session_state.sitting_out_index + 1) % num_players
                st.rerun()
        
        st.divider()
    else:
        # Info für 4 Spieler
        if num_players == 4:
            st.info("ℹ️ Bei 4 Spielern spielen alle mit. Füge einen 5. Spieler hinzu, um die Aussetzenden-Funktion zu aktivieren.")
    
    # Punkteingabe ZUERST
    st.subheader("Punkte")
    col_points1, col_points2 = st.columns([3, 1])
    
    with col_points1:
        points_quick = st.selectbox(
            "Schnellauswahl",
            options=list(range(0, 11)),
            index=2,
            help="Wähle eine Punktzahl von 0-10"
        )
    
    with col_points2:
        use_custom = st.checkbox("Andere", help="Aktiviere für negative oder höhere Punktzahlen")
    
    if use_custom:
        points = st.number_input(
            "Benutzerdefinierte Punkte",
            min_value=-100,
            max_value=100,
            value=points_quick,
            help="Gib eine beliebige Punktzahl ein"
        )    
    else:
        points = points_quick
    
    st.divider()
    
    # Gewinner-Auswahl (automatische Solo-Erkennung)
    st.subheader("Gewinner")
    
    # Dynamischer Hinweistext je nach Spielerzahl
    if num_players == 4:
        st.caption("💡 Tipp: 1 Gewinner = Solo gewonnen | 2 Gewinner = Normalspiel | 3 Gewinner = Solo verloren")
    else:
        if sitting_out_player:
            st.caption("💡 Tipp: 1 Gewinner = Solo gewonnen | 2 Gewinner = Normalspiel | 3 Gewinner = Solo verloren")
        else:
            st.caption("💡 Tipp: 1 Gewinner = Solo | 2-3 Gewinner = Normalspiel | 4 Gewinner = Solo verloren")
    winners = []
    active_players = [p for p in st.session_state.players if p['name'] != sitting_out_player]
    cols = st.columns(min(len(active_players), 4))
    
    # Eindeutige Keys basierend auf reset_flag
    key_suffix = "_reset" if st.session_state.reset_round_form else ""
    
    for idx, player in enumerate(active_players):
        with cols[idx % len(cols)]:
            if st.checkbox(player['name'], key=f"winner_{player['id']}{key_suffix}"):
                winners.append(player['name'])
    
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
        _handle_round_submission(winners, points, sitting_out_player)


def _handle_round_submission(winners, points, sitting_out_player=None):
    """Verarbeitet die Rundeneintragung"""
    import time
    
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
            time.sleep(1.5)
            _auto_rotate_sitting_out()
            st.rerun()
        
        elif num_winners == 2:
            # Normalspiel (2 vs 2)
            add_round(winners, points, sitting_out=sitting_out_player)
            st.success(f"✅ Runde eingetragen! {winners[0]} & {winners[1]} gewinnen {points:+d} Punkte")
            time.sleep(1.5)
            _auto_rotate_sitting_out()
            st.rerun()
        
        elif num_winners == 3:
            # Solo verloren (1 vs 3)
            solo_player = [p for p in active_players if p not in winners][0]
            add_round(winners, points, is_solo=True, solo_player=solo_player, sitting_out=sitting_out_player)
            st.success(f"✅ Solo-Runde eingetragen! {solo_player} verliert Solo, andere gewinnen je {points:+d} Punkte")
            time.sleep(1.5)
            _auto_rotate_sitting_out()
            st.rerun()
        
        else:
            st.error(f"❌ Du hast {num_winners} Gewinner gewählt. Bei 4 aktiven Spielern: 1 (Solo gewonnen), 2 (Normal) oder 3 (Solo verloren)!")
    
    # Bei 5-6 Spielern (ohne Aussetzenden)
    else:
        if num_winners == 1:
            # Solo gewonnen
            solo_player = winners[0]
            add_round(winners, points, is_solo=True, solo_player=solo_player, sitting_out=sitting_out_player)
            st.success(f"✅ Solo-Runde eingetragen! {solo_player} gewinnt Solo mit {points:+d} Punkten")
            time.sleep(1.5)
            _auto_rotate_sitting_out()
            st.rerun()
        
        elif num_winners in [2, 3]:
            # Normalspiel bei 5-6 Spielern
            add_round(winners, points, sitting_out=sitting_out_player)
            winner_names = " & ".join(winners)
            st.success(f"✅ Runde eingetragen! {winner_names} gewinnen {points:+d} Punkte")
            time.sleep(1.5)
            _auto_rotate_sitting_out()
            st.rerun()
        
        elif num_winners == num_active - 1:
            # Solo verloren (alle außer einem gewinnen)
            solo_player = [p for p in active_players if p not in winners][0]
            add_round(winners, points, is_solo=True, solo_player=solo_player, sitting_out=sitting_out_player)
            st.success(f"✅ Solo-Runde eingetragen! {solo_player} verliert Solo, andere gewinnen je {points:+d} Punkte")
            time.sleep(1.5)
            _auto_rotate_sitting_out()
            st.rerun()
        
        else:
            st.error(f"❌ Ungültige Gewinner-Anzahl für {num_active} aktive Spieler!")


def _auto_rotate_sitting_out():
    """Rotiert automatisch zum nächsten aussetzenden Spieler"""
    if len(st.session_state.players) >= 5:
        st.session_state.sitting_out_index = (st.session_state.sitting_out_index + 1) % len(st.session_state.players)
