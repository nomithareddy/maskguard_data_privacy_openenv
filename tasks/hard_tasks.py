"""Five hard scenarios requiring full dataset readiness."""

SCENARIOS = [
    {
        "columns": ["id", "email", "name", "dob"],
        "pii_detected": ["email"],
        "missing_values": ["dob"],
        "duplicates": True,
        "schema_valid": False,
        "bias_detected": True,
        "policy_rules": [],
    },
    {
        "columns": ["id", "phone", "address", "income"],
        "pii_detected": ["phone"],
        "missing_values": ["address", "income"],
        "duplicates": True,
        "schema_valid": False,
        "bias_detected": False,
        "policy_rules": [],
    },
    {
        "columns": ["id", "email", "signup_date", "country"],
        "pii_detected": ["email"],
        "missing_values": ["signup_date"],
        "duplicates": True,
        "schema_valid": False,
        "bias_detected": True,
        "policy_rules": [],
    },
    {
        "columns": ["id", "ssn", "name", "age"],
        "pii_detected": ["ssn"],
        "missing_values": [],
        "duplicates": True,
        "schema_valid": True,
        "bias_detected": True,
        "policy_rules": [],
    },
    {
        "columns": ["id", "email", "phone", "address", "dob"],
        "pii_detected": ["email", "phone"],
        "missing_values": ["dob"],
        "duplicates": True,
        "schema_valid": False,
        "bias_detected": True,
        "policy_rules": [],
    },
]
