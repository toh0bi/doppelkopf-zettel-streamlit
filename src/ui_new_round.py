"""
Neue Runde eintragen UI-Komponente
"""
import streamlit as st
from src.game_logic import add_round


def render_new_round_tab():
    """Rendert den Tab für neue Runden"""
    st.header("Neue Runde eintragen")
    
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
    st.caption("💡 Tipp: 1 Gewinner = Solo gewonnen | 2 Gewinner = Normalspiel | 3 Gewinner = Solo verloren")
    
    winners = []
    cols = st.columns(min(len(st.session_state.players), 4))
    
    for idx, player in enumerate(st.session_state.players):
        with cols[idx % len(cols)]:
            if st.checkbox(player['name'], key=f"winner_{player['id']}"):
                winners.append(player['name'])
    
    st.divider()
    
    # Runde hinzufügen mit Validierung
    col_btn1, col_btn2 = st.columns([3, 1])
    
    with col_btn1:
        submit_button = st.button("✅ Runde eintragen", type="primary", use_container_width=True)
    
    with col_btn2:
        if st.button("🔄", help="Auswahl zurücksetzen"):
            st.rerun()
    
    if submit_button:
        _handle_round_submission(winners, points)


def _handle_round_submission(winners, points):
    """Verarbeitet die Rundeneintragung"""
    num_winners = len(winners)
    
    if num_winners == 0:
        st.error("❌ Bitte wähle mindestens einen Gewinner aus!")
    
    elif num_winners == 1:
        # Solo gewonnen (1 vs 3)
        solo_player = winners[0]
        add_round(winners, points, is_solo=True, solo_player=solo_player)
        st.success(f"✅ Solo-Runde eingetragen! {solo_player} gewinnt Solo mit {points:+d} Punkten")
        st.balloons()
        st.rerun()
    
    elif num_winners == 2:
        # Normalspiel (2 vs 2)
        add_round(winners, points)
        st.success(f"✅ Runde eingetragen! {winners[0]} & {winners[1]} gewinnen {points:+d} Punkte")
        st.balloons()
        st.rerun()
    
    elif num_winners == 3:
        # Solo verloren (1 vs 3)
        all_players = [p['name'] for p in st.session_state.players]
        solo_player = [p for p in all_players if p not in winners][0]
        add_round(winners, points, is_solo=True, solo_player=solo_player)
        st.success(f"✅ Solo-Runde eingetragen! {solo_player} verliert Solo, andere gewinnen je {points:+d} Punkte")
        st.balloons()
        st.rerun()
    
    else:
        st.error(f"❌ Du hast {num_winners} Gewinner gewählt. Bitte wähle 1 (Solo gewonnen), 2 (Normal) oder 3 (Solo verloren)!")
