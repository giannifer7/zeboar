from sqlmodel import SQLModel, Field
from typing import Optional


class Book(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: str


# Code above omitted 👆


class HeroBase(SQLModel):
    name: str = Field(index=True)
    secret_name: str
    age: Optional[int] = Field(default=None, index=True)


class Hero(HeroBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)


class HeroCreate(HeroBase):
    pass


class HeroRead(HeroBase):
    id: int


class HeroUpdate(SQLModel):
    name: Optional[str] = None
    secret_name: Optional[str] = None
    age: Optional[int] = None


# Code below omitted 👇


class Pannello(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    tipo: str  # = Field(default=None, primary_key=True)
    subtipo: str
    name: str
    descr: str
    barcode: str
    brand: str
    units: float
    quantity: int
    position: str
    pos_pics: str
    box_pics: str
    obj_pics: str
    comm: str


class PannelloMain(SQLModel):
    id: Optional[int] = Field(default=None, primary_key=True)
    units: float
    quantity: int
    comm: str
    position: str


class PannelloUpdate(SQLModel):
    tipo: Optional[str] = None
    subtipo: Optional[str] = None
    name: Optional[str] = None
    descr: Optional[str] = None
    barcode: Optional[str] = None
    brand: Optional[str] = None
    units: Optional[float] = None
    quantity: Optional[int] = None
    position: Optional[str] = None
    pos_pics: Optional[str] = None
    box_pics: Optional[str] = None
    obj_pics: Optional[str] = None
    comm: Optional[str] = None
