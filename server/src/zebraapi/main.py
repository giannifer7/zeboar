from fastapi import FastAPI, status
from fastapi.exceptions import HTTPException
from sqlmodel import Session, select
from typing import List
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import load_only
from .models import Book
from .models import Pannello, PannelloMain, PannelloUpdate
from .database import engine

from sqlmodel.sql.expression import Select, SelectOfScalar

SelectOfScalar.inherit_cache = True  # type: ignore
Select.inherit_cache = True  # type: ignore


app = FastAPI()
session = Session(bind=engine)

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.post("/books", response_model=Book, status_code=status.HTTP_201_CREATED)
async def create_a_book(book: Book):
    new_book = Book(title=book.title, description=book.description)
    session.add(new_book)
    session.commit()
    return new_book


@app.get(
    "/cose/elettronica/rack/panels_main",
    response_model=List[PannelloMain],
    status_code=status.HTTP_200_OK,
)
async def get_all_panels_main():
    statement = select(
        Pannello.id,
        Pannello.units,
        Pannello.quantity,
        Pannello.comm,
        Pannello.position,
    )
    results = session.exec(statement).all()
    return results


@app.get(
    "/cose/elettronica/rack/panels",
    response_model=List[Pannello],
    status_code=status.HTTP_200_OK,
)
async def get_all_panels():
    statement = (
        select(Pannello).options(load_only("id", "name"))
        # .where(Pannello.tipo==tipo)
    )
    results = session.exec(statement).all()
    return results


@app.get(
    "/cose/elettronica/rack/panels_main/{tipo}",
    response_model=List[PannelloMain],
    status_code=status.HTTP_200_OK,
)
async def get_all_panels_by_tipo_main(tipo: str):
    statement = select(
        Pannello.id,
        Pannello.units,
        Pannello.quantity,
        Pannello.comm,
        Pannello.position,
    ).where(Pannello.tipo == tipo)
    results = session.exec(statement).all()
    return results


@app.get(
    "/cose/elettronica/rack/panels/{tipo}",
    response_model=List[Pannello],
    status_code=status.HTTP_200_OK,
)
async def get_all_panels_by_tipo(tipo: str):
    statement = select(Pannello).where(Pannello.tipo == tipo)
    results = session.exec(statement).all()
    return results


@app.get(
    "/cose/elettronica/rack/panel/{tipo}/{panel_id}",
    response_model=Pannello,
    status_code=status.HTTP_200_OK,
)
async def get_a_panel(tipo: str, panel_id: int):
    statement = select(Pannello).where(Pannello.tipo == tipo, Pannello.id == panel_id)
    result = session.exec(statement).first()
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return result


@app.get(
    "/cose/elettronica/rack/panels_main/{tipo}/{subtipo}",
    response_model=List[PannelloMain],
    status_code=status.HTTP_200_OK,
)
async def get_all_panels_by_tipo_subtipo_main(tipo: str, subtipo: str):
    statement = select(
        Pannello.id,
        Pannello.units,
        Pannello.quantity,
        Pannello.comm,
        Pannello.position,
    ).where(Pannello.tipo == tipo, Pannello.subtipo == subtipo)
    results = session.exec(statement).all()
    return results


@app.get(
    "/cose/elettronica/rack/one_panel/{panel_id}",
    response_model=Pannello,
    status_code=status.HTTP_200_OK,
)
async def get_one_panel(panel_id: int):
    statement = select(Pannello).where(Pannello.id == panel_id)
    result = session.exec(statement).first()
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return result


# https://sqlmodel.tiangolo.com/tutorial/fastapi/update/
@app.patch(
    "/cose/elettronica/rack/one_panel/{panel_id}",
    response_model=Pannello,
)
async def update_one_panel(panel_id: int, panel: PannelloUpdate):
    with Session(engine) as session:
        db_panel = session.get(Pannello, panel_id)
        if not db_panel:
            raise HTTPException(status_code=404, detail="Panel not found")
        panel_data = panel.dict(exclude_unset=True)
        for key, value in panel_data.items():
            setattr(db_panel, key, value)
        session.add(db_panel)
        session.commit()
        session.refresh(db_panel)
        return db_panel


@app.delete("/book/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_a_book(book_id: int):
    statement = select(Book).where(Book.id == book_id)
    result = session.exec(statement).one_or_none()
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Resource Not Found"
        )
    session.delete(result)
    return result
