from pydantic import BaseModel


# class File_entity(BaseModel):
#     __tablename__ = "File"
#     id = Column(Integer, primary_key=True, index=True)
#     file_name = Column(String, nullable=False)
#     user_id = Column(String, nullable=False)
#     file_type = Column(String, nullable=False)
#     file_location = Column(String, nullable=False)

class File_entity(BaseModel):
    file_name : str
    user_id : str
    file_type : str
    file_location :str

# from pydantic import BaseModel

# class User(BaseModel):
#     name: str
#     email: str
    

