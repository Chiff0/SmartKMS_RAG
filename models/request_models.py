from pydantic import BaseModel
from typing import Optional, Dict, Any

class QueryRequest(BaseModel):
    query: str
    user: str  
    type: Optional[str] = None
    source: Optional[str] = None

class PushRequest(BaseModel):
    typefield: str
    platform: str
    id: str
    timestamp: str
    content: Dict[str, Any]