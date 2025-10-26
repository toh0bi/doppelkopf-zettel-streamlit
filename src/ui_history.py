"""
Rundenhistorie UI-Komponente
"""
import streamlit as st
from src.game_logic import delete_round


def render_history_tab():
    """Rendert den Historie-Tab"""
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
                        delete_round(round_data['id'])
                        st.rerun()
                
                st.divider()
    else:
        st.info("Noch keine Runden gespielt")
