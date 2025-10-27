"""
Statistik-Berechnungen für erweiterte Auswertungen
"""
import streamlit as st
from typing import Dict, List, Tuple
from collections import defaultdict


def calculate_win_rate() -> Dict[str, float]:
    """Berechnet die Gewinnrate pro Spieler in Prozent"""
    player_stats = {player['name']: {'wins': 0, 'total': 0} for player in st.session_state.players}
    
    for round_data in st.session_state.rounds:
        # Nur aktive Spieler dieser Runde zählen
        sitting_out = round_data.get('sitting_out')
        
        for player in st.session_state.players:
            player_name = player['name']
            
            # Überspringe aussetzende Spieler
            if player_name == sitting_out:
                continue
            
            player_stats[player_name]['total'] += 1
            
            # Gewinner zählen
            if player_name in round_data['winners']:
                player_stats[player_name]['wins'] += 1
    
    # Berechne Prozentsätze
    win_rates = {}
    for player_name, stats in player_stats.items():
        if stats['total'] > 0:
            win_rates[player_name] = (stats['wins'] / stats['total']) * 100
        else:
            win_rates[player_name] = 0.0
    
    return win_rates


def calculate_team_performance() -> Tuple[List[Tuple[str, str, float, int]], List[Tuple[str, str, float, int]]]:
    """
    Berechnet welche Pärchen am besten/schlechtesten zusammen spielen
    Basierend auf durchschnittlichen Punkten pro Spiel (nicht Gesamtpunkte!)
    Gibt zurück: (beste_paerchen, schlechteste_paerchen)
    Jedes Tupel: (spieler1, spieler2, avg_punkte_pro_spiel, anzahl_spiele)
    """
    # Speichere Performance für jedes Pärchen
    team_scores = defaultdict(int)
    team_games = defaultdict(int)
    
    for round_data in st.session_state.rounds:
        # Nur Normalspiele (2 vs 2) zählen
        if not round_data['is_solo'] and len(round_data['winners']) == 2:
            # Gewinner-Pärchen
            winner_pair = tuple(sorted(round_data['winners']))
            team_scores[winner_pair] += round_data['points']
            team_games[winner_pair] += 1
            
            # Verlierer-Pärchen
            all_players = [p['name'] for p in st.session_state.players if p['name'] != round_data.get('sitting_out')]
            losers = [p for p in all_players if p not in round_data['winners']]
            if len(losers) == 2:
                loser_pair = tuple(sorted(losers))
                team_scores[loser_pair] -= round_data['points']
                team_games[loser_pair] += 1
    
    # Berechne Durchschnitt pro Spiel und sortiere
    team_performance = [
        (pair[0], pair[1], team_scores[pair] / team_games[pair], team_games[pair]) 
        for pair in team_scores.keys() 
        if team_games[pair] >= 2  # Min. 2 Spiele
    ]
    team_performance.sort(key=lambda x: x[2], reverse=True)  # Sortiere nach avg_punkte
    
    best_teams = team_performance[:3] if len(team_performance) >= 3 else team_performance
    worst_teams = team_performance[-3:] if len(team_performance) >= 3 else []
    
    return best_teams, worst_teams


def calculate_average_points() -> Tuple[float, float]:
    """
    Berechnet durchschnittliche Punkte pro Normalrunde und Bockrunde
    Gibt zurück: (avg_normal, avg_bock)
    """
    normal_rounds = []
    bock_rounds = []
    
    for round_data in st.session_state.rounds:
        points = round_data['points']
        
        if round_data.get('is_bock', False):
            bock_rounds.append(points)
        else:
            normal_rounds.append(points)
    
    avg_normal = sum(normal_rounds) / len(normal_rounds) if normal_rounds else 0.0
    avg_bock = sum(bock_rounds) / len(bock_rounds) if bock_rounds else 0.0
    
    return avg_normal, avg_bock


def calculate_solo_stats() -> Dict[str, Dict]:
    """
    Berechnet Solo-Statistiken pro Spieler
    Gibt zurück: {spieler_name: {'solo_count': X, 'solo_wins': Y, 'solo_rate': Z%}}
    """
    solo_stats = {player['name']: {'solo_count': 0, 'solo_wins': 0, 'solo_rate': 0.0} 
                  for player in st.session_state.players}
    
    for round_data in st.session_state.rounds:
        if round_data['is_solo'] and round_data.get('solo_player'):
            solo_player = round_data['solo_player']
            
            if solo_player in solo_stats:
                solo_stats[solo_player]['solo_count'] += 1
                
                # Solo gewonnen?
                if solo_player in round_data['winners']:
                    solo_stats[solo_player]['solo_wins'] += 1
    
    # Berechne Erfolgsrate
    for player_name, stats in solo_stats.items():
        if stats['solo_count'] > 0:
            stats['solo_rate'] = (stats['solo_wins'] / stats['solo_count']) * 100
    
    return solo_stats


def calculate_longest_streak() -> Dict[str, Dict]:
    """
    Berechnet die längste Gewinn- und Verluststrähne pro Spieler
    Gibt zurück: {spieler_name: {'win_streak': X, 'loss_streak': Y}}
    """
    streaks = {player['name']: {'win_streak': 0, 'loss_streak': 0, 'current_win': 0, 'current_loss': 0}
               for player in st.session_state.players}
    
    for round_data in st.session_state.rounds:
        sitting_out = round_data.get('sitting_out')
        
        for player in st.session_state.players:
            player_name = player['name']
            
            # Überspringe aussetzende Spieler
            if player_name == sitting_out:
                continue
            
            if player_name in round_data['winners']:
                # Gewonnen
                streaks[player_name]['current_win'] += 1
                streaks[player_name]['current_loss'] = 0  # Reset loss streak
                
                # Update max win streak
                if streaks[player_name]['current_win'] > streaks[player_name]['win_streak']:
                    streaks[player_name]['win_streak'] = streaks[player_name]['current_win']
            else:
                # Verloren
                streaks[player_name]['current_loss'] += 1
                streaks[player_name]['current_win'] = 0  # Reset win streak
                
                # Update max loss streak
                if streaks[player_name]['current_loss'] > streaks[player_name]['loss_streak']:
                    streaks[player_name]['loss_streak'] = streaks[player_name]['current_loss']
    
    # Entferne temporäre current-Werte
    result = {player_name: {'win_streak': stats['win_streak'], 'loss_streak': stats['loss_streak']}
              for player_name, stats in streaks.items()}
    
    return result


def calculate_re_kontra_stats() -> Dict[str, int]:
    """
    Berechnet wie oft Re vs. Kontra gewinnt
    Gibt zurück: {'re_wins': X, 'kontra_wins': Y, 're_rate': Z%}
    """
    re_wins = 0
    kontra_wins = 0
    
    for round_data in st.session_state.rounds:
        winning_team = round_data.get('winning_team', 'Re')  # Default: Re
        
        if winning_team == 'Re':
            re_wins += 1
        elif winning_team == 'Kontra':
            kontra_wins += 1
    
    total_games = re_wins + kontra_wins
    re_rate = (re_wins / total_games * 100) if total_games > 0 else 0.0
    kontra_rate = (kontra_wins / total_games * 100) if total_games > 0 else 0.0
    
    return {
        're_wins': re_wins,
        'kontra_wins': kontra_wins,
        're_rate': re_rate,
        'kontra_rate': kontra_rate,
        'total': total_games
    }
