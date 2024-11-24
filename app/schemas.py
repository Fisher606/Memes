from pydantic import BaseModel

class MemeBase(BaseModel):
    text: str
    image_url: str

class MemeCreate(MemeBase):
    pass

class Meme(MemeBase):
    id: int

    class Config:
        orm_mode = True
