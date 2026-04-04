"""Five easy scenarios focused on detecting issues."""

SCENARIOS = [
    {
        "columns": ["id", "email", "name"],
        "pii_detected": ["email"],
        "missing_values": [],
        "duplicates": False,
        "schema_valid": True,
        "bias_detected": False,
        "policy_rules": [],
    },
    {
        "columns": ["id", "phone", "name"],
        "pii_detected": ["phone"],
        "missing_values": [],
        "duplicates": False,
        "schema_valid": True,
        "bias_detected": False,
        "policy_rules": [],
    },
    {
        "columns": ["id", "email", "signup_date"],
        "pii_detected": ["email"],
        "missing_values": ["signup_date"],
        "duplicates": False,
        "schema_valid": True,
        "bias_detected": False,
        "policy_rules": [],
    },
    {
        "columns": ["id", "name"],
        "pii_detected": [],
        "missing_values": [],
        "duplicates": True,
        "schema_valid": True,
        "bias_detected": False,
        "policy_rules": [],
    },
    {
        "columns": ["id", "email", "phone", "age"],
        "pii_detected": ["email", "phone"],
        "missing_values": ["age"],
        "duplicates": False,
        "schema_valid": True,
        "bias_detected": True,
        "policy_rules": [],
    },
]
