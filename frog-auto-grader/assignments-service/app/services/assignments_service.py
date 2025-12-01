from datetime import datetime
from typing import List, Optional, Dict, Any

from app.core.firebase import db


def create_assignment(data: Dict[str, Any]) -> Dict[str, Any]:
    ref = db.collection("assignments").document()
    payload = {
        "title": data["title"],
        "description": data.get("description"),
        "course": data["course"],
        "deadline": data["deadline"],   # datetime, Firestore lo guarda como timestamp
        "grading_criteria": data.get("grading_criteria"),
        "created_by": data["created_by"],
        "created_at": datetime.utcnow(),
    }
    ref.set(payload)
    payload["id"] = ref.id
    return payload


def list_assignments() -> List[Dict[str, Any]]:
    docs = db.collection("assignments").order_by("created_at", direction="DESCENDING").stream()
    result = []
    for doc in docs:
        d = doc.to_dict()
        d["id"] = doc.id
        result.append(d)
    return result


def get_assignment(assignment_id: str) -> Optional[Dict[str, Any]]:
    doc = db.collection("assignments").document(assignment_id).get()
    if not doc.exists:
        return None
    d = doc.to_dict()
    d["id"] = doc.id
    return d


def update_assignment(assignment_id: str, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    ref = db.collection("assignments").document(assignment_id)
    doc = ref.get()
    if not doc.exists:
        return None

    update_data = {k: v for k, v in data.items() if v is not None}
    if not update_data:
        d = doc.to_dict()
        d["id"] = doc.id
        return d

    ref.update(update_data)
    updated = ref.get().to_dict()
    updated["id"] = ref.id
    return updated
