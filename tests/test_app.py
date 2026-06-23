from tic_tac_toe_ynov.app import create_app


def test_health_endpoint() -> None:
    app = create_app()

    with app.test_client() as client:
        response = client.get("/health")

    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}


def test_index_endpoint() -> None:
    app = create_app()

    with app.test_client() as client:
        response = client.get("/")

    payload = response.get_json()
    assert response.status_code == 200
    assert payload["name"] == "tic-tac-toe-ynov"
    assert payload["available_moves"] == list(range(9))
