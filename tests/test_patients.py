def test_create_patient(client):
    response = client.post(
        "/patients",
        json={
            "name": "Test Patient",
            "email": "patient@example.com",
            "phone": "9876543210",
        },
    )

    assert response.status_code == 201
    assert response.json()["name"] == "Test Patient"


def test_get_patients(client):
    client.post(
        "/patients",
        json={
            "name": "Test Patient",
            "email": "patient@example.com",
            "phone": "9876543210",
        },
    )

    response = client.get("/patients")

    assert response.status_code == 200
    assert len(response.json()) == 1


def test_get_patient(client):
    created = client.post(
        "/patients",
        json={
            "name": "Test Patient",
            "email": "patient@example.com",
            "phone": "9876543210",
        },
    )

    patient_id = created.json()["id"]
    response = client.get(f"/patients/{patient_id}")

    assert response.status_code == 200
    assert response.json()["id"] == patient_id


def test_patient_not_found(client):
    response = client.get("/patients/999")

    assert response.status_code == 404


def test_duplicate_patient_email(client):
    data = {
        "name": "Test Patient",
        "email": "patient@example.com",
        "phone": "9876543210",
    }

    first = client.post("/patients", json=data)
    second = client.post("/patients", json=data)

    assert first.status_code == 201
    assert second.status_code == 409
