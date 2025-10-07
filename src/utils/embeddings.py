"""
Utilitários de Embeddings e Busca Semântica usando OpenAI/DeepSeek
"""

from __future__ import annotations

import json
import os
import math
from typing import List, Dict

from openai import OpenAI

from ..core.database import db_manager


EMBED_MODEL = "text-embedding-3-small"


def _get_client() -> OpenAI | None:
    """Inicializa um cliente OpenAI-compatível.

    Ordem de prioridade:
    1) DeepSeek (se DEEPSEEK_API_KEY setado) via base_url compatível
    2) OpenAI oficial (se OPENAI_API_KEY setado)
    """
    deepseek_key = os.getenv("DEEPSEEK_API_KEY", "").strip()
    deepseek_base = os.getenv("DEEPSEEK_BASE_URL", "").strip() or "https://api.deepseek.com"
    if deepseek_key:
        try:
            return OpenAI(api_key=deepseek_key, base_url=deepseek_base)
        except Exception:
            pass

    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    if api_key:
        try:
            return OpenAI(api_key=api_key)
        except Exception:
            return None
    return None


def _text_for_embedding(aula: Dict) -> str:
    parts = [aula.get("titulo"), aula.get("descricao"), aula.get("tags"), aula.get("legendas")]
    return " | ".join([str(p) for p in parts if p])


def embed_text(text: str) -> List[float]:
    client = _get_client()
    if client is None:
        raise RuntimeError("Cliente de embeddings não disponível (configure DEEPSEEK_API_KEY ou OPENAI_API_KEY)")
    out = client.embeddings.create(model=EMBED_MODEL, input=text)
    return out.data[0].embedding  # type: ignore


def cosine_similarity(a: List[float], b: List[float]) -> float:
    if not a or not b or len(a) != len(b):
        return -1.0
    dot = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(y * y for y in b))
    if na == 0 or nb == 0:
        return -1.0
    return dot / (na * nb)


def ensure_schema() -> None:
    """Garante coluna para embeddings em `aulas`."""
    db_manager.ensure_aulas_embedding_column()


def ensure_aula_embeddings() -> None:
    """Gera embeddings para aulas que não possuem ainda."""
    ensure_schema()
    aulas = db_manager.get_all_aulas()
    for a in aulas:
        if not a.get("embedding_json"):
            text = _text_for_embedding(a)
            if not text:
                continue
            vec = embed_text(text)
            db_manager.update_aula_embedding_json(a.get("id_aula") or a.get("id"), vec)


def search_similar_aulas(query: str, top_k: int = 3) -> List[Dict]:
    """Busca aulas similares à `query` usando embeddings em Python."""
    ensure_schema()
    # Tentar embeddings; caso falhe, usa keyword search
    try:
        ensure_aula_embeddings()
        q_vec = embed_text(query)
        aulas = db_manager.get_all_aulas_with_embeddings()
    except Exception:
        # Sem chave/crédito: fallback por keyword
        return db_manager.search_aulas_keyword(query, limit=top_k)
    scored: List[Dict] = []
    for a in aulas:
        emb_json = a.get("embedding_json")
        if not emb_json:
            continue
        try:
            vec = json.loads(emb_json)
        except Exception:
            continue
        score = cosine_similarity(q_vec, vec)
        a_copy = dict(a)
        a_copy["score"] = score
        scored.append(a_copy)
    scored.sort(key=lambda x: x.get("score", -1), reverse=True)
    return scored[: top_k if top_k > 0 else 3]


