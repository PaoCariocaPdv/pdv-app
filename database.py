"""
PDV - Ponto de Venda
Conexão com Firebase Firestore
"""

import os
import json

_db = None
_initialized = False


def initialize_firebase():
    """Inicializa a conexão com o Firebase."""
    global _db, _initialized

    if _initialized:
        return _db

    try:
        import firebase_admin
        from firebase_admin import credentials, firestore

        cred_path = "firebase_credentials.json"

        if not os.path.exists(cred_path):
            print("[Firebase] Arquivo de credenciais não encontrado. Rodando em modo offline.")
            _initialized = True
            return None

        if not firebase_admin._apps:
            cred = credentials.Certificate(cred_path)
            firebase_admin.initialize_app(cred)

        _db = firestore.client()
        _initialized = True
        print("[Firebase] Conectado com sucesso!")
        return _db

    except Exception as e:
        print(f"[Firebase] Erro ao conectar: {e}")
        _initialized = True
        return None


def get_db():
    """Retorna a instância do banco de dados."""
    global _db, _initialized
    if not _initialized:
        initialize_firebase()
    return _db


def is_connected():
    """Verifica se está conectado ao Firebase."""
    return _db is not None
