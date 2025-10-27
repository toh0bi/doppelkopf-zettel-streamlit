"""
Statistik-Übersicht UI-Komponente
"""
import streamlit as st
from src.statistics import (
    calculate_win_rate,
    calculate_team_performance,
    calculate_average_points,
    calculate_solo_stats,
    calculate_longest_streak,
    calculate_re_kontra_stats
)


def render_statistics_tab():
    """Rendert den Statistik-Tab mit erweiterten Auswertungen"""
    st.header("📊 Erweiterte Statistiken")
    
    if not st.session_state.rounds:
        st.info("Noch keine Runden gespielt - Statistiken werden nach der ersten Runde angezeigt.")
        return
    
    # Tab-Struktur für bessere Übersichtlichkeit
    stats_tab1, stats_tab2, stats_tab3 = st.tabs([
        "🎯 Spieler-Statistiken", 
        "👥 Team-Statistiken", 
        "📈 Allgemeine Stats"
    ])
    
    # ===== TAB 1: Spieler-Statistiken =====
    with stats_tab1:
        st.subheader("🏆 Gewinnrate pro Spieler")
        
        win_rates = calculate_win_rate()
        sorted_win_rates = sorted(win_rates.items(), key=lambda x: x[1], reverse=True)
        
        for idx, (player_name, win_rate) in enumerate(sorted_win_rates):
            col1, col2, col3 = st.columns([1, 3, 2])
            
            with col1:
                medal = "🥇" if idx == 0 else "🥈" if idx == 1 else "🥉" if idx == 2 else f"{idx + 1}."
                st.write(medal)
            
            with col2:
                st.write(f"**{player_name}**")
            
            with col3:
                # Farbcodierung: >60% grün, 40-60% gelb, <40% rot
                if win_rate >= 60:
                    color = "#28a745"
                elif win_rate >= 40:
                    color = "#ffc107"
                else:
                    color = "#dc3545"
                
                st.markdown(f"<span style='color: {color}; font-weight: bold;'>{win_rate:.1f}%</span>", 
                           unsafe_allow_html=True)
                st.progress(win_rate / 100)
        
        st.divider()
        
        # Solo-Statistiken
        st.subheader("🎯 Solo-Spiele & Erfolgsrate")
        
        solo_stats = calculate_solo_stats()
        
        # Filtern: Nur Spieler mit Solo-Spielen anzeigen
        players_with_solos = [(name, stats) for name, stats in solo_stats.items() if stats['solo_count'] > 0]
        
        if players_with_solos:
            for player_name, stats in sorted(players_with_solos, key=lambda x: x[1]['solo_rate'], reverse=True):
                col1, col2, col3, col4 = st.columns([2, 1, 1, 2])
                
                with col1:
                    st.write(f"**{player_name}**")
                
                with col2:
                    st.metric("Gesamt", stats['solo_count'])
                
                with col3:
                    st.metric("Gewonnen", stats['solo_wins'])
                
                with col4:
                    rate_color = "#28a745" if stats['solo_rate'] >= 50 else "#dc3545"
                    st.markdown(f"<span style='color: {rate_color}; font-weight: bold;'>Erfolgsrate: {stats['solo_rate']:.1f}%</span>",
                               unsafe_allow_html=True)
        else:
            st.info("Noch keine Solo-Spiele gespielt")
        
        st.divider()
        
        # Gewinn-/Verluststrähnen
        st.subheader("🔥 Längste Gewinn-/Verluststrähne")
        
        streaks = calculate_longest_streak()
        
        for player_name, streak_data in sorted(streaks.items(), 
                                               key=lambda x: x[1]['win_streak'], 
                                               reverse=True):
            col1, col2, col3 = st.columns([2, 1, 1])
            
            with col1:
                st.write(f"**{player_name}**")
            
            with col2:
                if streak_data['win_streak'] > 0:
                    st.markdown(f"<span style='color: #28a745;'>🔥 {streak_data['win_streak']} Siege</span>",
                               unsafe_allow_html=True)
                else:
                    st.caption("Keine Siegesserie")
            
            with col3:
                if streak_data['loss_streak'] > 0:
                    st.markdown(f"<span style='color: #dc3545;'>❄️ {streak_data['loss_streak']} Niederlagen</span>",
                               unsafe_allow_html=True)
                else:
                    st.caption("Keine Pechsträhne")
      # ===== TAB 2: Team-Statistiken =====
    with stats_tab2:
        st.subheader("👥 Beste & Schlechteste Pärchen")
        st.caption("Basierend auf durchschnittlichen Punkten pro Spiel (mind. 2 gemeinsame Runden)")
        
        best_teams, worst_teams = calculate_team_performance()
        
        if best_teams:
            st.markdown("### 🏆 Beste Pärchen")
            for player1, player2, avg_score, games in best_teams:
                col1, col2, col3 = st.columns([3, 1, 1])
                
                with col1:
                    st.write(f"**{player1}** & **{player2}**")
                
                with col2:
                    color = "#28a745" if avg_score > 0 else "#ffc107" if avg_score == 0 else "#dc3545"
                    st.markdown(f"<span style='color: {color}; font-weight: bold;'>{avg_score:+.2f} Ø Pkt/Spiel</span>",
                               unsafe_allow_html=True)
                
                with col3:
                    st.caption(f"{games} Spiele")
            
            st.divider()
            
            if worst_teams:
                st.markdown("### 💔 Schlechteste Pärchen")
                for player1, player2, avg_score, games in worst_teams:
                    col1, col2, col3 = st.columns([3, 1, 1])
                    
                    with col1:
                        st.write(f"**{player1}** & **{player2}**")
                    
                    with col2:
                        color = "#dc3545" if avg_score < 0 else "#ffc107" if avg_score == 0 else "#28a745"
                        st.markdown(f"<span style='color: {color}; font-weight: bold;'>{avg_score:+.2f} Ø Pkt/Spiel</span>",
                                   unsafe_allow_html=True)
                    
                    with col3:
                        st.caption(f"{games} Spiele")
        else:
            st.info("Noch nicht genug Normalspiele für Team-Statistiken (mind. 2 Spiele pro Pärchen)")
    
    # ===== TAB 3: Allgemeine Statistiken =====
    with stats_tab3:
        st.subheader("📈 Allgemeine Statistiken")
        
        # Durchschnittliche Punkte
        avg_normal, avg_bock = calculate_average_points()
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric(
                "Ø Punkte pro Normalrunde",
                f"{avg_normal:.1f}",
                help="Durchschnittliche Punktzahl bei Normalrunden"
            )
        
        with col2:
            if avg_bock > 0:
                st.metric(
                    "Ø Punkte pro Bockrunde",
                    f"{avg_bock:.1f}",
                    help="Durchschnittliche Punktzahl bei Bock-Runden"
                )
            else:
                st.metric(
                    "Ø Punkte pro Bockrunde",
                    "N/A",
                    help="Noch keine Bock-Runden gespielt"
                )
        
        st.divider()
        
        # Re vs. Kontra Statistik
        st.subheader("🟢 Re vs. 🔴 Kontra")
        
        re_kontra = calculate_re_kontra_stats()
        
        if re_kontra['total'] > 0:
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("🟢 Re gewinnt", re_kontra['re_wins'])
                st.progress(re_kontra['re_rate'] / 100)
                st.caption(f"{re_kontra['re_rate']:.1f}%")
            
            with col2:
                st.metric("🔴 Kontra gewinnt", re_kontra['kontra_wins'])
                st.progress(re_kontra['kontra_rate'] / 100)
                st.caption(f"{re_kontra['kontra_rate']:.1f}%")
            
            with col3:
                # Welches Team dominiert?
                if re_kontra['re_rate'] > re_kontra['kontra_rate']:
                    diff = re_kontra['re_rate'] - re_kontra['kontra_rate']
                    st.info(f"🟢 **Re dominiert** mit +{diff:.1f}%")
                elif re_kontra['kontra_rate'] > re_kontra['re_rate']:
                    diff = re_kontra['kontra_rate'] - re_kontra['re_rate']
                    st.info(f"🔴 **Kontra dominiert** mit +{diff:.1f}%")
                else:
                    st.success("⚖️ **Perfekt ausgeglichen!**")
        else:
            st.info("Noch keine Runden gespielt")
        
        st.divider()
        
        # Weitere allgemeine Stats
        st.subheader("🎮 Spielübersicht")
        
        total_rounds = len(st.session_state.rounds)
        solo_count = sum(1 for r in st.session_state.rounds if r['is_solo'])
        bock_count = sum(1 for r in st.session_state.rounds if r.get('is_bock', False))
        normal_count = total_rounds - solo_count
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Gesamt Runden", total_rounds)
        
        with col2:
            st.metric("👥 Normalspiele", normal_count)
        
        with col3:
            st.metric("🎯 Solo-Spiele", solo_count)
        
        with col4:
            st.metric("🎯 Bock-Runden", bock_count)
        
        # Prozentuale Verteilung
        if total_rounds > 0:
            st.divider()
            st.subheader("📊 Spieltypen-Verteilung")
            
            col1, col2 = st.columns(2)
            
            with col1:
                normal_pct = (normal_count / total_rounds) * 100
                st.progress(normal_pct / 100)
                st.caption(f"👥 Normalspiele: {normal_pct:.1f}%")
            
            with col2:
                solo_pct = (solo_count / total_rounds) * 100
                st.progress(solo_pct / 100)
                st.caption(f"🎯 Solo-Spiele: {solo_pct:.1f}%")
