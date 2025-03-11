from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from google.oauth2 import id_token
from google.auth.transport import requests
import requests as http_requests
from .. import database, models, oauth2
from ..config import settings

router = APIRouter(
    prefix="/auth/google",
    tags=['Google Authentication']
)

@router.get("/")
async def google_login():
    """Google login endpoint that redirects to Google's OAuth consent screen"""
    return RedirectResponse(
        f"https://accounts.google.com/o/oauth2/v2/auth?"
        f"client_id={settings.google_client_id}&"
        f"response_type=code&"
        f"scope=openid email profile&"
        f"redirect_uri={settings.google_redirect_uri}"
    )

@router.get("/callback")
async def google_callback(code: str, db: Session = Depends(database.get_db)):
    """Callback endpoint that Google redirects to after successful authentication"""
    try:
        # Exchange the authorization code for tokens
        token_url = "https://oauth2.googleapis.com/token"
        token_data = {
            "code": code,
            "client_id": settings.google_client_id,
            "client_secret": settings.google_client_secret,
            "redirect_uri": settings.google_redirect_uri,
            "grant_type": "authorization_code"
        }
        
        # HTTP isteği için requests kütüphanesini kullanıyoruz
        token_response = http_requests.post(token_url, data=token_data)
        token_response.raise_for_status()
        tokens = token_response.json()

        # Google token'ı doğrulama
        id_info = id_token.verify_oauth2_token(
            tokens["id_token"],
            requests.Request(),
            settings.google_client_id
        )

        # Kullanıcıyı bul veya oluştur
        user = db.query(models.User).filter(models.User.email == id_info["email"]).first()
        if not user:
            # Yeni kullanıcı oluştur
            user = models.User(
                email=id_info["email"],
                password="",  # Google kullanıcıları için şifre boş
                is_google_user=True
            )
            db.add(user)
            db.commit()
            db.refresh(user)

        # Kendi JWT token'ımızı oluştur
        access_token = oauth2.create_accsess_token(data={"user_id": user.id})
        
        return {"access_token": access_token, "token_type": "bearer"}

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Could not validate Google credentials: {str(e)}"
        )
