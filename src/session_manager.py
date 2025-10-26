"""
Session State Management für Doppelkopf Zettel
"""
import streamlit as st
from datetime import datetime
import uuid


def init_session_state():
    """Initialisiert den Session State"""
    if 'session_id' not in st.session_state:
        st.session_state.session_id = str(uuid.uuid4())
    
    if 'players' not in st.session_state:
        st.session_state.players = []
    
    if 'rounds' not in st.session_state:
        st.session_state.rounds = []
    
    if 'session_started' not in st.session_state:
        st.session_state.session_started = False
    
    if 'created_at' not in st.session_state:
        st.session_state.created_at = datetime.now().isoformat()
    
    if 'last_imported_file' not in st.session_state:
        st.session_state.last_imported_file = None


def reset_session():
    """Setzt die Session komplett zurück"""
    keys_to_delete = list(st.session_state.keys())
    for key in keys_to_delete:
        del st.session_state[key]
    st.rerun()
