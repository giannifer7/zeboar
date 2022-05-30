from fastapi.testclient import TestClient
from zebraapi.main import app

# import pprint


client = TestClient(app)


def test_read_all_panels():
    response = client.get("/cose/elettronica/rack/panels")
    assert response.status_code == 200
    # pp = pprint.PrettyPrinter(indent=4)
    # rjs = response.json()
    # pp.pprint(rjs)
    # print(rjs)
    assert response.json() == [
        {
            "barcode": "8057685301993",
            "box_pics": "pannello/cieco/0",
            "brand": "Techly",
            "comm": "d899",
            "descr": "pannello cieco 1 unità Techly nero",
            "id": 1,
            "name": "orbo",
            "obj_pics": "pannello/cieco/0",
            "pos_pics": "pannello/cieco/0",
            "position": "e034",
            "quantity": 1,
            "subtipo": "cieco",
            "tipo": "pannello",
            "units": 1.0,
        },
        {
            "barcode": "8057685302013",
            "box_pics": "pannello/cieco/1",
            "brand": "Techly",
            "comm": "d898",
            "descr": "pannello cieco 1 unità Techly nero",
            "id": 2,
            "name": "orbo",
            "obj_pics": "pannello/cieco/1",
            "pos_pics": "pannello/cieco/1",
            "position": "e035",
            "quantity": 2,
            "subtipo": "cieco",
            "tipo": "pannello",
            "units": 2.0,
        },
    ]


def test_read_all_panels_main():
    response = client.get("/cose/elettronica/rack/panels_main")
    assert response.status_code == 200
    # pp = pprint.PrettyPrinter(indent=4)
    # rjs = response.json()
    # pp.pprint(rjs)
    # print(rjs)
    assert response.json() == [
        {"comm": "d899", "id": 1, "position": "e034", "quantity": 1, "units": 1.0},
        {"comm": "d898", "id": 2, "position": "e035", "quantity": 2, "units": 2.0},
    ]


def test_read_all_panels_by_tipo_main():
    tipo = "pannello"
    response = client.get(f"/cose/elettronica/rack/panels_main/{tipo}")
    assert response.status_code == 200
    assert response.json() == [
        {"comm": "d899", "id": 1, "position": "e034", "quantity": 1, "units": 1.0},
        {"comm": "d898", "id": 2, "position": "e035", "quantity": 2, "units": 2.0},
    ]


def test_read_all_panels_by_tipo():
    tipo = "pannello"
    response = client.get(f"/cose/elettronica/rack/panels/{tipo}")
    assert response.status_code == 200
    assert response.json() == [
        {
            "barcode": "8057685301993",
            "box_pics": "pannello/cieco/0",
            "brand": "Techly",
            "comm": "d899",
            "descr": "pannello cieco 1 unità Techly nero",
            "id": 1,
            "name": "orbo",
            "obj_pics": "pannello/cieco/0",
            "pos_pics": "pannello/cieco/0",
            "position": "e034",
            "quantity": 1,
            "subtipo": "cieco",
            "tipo": "pannello",
            "units": 1.0,
        },
        {
            "barcode": "8057685302013",
            "box_pics": "pannello/cieco/1",
            "brand": "Techly",
            "comm": "d898",
            "descr": "pannello cieco 1 unità Techly nero",
            "id": 2,
            "name": "orbo",
            "obj_pics": "pannello/cieco/1",
            "pos_pics": "pannello/cieco/1",
            "position": "e035",
            "quantity": 2,
            "subtipo": "cieco",
            "tipo": "pannello",
            "units": 2.0,
        },
    ]


def test_read_all_panels_by_tipo_subtipo_main():
    tipo = "pannello"
    subtipo = "cieco"
    response = client.get(f"/cose/elettronica/rack/panels_main/{tipo}/{subtipo}")
    assert response.status_code == 200
    assert response.json() == [
        {"comm": "d899", "id": 1, "position": "e034", "quantity": 1, "units": 1.0},
        {"comm": "d898", "id": 2, "position": "e035", "quantity": 2, "units": 2.0},
    ]


def test_read_one_panel():
    panel_id = 1
    response = client.get(f"/cose/elettronica/rack/one_panel/{panel_id}")
    assert response.status_code == 200
    assert response.json() == {
        "barcode": "8057685301993",
        "box_pics": "pannello/cieco/0",
        "brand": "Techly",
        "comm": "d899",
        "descr": "pannello cieco 1 unità Techly nero",
        "id": 1,
        "name": "orbo",
        "obj_pics": "pannello/cieco/0",
        "pos_pics": "pannello/cieco/0",
        "position": "e034",
        "quantity": 1,
        "subtipo": "cieco",
        "tipo": "pannello",
        "units": 1.0,
    }


def test_update_one_panel():
    panel_id = 1
    panel = {
        "name": "sgnaf",
        "obj_pics": "trallallero",
    }
    response = client.patch(f"/cose/elettronica/rack/one_panel/{panel_id}", data=panel)
    assert response.status_code == 200
