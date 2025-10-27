"""
UI für Cloud-Session Management
Dialog für Session-Name Eingabe und Cloud-Sync Aktivierung
"""
import streamlit as st
from src.cloud_sync import (
    load_from_dynamodb,
    save_to_dynamodb,
    check_cloud_credentials
)


def render_cloud_session_dialog():
    """
    Zeigt Dialog für Cloud-Sync Aktivierung an
    Wird beim Spieler-Setup aufgerufen
    """
    if not check_cloud_credentials():
        return  # Keine AWS Credentials → Cloud-Sync nicht verfügbar
    
    st.markdown("---")
    st.markdown("### ☁️ Cloud-Speicherung (Optional)")
    
    with st.expander("ℹ️ Was ist Cloud-Speicherung?", expanded=False):
        st.info("""
        **Vorteile:**
        - 📱 Spiel auf jedem Gerät fortsetzen
        - 🔄 Automatische Speicherung nach jeder Runde
        - 💾 Daten bleiben 1 Jahr gespeichert
        
        **Wichtig:**
        - Der Session-Name ist wie ein **Passwort**
        - Jeder der ihn kennt, kann das Spiel laden/verändern
        - Wähle einen **einzigartigen Namen** (z.B. "Stammtisch_Oktober_2025_Ziege")
        """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        cloud_enabled = st.checkbox(
            "☁️ Cloud-Speicherung aktivieren",
            value=st.session_state.get('cloud_sync_enabled', False),
            help="Speichere das Spiel automatisch in der Cloud"
        )
    
    if cloud_enabled:
        with col2:
            session_name = st.text_input(
                "Session-Name (wie Passwort!)",
                value=st.session_state.get('cloud_session_name', ''),
                placeholder="z.B. Stammtisch_Oktober_2025_Ziege",
                help="Merke dir diesen Namen! Du brauchst ihn zum Wiederladen.",
                max_chars=50
            )
        
        if session_name and len(session_name) >= 15:
            st.session_state.cloud_sync_enabled = True
            st.session_state.cloud_session_name = session_name
            
            st.success(f"✅ Cloud-Sync aktiv für Session: `{session_name}`")
            
            # Info zur Sicherheit
            st.caption("⚠️ **Sicherheitshinweis:** Dieser Name ist NICHT verschlüsselt. Jeder der ihn kennt, kann dein Spiel laden.")
        elif cloud_enabled and session_name:
            st.warning("⚠️ Session-Name muss mindestens 15 Zeichen lang sein")
    else:
        st.session_state.cloud_sync_enabled = False
        st.session_state.cloud_session_name = None


def render_load_session_dialog():
    """
    Dialog zum Laden einer existierenden Cloud-Session
    Wird beim App-Start angezeigt
    """
    if not check_cloud_credentials():
        return False
    
    st.markdown("### 📂 Existierendes Spiel laden")
    
    with st.expander("ℹ️ Cloud-Spiel laden", expanded=True):
        st.info("""
        Hast du bereits ein Spiel in der Cloud gespeichert?
        Gib den **Session-Namen** ein, um es zu laden.
        """)
        
        session_name = st.text_input(
            "Session-Name eingeben",
            placeholder="z.B. Stammtisch_Oktober_2025",
            key="load_session_input"
        )
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📥 Laden", type="primary", disabled=not session_name):
                if load_from_dynamodb(session_name):
                    st.rerun()  # Refresh UI nach erfolgreichem Laden
        
        with col2:
            st.caption("oder starte ein neues Spiel unten")
    
    st.markdown("---")
    return False


def render_cloud_sync_status():
    """
    Zeigt Cloud-Sync Status in der Sidebar an
    """
    if not check_cloud_credentials():
        return
    
    if st.session_state.get('cloud_sync_enabled', False):
        session_name = st.session_state.get('cloud_session_name', 'Unknown')
        st.sidebar.success(f"☁️ Cloud-Sync aktiv")
        st.sidebar.caption(f"Session: `{session_name}`")
        
        # Manuelle Sync-Option
        if st.sidebar.button("💾 Jetzt speichern", help="Manuelles Backup erstellen"):
            if save_to_dynamodb(session_name):
                st.sidebar.success("✅ Gespeichert!")
    else:
        st.sidebar.info("💾 Nur lokal")
