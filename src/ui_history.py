"""
Rundenhistorie UI-Komponente
"""
import streamlit as st
from src.game_logic import delete_round


def render_history_tab():
    """Rendert den Historie-Tab als große Tabelle"""
    st.header("Rundenhistorie")
    
    if st.session_state.rounds:
        # Berechne kumulative Gesamtpunkte pro Spieler über alle Runden
        player_names = [p['name'] for p in st.session_state.players]
        
        # Zeige Runden in umgekehrter Reihenfolge (neueste zuerst)
        for round_data in reversed(st.session_state.rounds):
            # Spaltenbreiten: Info + Spieler + Löschen-Button
            col_widths = [3] + [2] * len(player_names) + [0.5]
            cols = st.columns(col_widths)
            
            # Info-Spalte
            with cols[0]:
                round_type = "🎯 Solo" if round_data['is_solo'] else "👥 Normal"
                team = "🟢 Re" if round_data.get('winning_team') == 'Re' else "🔴 Kontra"
                bock = " 🎯" if round_data.get('is_bock') else ""
                st.markdown(f"**R{round_data['round_number']}** {round_type} {team}{bock}")
            
            # Berechne Gesamtpunkte bis zu dieser Runde
            cumulative_scores = {name: 0 for name in player_names}
            for r in st.session_state.rounds:
                if r['round_number'] <= round_data['round_number']:
                    for name, score in r['scores'].items():
                        if name in cumulative_scores:
                            cumulative_scores[name] += score
            
            # Spieler-Spalten
            for idx, player_name in enumerate(player_names):
                with cols[idx + 1]:
                    score_change = round_data['scores'].get(player_name, 0)
                    total_score = cumulative_scores.get(player_name, 0)
                    
                    # Gewinner grün markieren
                    is_winner = player_name in round_data['winners']
                    
                    if is_winner:
                        st.markdown(f"<span style='color: #28a745; font-weight: bold;'>{total_score} ({score_change:+d})</span>", unsafe_allow_html=True)
                    else:
                        if score_change > 0:
                            st.markdown(f"{total_score} (<span style='color: #28a745;'>{score_change:+d}</span>)", unsafe_allow_html=True)
                        elif score_change < 0:
                            st.markdown(f"{total_score} (<span style='color: #dc3545;'>{score_change:+d}</span>)", unsafe_allow_html=True)
                        else:
                            st.markdown(f"{total_score} ({score_change:+d})")
            
            # Löschen-Button
            with cols[-1]:
                if st.button("🗑️", key=f"delete_{round_data['id']}"):
                    delete_round(round_data['id'])
                    st.rerun()
            
            st.divider()
    else:
        st.info("Noch keine Runden gespielt")
