def test_login_success(client):
    """Test successful login"""
    # Create a user first
    user_data = {
        "email": "test@example.com",
        "username": "testuser",
        "password": "testpassword123",
    }
    client.post("/api/v1/users/", json=user_data)

    # Try to login
    login_data = {"username": "testuser", "password": "testpassword123"}
    response = client.post("/api/v1/auth/login", json=login_data)

    assert response.status_code == 200
    body = response.json()
    assert body["success"] is True
    assert "access_token" in body["data"]
    assert body["data"]["token_type"] == "bearer"


def test_login_wrong_password(client):
    """Test login with wrong password"""
    # Create a user first
    user_data = {
        "email": "test@example.com",
        "username": "testuser",
        "password": "testpassword123",
    }
    client.post("/api/v1/users/", json=user_data)

    # Try to login with wrong password
    login_data = {"username": "testuser", "password": "wrongpassword"}
    response = client.post("/api/v1/auth/login", json=login_data)

    assert response.status_code == 401
    body = response.json()
    assert body["success"] is False


def test_login_nonexistent_user(client):
    """Test login with non-existent user"""
    login_data = {"username": "nonexistent", "password": "password123"}
    response = client.post("/api/v1/auth/login", json=login_data)

    assert response.status_code == 401
    body = response.json()
    assert body["success"] is False


def test_get_current_user(client):
    """Test getting current user profile"""
    # Create a user and login
    user_data = {
        "email": "test@example.com",
        "username": "testuser",
        "password": "testpassword123",
    }
    client.post("/api/v1/users/", json=user_data)

    login_data = {"username": "testuser", "password": "testpassword123"}
    login_response = client.post("/api/v1/auth/login", json=login_data)
    token = login_response.json()["data"]["access_token"]

    # Get current user
    response = client.get(
        "/api/v1/auth/me", headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    body = response.json()
    assert body["success"] is True
    assert body["data"]["username"] == "testuser"


def test_get_current_user_invalid_token(client):
    """Test getting current user with invalid token"""
    response = client.get(
        "/api/v1/auth/me", headers={"Authorization": "Bearer invalid_token"}
    )

    assert response.status_code == 401
    body = response.json()
    assert body["success"] is False
