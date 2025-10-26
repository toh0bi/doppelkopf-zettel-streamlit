"""
Spielstand-Übersicht UI-Komponente
"""
import streamlit as st
from src.game_logic import calculate_scores


def render_overview_tab():
    """Rendert den Übersichts-Tab"""
    st.header("Aktueller Spielstand")
    
    # Berechne Scores
    scores = calculate_scores()
    
    # Sortiere nach Punktzahl
    sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
      # Berechne Solo-Anzahl pro Spieler
    solo_counts = {player['name']: 0 for player in st.session_state.players}
    for round_data in st.session_state.rounds:
        if round_data['is_solo'] and round_data.get('solo_player'):
            solo_player = round_data['solo_player']
            if solo_player in solo_counts:
                solo_counts[solo_player] += 1
    
    # Zeige Tabelle
    st.subheader("🏆 Rangliste")
    
    for idx, (player_name, score) in enumerate(sorted_scores):
        col1, col2, col3, col4 = st.columns([1, 3, 2, 1])
        
        with col1:
            medal = "🥇" if idx == 0 else "🥈" if idx == 1 else "🥉" if idx == 2 else f"{idx + 1}."
            st.write(medal)
        
        with col2:
            st.write(f"**{player_name}**")
        
        with col3:
            score_class = "score-positive" if score > 0 else "score-negative" if score < 0 else ""
            st.markdown(f"<span class='{score_class}'>{score:+d} Punkte</span>", unsafe_allow_html=True)
        
        with col4:
            solo_count = solo_counts.get(player_name, 0)
            if solo_count > 0:
                st.caption(f"🎯 {solo_count}")
            else:
                st.caption("")
    
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
            # Gesamtpunkte = Summe aller absoluten Punkteänderungen
            total_points = sum(abs(score) for r in st.session_state.rounds for score in r['scores'].values())
            st.metric("Gesamtpunkte", total_points)
