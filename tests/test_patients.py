def test_create_patient(client):
    response = client.post(
        "/patients/",
        json={
            "name": "Test Patient",
            "email": "testpatient@example.com",
            "phone": "9876543210",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["id"] == 1
    assert data["name"] == "Test Patient"
    assert data["email"] == "testpatient@example.com"
    assert data["phone"] == "9876543210"


def test_get_patients(client):
    client.post(
        "/patients/",
        json={
            "name": "Patient One",
            "email": "patient1@example.com",
            "phone": "1111111111",
        },
    )

    response = client.get("/patients/")

    assert response.status_code == 200
    assert len(response.json()) == 1


def test_get_patient_by_id(client):
    create_response = client.post(
        "/patients/",
        json={
            "name": "Patient One",
            "email": "patient2@example.com",
            "phone": "2222222222",
        },
    )

    patient_id = create_response.json()["id"]

    response = client.get(f"/patients/{patient_id}")

    assert response.status_code == 200
    assert response.json()["id"] == patient_id


def test_get_missing_patient(client):
    response = client.get("/patients/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Patient not found"


def test_duplicate_patient_email(client):
    patient = {
        "name": "Patient One",
        "email": "duplicate@example.com",
        "phone": "3333333333",
    }

    first_response = client.post("/patients/", json=patient)
    second_response = client.post("/patients/", json=patient)

    assert first_response.status_code == 201
    assert second_response.status_code == 409
    assert second_response.json()["detail"] == (
        "Patient with this email already exists"
    )