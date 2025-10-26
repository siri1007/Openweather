from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.orm import declarative_base, sessionmaker


DATABASE_URL = "sqlite:///./weather_preferences.db"  


engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})


Base = declarative_base()

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


class UserPreferences(Base):
    __tablename__ = "preferences"
    id = Column(Integer, primary_key=True, index=True)
    default_city = Column(String, default="Hyderabad")
    units = Column(String, default="metric")
    language = Column(String, default="en")


Base.metadata.create_all(bind=engine)
