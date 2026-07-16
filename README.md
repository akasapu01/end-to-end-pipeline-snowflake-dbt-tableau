# End-to-End Pipeline: Snowflake + dbt + Tableau

![Snowflake](https://img.shields.io/badge/Snowflake-Warehouse-29B5E8?logo=snowflake)
![dbt](https://img.shields.io/badge/dbt-1.7-orange?logo=dbt)
![Tableau](https://img.shields.io/badge/Tableau-BI-E97627?logo=tableau)
![DuckDB](https://img.shields.io/badge/DuckDB-local%20verify-FFF000?logo=duckdb)

An end-to-end analytics engineering pipeline for **EmekaMarkt**, a retail /
supermarket business: raw sales data is loaded into **Snowflake**, modeled into a
**star schema** with **dbt** (staging → marts, with data tests), and served to
**Tableau** for dashboards.

The project ships with sample seed data so the whole pipeline runs out of the box —
either against Snowflake, or locally against **DuckDB** with no cloud account.

## Architecture

```
raw_sales (dbt seed)  ──▶  stg_sales (view)  ──▶  ┌ dim_customers ┐
   supermarket order lines    clean + type       │ dim_products  │  star schema
                                                  └ fact_sales ───┘        │
                                                        │                  ▼
                                          data tests (not_null, unique,   Tableau
                                          relationships, accepted_range,  dashboards
                                          assert_positive_quantity)
```

## Data model (star schema)

| Model | Type | Grain / description |
|-------|------|---------------------|
| `stg_sales` | view | Cleaned, typed order lines; trims whitespace, computes `line_total` |
| `dim_customers` | table | One row per customer + lifetime value, order count, first/last order |
| `dim_products` | table | One row per product + units sold and revenue |
| `fact_sales` | table | One row per order line; surrogate key, FKs to both dimensions |

## Tech stack

- **Snowflake** — cloud data warehouse
- **dbt Core 1.7** (dbt-snowflake) — transformation, testing, docs; `dbt_utils` for surrogate keys and range tests
- **Tableau** — BI / dashboards on the marts
- **DuckDB** (dbt-duckdb) — optional local target for running the pipeline without cloud

## Project structure

```
config.py                     # Snowflake connection helper + connectivity check
requirements.txt
.env.example                  # Snowflake credentials template
emekamarkt/                   # dbt project
  dbt_project.yml
  profiles.yml                # snowflake (dev) + duckdb targets
  packages.yml                # dbt_utils
  seeds/raw_sales.csv         # sample supermarket sales
  models/
    staging/stg_sales.sql + schema.yml
    marts/dim_customers.sql, dim_products.sql, fact_sales.sql + schema.yml
  tests/assert_positive_quantity.sql   # singular test: no negative quantities
```

## Setup

```bash
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env          # fill in your Snowflake credentials
```

Verify Snowflake connectivity (optional):
```bash
python config.py              # prints the Snowflake version
```

## Run the pipeline

```bash
cd emekamarkt
export DBT_PROFILES_DIR=$PWD

dbt deps                      # install dbt_utils
dbt seed                      # load raw_sales into the warehouse
dbt run                       # build staging + star schema
dbt test                      # run all data tests
dbt docs generate && dbt docs serve   # lineage + docs
```

### Run locally with no Snowflake account
The `duckdb` target builds the identical pipeline on your laptop:
```bash
cd emekamarkt
export DBT_PROFILES_DIR=$PWD
dbt deps
dbt build --target duckdb     # seed + run + test in one command
```
> Verified: `dbt build --target duckdb` produces 4 models and **22 passing tests**.

## Connect Tableau

1. In Tableau Desktop: **Connect → To a Server → Snowflake**.
2. Enter your Snowflake **Server** (`<account>.snowflakecomputing.com`), warehouse,
   and credentials (the same values as `.env`).
3. Choose the **`EMEKAMARKT`** database and the **`marts`** schema.
4. Drag in `fact_sales` and join to `dim_customers` (on `customer_id`) and
   `dim_products` (on `product_id`) to build the star-schema data source.
5. Build dashboards: revenue by category, top customers by lifetime value,
   daily sales trend, etc.

## Maintainer
**Jyothi Sree** — Senior Data Engineer
- Email: Jyothisree.work@gmail.com
- LinkedIn: https://www.linkedin.com/in/jyothisree123/
