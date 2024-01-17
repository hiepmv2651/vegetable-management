from pydantic_settings import BaseSettings


class Setting(BaseSettings):
    DATABASE_HOSTNAME: str
    DATABASE_NAME: str
    DATABASE_USERNAME: str
    DATABASE_PASSWORD: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    @property
    def DATABASE_URL(self):
        return f"mysql://{self.DATABASE_USERNAME}:{self.DATABASE_PASSWORD}@{self.DATABASE_HOSTNAME}/{self.DATABASE_NAME}"
    
    @staticmethod
    def get_secret(secret_name):
        try:
            with open(f'/run/secrets/{secret_name}', 'r') as secret_file:
                return secret_file.read().strip()
        except IOError:
            return None

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True
        
settings = Setting()