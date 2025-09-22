import pytest
from fastapi.testclient import TestClient
from main import api, tickets   # import app + in-memory list

client = TestClient(api)

@pytest.fixture(autouse=True)
def clear_tickets():
    """Clear tickets before each test to avoid data leaking between tests."""
    tickets.clear()


def test_index():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Message": "Welcome to the Ticket Booking System"}


def test_add_ticket():
    ticket_data = {
        "id": 1,
        "flight_name": "AirAsia",
        "flight_date": "2025-10-15",
        "flight_time": "14:30",
        "destination": "Bangkok"
    }
    response = client.post("/ticket", json=ticket_data)
    assert response.status_code == 200
    assert response.json() == ticket_data


def test_get_tickets():
    # Add one ticket first
    client.post("/ticket", json={
        "id": 1,
        "flight_name": "AirAsia",
        "flight_date": "2025-10-15",
        "flight_time": "14:30",
        "destination": "Bangkok"
    })
    response = client.get("/ticket")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["id"] == 1


def test_update_ticket():
    # Add ticket
    client.post("/ticket", json={
        "id": 1,
        "flight_name": "AirAsia",
        "flight_date": "2025-10-15",
        "flight_time": "14:30",
        "destination": "Bangkok"
    })
    # Update ticket
    updated_ticket = {
        "id": 1,
        "flight_name": "Thai Airways",
        "flight_date": "2025-10-20",
        "flight_time": "18:00",
        "destination": "Phuket"
    }
    response = client.put("/ticket/1", json=updated_ticket)
    assert response.status_code == 200
    assert response.json() == updated_ticket


def test_delete_ticket():
    # Add ticket
    client.post("/ticket", json={
        "id": 1,
        "flight_name": "AirAsia",
        "flight_date": "2025-10-15",
        "flight_time": "14:30",
        "destination": "Bangkok"
    })
    # Delete ticket
    response = client.delete("/ticket/1")
    assert response.status_code == 200
    deleted_ticket = response.json()
    assert deleted_ticket["id"] == 1


def test_delete_nonexistent_ticket():
    response = client.delete("/ticket/99")
    assert response.status_code == 200
    assert response.json() == {"error": "Ticket not found, deletion failed"}
