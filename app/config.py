from pydantic_settings import BaseSettings

# BaseSettings yok burda
class Settings(BaseSettings):
    # database_password: str = "localhost"
    # database_username: str = "postgres"
    # secret_key: str = "123"
    # # path: int  # ---> hata verir.
    database_hostname: str
    database_port: int
    database_password: str
    database_name: str
    database_username: str
    secret_key: str
    algorithm: str
    access_token_exp_min: int
    
    # Google OAuth Settings
    google_client_id: str
    google_client_secret: str
    google_redirect_uri: str

    class Config:
        env_file = ".env"

settings = Settings()