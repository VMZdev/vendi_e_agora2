from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from src.models.sqlite.settings.base import Base

class UploadsTable(Base):
    __tablename__ = "uploads"

    upload_id = Column(Integer, primary_key=True)
    file_name = Column(String, nullable=False)
    file_size = Column(String)
    file_type = Column(String)
    upload_date = Column(DateTime, default=datetime.now)
    file_path = Column(String)

    def __repr__(self):
        return f"Upload [name={self.file_name}, date={self.upload_date}]"