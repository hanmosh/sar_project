import pytest
from datetime import datetime
from sar_project.agents.medical_agent import MedicalTeamLeader

class TestMedicalTeamLeader:
    @pytest.fixture
    def agent(self):
        return MedicalTeamLeader()

    @pytest.fixture
    def sample_patient(self):
        return {
            "id": "test_patient",
            "name": "John Doe",
            "age": 45,
            "condition": "Fractured leg",
            "severity": "medium"
        }

    def test_initialization(self, agent):
        assert agent.name == "Medical_Team_Leader"
        assert agent.role == "Medical Team Leader"
        assert isinstance(agent.patient_records, dict)
        assert len(agent.patient_records) == 0

    def test_process_request_triage(self, agent):
        message = {
            "triage_request": True,
            "patients": [
                {"id": "patient1", "severity": "high", "arrival_time": 1},
                {"id": "patient2", "severity": "high", "arrival_time": 2},
                {"id": "patient3", "severity": "low", "arrival_time": 3}
            ]
        }
        response = agent.handle_triage(message['patients'])
        assert isinstance(response, dict)
        assert set(response.keys()) == {"patient1", "patient2", "patient3"}
        assert response["patient1"] == 1 
        assert response["patient2"] == 2 
        assert response["patient3"] == 3 
        
        # Check that patient records were created during triage
        assert len(agent.patient_records) == 3
        assert "patient1" in agent.patient_records
        assert agent.patient_records["patient1"]["severity"] == "high"
        assert agent.patient_records["patient1"]["status"] == "triaged"

    def test_process_request_transport(self, agent):
        agent.add_patient({
            "id": "patient1",
            "severity": "high",
            "status": "triaged"
        })
        
        message = {
            "transport_request": True,
            "patient_id": "patient1",
            "destination": "Hospital A",
            "urgency": "high"
        }
        response = agent.process_request(message)
        assert "transport_status" in response
        assert response["transport_status"] == "organized"
        assert response["transport_type"] == "helicopter"
        
        # Check that patient record was updated with transport info
        assert agent.patient_records["patient1"]["status"] == "in transit"
        assert agent.patient_records["patient1"]["destination"] == "Hospital A"
        assert "transport_time" in agent.patient_records["patient1"]

    def test_process_request_supply_management(self, agent):
        message = {
            "supply_request": True,
            "item": "bandages",
            "quantity": 20
        }
        response = agent.process_request(message)
        assert "status" in response
        assert response["status"] == "updated"
        assert "reorder_status" in response

    def test_status_update(self, agent):
        response = agent.update_status("active")
        assert response["new_status"] == "active"
        assert agent.get_status() == "active"

    def test_inventory_check(self, agent):
        current_inventory = agent.check_inventory("bandages")
        assert isinstance(current_inventory, int)
        assert current_inventory == 120  # previous test adjusts inventory to 120

    def test_inventory_update(self, agent):
        agent.update_inventory("antiseptic", 40)
        current_inventory = agent.check_inventory("antiseptic")
        assert current_inventory == 40  

    def test_update_team_health(self, agent):
        # Update the stress level and number of high-risk members
        update_response = agent.update_team_health("high", 5, ["increase surveillance"])
        assert update_response["new_health_data"]["average_stress_level"] == "high"
        assert update_response["new_health_data"]["high_risk_members"] == 5
        assert "increase surveillance" in update_response["new_health_data"]["recommendations"]

        # Check if updates are reflected in monitoring
        current_health = agent.monitor_team_health()
        assert current_health["average_stress_level"] == "high"
        assert current_health["high_risk_members"] == 5
        assert "increase surveillance" in current_health["recommendations"]
    
    def test_adapt_to_stormy_weather(self, agent):
        conditions = {"weather": "stormy", "terrain": "flat"}
        response = agent.adapt_to_field_conditions(conditions)
        assert response["adjustments"] == "Limit aerial operations, increase ground unit readiness"
        assert response["conditions_assessed"] == conditions

    def test_adapt_to_mountainous_terrain(self, agent):
        conditions = {"weather": "clear", "terrain": "mountainous"}
        response = agent.adapt_to_field_conditions(conditions)
        assert response["adjustments"] == "Deploy mountain rescue teams, use specialized gear"
        assert response["conditions_assessed"] == conditions

    def test_adapt_to_standard_operations(self, agent):
        conditions = {"weather": "clear", "terrain": "flat"}
        response = agent.adapt_to_field_conditions(conditions)
        assert response["adjustments"] == "Standard operations"
        assert response["conditions_assessed"] == conditions
        
    # New tests for patient record functionality
    
    def test_add_patient(self, agent, sample_patient):
        response = agent.add_patient(sample_patient)
        assert response["status"] == "success"
        assert response["patient_id"] == "test_patient"
        assert "test_patient" in agent.patient_records
        assert agent.patient_records["test_patient"]["name"] == "John Doe"
        assert "registration_time" in agent.patient_records["test_patient"]
        assert agent.patient_records["test_patient"]["status"] == "registered"
        
    def test_add_duplicate_patient(self, agent, sample_patient):
        agent.add_patient(sample_patient)
        response = agent.add_patient(sample_patient)
        assert "error" in response
        assert response["error"] == "Patient already exists"
        
    def test_update_patient_record(self, agent, sample_patient):
        agent.add_patient(sample_patient)
        update_data = {
            "severity": "high",
            "notes": "Condition worsening"
        }
        response = agent.update_patient_record("test_patient", update_data)
        assert response["status"] == "success"
        assert agent.patient_records["test_patient"]["severity"] == "high"
        assert agent.patient_records["test_patient"]["notes"] == "Condition worsening"
        assert "last_updated" in agent.patient_records["test_patient"]
        
    def test_update_nonexistent_patient(self, agent):
        response = agent.update_patient_record("nonexistent", {"severity": "high"})
        assert "error" in response
        assert response["error"] == "Patient not found"
        
    def test_get_patient_record(self, agent, sample_patient):
        agent.add_patient(sample_patient)
        response = agent.get_patient_record("test_patient")
        assert response["status"] == "success"
        assert response["patient_id"] == "test_patient"
        assert response["patient_data"]["name"] == "John Doe"
        
    def test_get_nonexistent_patient(self, agent):
        response = agent.get_patient_record("nonexistent")
        assert "error" in response
        assert response["error"] == "Patient not found"
        
    def test_list_patients(self, agent):
        agent.add_patient({"id": "patient1", "severity": "high", "status": "triaged"})
        agent.add_patient({"id": "patient2", "severity": "medium", "status": "triaged"})
        agent.add_patient({"id": "patient3", "severity": "low", "status": "discharged"})
        
        response = agent.list_patients()
        assert response["status"] == "success"
        assert response["count"] == 3
        assert len(response["patients"]) == 3
        
        response = agent.list_patients("triaged")
        assert response["status"] == "success"
        assert response["count"] == 2
        assert len(response["patients"]) == 2
        
        response = agent.list_patients("discharged")
        assert response["status"] == "success"
        assert response["count"] == 1
        assert len(response["patients"]) == 1
        assert response["patients"][0]["id"] == "patient3"
        
    def test_discharge_patient(self, agent, sample_patient):
        agent.add_patient(sample_patient)
        response = agent.discharge_patient("test_patient", "Patient recovered fully")
        assert response["status"] == "success"
        assert agent.patient_records["test_patient"]["status"] == "discharged"
        assert agent.patient_records["test_patient"]["discharge_notes"] == "Patient recovered fully"
        assert "discharge_time" in agent.patient_records["test_patient"]
        
    def test_discharge_nonexistent_patient(self, agent):
        response = agent.discharge_patient("nonexistent")
        assert "error" in response
        assert response["error"] == "Patient not found"
        
    def test_process_request_patient_operations(self, agent, sample_patient):
        add_request = {
            "add_patient_request": True,
            "patient_data": sample_patient
        }
        response = agent.process_request(add_request)
        assert response["status"] == "success"
        
        update_request = {
            "update_patient_request": True,
            "patient_id": "test_patient",
            "update_data": {"severity": "high"}
        }
        response = agent.process_request(update_request)
        assert response["status"] == "success"
        
        get_request = {
            "get_patient_request": True,
            "patient_id": "test_patient"
        }
        response = agent.process_request(get_request)
        assert response["status"] == "success"
        
        list_request = {
            "list_patients_request": True
        }
        response = agent.process_request(list_request)
        assert response["status"] == "success"
        
        discharge_request = {
            "discharge_patient_request": True,
            "patient_id": "test_patient",
            "discharge_notes": "Fully recovered"
        }
        response = agent.process_request(discharge_request)
        assert response["status"] == "success"