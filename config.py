"""Snowflake connection configuration for the emekamarkt pipeline.

dbt reads Snowflake settings from environment variables via emekamarkt/profiles.yml.
This module reuses the same variables so you can run a standalone connectivity
check (and reuse the same credentials for the Tableau connection):

    python config.py        # prints Snowflake version if credentials are valid
"""

from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass
class SnowflakeConfig:
    account: str
    user: str
    password: str
    role: str = "TRANSFORMER"
    warehouse: str = "COMPUTE_WH"
    database: str = "EMEKAMARKT"
    schema: str = "PUBLIC"

    @classmethod
    def from_env(cls) -> "SnowflakeConfig":
        try:
            return cls(
                account=os.environ["SNOWFLAKE_ACCOUNT"],
                user=os.environ["SNOWFLAKE_USER"],
                password=os.environ["SNOWFLAKE_PASSWORD"],
                role=os.environ.get("SNOWFLAKE_ROLE", "TRANSFORMER"),
                warehouse=os.environ.get("SNOWFLAKE_WAREHOUSE", "COMPUTE_WH"),
                database=os.environ.get("SNOWFLAKE_DATABASE", "EMEKAMARKT"),
                schema=os.environ.get("SNOWFLAKE_SCHEMA", "PUBLIC"),
            )
        except KeyError as missing:
            raise SystemExit(
                f"Missing required environment variable: {missing}. "
                "Copy .env.example to .env and fill in your Snowflake credentials."
            )

    def connection_kwargs(self) -> dict:
        return {
            "account": self.account,
            "user": self.user,
            "password": self.password,
            "role": self.role,
            "warehouse": self.warehouse,
            "database": self.database,
            "schema": self.schema,
        }


def check_connection() -> str:
    """Connect to Snowflake and return the server version."""
    import snowflake.connector  # lazy import: only needed for the live check

    cfg = SnowflakeConfig.from_env()
    conn = snowflake.connector.connect(**cfg.connection_kwargs())
    try:
        cur = conn.cursor()
        cur.execute("select current_version()")
        (version,) = cur.fetchone()
        return version
    finally:
        conn.close()


if __name__ == "__main__":
    print(f"Connected to Snowflake. Version: {check_connection()}")
