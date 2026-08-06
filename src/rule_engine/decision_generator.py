from src.rule_engine.models import (
    ComplianceDecision,
    RuleEngineResult,
)


class DecisionGenerator:
    """
    Generates the final compliance decision
    from all evaluated rules.
    """

    def generate(
        self,
        result: RuleEngineResult,
    ) -> ComplianceDecision:

        requirements: list[str] = []
        warnings: list[str] = []
        blockers: list[str] = []

        status = "COMPLIANT"
        summary = (
            "Traveller meets all evaluated compliance requirements."
        )

        #
        # 1. Entry Restrictions (Highest Priority)
        #
        if (
            result.entry_restriction is not None
            and result.entry_restriction.restriction_type.upper()
            != "NONE"
        ):
            blockers.append(
                result.entry_restriction.reason
                or "Entry to the destination country is restricted."
            )

            return ComplianceDecision(
                status="ENTRY_RESTRICTED",
                summary=(
                    "Traveller is not permitted to enter "
                    "the destination country."
                ),
                requirements=requirements,
                warnings=warnings,
                blockers=blockers,
            )

        #
        # 2. Visa Requirements
        #
        if (
            result.visa is not None
            and result.visa.visa_required
        ):
            status = "ACTION_REQUIRED"

            summary = (
                "Traveller must complete one or more "
                "requirements before travelling."
            )

            visa_type = (
                result.visa.visa_type
                if result.visa.visa_type
                else "Visa"
            )

            requirements.append(
                f"Obtain {visa_type} before travelling."
            )

        #
        # 3. Passport Requirements
        #
        if result.passport is not None:

            if result.passport.minimum_validity_months:
                requirements.append(
                    "Passport must be valid for at least "
                    f"{result.passport.minimum_validity_months} months."
                )

            if result.passport.blank_pages_required:
                requirements.append(
                    "Passport must contain at least "
                    f"{result.passport.blank_pages_required} blank pages."
                )

            if result.passport.machine_readable_required:
                requirements.append(
                    "Passport must be machine readable."
                )

            if not result.passport.temporary_passport_allowed:
                warnings.append(
                    "Temporary passports are not accepted."
                )

        #
        # 4. Health Requirements
        #
        if result.health is not None:

            if result.health.health_form_required:
                requirements.append(
                    "Complete the required health declaration form."
                )

            if result.health.quarantine_required:
                requirements.append(
                    "Complete the required quarantine period."
                )

            if result.health.medical_certificate_required:
                requirements.append(
                    "Carry the required medical certificate."
                )

            for vaccine in result.health.vaccines:

                if vaccine.certificate_required:
                    requirements.append(
                        f"Carry a valid {vaccine.vaccine_name} vaccination certificate."
                    )
                else:
                    warnings.append(
                        f"{vaccine.vaccine_name} vaccination is recommended."
                    )

        #
        # 5. Immigration Requirements
        #
        if result.immigration is not None:

            if result.immigration.onward_ticket_required:
                requirements.append(
                    "Carry proof of onward or return travel."
                )

            if result.immigration.accommodation_proof_required:
                requirements.append(
                    "Carry proof of accommodation."
                )

            if result.immigration.proof_of_funds_required:
                requirements.append(
                    "Carry proof of sufficient funds."
                )

            if result.immigration.biometric_required:
                requirements.append(
                    "Complete biometric verification."
                )

            if result.immigration.interview_required:
                requirements.append(
                    "Attend the required immigration interview."
                )

            if result.immigration.arrival_card_required:
                requirements.append(
                    "Complete the arrival card."
                )

            if result.immigration.digital_arrival_card:
                requirements.append(
                    "Complete the digital arrival card."
                )

            if result.immigration.arrival_registration_required:
                requirements.append(
                    "Complete the required arrival registration."
                )

        #
        # 6. Transit Requirements
        #
        if result.transit is not None:

            if result.transit.transit_visa_required:
                requirements.append(
                    "Obtain the required transit visa."
                )

            if not result.transit.airside_transit_allowed:
                warnings.append(
                    "Airside transit is not permitted."
                )

            if result.transit.baggage_collection_required:
                requirements.append(
                    "Collect and re-check baggage during transit."
                )

            if not result.transit.overnight_transit_allowed:
                warnings.append(
                    "Overnight transit is not permitted."
                )

        #
        # 7. Customs Requirements
        #
        if result.customs is not None:

            if result.customs.currency_declaration_required:
                requirements.append(
                    "Declare currency exceeding the permitted limit."
                )

            if result.customs.medication_rules:
                warnings.append(
                    "Ensure prescription medicines comply with destination regulations."
                )

            if result.customs.pet_import_rules:
                warnings.append(
                    "Verify pet import requirements before travelling."
                )

        #
        # Final Decision
        #
        return ComplianceDecision(
            status=status,
            summary=summary,
            requirements=requirements,
            warnings=warnings,
            blockers=blockers,
        )