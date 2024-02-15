from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base
# Database connection (replace with your actual connection details)
engine = create_engine("sqlite:///stories.db")
Base = declarative_base()

# Define database model
class Story(Base):
    __tablename__ = "stories"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    meta_info = Column(String)

    def __repr__(self):
        return f"<Story {self.id}: {self.title}>"

# Create database tables (if not already existing)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()