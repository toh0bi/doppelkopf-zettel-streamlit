"""
DynamoDB Cloud Sync für Doppelkopf Zettel
Speichert und lädt Spielstände aus AWS DynamoDB
"""
import streamlit as st
import boto3
from datetime import datetime, timedelta
from botocore.exceptions import ClientError
import json


def get_dynamodb_client():
    """Erstellt einen DynamoDB Client mit Streamlit Secrets"""
    try:
        return boto3.client(
            'dynamodb',
            aws_access_key_id=st.secrets["aws"]["aws_access_key_id"],
            aws_secret_access_key=st.secrets["aws"]["aws_secret_access_key"],
            region_name=st.secrets["aws"]["aws_region"]
        )
    except KeyError:
        st.error("❌ AWS Credentials nicht in Streamlit Secrets konfiguriert!")
        return None


def get_table_name():
    """Holt den DynamoDB Tabellennamen aus Secrets"""
    try:
        return st.secrets["aws"]["dynamodb_table_name"]
    except KeyError:
        return "doppelkopf_sessions"


def calculate_ttl(days=365):
    """Berechnet TTL (Unix Timestamp) für DynamoDB"""
    expire_date = datetime.now() + timedelta(days=days)
    return int(expire_date.timestamp())


def serialize_game_data(state=None):
    """
    Serialisiert den aktuellen Session State für DynamoDB
    
    Args:
        state: Session State Objekt (default: st.session_state)
    
    Returns:
        Dictionary mit serialisierten Spieldaten
    """
    if state is None:
        state = st.session_state
    
    return {
        "players": state.players,
        "rounds": state.rounds,
        "session_started": state.session_started,
        "created_at": state.get('created_at', datetime.now().isoformat()),
        "sitting_out_index": state.get('sitting_out_index', 0)
    }


def deserialize_game_data(game_data, state=None):
    """
    Lädt gespeicherte Spieldaten in den Session State
    
    Args:
        game_data: Dictionary mit Spieldaten
        state: Session State Objekt (default: st.session_state)
    """
    if state is None:
        state = st.session_state
    
    state.players = game_data.get("players", [])
    state.rounds = game_data.get("rounds", [])
    state.session_started = game_data.get("session_started", False)
    state.created_at = game_data.get("created_at", datetime.now().isoformat())
    state.sitting_out_index = game_data.get("sitting_out_index", 0)


def save_to_dynamodb(session_name: str) -> bool:
    """
    Speichert den aktuellen Spielstand in DynamoDB
    
    Args:
        session_name: Der eindeutige Session-Name (wie ein Passwort)
    
    Returns:
        True wenn erfolgreich, False bei Fehler
    """
    client = get_dynamodb_client()
    if not client:
        return False
    
    try:
        table_name = get_table_name()
        now = datetime.now().isoformat()
        
        # Spieldaten serialisieren
        game_data = serialize_game_data()
        
        # In DynamoDB speichern
        client.put_item(
            TableName=table_name,
            Item={
                'session_name': {'S': session_name},
                'last_updated': {'S': now},
                'created_at': {'S': game_data.get('created_at', now)},
                'game_data': {'S': json.dumps(game_data)},
                'ttl': {'N': str(calculate_ttl(365))}  # 1 Jahr TTL
            }
        )
        
        return True
        
    except ClientError as e:
        st.error(f"❌ DynamoDB Fehler: {e.response['Error']['Message']}")
        return False
    except Exception as e:
        st.error(f"❌ Unerwarteter Fehler: {str(e)}")
        return False


def load_from_dynamodb(session_name: str) -> bool:
    """
    Lädt einen Spielstand aus DynamoDB
    
    Args:
        session_name: Der eindeutige Session-Name
    
    Returns:
        True wenn erfolgreich geladen, False wenn nicht gefunden oder Fehler
    """
    client = get_dynamodb_client()
    if not client:
        return False
    
    try:
        table_name = get_table_name()
        
        # Item aus DynamoDB laden
        response = client.get_item(
            TableName=table_name,
            Key={
                'session_name': {'S': session_name}
            }
        )
        
        # Prüfen ob Item existiert
        if 'Item' not in response:
            st.warning(f"⚠️ Keine Session mit dem Namen '{session_name}' gefunden.")
            return False
        
        # Spieldaten deserialisieren
        item = response['Item']
        game_data = json.loads(item['game_data']['S'])
        
        # In Session State laden
        deserialize_game_data(game_data)
        
        # Cloud-Sync aktivieren
        st.session_state.cloud_session_name = session_name
        st.session_state.cloud_sync_enabled = True
        
        st.success(f"✅ Session '{session_name}' erfolgreich geladen!")
        return True
        
    except ClientError as e:
        st.error(f"❌ DynamoDB Fehler: {e.response['Error']['Message']}")
        return False
    except Exception as e:
        st.error(f"❌ Fehler beim Laden: {str(e)}")
        return False


def auto_sync_after_round():
    """
    Automatisches Speichern nach jeder Runde (wenn Cloud-Sync aktiv)
    Sollte nach jeder Runde aufgerufen werden
    """
    if st.session_state.get('cloud_sync_enabled', False):
        session_name = st.session_state.get('cloud_session_name')
        if session_name:
            if save_to_dynamodb(session_name):
                st.success(f"☁️ Spielstand automatisch gespeichert!")
            else:
                st.warning("⚠️ Automatische Speicherung fehlgeschlagen")


def check_cloud_credentials() -> bool:
    """Prüft ob AWS Credentials konfiguriert sind"""
    try:
        st.secrets["aws"]["aws_access_key_id"]
        st.secrets["aws"]["aws_secret_access_key"]
        st.secrets["aws"]["aws_region"]
        return True
    except (KeyError, FileNotFoundError):
        return False
