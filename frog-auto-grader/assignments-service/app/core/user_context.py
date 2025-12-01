from fastapi import Header, HTTPException


def get_user_context(
    x_user_id: str = Header(..., alias="X-User-Id"),
    x_user_role: str = Header(..., alias="X-User-Role"),
):
    if not x_user_id or not x_user_role:
        raise HTTPException(status_code=400, detail="Missing user context headers")

    return {
        "user_id": x_user_id,
        "role": x_user_role.upper(),  # STUDENT / TEACHER / ADMIN
    }
