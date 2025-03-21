# Search and Rescue (SAR) Agent Framework - CSC 581

## Functionality of the Medical Team Leader
- Manages medical roles and supplies
- Handles patient triage and transport
- Monitors and updates team health
- Adapts to field conditions
- Updates and retrieves agent status

## Description of functions

- **process_request(message)**: Handles requests based on type ('triage_request', 'transport_request', 'supply_request', 'health_monitoring_request', 'field_adaptation_request'). Returns various outputs depending on the request type.
  
- **handle_triage(patients)**: Sorts patients based on severity and arrival time for triage purposes. Input is a list of patient dictionaries; returns a dictionary mapping patient IDs to triage priority.

- **organize_transport(patient_id, destination, urgency)**: Organizes transport for patients based on urgency (high, medium, low), affecting the choice of transport (helicopter, ambulance, non-emergency vehicle). Returns transport details including status and type.

- **check_transport_availability(transport_type)**: Checks the availability of specified transport types. Returns a boolean.

- **manage_supplies(item, quantity)**: Manages inventory by updating quantities and reordering if necessary, based on reorder thresholds. Returns an updated status of the inventory and reorder action.

- **check_inventory(item)**: Returns the current inventory level for a specified item.

- **update_inventory(item, new_quantity)**: Updates the inventory with a new quantity for a specific item.

- **get_reorder_threshold(item)**: Retrieves the reorder threshold for a specific item.

- **reorder_supplies(item, quantity_needed)**: Places an order for supplies that are below the reorder threshold.

- **monitor_team_health()**: Reports on the health and stress levels of the SAR team based on current data. Returns health data including stress levels and recommendations.

- **update_team_health(average_stress_level, high_risk_members, recommendations)**: Updates the health data of the SAR team. Accepts new values for stress level, high-risk members, and health recommendations.

- **adapt_to_field_conditions(conditions)**: Adapts operations based on real-time field conditions like weather and terrain. Returns the adjustments made to operations.

- **update_status(status)**: Updates the agent's status.

- **get_status()**: Returns the agent's current status.

*new functions in modifications section*

## Examples of how to use

Create an instance of the MedicalTeamLeader
```
from medical_agent import MedicalTeamLeader
mtl = MedicalTeamLeader()
```

Triage patients
```
triage_result = mtl.process_request({
    "triage_request": True,
    "patients": [
        {"id": "001", "severity": "high", "arrival_time": 1},
        {"id": "002", "severity": "medium", "arrival_time": 2}
    ]
})
```

Organize transport for a patient
```
transport_result = mtl.process_request({
    "transport_request": True,
    "patient_id": "001",
    "destination": "Local Hospital",
    "urgency": "high"
})
```

Manage medical supplies and reorder if necessary
```
supply_result = mtl.process_request({
    "supply_request": True,
    "item": "bandages",
    "quantity": -5  # Reduce inventory by 5
})
```

Update the health data of the team
```
health_update_result = mtl.update_team_health("low", 1, ["regular check-ups recommended"])
```

Adapt operations to stormy weather conditions
```
adaptation_result = mtl.adapt_to_field_conditions({
    "weather": "stormy",
    "terrain": "flat"
})
```
## Modifications 

### New suggested patient record functionality: 
- **add_patient(patient_data)**: Adds a new patient to the record with specified info and returns status and patient ID
- **update_patient_record(patient_id, update_data)**: updates the existing patient record with new info, returns status and updated data
- **get_patient_record(patient_id)**: retrieves a patient's complete medical record and returns patient data or an error
- **list_patients(status)**: lists all patients, can be filtered by status. Returns a list of patient IDs + basic info
- **discharge_patient(patient_id, discharge_notes)**: marks a patient as discharged with notes and a timestamp, and returns operation status

## Insights Gained
Something I learned was the importance of good documentation and effectively sharing your code with others. It is important to not only write code that is easy to use but also code that is easy to follow. Through developing this SAR framework, I gained appreciation for how complex real-world emergency systems can be - even with just patient care there are countless moving parts to coordinate: resource management, personnel tracking, and field adaptations, to name a few. This project helped me see that writing clean, well-organized code with thorough documentation is a practical necessity when building these systems. I got good feedback on my documentation, so I will make sure to keep that up and continue making my code accessible and understandable to others, especially in domains like SAR, where many different specialists need to work together.

