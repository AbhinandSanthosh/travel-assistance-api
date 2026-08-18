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