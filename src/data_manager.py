"""
Import/Export Funktionalität für Sessions
"""
import streamlit as st
import json
from datetime import datetime
import uuid


def export_session() -> str:
    """Exportiert die aktuelle Session als JSON"""
    export_data = {
        'session_id': st.session_state.session_id,
        'created_at': st.session_state.created_at,
        'exported_at': datetime.now().isoformat(),
        'players': st.session_state.players,
        'rounds': st.session_state.rounds
    }
    
    return json.dumps(export_data, indent=2, ensure_ascii=False)


def import_session(json_data: str) -> bool:
    """Importiert eine Session aus JSON"""
    try:
        data = json.loads(json_data)
        st.session_state.session_id = data.get('session_id', str(uuid.uuid4()))
        st.session_state.created_at = data.get('created_at', datetime.now().isoformat())
        st.session_state.players = data.get('players', [])
        st.session_state.rounds = data.get('rounds', [])
        st.session_state.session_started = len(st.session_state.players) > 0
        return True
    except Exception as e:
        st.error(f"Fehler beim Importieren: {e}")
        return False
