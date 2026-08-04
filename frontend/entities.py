

ENUMS = {
    "rule_type": ["VISA", "PASSPORT", "TRAVEL_AUTHORIZATION", "TRANSIT", "HEALTH", "CUSTOMS", "IMMIGRATION", "ENTRY_RESTRICTION"],
    "decision": ["ALLOWED", "CONDITIONAL", "NOT_ALLOWED"],
    "subscription_plan": ["STANDARD", "PREMIUM", "ENTERPRISE"],
    "http_method": ["GET", "POST", "PUT", "DELETE"],
    "audit_action": ["INSERT", "UPDATE", "DELETE"],
    "approval_status": ["APPROVED", "REJECTED"],
    "change_type": ["CREATE", "UPDATE", "DELETE", "PUBLISH", "EXPIRE"],
    "simulation_status": ["PASSED", "FAILED", "ERROR"],
    "source_type": ["API", "WEBSITE", "PDF", "EMAIL"],
    "document_type": ["PDF", "HTML", "API_RESPONSE"],
    "collection_type": ["MANUAL", "API", "CRAWLER"],
    "collection_status": ["SUCCESS", "FAILED"],
    "validation_status": ["PENDING", "APPROVED", "REJECTED"],
    "extraction_status": ["SUCCESS", "FAILED"],
    "update_frequency": ["DAILY", "WEEKLY", "MONTHLY", "ON_DEMAND"],
}


def f(name, type_, required=False, enum=None, help=None, default=None):
    return {"name": name, "type": type_, "required": required, "enum": enum, "help": help, "default": default}


FULL = {"create", "read", "update", "delete"}
CR = {"create", "read"}          # create + read only (log/audit style entities)
CRU = {"create", "read", "update"}

ENTITIES = {
    # ---------------- REFERENCE ----------------
    "Countries": {
        "endpoint": "/countries", "category": "Reference", "ops": FULL,
        "fields": [
            f("iso2", "str", True, help="ISO 3166-1 alpha-2 code, e.g. US"),
            f("iso3", "str", True, help="ISO 3166-1 alpha-3 code, e.g. USA"),
            f("country_name", "str", True),
            f("nationality", "str", True),
            f("region_id", "int", True),
            f("capital", "str"),
            f("currency_id", "int", True),
            f("official_language", "str"),
            f("timezone", "str"),
        ],
    },
    "Regions": {
        "endpoint": "/regions", "category": "Reference", "ops": FULL,
        "fields": [f("region_name", "str", True), f("description", "text")],
    },
    "Currencies": {
        "endpoint": "/currencies", "category": "Reference", "ops": FULL,
        "fields": [
            f("currency_code", "str", True, help="ISO 4217 code, e.g. USD"),
            f("currency_name", "str", True),
            f("currency_symbol", "str"),
        ],
    },
    "Passport Types": {
        "endpoint": "/passport-types", "category": "Reference", "ops": FULL,
        "fields": [f("passport_code", "str", True), f("passport_name", "str", True), f("description", "text")],
    },
    "Visa Types": {
        "endpoint": "/visa-types", "category": "Reference", "ops": FULL,
        "fields": [f("visa_code", "str", True), f("visa_name", "str", True), f("description", "text")],
    },
    "Airlines": {
        "endpoint": "/airlines", "category": "Reference", "ops": FULL,
        "fields": [
            f("airline_name", "str", True),
            f("iata_code", "str", help="2 characters"),
            f("icao_code", "str", help="3 characters"),
            f("country_id", "int", True),
        ],
    },
    "Airports": {
        "endpoint": "/airports", "category": "Reference", "ops": FULL,
        "fields": [
            f("airport_name", "str", True),
            f("iata_code", "str", help="3 characters"),
            f("icao_code", "str", help="4 characters"),
            f("city", "str", True),
            f("country_id", "int", True),
            f("timezone", "str"),
            f("international", "bool", default=True),
        ],
    },
    "Purposes": {
        "endpoint": "/purposes", "category": "Reference", "ops": FULL,
        "fields": [f("purpose_code", "str", True), f("purpose_name", "str", True), f("description", "text")],
    },
    "Passenger Types": {
        "endpoint": "/passenger-types/", "category": "Reference", "ops": FULL,
        "fields": [f("passenger_type_code", "str", True), f("passenger_type_name", "str", True), f("description", "text")],
    },
    "Travel Authorizations": {
        "endpoint": "/travel-authorizations/", "category": "Reference", "ops": FULL,
        "fields": [
            f("authorization_code", "str", True),
            f("authorization_name", "str", True),
            f("destination_country_id", "int", True),
            f("description", "text"),
        ],
    },

    # ---------------- COMPLIANCE ----------------
    "Rules": {
        "endpoint": "/rules", "category": "Compliance", "ops": FULL,
        "fields": [
            f("rule_code", "str", True),
            f("rule_type", "enum", True, enum="rule_type"),
            f("source_id", "int", True),
            f("status_id", "int", True),
            f("priority", "int", default=3),
            f("created_by", "int"),
            f("updated_by", "int"),
        ],
    },
    "Visa Rules": {
        "endpoint": "/visa-rules", "category": "Compliance", "ops": FULL,
        "fields": [
            f("rule_id", "int", True), f("nationality_country_id", "int", True),
            f("destination_country_id", "int", True), f("passport_type_id", "int", True),
            f("visa_type_id", "int", True), f("purpose_id", "int", True),
            f("visa_required", "bool"), f("visa_on_arrival", "bool"), f("evisa_available", "bool"),
            f("max_stay_days", "int"), f("multiple_entry", "bool"),
            f("condition_expression", "json"), f("exemption_expression", "json"), f("remarks", "text"),
        ],
    },
    "Passport Rules": {
        "endpoint": "/passport-rules", "category": "Compliance", "ops": FULL,
        "fields": [
            f("rule_id", "int", True), f("destination_country_id", "int", True), f("passport_type_id", "int", True),
            f("minimum_validity_months", "int"), f("blank_pages_required", "int"),
            f("machine_readable_required", "bool"), f("damaged_passport_allowed", "bool"),
            f("temporary_passport_allowed", "bool"), f("passport_issue_date_required", "bool"),
            f("condition_expression", "json"), f("exemption_expression", "json"), f("remarks", "text"),
        ],
    },
    "Travel Authorization Rules": {
        "endpoint": "/travel-authorization-rules", "category": "Compliance", "ops": FULL,
        "fields": [
            f("rule_id", "int", True), f("authorization_id", "int", True),
            f("nationality_country_id", "int", True), f("destination_country_id", "int", True),
            f("passport_type_id", "int", True), f("purpose_id", "int", True),
            f("authorization_required", "bool"), f("validity_days", "int"),
            f("condition_expression", "json"), f("exemption_expression", "json"), f("remarks", "text"),
        ],
    },
    "Transit Rules": {
        "endpoint": "/transit-rules", "category": "Compliance", "ops": FULL,
        "fields": [
            f("rule_id", "int", True), f("nationality_country_id", "int", True),
            f("transit_country_id", "int", True), f("transit_airport_id", "int", True),
            f("transit_visa_required", "bool"), f("airside_transit_allowed", "bool"),
            f("baggage_collection_required", "bool"), f("overnight_transit_allowed", "bool"),
            f("max_transit_hours", "int"),
            f("condition_expression", "json"), f("exemption_expression", "json"), f("remarks", "text"),
        ],
    },
    "Health Rules": {
        "endpoint": "/health-rules", "category": "Compliance", "ops": FULL,
        "fields": [
            f("rule_id", "int", True), f("destination_country_id", "int", True), f("nationality_country_id", "int", True),
            f("health_form_required", "bool"), f("quarantine_required", "bool"), f("quarantine_days", "int"),
            f("medical_certificate_required", "bool"),
            f("condition_expression", "json"), f("exemption_expression", "json"), f("remarks", "text"),
        ],
    },
    "Vaccines": {
        "endpoint": "/vaccines", "category": "Compliance", "ops": FULL,
        "fields": [f("vaccine_name", "str", True), f("disease", "str", True)],
    },
    "Health Rule Vaccines": {
        "endpoint": "/health-rule-vaccines", "category": "Compliance", "ops": FULL,
        "fields": [
            f("health_rule_id", "int", True), f("vaccine_id", "int", True),
            f("certificate_required", "bool"), f("created_by", "int", True), f("updated_by", "int", True),
        ],
    },
    "Immigration Rules": {
        "endpoint": "/immigration-rules", "category": "Compliance", "ops": FULL,
        "fields": [
            f("rule_id", "int", True), f("destination_country_id", "int", True),
            f("onward_ticket_required", "bool"), f("accommodation_proof_required", "bool"),
            f("proof_of_funds_required", "bool"), f("biometric_required", "bool"),
            f("interview_required", "bool"), f("arrival_card_required", "bool"),
            f("digital_arrival_card", "bool"), f("arrival_registration_required", "bool"),
            f("condition_expression", "json"), f("exemption_expression", "json"), f("remarks", "text"),
            f("created_by", "int", True), f("updated_by", "int", True),
        ],
    },
    "Customs Rules": {
        "endpoint": "/customs-rules", "category": "Compliance", "ops": FULL,
        "fields": [
            f("rule_id", "int", True), f("destination_country_id", "int", True), f("nationality_country_id", "int", True),
            f("alcohol_limit", "str"), f("tobacco_limit", "str"),
            f("currency_limit_amount", "decimal"), f("currency_id", "int"),
            f("currency_declaration_required", "bool"),
            f("medication_rules", "text"), f("prohibited_items", "text"), f("restricted_items", "text"),
            f("pet_import_rules", "text"),
            f("condition_expression", "json"), f("exemption_expression", "json"), f("remarks", "text"),
        ],
    },
    "Entry Restrictions": {
        "endpoint": "/entry-restrictions", "category": "Compliance", "ops": FULL,
        "fields": [
            f("rule_id", "int", True), f("destination_country_id", "int", True), f("nationality_country_id", "int", True),
            f("restriction_type", "str", True), f("reason", "text"),
            f("effective_date", "date", True), f("expiry_date", "date"),
            f("source_id", "int", True), f("condition_expression", "json"), f("remarks", "text"),
        ],
    },
    "Compliance Checks": {
        "endpoint": "/compliance-checks", "category": "Compliance", "ops": FULL,
        "fields": [
            f("request_id", "str", True), f("client_id", "int", True), f("input_hash", "str", True),
            f("rule_version_id", "int", True), f("decision", "enum", True, enum="decision"),
            f("decision_reasons", "json"), f("response_json", "json", True),
        ],
    },
    "Rule Execution Logs": {
        "endpoint": "/rule-execution-logs", "category": "Compliance", "ops": FULL,
        "fields": [
            f("request_id", "str", True), f("rule_id", "int", True), f("matched", "bool", True),
            f("skipped", "bool"), f("execution_time_ms", "int", True), f("reason", "text"),
        ],
    },

    # ---------------- ADMINISTRATION ----------------
    "Roles": {
        "endpoint": "/roles", "category": "Administration", "ops": FULL,
        "fields": [f("role_name", "str", True), f("description", "text")],
    },
    "Permissions": {
        "endpoint": "/permissions", "category": "Administration", "ops": FULL,
        "fields": [f("permission_code", "str", True), f("permission_name", "str", True), f("description", "text")],
    },
    "Role Permissions": {
        "endpoint": "/role-permissions", "category": "Administration", "ops": FULL,
        "fields": [f("role_id", "int", True), f("permission_id", "int", True)],
    },
    "Users": {
        "endpoint": "/users", "category": "Administration", "ops": FULL,
        "fields": [
            f("username", "str", True), f("full_name", "str", True), f("email", "email", True),
            f("role_id", "int", True), f("phone", "str"),
            f("password", "str", True, help="min 8 characters (create only)"),
            f("status", "bool", default=True),
        ],
    },
    "API Clients": {
        "endpoint": "/api-clients", "category": "Administration", "ops": FULL,
        "fields": [
            f("client_name", "str", True), f("company_name", "str", True), f("client_code", "str", True),
            f("api_key", "str", True), f("contact_name", "str"), f("contact_email", "email", True),
            f("contact_phone", "str"), f("subscription_plan", "enum", True, enum="subscription_plan"),
            f("requests_per_minute", "int", default=60), f("status", "bool", default=True),
            f("expires_at", "datetime"),
        ],
    },
    "Client IP Whitelists": {
        "endpoint": "/client-ip-whitelists", "category": "Administration", "ops": FULL,
        "fields": [
            f("client_id", "int", True), f("ip_address", "str"), f("cidr_range", "str"),
            f("description", "text"), f("is_primary", "bool"), f("active", "bool", default=True),
        ],
    },
    "Audit Logs": {
        "endpoint": "/audit-logs", "category": "Administration", "ops": CR,
        "fields": [
            f("user_id", "int", True), f("entity_name", "str", True), f("entity_id", "int", True),
            f("action", "enum", True, enum="audit_action"), f("old_value", "json"), f("new_value", "json"),
            f("ip_address", "str"),
        ],
    },
    "API Request Logs": {
        "endpoint": "/api-request-logs", "category": "Administration", "ops": CR,
        "fields": [
            f("client_id", "int", True), f("ip_address", "str", True), f("endpoint", "str", True),
            f("http_method", "enum", True, enum="http_method"), f("request_id", "str", True),
            f("request_body", "json"), f("response_status", "int", True), f("response_time_ms", "int", True),
        ],
    },
    "Client Usage Statistics": {
        "endpoint": "/client-usage-statistics", "category": "Administration", "ops": CRU,
        "fields": [
            f("client_id", "int", True), f("usage_date", "date", True),
            f("total_requests", "int", default=0), f("successful_requests", "int", default=0),
            f("failed_requests", "int", default=0), f("average_response_time", "int"),
        ],
    },

    # ---------------- DATA COLLECTION ----------------
    "Source Registries": {
        "endpoint": "/source-registries", "category": "Data Collection", "ops": FULL,
        "fields": [
            f("country_id", "int", True), f("authority_name", "str", True), f("website", "str", True),
            f("source_type", "enum", True, enum="source_type"), f("language", "str"),
            f("update_frequency", "enum", enum="update_frequency"), f("contact_email", "str"),
            f("active", "bool", default=True),
        ],
    },
    "Source Documents": {
        "endpoint": "/source-documents", "category": "Data Collection", "ops": FULL,
        "fields": [
            f("source_id", "int", True), f("document_name", "str", True),
            f("document_type", "enum", True, enum="document_type"), f("document_url", "str", True),
            f("file_hash", "str", True), f("downloaded_at", "datetime", True),
        ],
    },
    "Document Versions": {
        "endpoint": "/document-versions", "category": "Data Collection", "ops": FULL,
        "fields": [
            f("document_id", "int", True), f("version_number", "str", True), f("file_hash", "str", True),
            f("effective_date", "date"), f("archived", "bool"),
        ],
    },
    "Collection Logs": {
        "endpoint": "/collection-logs", "category": "Data Collection", "ops": FULL,
        "fields": [
            f("source_id", "int", True), f("collection_type", "enum", True, enum="collection_type"),
            f("collection_status", "enum", True, enum="collection_status"), f("message", "text"),
            f("collected_by", "int", True), f("collected_at", "datetime", True),
        ],
    },
    "Document Validations": {
        "endpoint": "/document-validations", "category": "Data Collection", "ops": FULL,
        "fields": [
            f("document_id", "int", True), f("validator_id", "int", True),
            f("validation_status", "enum", True, enum="validation_status"), f("comments", "text"),
            f("validated_at", "datetime", True),
        ],
    },
    "AI Extractions": {
        "endpoint": "/ai-extractions", "category": "Data Collection", "ops": FULL,
        "fields": [
            f("document_id", "int", True), f("extraction_engine", "str", True),
            f("extraction_status", "enum", True, enum="extraction_status"), f("confidence_score", "decimal"),
            f("extracted_at", "datetime", True),
        ],
    },

    # ---------------- RULE MANAGEMENT ----------------
    "Rule Statuses": {
        "endpoint": "/rule-statuses", "category": "Rule Management", "ops": FULL,
        "fields": [
            f("status_code", "str", True), f("status_name", "str", True), f("description", "text"),
            f("active", "bool", default=True),
        ],
    },
    "Rule Versions": {
        "endpoint": "/rule-versions", "category": "Rule Management", "ops": FULL,
        "fields": [
            f("rule_id", "int", True), f("version_number", "str", True), f("release_notes", "text"),
            f("effective_date", "date", True), f("expiry_date", "date"),
            f("published_by", "int"), f("published_at", "datetime"),
        ],
    },
    "Rule Approvals": {
        "endpoint": "/rule-approvals", "category": "Rule Management", "ops": CR,
        "fields": [
            f("rule_id", "int", True), f("reviewer_id", "int", True),
            f("approval_status", "enum", True, enum="approval_status"), f("comments", "text"),
        ],
    },
    "Rule History": {
        "endpoint": "/rule-history", "category": "Rule Management", "ops": {"read"},
        "fields": [
            f("rule_id", "int"), f("previous_version_id", "int"), f("new_version_id", "int"),
            f("change_type", "enum", enum="change_type"), f("change_summary", "text"), f("changed_by", "int"),
        ],
    },
    "Rule Simulations": {
        "endpoint": "/rule-simulations", "category": "Rule Management", "ops": CR,
        "fields": [
            f("simulation_name", "str", True), f("rule_id", "int", True), f("rule_version_id", "int", True),
            f("request_payload", "json", True), f("expected_result", "json", True), f("actual_result", "json"),
            f("simulation_status", "enum", True, enum="simulation_status"), f("executed_by", "int", True),
            f("remarks", "text"),
        ],
    },
}

CATEGORY_ORDER = ["Reference", "Compliance", "Administration", "Rule Management", "Data Collection"]

# Entities whose Update schema adds a soft-delete "active" flag not present at create time
# (and which don't already expose an equivalent field like status/active in their base fields).
_ACTIVE_ON_UPDATE = {
    "Countries", "Regions", "Currencies", "Passport Types", "Visa Types", "Airlines", "Airports",
    "Purposes", "Passenger Types", "Travel Authorizations", "Rules", "Visa Rules", "Passport Rules",
    "Travel Authorization Rules", "Transit Rules", "Health Rules", "Vaccines", "Health Rule Vaccines",
    "Immigration Rules", "Customs Rules", "Entry Restrictions", "Rule Versions",
}
for _name in _ACTIVE_ON_UPDATE:
    ENTITIES[_name]["extra_update_fields"] = [f("active", "bool", help="Enable/disable this record")]

