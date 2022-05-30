from sqlmodel import Session, SQLModel
from database import engine


from models import (
    Pannello,
)


def populate(engine):
    pannelli = [
        Pannello(
            tipo="pannello",
            subtipo="cieco",
            name="",
            descr="pannello cieco 1 unità Techly nero",
            barcode="8057685301993",
            brand="Techly",
            units=1.0,
            quantity=1,
            position="e034",
            pos_pics="e0",
            box_pics="pannello/cieco/0",
            obj_pics="pannello/cieco/0",
            comm="d899",
        ),
        Pannello(
            tipo="pannello",
            subtipo="cieco",
            name="orbo",
            descr="pannello cieco 2 unità Techly nero",
            barcode="8057685302013",
            brand="Techly",
            units=2.0,
            quantity=2,
            position="e035",
            pos_pics="e1",
            box_pics="pannello/cieco/1",
            obj_pics="pannello/cieco/1",
            comm="d898",
        ),
    ]

    with Session(engine) as ssn:
        for p in pannelli:
            ssn.add(p)
        ssn.commit()


if __name__ == "__main__":
    print("creating database...")
    # engine = create_engine("sqlite:///database.db")
    SQLModel.metadata.create_all(engine)
    print("populating tables...")
    populate(engine)

# https://www.google.com/search?tbm=shop&q=
