from pydantic import BaseModel

class Structure(BaseModel):
    path: str

class Input_Inference(BaseModel):
    input: str