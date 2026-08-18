def create_patient(client):
    response = client.post(
        "/patients/",
        json={
            "name": "Test Patient",
            "email": "appointmentpatient@example.com",
            "phone": "9999999999",
        },
    )

    assert response.status_code == 201

    return response.json()["id"]


def create_doctor(client):
    response = client.post(
        "/doctors/",
        json={
            "name": "Dr. Appointment",
            "specialization": "Cardiology",
        },
    )

    assert response.status_code == 201

    return response.json()["id"]


def test_create_appointment(client):
    patient_id = create_patient(client)
    doctor_id = create_doctor(client)

    response = client.post(
        "/appointments/",
        json={
            "patient_id": patient_id,
            "doctor_id": doctor_id,
            "appointment_start": "2026-08-20T10:00:00",
            "appointment_end": "2026-08-20T11:00:00",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["id"] == 1
    assert data["patient_id"] == patient_id
    assert data["doctor_id"] == doctor_id
    assert data["appointment_start"] == "2026-08-20T10:00:00"
    assert data["appointment_end"] == "2026-08-20T11:00:00"


def test_get_appointments(client):
    patient_id = create_patient(client)
    doctor_id = create_doctor(client)

    client.post(
        "/appointments/",
        json={
            "patient_id": patient_id,
            "doctor_id": doctor_id,
            "appointment_start": "2026-08-20T10:00:00",
            "appointment_end": "2026-08-20T11:00:00",
        },
    )

    response = client.get("/appointments/")

    assert response.status_code == 200
    assert len(response.json()) == 1


def test_get_appointment_by_id(client):
    patient_id = create_patient(client)
    doctor_id = create_doctor(client)

    create_response = client.post(
        "/appointments/",
        json={
            "patient_id": patient_id,
            "doctor_id": doctor_id,
            "appointment_start": "2026-08-20T10:00:00",
            "appointment_end": "2026-08-20T11:00:00",
        },
    )

    appointment_id = create_response.json()["id"]

    response = client.get(f"/appointments/{appointment_id}")

    assert response.status_code == 200
    assert response.json()["id"] == appointment_id


def test_get_missing_appointment(client):
    response = client.get("/appointments/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Appointment not found"


def test_reject_overlapping_appointment(client):
    patient_id = create_patient(client)
    doctor_id = create_doctor(client)

    first_response = client.post(
        "/appointments/",
        json={
            "patient_id": patient_id,
            "doctor_id": doctor_id,
            "appointment_start": "2026-08-20T10:00:00",
            "appointment_end": "2026-08-20T11:00:00",
        },
    )

    assert first_response.status_code == 201

    second_response = client.post(
        "/appointments/",
        json={
            "patient_id": patient_id,
            "doctor_id": doctor_id,
            "appointment_start": "2026-08-20T10:30:00",
            "appointment_end": "2026-08-20T11:30:00",
        },
    )

    assert second_response.status_code == 409
    assert second_response.json()["detail"] == (
        "Doctor already has an overlapping appointment"
    )


def test_adjacent_appointment_is_allowed(client):
    patient_id = create_patient(client)
    doctor_id = create_doctor(client)

    first_response = client.post(
        "/appointments/",
        json={
            "patient_id": patient_id,
            "doctor_id": doctor_id,
            "appointment_start": "2026-08-20T10:00:00",
            "appointment_end": "2026-08-20T11:00:00",
        },
    )

    assert first_response.status_code == 201

    second_response = client.post(
        "/appointments/",
        json={
            "patient_id": patient_id,
            "doctor_id": doctor_id,
            "appointment_start": "2026-08-20T11:00:00",
            "appointment_end": "2026-08-20T12:00:00",
        },
    )

    assert second_response.status_code == 201


def test_appointment_with_missing_patient(client):
    doctor_id = create_doctor(client)

    response = client.post(
        "/appointments/",
        json={
            "patient_id": 999,
            "doctor_id": doctor_id,
            "appointment_start": "2026-08-20T10:00:00",
            "appointment_end": "2026-08-20T11:00:00",
        },
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Patient not found"


def test_appointment_with_missing_doctor(client):
    patient_id = create_patient(client)

    response = client.post(
        "/appointments/",
        json={
            "patient_id": patient_id,
            "doctor_id": 999,
            "appointment_start": "2026-08-20T10:00:00",
            "appointment_end": "2026-08-20T11:00:00",
        },
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Doctor not found"


def test_invalid_appointment_time(client):
    patient_id = create_patient(client)
    doctor_id = create_doctor(client)

    response = client.post(
        "/appointments/",
        json={
            "patient_id": patient_id,
            "doctor_id": doctor_id,
            "appointment_start": "2026-08-20T11:00:00",
            "appointment_end": "2026-08-20T10:00:00",
        },
    )

    assert response.status_code == 422