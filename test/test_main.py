from fastapi.testclient import TestClient
from src.main import api, tickets

client = TestClient(api)

def test_index():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Message": "Welcome to the Ticket Booking System"}

def test_add_ticket():
    new_ticket = {
        "id": 1,
        "flight_name": "Air Bangladesh",
        "flight_date": "2025-10-15",
        "flight_time": "14:30",
        "destination": "Dhaka"
    }
    response = client.post("/ticket", json=new_ticket)
    assert response.status_code == 200
    assert response.json() == new_ticket

def test_get_tickets():
    response = client.get("/ticket")
    assert response.status_code == 200
    assert len(response.json()) > 0  # at least 1 ticket added

def test_update_ticket():
    updated_ticket = {
        "id": 1,
        "flight_name": "Air Bangladesh",
        "flight_date": "2025-10-16",
        "flight_time": "16:00",
        "destination": "Chittagong"
    }
    response = client.put("/ticket/1", json=updated_ticket)
    assert response.status_code == 200
    assert response.json()["destination"] == "Chittagong"

def test_delete_ticket():
    response = client.delete("/ticket/1")
    assert response.status_code == 200
    assert response.json()["id"] == 1

    # Try deleting again → should fail
    response = client.delete("/ticket/1")
    assert response.status_code == 200
    assert response.json()["error"] == "Ticket not found, deletion failed"
