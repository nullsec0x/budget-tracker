from sqlalchemy.orm import Session
from .database import Settings

def get_settings(session: Session) -> Settings:
    settings = session.query(Settings).first()
    if not settings:
        settings = Settings()
        session.add(settings)
        session.commit()
    return settings

def set_currency_symbol(session: Session, symbol: str) -> Settings:
    settings = get_settings(session)
    settings.currency_symbol = symbol
    session.commit()
    return settings

def get_currency_symbol(session: Session) -> str:
    settings = get_settings(session)
    return settings.currency_symbol
