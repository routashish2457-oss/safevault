def test_sql_injection(client):
    response = client.post("/login", data={
        "username": "' OR 1=1 --",
        "password": "test"
    })
    assert b"Invalid credentials" in response.data
