from sar_project.agents.base_agent import SARBaseAgent
from datetime import datetime

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
            elif "add_patient_request" in message:
                return self.add_patient(message["patient_data"])
            elif "update_patient_request" in message:
                return self.update_patient_record(
                    message["patient_id"],
                    message["update_data"]
                )
            elif "get_patient_request" in message:
                return self.get_patient_record(message["patient_id"])
            elif "list_patients_request" in message:
                return self.list_patients(message.get("status", None))
            elif "discharge_patient_request" in message:
                return self.discharge_patient(
                    message["patient_id"],
                    message.get("discharge_notes", "")
                )
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
        
        for patient in patients:
            if patient["id"] not in self.patient_records:
                self.add_patient({
                    "id": patient["id"],
                    "severity": patient["severity"],
                    "arrival_time": patient["arrival_time"],
                    "triage_time": datetime.now().isoformat(),
                    "status": "triaged"
                })
            else:
                self.update_patient_record(
                    patient["id"],
                    {
                        "severity": patient["severity"],
                        "triage_time": datetime.now().isoformat(),
                        "status": "triaged"
                    }
                )
                
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
                # Update patient record with transport information
                if patient_id in self.patient_records:
                    self.update_patient_record(
                        patient_id,
                        {
                            "transport_type": transport_type,
                            "destination": destination,
                            "transport_time": datetime.now().isoformat(),
                            "status": "in transit"
                        }
                    )
                
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
            
    def add_patient(self, patient_data):
        """Add a new patient to the records.
        
        Args:
            patient_data (dict): Patient information including id, condition, etc.
            
        Returns:
            dict: Status of the operation and patient ID
        """
        if "id" not in patient_data:
            return {"error": "Patient ID is required"}
            
        patient_id = patient_data["id"]
        
        if "status" not in patient_data:
            patient_data["status"] = "registered"
        if "registration_time" not in patient_data:
            patient_data["registration_time"] = datetime.now().isoformat()
            
        if patient_id in self.patient_records:
            return {"error": "Patient already exists", "patient_id": patient_id}
            
        self.patient_records[patient_id] = patient_data
        return {"status": "success", "message": "Patient added", "patient_id": patient_id}
        
    def update_patient_record(self, patient_id, update_data):
        """Update an existing patient record with new information.
        
        Args:
            patient_id (str): The identifier for the patient
            update_data (dict): New data to update the patient record
            
        Returns:
            dict: Status of the operation and updated patient data
        """
        if patient_id not in self.patient_records:
            return {"error": "Patient not found", "patient_id": patient_id}
            
        self.patient_records[patient_id].update(update_data)
        
        self.patient_records[patient_id]["last_updated"] = datetime.now().isoformat()
        
        return {
            "status": "success", 
            "message": "Patient record updated", 
            "patient_id": patient_id,
            "patient_data": self.patient_records[patient_id]
        }
        
    def get_patient_record(self, patient_id):
        """Retrieve a patient's medical record.
        
        Args:
            patient_id (str): The identifier for the patient
            
        Returns:
            dict: Patient data or error message
        """
        if patient_id not in self.patient_records:
            return {"error": "Patient not found", "patient_id": patient_id}
            
        return {
            "status": "success",
            "patient_id": patient_id,
            "patient_data": self.patient_records[patient_id]
        }
        
    def list_patients(self, status=None):
        """List all patients, optionally filtered by status.
        
        Args:
            status (str, optional): Filter patients by this status
            
        Returns:
            dict: List of patient IDs and their basic information
        """
        if status:
            filtered_patients = {
                pid: data for pid, data in self.patient_records.items() 
                if data.get("status") == status
            }
        else:
            filtered_patients = self.patient_records
            
        patient_list = [
            {
                "id": pid,
                "status": data.get("status", "unknown"),
                "severity": data.get("severity", "unknown"),
                "registration_time": data.get("registration_time", "unknown")
            }
            for pid, data in filtered_patients.items()
        ]
        
        return {
            "status": "success",
            "count": len(patient_list),
            "patients": patient_list
        }
        
    def discharge_patient(self, patient_id, discharge_notes=""):
        """Discharge a patient from medical care.
        
        Args:
            patient_id (str): The identifier for the patient
            discharge_notes (str, optional): Notes regarding the discharge
            
        Returns:
            dict: Status of the operation
        """
        if patient_id not in self.patient_records:
            return {"error": "Patient not found", "patient_id": patient_id}
            
        self.patient_records[patient_id].update({
            "status": "discharged",
            "discharge_time": datetime.now().isoformat(),
            "discharge_notes": discharge_notes
        })
        
        return {
            "status": "success",
            "message": "Patient discharged",
            "patient_id": patient_id
        }