import pytest
from sar_project.agents.medical_agent import MedicalTeamLeader

class TestMedicalTeamLeader:
    @pytest.fixture
    def agent(self):
        return MedicalTeamLeader()

    def test_initialization(self, agent):
        assert agent.name == "Medical_Team_Leader"
        assert agent.role == "Medical Team Leader"

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


    def test_process_request_transport(self, agent):
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
        assert current_inventory == 120  

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