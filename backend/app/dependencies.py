from functools import lru_cache
from app.services.tigergraph_service import TigerGraphService


@lru_cache()
def get_tg_service() -> TigerGraphService:
    return TigerGraphService()
