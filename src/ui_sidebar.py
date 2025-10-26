"""
Sidebar UI-Komponente
"""
import streamlit as st
from datetime import datetime
from src.data_manager import export_session, import_session
from src.session_manager import reset_session


def render_sidebar():
    """Rendert die Sidebar mit Session-Management"""
    with st.sidebar:
        st.header("📋 Session-Verwaltung")
        
        # Status-Anzeige
        if st.session_state.session_started:
            st.success("✅ Session aktiv")
            st.caption(f"🎮 {len(st.session_state.players)} Spieler")
            st.caption(f"🎯 {len(st.session_state.rounds)} Runden")
        else:
            st.info("ℹ️ Keine aktive Session")
        
        st.divider()
        
        # Export/Import
        st.subheader("💾 Speichern/Laden")
        
        if st.session_state.session_started:
            # Export
            json_export = export_session()
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"doppelkopf_{timestamp}.json"
            
            st.download_button(
                label="📥 Session exportieren",
                data=json_export,
                file_name=filename,
                mime="application/json",
                use_container_width=True,
                help="Speichere die Session als JSON-Datei"
            )
            
            st.caption("💡 Tipp: Exportiere regelmäßig!")
        
        # Import
        uploaded_file = st.file_uploader("📤 Session importieren", type=['json'], help="Lade eine gespeicherte Session")
        if uploaded_file is not None:
            file_id = f"{uploaded_file.name}_{uploaded_file.size}"
            if st.session_state.last_imported_file != file_id:
                json_data = uploaded_file.read().decode('utf-8')
                if import_session(json_data):
                    st.session_state.last_imported_file = file_id
                    st.success("✅ Session erfolgreich importiert!")
                    st.rerun()
            else:
                st.info("ℹ️ Diese Session ist bereits geladen")
        
        st.divider()
        
        # Neue Session starten
        if st.button("🔄 Neue Session starten", type="secondary", use_container_width=True):
            reset_session()
