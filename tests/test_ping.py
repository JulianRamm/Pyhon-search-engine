from flask import url_for

def test_ping(client):
    response = client.get(url_for("ping.pong"))
    assert response.status_code == 200
