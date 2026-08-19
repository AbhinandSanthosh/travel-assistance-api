from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str
    app_version: str
    app_env: str
    debug: bool

    host: str
    port: int

    database_url: str
    secret_key: str
    access_token_expire_minutes: int

    # --- Data protection (Phase 4.3) --------------------------------------
    # database_url is the app's RUNTIME connection -- intended to be a
    # least-privilege role with SELECT/INSERT/UPDATE/DELETE on
    # application tables only (see scripts/setup_least_privilege_db_role.sql),
    # no DDL, no superuser. migration_database_url is a SEPARATE,
    # elevated connection used ONLY by Alembic (alembic/env.py) to run
    # schema migrations, since CREATE TABLE/ALTER TABLE genuinely needs
    # privileges the running app should never hold. Falls back to
    # database_url when unset, so this stays optional for anyone who
    # hasn't split the roles yet -- but for that fallback case to work,
    # database_url would need elevated privileges again, which defeats
    # the point; set this explicitly once the least-privilege role is
    # provisioned.
    migration_database_url: str | None = None

    redis_url: str = "redis://localhost:6379/0"

    # --- Security (Phase 1) ---------------------------------------------
    # Comma-separated IPs of reverse proxies/load balancers allowed to set
    # X-Forwarded-For. Empty (default) = trust nothing, always use the
    # direct socket peer. Fill in once you know what sits in front of
    # this in prod (nginx/ALB/Cloudflare/etc).
    trusted_proxy_ips: str = ""

    # Comma-separated browser origins allowed to call this API cross-origin.
    # Empty (default) = no browser origin is allowed. The bundled Streamlit
    # frontend calls the API server-to-server and doesn't need this; set it
    # only if/when a JS frontend is added.
    cors_allowed_origins: str = ""

    # Comma-separated hostnames this API will answer requests for.
    # Defaults to local dev only -- add your real domain(s) in prod.
    allowed_hosts: str = "localhost,127.0.0.1"

    # Max failed-attempt-inclusive login requests per IP per 60s window.
    login_rate_limit_per_minute: int = 10

    # Hard cap on request body size, in bytes. No endpoint currently
    # accepts file uploads, so 1MB comfortably covers real JSON payloads
    # while blocking oversized-body DoS attempts.
    max_request_body_bytes: int = 1_000_000
    # --- Security (Phase 2) ---------------------------------------------
    # Refresh token lifetime. Access tokens stay at
    # access_token_expire_minutes (unchanged, 60min) -- refresh tokens
    # are the long-lived credential now, and unlike access tokens they
    # ARE individually revocable (logout/password change/role change).
    refresh_token_expire_days: int = 7
    # --- Observability (Phase 3) -----------------------------------------
    # "text" (human-readable, current behavior) or "json" (structured,
    # for shipping into a log aggregator). Console output is unaffected
    # either way -- this only changes the two file handlers.
    log_format: str = "text"
    # Optional webhook URL (Slack-compatible incoming webhook, or any
    # endpoint that accepts a JSON POST) for security alerts. Unset by
    # default -- alert conditions are still logged at ERROR either way,
    # this just adds a push notification on top once you have somewhere
    # to send it.
    alert_webhook_url: str = ""
    # How many occurrences of the same event from the same source
    # within one minute before an alert fires. One alert per window,
    # not one per occurrence, so a sustained attack doesn't spam.
    alert_threshold_per_minute: int = 5
    # --- Data retention (Phase 4) -----------------------------------------
    # High-volume operational logs -- safe to purge automatically, no
    # legal/audit hold on these. Not the compliance decision record
    # itself (see compliance_checks below).
    api_request_log_retention_days: int = 90
    rule_execution_log_retention_days: int = 90
    # The actual compliance decisions (compliance_checks) and the admin
    # action trail (audit_logs) are the audit surface a regulator or
    # enterprise client would ask for. Still deliberately NOT purged
    # by the default script run -- --include-compliance-checks /
    # --include-audit-logs must be passed explicitly, even with a
    # retention window set below, so a stray cron invocation can't
    # silently start deleting the compliance evidence trail.
    #
    # Defaults below are a placeholder, not a legal conclusion: no
    # single retention law governs these tables (compliance_checks
    # contains no PNR-equivalent traveller-identity data, so the EU
    # PNR Directive's 5-year figure isn't a direct citation here).
    # The real drivers are contract/liability exposure -- how long a
    # client could plausibly dispute a decision -- and, for
    # audit_logs, standard security-review expectations (SOC2/ISO
    # 27001 reviewers commonly expect >=1 year). 3 years / 2 years is
    # a conservative starting point pending confirmation from
    # whoever handles contracts/legal -- check existing client
    # MSAs first, they may already specify a number.
    compliance_check_retention_days: int = 1095  # ~3 years
    audit_log_retention_days: int = 730  # ~2 years

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )

    @property
    def trusted_proxy_ip_list(self) -> list[str]:
        return [ip.strip() for ip in self.trusted_proxy_ips.split(",") if ip.strip()]

    @property
    def cors_allowed_origin_list(self) -> list[str]:
        return [
            origin.strip()
            for origin in self.cors_allowed_origins.split(",")
            if origin.strip()
        ]

    @property
    def allowed_host_list(self) -> list[str]:
        return [host.strip() for host in self.allowed_hosts.split(",") if host.strip()]


settings = Settings()