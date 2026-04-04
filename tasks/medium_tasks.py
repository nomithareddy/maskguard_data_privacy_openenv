"""Five medium scenarios focused on fixing issues."""

SCENARIOS = [
    {
        "columns": ["id", "email", "name"],
        "pii_detected": ["email"],
        "missing_values": ["name"],
        "duplicates": True,
        "schema_valid": False,
        "bias_detected": False,
        "policy_rules": [],
    },
    {
        "columns": ["id", "phone", "address"],
        "pii_detected": ["phone"],
        "missing_values": ["address"],
        "duplicates": True,
        "schema_valid": True,
        "bias_detected": False,
        "policy_rules": [],
    },
    {
        "columns": ["id", "email", "signup_date"],
        "pii_detected": ["email"],
        "missing_values": ["signup_date"],
        "duplicates": False,
        "schema_valid": False,
        "bias_detected": True,
        "policy_rules": [],
    },
    {
        "columns": ["id", "name", "age"],
        "pii_detected": [],
        "missing_values": ["age"],
        "duplicates": True,
        "schema_valid": True,
        "bias_detected": False,
        "policy_rules": [],
    },
    {
        "columns": ["id", "email", "phone", "country"],
        "pii_detected": ["email", "phone"],
        "missing_values": [],
        "duplicates": True,
        "schema_valid": False,
        "bias_detected": True,
        "policy_rules": [],
    },
]
