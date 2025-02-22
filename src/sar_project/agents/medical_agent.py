from sar_project.agents.base_agent import SARBaseAgent

class MedicalTeamLeader(SARBaseAgent):

    def __init__(self):
        super().__init__(
            name="Medical_Team_Leader",
            role="Medical Team Leader",
            system_message="""You are the Medical Team Leader for SAR operations. Your role is to:
            1. Triage and treat injuries
            2. Coordinate patient transport
            3. Manage medical supplies
            4. Provide medical care to injured personnel
            5. Manage medical resources and coordinate with local hospitals if needed"""
        )
        self.patient_records = {}

    inventory_database = {
        "bandages": 100,
        "antiseptic": 50,
        "painkillers": 75
    }

    reorder_thresholds = {
        "bandages": 80,
        "antiseptic": 40,
        "painkillers": 50
    }
    
    health_data = {
        "average_stress_level": "moderate",
        "high_risk_members": 2,
        "recommendations": ["mandatory rest for high-risk members", "team debriefing session"]
    }

    def process_request(self, message):
        """Process medical-related requests"""
        try:
            if "triage_request" in message:
                return self.handle_triage(message["patients"])
            elif "transport_request" in message:
                return self.organize_transport(
                    message["patient_id"], 
                    message["destination"], 
                    message["urgency"]
                )
            elif "supply_request" in message:
                return self.manage_supplies(message["item"], message["quantity"])
            elif "health_monitoring_request" in message:
                return self.monitor_team_health()
            elif "field_adaptation_request" in message:
                return self.adapt_to_field_conditions(message["conditions"])
            else:
                return {"error": "Unknown request type"}
        except Exception as e:
            return {"error": str(e)}


    def handle_triage(self, patients):
        """Handle triage of incoming patients by sorting them from high to low severity and within the same severity by time of arrival."""
        severity_to_priority = {"high": 1, "medium": 2, "low": 3}
        # sorting patients by severity and then arrival time, if severities are the same
        sorted_patients = sorted(patients, key=lambda x: (severity_to_priority[x["severity"]], x["arrival_time"]))
        triaged_data = {patient["id"]: i+1 for i, patient in enumerate(sorted_patients)}
        return triaged_data

    def organize_transport(self, patient_id, destination, urgency):
        """Organize transport for a patient based on their condition and urgency.
        
        Args:
            patient_id (str): The identifier for the patient.
            destination (str): The destination hospital or medical facility.
            urgency (str): The urgency level ('high', 'medium', 'low') which affects transport choice.

        Returns:
            dict: A dictionary containing the transport status and details.
        """
        transport_options = {
            'high': 'helicopter',
            'medium': 'ambulance',
            'low': 'non-emergency vehicle'
        }

        if urgency in transport_options:
            transport_type = transport_options[urgency]
            if self.check_transport_availability(transport_type):
                return {
                    "patient_id": patient_id,
                    "transport_status": "organized",
                    "transport_type": transport_type,
                    "destination": destination
                }
            else:
                return {
                    "patient_id": patient_id,
                    "transport_status": "unavailable",
                    "error": f"{transport_type} is not available currently"
                }
        else:
            return {
                "patient_id": patient_id,
                "transport_status": "error",
                "error": "Invalid urgency level specified"
            }

    def check_transport_availability(self, transport_type):
        """Check the availability of a transport type.
        
        Args:
            transport_type (str): The type of transport to check.

        Returns:
            bool: True if the transport is available, False otherwise.
        """
        # Placeholder for actual availability check logic
        # In a real scenario we could query a database or a schedule system
        # Here, we'll assume all transport types are always available
        return True

    
    def manage_supplies(self, item, quantity):
        """Manage medical supplies by updating inventory and reordering if necessary."""
        current_inventory = self.check_inventory(item)
        new_inventory = current_inventory + quantity
        self.update_inventory(item, new_inventory)

        # Check if the inventory level is below the reorder threshold
        reorder_threshold = self.get_reorder_threshold(item)
        if new_inventory < reorder_threshold:
            self.reorder_supplies(item, reorder_threshold - new_inventory)
            reorder_status = "reorder placed"
        else:
            reorder_status = "no reorder needed"

        return {
            "item": item,
            "updated_quantity": new_inventory,
            "status": "updated",
            "reorder_status": reorder_status
        }

    def check_inventory(self, item):
        """Check the current inventory level for a specific item."""
        return self.inventory_database.get(item, 0)

    def update_inventory(self, item, new_quantity):
        """Update the inventory with the new quantity for a specific item."""
        self.inventory_database[item] = new_quantity
        print(f"Inventory updated for {item}: {new_quantity} units")

    def get_reorder_threshold(self, item):
        """Retrieve the reorder threshold for a specific item."""
        return self.reorder_thresholds.get(item, 10)

    def reorder_supplies(self, item, quantity_needed):
        """Place an order for supplies that are below the reorder threshold."""
        # Placeholder, for now 
        # Can be replaced with an order and payment system for getting new supplies
        print(f"Reorder placed for {item}: {quantity_needed} units")

    def monitor_team_health(self):
        """Monitor and report on the health and stress levels of the SAR team."""
        return self.health_data

    def update_team_health(self, average_stress_level=None, high_risk_members=None, recommendations=None):
        """Update the health and stress levels of the SAR team based on new data."""
        if average_stress_level is not None:
            self.health_data['average_stress_level'] = average_stress_level
        if high_risk_members is not None:
            self.health_data['high_risk_members'] = high_risk_members
        if recommendations is not None:
            self.health_data['recommendations'] = recommendations

        return {"status": "Team health updated", "new_health_data": self.health_data}

    def adapt_to_field_conditions(self, conditions):
        """Adapt the search and rescue operations based on real-time field conditions.
        
        Args:
            conditions (dict): Current environmental and operational conditions.
            
        Returns:
            dict: Adjusted operation plans based on the conditions.
        """
        if conditions.get("weather", "") == "stormy":
            operational_adjustments = "Limit aerial operations, increase ground unit readiness"
        elif conditions.get("terrain", "") == "mountainous":
            operational_adjustments = "Deploy mountain rescue teams, use specialized gear"
        else:
            operational_adjustments = "Standard operations"

        return {
            "conditions_assessed": conditions,
            "adjustments": operational_adjustments
        }

    def update_status(self, status):
        """Update the agent's status"""
        self.status = status
        return {"status": "updated", "new_status": status}

    def get_status(self):
        """Get the agent's current status"""
        return getattr(self, "status", "unknown")
