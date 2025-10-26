"""
Spiellogik für Doppelkopf-Punkteberechnung
"""
import streamlit as st
from typing import List, Dict, Optional
from datetime import datetime
import uuid


def calculate_scores() -> Dict[str, int]:
    """Berechnet die Gesamtpunktzahl für jeden Spieler"""
    scores = {player['name']: 0 for player in st.session_state.players}
    
    for round_data in st.session_state.rounds:
        for player_name, points in round_data['scores'].items():
            if player_name in scores:
                scores[player_name] += points
    
    return scores


def add_round(winners: List[str], points: int, is_solo: bool = False, solo_player: Optional[str] = None):
    """Fügt eine neue Runde hinzu"""
    round_data = {
        'id': str(uuid.uuid4()),
        'round_number': len(st.session_state.rounds) + 1,
        'timestamp': datetime.now().isoformat(),
        'is_solo': is_solo,
        'winners': winners,
        'points': points,
        'solo_player': solo_player,
        'scores': {}
    }
    
    # Berechne Punkteverteilung
    if is_solo and solo_player:
        # Solo-Spiel
        if solo_player in winners:
            # Solo gewinnt
            for player in st.session_state.players:
                if player['name'] == solo_player:
                    round_data['scores'][player['name']] = points * 3
                else:
                    round_data['scores'][player['name']] = -points
        else:
            # Solo verliert
            for player in st.session_state.players:
                if player['name'] == solo_player:
                    round_data['scores'][player['name']] = -points * 3
                else:
                    round_data['scores'][player['name']] = points
    else:
        # Normalspiel (2 vs 2)
        for player in st.session_state.players:
            if player['name'] in winners:
                round_data['scores'][player['name']] = points
            else:
                round_data['scores'][player['name']] = -points
    
    st.session_state.rounds.append(round_data)


def delete_round(round_id: str):
    """Löscht eine Runde"""
    st.session_state.rounds = [r for r in st.session_state.rounds if r['id'] != round_id]
