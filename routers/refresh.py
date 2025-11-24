from fastapi import APIRouter, HTTPException
import auth_utils, schemas

router = APIRouter(prefix="/refresh", tags=["refresh"])

@router.post("/", response_model=schemas.Token)
def refresh_token(refresh_token: str):
    payload = auth_utils.verify_token(refresh_token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    email = payload.get("sub")
    new_access_token = auth_utils.create_access_token({"sub": email})
    new_refresh_token = auth_utils.create_refresh_token({"sub": email})

    return {"access_token": new_access_token, "refresh_token": new_refresh_token}
