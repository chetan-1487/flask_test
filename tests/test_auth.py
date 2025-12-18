import io

def test_signup_success(client):
  payload={
    "first_name":"hello",
    "last_name":"world",
    "email":"hello@gmail.com",
    "password":"Hello@123",
    "status":"active",
    "username":"Hello12",
    "role":"Admin",
    "profile_image_url": (io.BytesIO(b"fake image data"), "photo-1514888286974-6c03e2ca1dba.avif")
  }

  response = client.post("/create", data=payload, content_type="multipart/form-data")

  assert response.status_code == 201
  data = response.get_json()
  assert "registration" in data["message"].lower()
