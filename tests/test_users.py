def test_create_user(client):
    """Test creating a new user"""
    user_data = {
        "email": "test@example.com",
        "username": "testuser",
        "password": "testpassword123",
        "full_name": "Test User",
    }
    response = client.post("/api/v1/users/", json=user_data)
    assert response.status_code == 201
    body = response.json()
    assert body["success"] is True
    data = body["data"]
    assert data["email"] == user_data["email"]
    assert data["username"] == user_data["username"]
    assert "id" in data
    assert "hashed_password" not in data


def test_read_users(client):
    """Test reading users list"""
    # Create a user first
    user_data = {
        "email": "test@example.com",
        "username": "testuser",
        "password": "testpassword123",
    }
    client.post("/api/v1/users/", json=user_data)

    # Read users
    response = client.get("/api/v1/users/")
    assert response.status_code == 200
    body = response.json()
    assert body["success"] is True
    assert isinstance(body["data"], list)
    assert len(body["data"]) > 0


def test_read_user(client):
    """Test reading a specific user"""
    # Create a user first
    user_data = {
        "email": "test@example.com",
        "username": "testuser",
        "password": "testpassword123",
    }
    create_response = client.post("/api/v1/users/", json=user_data)
    user_id = create_response.json()["data"]["id"]

    # Read the user
    response = client.get(f"/api/v1/users/{user_id}")
    assert response.status_code == 200
    body = response.json()
    assert body["success"] is True
    assert body["data"]["id"] == user_id


def test_update_user(client):
    """Test updating a user"""
    # Create a user first
    user_data = {
        "email": "test@example.com",
        "username": "testuser",
        "password": "testpassword123",
    }
    create_response = client.post("/api/v1/users/", json=user_data)
    user_id = create_response.json()["data"]["id"]

    # Update the user
    update_data = {"full_name": "Updated Name"}
    response = client.put(f"/api/v1/users/{user_id}", json=update_data)
    assert response.status_code == 200
    body = response.json()
    assert body["success"] is True
    assert body["data"]["full_name"] == "Updated Name"


def test_delete_user(client):
    """Test deleting a user"""
    # Create a user first
    user_data = {
        "email": "test@example.com",
        "username": "testuser",
        "password": "testpassword123",
    }
    create_response = client.post("/api/v1/users/", json=user_data)
    user_id = create_response.json()["data"]["id"]

    # Delete the user
    response = client.delete(f"/api/v1/users/{user_id}")
    assert response.status_code == 200
    body = response.json()
    assert body["success"] is True

    # Verify user is deleted
    get_response = client.get(f"/api/v1/users/{user_id}")
    assert get_response.status_code == 404


def test_create_duplicate_email(client):
    """Test that duplicate email is rejected"""
    user_data = {
        "email": "test@example.com",
        "username": "testuser",
        "password": "testpassword123",
    }
    client.post("/api/v1/users/", json=user_data)

    # Try to create another user with same email
    user_data2 = {
        "email": "test@example.com",
        "username": "testuser2",
        "password": "testpassword123",
    }
    response = client.post("/api/v1/users/", json=user_data2)
    assert response.status_code == 400
    body = response.json()
    assert body["success"] is False
    assert body["message"] == "Email already registered"


def test_create_duplicate_username(client):
    """Test that duplicate username is rejected"""
    user_data = {
        "email": "test@example.com",
        "username": "testuser",
        "password": "testpassword123",
    }
    client.post("/api/v1/users/", json=user_data)

    # Try to create another user with same username
    user_data2 = {
        "email": "test2@example.com",
        "username": "testuser",
        "password": "testpassword123",
    }
    response = client.post("/api/v1/users/", json=user_data2)
    assert response.status_code == 400
    body = response.json()
    assert body["success"] is False
    assert body["message"] == "Username already registered"
