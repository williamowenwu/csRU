from pydantic import BaseSettings


class Settings(BaseSettings):
    db_hostname: str
    db_name: str
    db_port: str
    db_password: str
    db_username: str
    secret_key: str = "jf9823jf(A*Goi3jSD(G*3wlgj(WS*gh#LWJGw98SH@*#"
    algorithm: str
    access_token_expire_seconds: int

    class Config:
        env_file = ".env"


settings = Settings()
