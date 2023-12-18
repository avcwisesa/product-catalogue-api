def test_index(client):
    response = client.get("/")
    print(response)
    print(response.data)
    assert response.status_code == 200
