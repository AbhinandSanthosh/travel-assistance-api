import os
import requests
import streamlit as st


# ============================================================
# ENUM VALUES
# ============================================================

ENUMS = {
    "rule_type": [
        "VISA",
        "PASSPORT",
        "TRAVEL_AUTHORIZATION",
        "TRANSIT",
        "HEALTH",
        "CUSTOMS",
        "IMMIGRATION",
        "ENTRY_RESTRICTION",
    ],
    "decision": [
        "ALLOWED",
        "CONDITIONAL",
        "NOT_ALLOWED",
    ],
    "subscription_plan": [
        "STANDARD",
        "PREMIUM",
        "ENTERPRISE",
    ],
    "http_method": [
        "GET",
        "POST",
        "PUT",
        "DELETE",
    ],
    "audit_action": [
        "INSERT",
        "UPDATE",
        "DELETE",
    ],
    "approval_status": [
        "APPROVED",
        "REJECTED",
    ],
    "change_type": [
        "CREATE",
        "UPDATE",
        "DELETE",
        "PUBLISH",
        "EXPIRE",
    ],
    "simulation_status": [
        "PASSED",
        "FAILED",
        "ERROR",
    ],
    "source_type": [
        "API",
        "WEBSITE",
        "PDF",
        "EMAIL",
    ],
    "document_type": [
        "PDF",
        "HTML",
        "API_RESPONSE",
    ],
    "collection_type": [
        "MANUAL",
        "API",
        "CRAWLER",
    ],
    "collection_status": [
        "SUCCESS",
        "FAILED",
    ],
    "validation_status": [
        "PENDING",
        "APPROVED",
        "REJECTED",
    ],
    "extraction_status": [
        "SUCCESS",
        "FAILED",
    ],
    "update_frequency": [
        "DAILY",
        "WEEKLY",
        "MONTHLY",
        "ON_DEMAND",
    ],
}


# ============================================================
# FIELD HELPER
# ============================================================

def f(
    name,
    type_,
    required=False,
    enum=None,
    help=None,
    default=None,
):
    return {
        "name": name,
        "type": type_,
        "required": required,
        "enum": enum,
        "help": help,
        "default": default,
    }


# ============================================================
# CRUD OPERATIONS
# ============================================================

FULL = {"create", "read", "update", "delete"}
CR = {"create", "read"}
CRU = {"create", "read", "update"}


# ============================================================
# ENTITY CONFIGURATION
# ============================================================

ENTITIES = {

    # ========================================================
    # REFERENCE
    # ========================================================

    "Countries": {
        "endpoint": "/countries",
        "category": "Reference",
        "ops": FULL,
        "fields": [
            f(
                "iso2",
                "str",
                True,
                help="ISO 3166-1 alpha-2 code, e.g. US",
            ),
            f(
                "iso3",
                "str",
                True,
                help="ISO 3166-1 alpha-3 code, e.g. USA",
            ),
            f(
                "country_name",
                "str",
                True,
            ),
            f(
                "nationality",
                "str",
                True,
            ),
            f(
                "region_id",
                "int",
                True,
            ),
            f(
                "capital",
                "str",
            ),
            f(
                "currency_id",
                "int",
                True,
            ),
            f(
                "official_language",
                "str",
            ),
            f(
                "timezone",
                "str",
            ),
        ],
    },

    "Regions": {
        "endpoint": "/regions",
        "category": "Reference",
        "ops": FULL,
        "fields": [
            f("region_name", "str", True),
            f("description", "text"),
        ],
    },

    "Currencies": {
        "endpoint": "/currencies",
        "category": "Reference",
        "ops": FULL,
        "fields": [
            f(
                "currency_code",
                "str",
                True,
                help="ISO 4217 code, e.g. USD",
            ),
            f(
                "currency_name",
                "str",
                True,
            ),
            f(
                "currency_symbol",
                "str",
            ),
        ],
    },

    "Passport Types": {
        "endpoint": "/passport-types",
        "category": "Reference",
        "ops": FULL,
        "fields": [
            f("passport_code", "str", True),
            f("passport_name", "str", True),
            f("description", "text"),
        ],
    },

    "Visa Types": {
        "endpoint": "/visa-types",
        "category": "Reference",
        "ops": FULL,
        "fields": [
            f("visa_code", "str", True),
            f("visa_name", "str", True),
            f("description", "text"),
        ],
    },

    "Airlines": {
        "endpoint": "/airlines",
        "category": "Reference",
        "ops": FULL,
        "fields": [
            f("airline_name", "str", True),
            f("iata_code", "str", help="2 characters"),
            f("icao_code", "str", help="3 characters"),
            f("country_id", "int", True),
        ],
    },

    "Airports": {
        "endpoint": "/airports",
        "category": "Reference",
        "ops": FULL,
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
        "endpoint": "/purposes",
        "category": "Reference",
        "ops": FULL,
        "fields": [
            f("purpose_code", "str", True),
            f("purpose_name", "str", True),
            f("description", "text"),
        ],
    },

    "Passenger Types": {
        "endpoint": "/passenger-types/",
        "category": "Reference",
        "ops": FULL,
        "fields": [
            f("passenger_type_code", "str", True),
            f("passenger_type_name", "str", True),
            f("description", "text"),
        ],
    },

    "Travel Authorizations": {
        "endpoint": "/travel-authorizations/",
        "category": "Reference",
        "ops": FULL,
        "fields": [
            f("authorization_code", "str", True),
            f("authorization_name", "str", True),
            f("destination_country_id", "int", True),
            f("description", "text"),
        ],
    },


    # ========================================================
    # COMPLIANCE
    # ========================================================

    "Rules": {
        "endpoint": "/rules",
        "category": "Compliance",
        "ops": FULL,
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
        "endpoint": "/visa-rules",
        "category": "Compliance",
        "ops": FULL,
        "fields": [
            f("rule_id", "int", True),
            f("nationality_country_id", "int", True),
            f("destination_country_id", "int", True),
            f("passport_type_id", "int", True),
            f("visa_type_id", "int", True),
            f("purpose_id", "int", True),
            f("visa_required", "bool"),
            f("visa_on_arrival", "bool"),
            f("evisa_available", "bool"),
            f("max_stay_days", "int"),
            f("multiple_entry", "bool"),
            f("condition_expression", "json"),
            f("exemption_expression", "json"),
            f("remarks", "text"),
        ],
    },

    "Passport Rules": {
        "endpoint": "/passport-rules",
        "category": "Compliance",
        "ops": FULL,
        "fields": [
            f("rule_id", "int", True),
            f("destination_country_id", "int", True),
            f("passport_type_id", "int", True),
            f("minimum_validity_months", "int"),
            f("blank_pages_required", "int"),
            f("machine_readable_required", "bool"),
            f("damaged_passport_allowed", "bool"),
            f("temporary_passport_allowed", "bool"),
            f("passport_issue_date_required", "bool"),
            f("condition_expression", "json"),
            f("exemption_expression", "json"),
            f("remarks", "text"),
        ],
    },

    "Travel Authorization Rules": {
        "endpoint": "/travel-authorization-rules",
        "category": "Compliance",
        "ops": FULL,
        "fields": [
            f("rule_id", "int", True),
            f("authorization_id", "int", True),
            f("nationality_country_id", "int", True),
            f("destination_country_id", "int", True),
            f("passport_type_id", "int", True),
            f("purpose_id", "int", True),
            f("authorization_required", "bool"),
            f("validity_days", "int"),
            f("condition_expression", "json"),
            f("exemption_expression", "json"),
            f("remarks", "text"),
        ],
    },

    "Transit Rules": {
        "endpoint": "/transit-rules",
        "category": "Compliance",
        "ops": FULL,
        "fields": [
            f("rule_id", "int", True),
            f("nationality_country_id", "int", True),
            f("transit_country_id", "int", True),
            f("transit_airport_id", "int", True),
            f("transit_visa_required", "bool"),
            f("airside_transit_allowed", "bool"),
            f("baggage_collection_required", "bool"),
            f("overnight_transit_allowed", "bool"),
            f("max_transit_hours", "int"),
            f("condition_expression", "json"),
            f("exemption_expression", "json"),
            f("remarks", "text"),
        ],
    },

    "Health Rules": {
        "endpoint": "/health-rules",
        "category": "Compliance",
        "ops": FULL,
        "fields": [
            f("rule_id", "int", True),
            f("destination_country_id", "int", True),
            f("nationality_country_id", "int", True),
            f("health_form_required", "bool"),
            f("quarantine_required", "bool"),
            f("quarantine_days", "int"),
            f("medical_certificate_required", "bool"),
            f("condition_expression", "json"),
            f("exemption_expression", "json"),
            f("remarks", "text"),
        ],
    },

    "Vaccines": {
        "endpoint": "/vaccines",
        "category": "Compliance",
        "ops": FULL,
        "fields": [
            f("vaccine_name", "str", True),
            f("disease", "str", True),
        ],
    },

    "Health Rule Vaccines": {
        "endpoint": "/health-rule-vaccines",
        "category": "Compliance",
        "ops": FULL,
        "fields": [
            f("health_rule_id", "int", True),
            f("vaccine_id", "int", True),
            f("certificate_required", "bool"),
            f("created_by", "int", True),
            f("updated_by", "int", True),
        ],
    },

    "Immigration Rules": {
        "endpoint": "/immigration-rules",
        "category": "Compliance",
        "ops": FULL,
        "fields": [
            f("rule_id", "int", True),
            f("destination_country_id", "int", True),
            f("onward_ticket_required", "bool"),
            f("accommodation_proof_required", "bool"),
            f("proof_of_funds_required", "bool"),
            f("biometric_required", "bool"),
            f("interview_required", "bool"),
            f("arrival_card_required", "bool"),
            f("digital_arrival_card", "bool"),
            f("arrival_registration_required", "bool"),
            f("condition_expression", "json"),
            f("exemption_expression", "json"),
            f("remarks", "text"),
            f("created_by", "int", True),
            f("updated_by", "int", True),
        ],
    },

    "Customs Rules": {
        "endpoint": "/customs-rules",
        "category": "Compliance",
        "ops": FULL,
        "fields": [
            f("rule_id", "int", True),
            f("destination_country_id", "int", True),
            f("nationality_country_id", "int", True),
            f("alcohol_limit", "str"),
            f("tobacco_limit", "str"),
            f("currency_limit_amount", "decimal"),
            f("currency_id", "int"),
            f("currency_declaration_required", "bool"),
            f("medication_rules", "text"),
            f("prohibited_items", "text"),
            f("restricted_items", "text"),
            f("pet_import_rules", "text"),
            f("condition_expression", "json"),
            f("exemption_expression", "json"),
            f("remarks", "text"),
        ],
    },

    "Entry Restrictions": {
        "endpoint": "/entry-restrictions",
        "category": "Compliance",
        "ops": FULL,
        "fields": [
            f("rule_id", "int", True),
            f("destination_country_id", "int", True),
            f("nationality_country_id", "int", True),
            f("restriction_type", "str", True),
            f("reason", "text"),
            f("effective_date", "date", True),
            f("expiry_date", "date"),
            f("source_id", "int", True),
            f("condition_expression", "json"),
            f("remarks", "text"),
        ],
    },

    "Compliance Checks": {
        "endpoint": "/compliance-checks",
        "category": "Compliance",
        "ops": FULL,
        "fields": [
            f("request_id", "str", True),
            f("client_id", "int", True),
            f("input_hash", "str", True),
            f("rule_version_id", "int", True),
            f("decision", "enum", True, enum="decision"),
            f("decision_reasons", "json"),
            f("response_json", "json", True),
        ],
    },

    "Rule Execution Logs": {
        "endpoint": "/rule-execution-logs",
        "category": "Compliance",
        "ops": FULL,
        "fields": [
            f("request_id", "str", True),
            f("rule_id", "int", True),
            f("matched", "bool", True),
            f("skipped", "bool"),
            f("execution_time_ms", "int", True),
            f("reason", "text"),
        ],
    },


    # ========================================================
    # ADMINISTRATION
    # ========================================================

    "Roles": {
        "endpoint": "/roles",
        "category": "Administration",
        "ops": FULL,
        "fields": [
            f("role_name", "str", True),
            f("description", "text"),
        ],
    },

    "Permissions": {
        "endpoint": "/permissions",
        "category": "Administration",
        "ops": FULL,
        "fields": [
            f("permission_code", "str", True),
            f("permission_name", "str", True),
            f("description", "text"),
        ],
    },

    "Role Permissions": {
        "endpoint": "/role-permissions",
        "category": "Administration",
        "ops": FULL,
        "fields": [
            f("role_id", "int", True),
            f("permission_id", "int", True),
        ],
    },

    "Users": {
        "endpoint": "/users",
        "category": "Administration",
        "ops": FULL,
        "fields": [
            f("username", "str", True),
            f("full_name", "str", True),
            f("email", "email", True),
            f("role_id", "int", True),
            f("phone", "str"),
            f(
                "password",
                "str",
                True,
                help="min 8 characters (create only)",
            ),
            f("status", "bool", default=True),
        ],
    },

    "API Clients": {
        "endpoint": "/api-clients",
        "category": "Administration",
        "ops": FULL,
        "fields": [
            f("client_name", "str", True),
            f("company_name", "str", True),
            f("client_code", "str", True),
            f(
                "api_key",
                "str",
                help=(
                    "Legacy plaintext key (admin-issued clients only). "
                    "Leave blank for portal clients -- they get a hashed "
                    "key from the Developer Portal instead."
                ),
            ),
            f("contact_name", "str"),
            f("contact_email", "email", True),
            f("contact_phone", "str"),
            f(
                "subscription_plan",
                "enum",
                True,
                enum="subscription_plan",
            ),
            f("requests_per_minute", "int", default=60),
            f("status", "bool", default=True),
            f("expires_at", "datetime"),
        ],
    },

    "Client IP Whitelists": {
        "endpoint": "/client-ip-whitelists",
        "category": "Administration",
        "ops": FULL,
        "fields": [
            f("client_id", "int", True),
            f("ip_address", "str"),
            f("cidr_range", "str"),
            f("description", "text"),
            f("is_primary", "bool"),
            f("active", "bool", default=True),
        ],
    },

    "Audit Logs": {
        "endpoint": "/audit-logs",
        "category": "Administration",
        "ops": CR,
        "fields": [
            f("user_id", "int", True),
            f("entity_name", "str", True),
            f("entity_id", "int", True),
            f("action", "enum", True, enum="audit_action"),
            f("old_value", "json"),
            f("new_value", "json"),
            f("ip_address", "str"),
        ],
    },

    "API Request Logs": {
        "endpoint": "/api-request-logs",
        "category": "Administration",
        "ops": CR,
        "fields": [
            f("client_id", "int", True),
            f("ip_address", "str", True),
            f("endpoint", "str", True),
            f("http_method", "enum", True, enum="http_method"),
            f("request_id", "str", True),
            f("request_body", "json"),
            f("response_status", "int", True),
            f("response_time_ms", "int", True),
        ],
    },

    "Client Usage Statistics": {
        "endpoint": "/client-usage-statistics",
        "category": "Administration",
        "ops": CRU,
        "fields": [
            f("client_id", "int", True),
            f("usage_date", "date", True),
            f("total_requests", "int", default=0),
            f("successful_requests", "int", default=0),
            f("failed_requests", "int", default=0),
            f("average_response_time", "int"),
        ],
    },


    # ========================================================
    # DATA COLLECTION
    # ========================================================

    "Source Registries": {
        "endpoint": "/source-registries",
        "category": "Data Collection",
        "ops": FULL,
        "fields": [
            f("country_id", "int", True),
            f("authority_name", "str", True),
            f("website", "str", True),
            f("source_type", "enum", True, enum="source_type"),
            f("language", "str"),
            f(
                "update_frequency",
                "enum",
                enum="update_frequency",
            ),
            f("contact_email", "str"),
            f("active", "bool", default=True),
        ],
    },

    "Source Documents": {
        "endpoint": "/source-documents",
        "category": "Data Collection",
        "ops": FULL,
        "fields": [
            f("source_id", "int", True),
            f("document_name", "str", True),
            f(
                "document_type",
                "enum",
                True,
                enum="document_type",
            ),
            f("document_url", "str", True),
            f("file_hash", "str", True),
            f("downloaded_at", "datetime", True),
        ],
    },

    "Document Versions": {
        "endpoint": "/document-versions",
        "category": "Data Collection",
        "ops": FULL,
        "fields": [
            f("document_id", "int", True),
            f("version_number", "str", True),
            f("file_hash", "str", True),
            f("effective_date", "date"),
            f("archived", "bool"),
        ],
    },

    "Collection Logs": {
        "endpoint": "/collection-logs",
        "category": "Data Collection",
        "ops": FULL,
        "fields": [
            f("source_id", "int", True),
            f(
                "collection_type",
                "enum",
                True,
                enum="collection_type",
            ),
            f(
                "collection_status",
                "enum",
                True,
                enum="collection_status",
            ),
            f("message", "text"),
            f("collected_by", "int", True),
            f("collected_at", "datetime", True),
        ],
    },

    "Document Validations": {
        "endpoint": "/document-validations",
        "category": "Data Collection",
        "ops": FULL,
        "fields": [
            f("document_id", "int", True),
            f("validator_id", "int", True),
            f(
                "validation_status",
                "enum",
                True,
                enum="validation_status",
            ),
            f("comments", "text"),
            f("validated_at", "datetime", True),
        ],
    },

    "AI Extractions": {
        "endpoint": "/ai-extractions",
        "category": "Data Collection",
        "ops": FULL,
        "fields": [
            f("document_id", "int", True),
            f("extraction_engine", "str", True),
            f(
                "extraction_status",
                "enum",
                True,
                enum="extraction_status",
            ),
            f("confidence_score", "decimal"),
            f("extracted_at", "datetime", True),
        ],
    },


    # ========================================================
    # RULE MANAGEMENT
    # ========================================================

    "Rule Statuses": {
        "endpoint": "/rule-statuses",
        "category": "Rule Management",
        "ops": FULL,
        "fields": [
            f("status_code", "str", True),
            f("status_name", "str", True),
            f("description", "text"),
            f("active", "bool", default=True),
        ],
    },

    "Rule Versions": {
        "endpoint": "/rule-versions",
        "category": "Rule Management",
        "ops": FULL,
        "fields": [
            f("rule_id", "int", True),
            f("version_number", "str", True),
            f("release_notes", "text"),
            f("effective_date", "date", True),
            f("expiry_date", "date"),
            f("published_by", "int"),
            f("published_at", "datetime"),
        ],
    },

    "Rule Approvals": {
        "endpoint": "/rule-approvals",
        "category": "Rule Management",
        "ops": CR,
        "fields": [
            f("rule_id", "int", True),
            f("reviewer_id", "int", True),
            f(
                "approval_status",
                "enum",
                True,
                enum="approval_status",
            ),
            f("comments", "text"),
        ],
    },

    "Rule History": {
        "endpoint": "/rule-history",
        "category": "Rule Management",
        "ops": {"read"},
        "fields": [
            f("rule_id", "int"),
            f("previous_version_id", "int"),
            f("new_version_id", "int"),
            f(
                "change_type",
                "enum",
                enum="change_type",
            ),
            f("change_summary", "text"),
            f("changed_by", "int"),
        ],
    },

    "Rule Simulations": {
        "endpoint": "/rule-simulations",
        "category": "Rule Management",
        "ops": CR,
        "fields": [
            f("simulation_name", "str", True),
            f("rule_id", "int", True),
            f("rule_version_id", "int", True),
            f("request_payload", "json", True),
            f("expected_result", "json", True),
            f("actual_result", "json"),
            f(
                "simulation_status",
                "enum",
                True,
                enum="simulation_status",
            ),
            f("executed_by", "int", True),
            f("remarks", "text"),
        ],
    },
}


# ============================================================
# FOREIGN-KEY RELATIONSHIPS
# ============================================================
#
# key:
#     The field in the current table.
#
# entity:
#     The entity whose records should appear in the dropdown.
#
# label_field:
#     The field to display next to the ID.
#
# Example:
#
# region_id -> Regions
#
# API:
#     GET /regions
#
# Result:
#     [
#         {"id": 1, "region_name": "Asia"},
#         {"id": 2, "region_name": "Europe"}
#     ]
#
# Streamlit:
#     1 - Asia
#     2 - Europe
#
# Submitted value:
#     1 or 2
#
# ============================================================

RELATIONS = {

    # ---------------- REFERENCE ----------------

    "region_id": {
        "entity": "Regions",
        "label_field": "region_name",
    },

    "currency_id": {
        "entity": "Currencies",
        "label_field": "currency_name",
    },

    "country_id": {
        "entity": "Countries",
        "label_field": "country_name",
    },

    "destination_country_id": {
        "entity": "Countries",
        "label_field": "country_name",
    },

    "nationality_country_id": {
        "entity": "Countries",
        "label_field": "country_name",
    },

    "transit_country_id": {
        "entity": "Countries",
        "label_field": "country_name",
    },

    "passport_type_id": {
        "entity": "Passport Types",
        "label_field": "passport_name",
    },

    "visa_type_id": {
        "entity": "Visa Types",
        "label_field": "visa_name",
    },

    "purpose_id": {
        "entity": "Purposes",
        "label_field": "purpose_name",
    },

    "authorization_id": {
        "entity": "Travel Authorizations",
        "label_field": "authorization_name",
    },

    "transit_airport_id": {
        "entity": "Airports",
        "label_field": "airport_name",
    },

    "vaccine_id": {
        "entity": "Vaccines",
        "label_field": "vaccine_name",
    },

    # ---------------- ADMINISTRATION ----------------

    "role_id": {
        "entity": "Roles",
        "label_field": "role_name",
    },

    "permission_id": {
        "entity": "Permissions",
        "label_field": "permission_name",
    },

    "client_id": {
        "entity": "API Clients",
        "label_field": "client_name",
    },

    # ---------------- RULE MANAGEMENT ----------------

    "status_id": {
        "entity": "Rule Statuses",
        "label_field": "status_name",
    },
}


# ============================================================
# CATEGORY ORDER
# ============================================================

CATEGORY_ORDER = [
    "Reference",
    "Compliance",
    "Administration",
    "Rule Management",
    "Data Collection",
]


# ============================================================
# SOFT DELETE
# ============================================================

_ACTIVE_ON_UPDATE = {
    "Countries",
    "Regions",
    "Currencies",
    "Passport Types",
    "Visa Types",
    "Airlines",
    "Airports",
    "Purposes",
    "Passenger Types",
    "Travel Authorizations",
    "Rules",
    "Visa Rules",
    "Passport Rules",
    "Travel Authorization Rules",
    "Transit Rules",
    "Health Rules",
    "Vaccines",
    "Health Rule Vaccines",
    "Immigration Rules",
    "Customs Rules",
    "Entry Restrictions",
    "Rule Versions",
}

for _name in _ACTIVE_ON_UPDATE:
    ENTITIES[_name]["extra_update_fields"] = [
        f(
            "active",
            "bool",
            help="Enable/disable this record",
        )
    ]


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def format_field_label(field_name):
    """
    Convert:

        region_id

    into:

        Region

    Convert:

        currency_id

    into:

        Currency
    """

    label = field_name.replace("_id", "")
    label = label.replace("_", " ")

    return label.title()


def get_relation_config(field_name):
    """
    Return relationship configuration for a field.

    Example:

        get_relation_config("region_id")

    returns:

        {
            "entity": "Regions",
            "label_field": "region_name"
        }
    """

    return RELATIONS.get(field_name)


def get_record_id(record):
    """
    Get primary key from an API record.

    The normal expected API format is:

        {
            "id": 1,
            ...
        }

    A small fallback is included for APIs that return a
    table-specific ID such as region_id.
    """

    if not isinstance(record, dict):
        return None

    if record.get("id") is not None:
        return record.get("id")

    # Fallbacks for common API response shapes.
    for key in (
        "region_id",
        "currency_id",
        "country_id",
        "role_id",
        "permission_id",
        "client_id",
        "passport_type_id",
        "visa_type_id",
        "purpose_id",
        "authorization_id",
        "airport_id",
        "vaccine_id",
        "status_id",
    ):
        if record.get(key) is not None:
            return record.get(key)

    return None


def get_relation_label(record, label_field):
    """
    Get the human-readable name from a related record.
    """

    value = record.get(label_field)

    if value is None:
        return "Unknown"

    return str(value)


# ============================================================
# API FETCH FUNCTION
# ============================================================
#
# IMPORTANT:
#
# Replace the body of this function with your existing API
# GET function if you already have one.
#
# It should return a Python list such as:
#
# [
#     {"id": 1, "region_name": "Asia"},
#     {"id": 2, "region_name": "Europe"},
# ]
#
# ============================================================

# ============================================================
# API CONFIGURATION FOR RELATION DROPDOWNS
# ============================================================
#
# Set API_BASE_URL in your environment if your backend is not
# running at http://localhost:8000.
#
# Example:
#
#   Windows:
#       set API_BASE_URL=http://127.0.0.1:8000
#
#   Linux/macOS:
#       export API_BASE_URL=http://127.0.0.1:8000
#
# If your application already has an API base URL constant,
# you can replace API_BASE_URL below with that existing value.
#
# ============================================================

API_BASE_URL = os.getenv(
    "API_BASE_URL",
    "http://localhost:8000",
)

API_TOKEN = os.getenv("API_TOKEN")


def api_get(endpoint):
    """
    Generic GET helper used by the relationship dropdowns.

    This replaces the undefined api_get() placeholder from the
    previous version.

    It returns the decoded JSON response. Authentication is
    optional and is taken from API_TOKEN when configured.
    """

    endpoint = str(endpoint)

    # Avoid producing /countries// or similar URLs.
    url = f"{API_BASE_URL.rstrip('/')}/{endpoint.lstrip('/')}"

    headers = {
        "Accept": "application/json",
    }

    if API_TOKEN:
        headers["Authorization"] = f"Bearer {API_TOKEN}"

    response = requests.get(
        url,
        headers=headers,
        timeout=15,
    )

    response.raise_for_status()

    return response.json()


def fetch_relation_records(endpoint):
    """
    Fetch records from a related endpoint.

    Supports the common response formats:

        [
            {"id": 1, "region_name": "Asia"},
            {"id": 2, "region_name": "Europe"}
        ]

    or:

        {"data": [...]}

    or:

        {"items": [...]}
    """

    try:
        response = api_get(endpoint)

    except requests.RequestException as exc:
        st.error(
            f"Unable to load related records from "
            f"{endpoint}: {exc}"
        )
        return []

    except ValueError as exc:
        st.error(
            f"Invalid JSON returned from "
            f"{endpoint}: {exc}"
        )
        return []

    if response is None:
        return []

    # If api_get() ever returns a requests.Response,
    # support that too.
    if hasattr(response, "json") and callable(response.json):
        try:
            response = response.json()
        except ValueError:
            st.error(
                f"Invalid JSON returned from {endpoint}."
            )
            return []

    # Plain list:
    #
    # [
    #     {"id": 1, ...},
    #     {"id": 2, ...}
    # ]
    if isinstance(response, list):
        return response

    # Wrapped response:
    #
    # {"data": [...]}
    #
    if isinstance(response, dict):
        data = response.get("data")

        if isinstance(data, list):
            return data

        items = response.get("items")

        if isinstance(items, list):
            return items

        # Some APIs return:
        #
        # {"results": [...]}
        #
        results = response.get("results")

        if isinstance(results, list):
            return results

    st.error(
        f"Unexpected response format from {endpoint}."
    )

    return []


# ============================================================
# LOAD RELATION OPTIONS
# ============================================================

@st.cache_data(ttl=60)
def load_relation_options(field_name):
    """
    Fetch related records and prepare Streamlit dropdown data.

    Returns:

        {
            "1 - Asia": 1,
            "2 - Europe": 2
        }
    """

    relation = get_relation_config(field_name)

    if relation is None:
        return {}

    related_entity_name = relation["entity"]
    label_field = relation["label_field"]

    related_entity = ENTITIES.get(related_entity_name)

    if related_entity is None:
        st.error(
            f"Relationship entity '{related_entity_name}' "
            f"does not exist in ENTITIES."
        )
        return {}

    endpoint = related_entity["endpoint"]

    try:
        records = fetch_relation_records(endpoint)
    except Exception as exc:
        st.error(
            f"Unable to load {related_entity_name}: {exc}"
        )
        return {}

    options = {}

    for record in records:

        record_id = get_record_id(record)

        if record_id is None:
            continue

        label = get_relation_label(
            record,
            label_field,
        )

        display_text = f"{record_id} - {label}"

        options[display_text] = record_id

    return options


# ============================================================
# RENDER FOREIGN-KEY FIELD
# ============================================================

def render_relation_field(
    entity_name,
    field,
    existing_value=None,
):
    """
    Render a foreign-key field as a Streamlit selectbox.

    Example:

        Region
        [ 1 - Asia       ▼ ]

    But returns:

        1

    """

    field_name = field["name"]

    options = load_relation_options(field_name)

    label = format_field_label(field_name)

    if not options:

        st.warning(
            f"No records available for {label}."
        )

        return None

    option_labels = list(options.keys())

    # --------------------------------------------------------
    # CREATE MODE
    # --------------------------------------------------------

    if existing_value is None:

        selected_label = st.selectbox(
            label,
            options=option_labels,
            index=0,
            key=f"{entity_name}_{field_name}",
            help=field.get("help"),
        )

        return options[selected_label]

    # --------------------------------------------------------
    # UPDATE MODE
    # --------------------------------------------------------

    existing_value = int(existing_value)

    selected_index = 0

    for index, option_label in enumerate(option_labels):

        if options[option_label] == existing_value:
            selected_index = index
            break

    selected_label = st.selectbox(
        label,
        options=option_labels,
        index=selected_index,
        key=f"{entity_name}_{field_name}",
        help=field.get("help"),
    )

    return options[selected_label]


# ============================================================
# GENERIC FIELD RENDERER
# ============================================================

def render_field(
    entity_name,
    field,
    existing_value=None,
):
    """
    Generic Streamlit renderer.

    Foreign-key fields are handled first.

    Everything else follows the normal field type.
    """

    field_name = field["name"]
    field_type = field["type"]

    # ========================================================
    # FOREIGN KEY
    # ========================================================

    if field_name in RELATIONS:

        return render_relation_field(
            entity_name=entity_name,
            field=field,
            existing_value=existing_value,
        )

    # ========================================================
    # ENUM
    # ========================================================

    if field_type == "enum":

        enum_name = field.get("enum")

        enum_values = ENUMS.get(
            enum_name,
            [],
        )

        if not enum_values:
            st.warning(
                f"No ENUM values configured for {field_name}."
            )
            return None

        # Update existing value
        if existing_value in enum_values:
            index = enum_values.index(existing_value)
        else:
            index = 0

        return st.selectbox(
            format_field_label(field_name),
            options=enum_values,
            index=index,
            key=f"{entity_name}_{field_name}",
            help=field.get("help"),
        )

    # ========================================================
    # STRING
    # ========================================================

    if field_type == "str":

        return st.text_input(
            format_field_label(field_name),
            value="" if existing_value is None else str(existing_value),
            key=f"{entity_name}_{field_name}",
            help=field.get("help"),
        )

    # ========================================================
    # EMAIL
    # ========================================================

    if field_type == "email":

        return st.text_input(
            format_field_label(field_name),
            value="" if existing_value is None else str(existing_value),
            key=f"{entity_name}_{field_name}",
            help=field.get("help"),
        )

    # ========================================================
    # TEXT
    # ========================================================

    if field_type == "text":

        return st.text_area(
            format_field_label(field_name),
            value="" if existing_value is None else str(existing_value),
            key=f"{entity_name}_{field_name}",
            help=field.get("help"),
        )

    # ========================================================
    # INTEGER
    # ========================================================

    if field_type == "int":

        default = field.get("default")

        if existing_value is not None:
            default = existing_value

        if default is None:
            default = 0

        return st.number_input(
            format_field_label(field_name),
            value=int(default),
            step=1,
            key=f"{entity_name}_{field_name}",
            help=field.get("help"),
        )

    # ========================================================
    # DECIMAL
    # ========================================================

    if field_type == "decimal":

        default = field.get("default")

        if existing_value is not None:
            default = existing_value

        if default is None:
            default = 0.0

        return st.number_input(
            format_field_label(field_name),
            value=float(default),
            step=0.01,
            key=f"{entity_name}_{field_name}",
            help=field.get("help"),
        )

    # ========================================================
    # BOOLEAN
    # ========================================================

    if field_type == "bool":

        default = field.get(
            "default",
            False,
        )

        if existing_value is not None:
            default = bool(existing_value)

        return st.checkbox(
            format_field_label(field_name),
            value=default,
            key=f"{entity_name}_{field_name}",
            help=field.get("help"),
        )

    # ========================================================
    # DATE
    # ========================================================

    if field_type == "date":

        import datetime

        default = existing_value

        if default is None:
            default = datetime.date.today()

        elif isinstance(default, str):
            try:
                default = datetime.date.fromisoformat(default)
            except ValueError:
                default = datetime.date.today()

        return st.date_input(
            format_field_label(field_name),
            value=default,
            key=f"{entity_name}_{field_name}",
            help=field.get("help"),
        )

    # ========================================================
    # DATETIME
    # ========================================================

    if field_type == "datetime":

        import datetime

        default = existing_value

        if default is None:
            default = datetime.datetime.now()

        elif isinstance(default, str):
            try:
                default = datetime.datetime.fromisoformat(default)
            except ValueError:
                default = datetime.datetime.now()

        return st.datetime_input(
            format_field_label(field_name),
            value=default,
            key=f"{entity_name}_{field_name}",
            help=field.get("help"),
        )

    # ========================================================
    # JSON
    # ========================================================

    if field_type == "json":

        import json

        if existing_value is None:
            default_text = ""
        elif isinstance(existing_value, str):
            default_text = existing_value
        else:
            default_text = json.dumps(
                existing_value,
                indent=2,
            )

        return st.text_area(
            format_field_label(field_name),
            value=default_text,
            key=f"{entity_name}_{field_name}",
            help=field.get("help"),
            height=150,
        )

    # ========================================================
    # FALLBACK
    # ========================================================

    return st.text_input(
        format_field_label(field_name),
        value="" if existing_value is None else str(existing_value),
        key=f"{entity_name}_{field_name}",
        help=field.get("help"),
    )


# ============================================================
# RENDER ENTITY FORM
# ============================================================

def render_entity_form(
    entity_name,
    existing_record=None,
):
    """
    Render the complete create/update form.

    existing_record:
        None -> create mode

        dict -> update mode
    """

    entity = ENTITIES[entity_name]

    is_update = existing_record is not None

    if is_update:
        st.subheader(f"Edit {entity_name}")
    else:
        st.subheader(f"Create {entity_name}")

    values = {}

    for field in entity["fields"]:

        field_name = field["name"]

        existing_value = None

        if existing_record:
            existing_value = existing_record.get(
                field_name
            )

        value = render_field(
            entity_name=entity_name,
            field=field,
            existing_value=existing_value,
        )

        values[field_name] = value

    # --------------------------------------------------------
    # UPDATE-ONLY FIELDS
    # --------------------------------------------------------

    if is_update:

        for field in entity.get(
            "extra_update_fields",
            [],
        ):

            field_name = field["name"]

            existing_value = existing_record.get(
                field_name,
                True,
            )

            values[field_name] = render_field(
                entity_name=entity_name,
                field=field,
                existing_value=existing_value,
            )

    return values