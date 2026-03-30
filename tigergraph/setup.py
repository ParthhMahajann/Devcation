"""
TigerGraph MedGraph — Schema & Query Setup Script
Run: python tigergraph/setup.py
"""
import sys
import os
import pyTigerGraph as tg

# ─── Config ──────────────────────────────────────────────────────────────────
HOST      = os.getenv("TG_HOST",      "https://tg-361a97df-0a30-49f7-a48b-d6d17a66a07c.tg-3452941248.i.tgcloud.io")
SECRET    = os.getenv("TG_SECRET",    "21Krw_szE1qHBiNWa5skCubiw5UNUqBTgOUaDwsc")
USERNAME  = os.getenv("TG_USERNAME",  "tigergraph")
PASSWORD  = os.getenv("TG_PASSWORD",  "")
GRAPH     = os.getenv("TG_GRAPHNAME", "MedGraph")
GS_PORT   = os.getenv("TG_GS_PORT",  "443")
RESTPP    = os.getenv("TG_RESTPP_PORT", "443")

SCHEMA_FILE  = os.path.join(os.path.dirname(__file__), "schema", "create_schema.gsql")
QUERIES_DIR  = os.path.join(os.path.dirname(__file__), "queries")

QUERY_FILES = [
    # Core queries
    "diagnose_from_symptoms.gsql",
    "check_drug_interactions.gsql",
    "find_treatment_path.gsql",
    "patient_risk_profile.gsql",
    "get_graph_stats.gsql",
    "explore_subgraph.gsql",
    # Advanced queries (v2.0)
    "pharmacogenomics_report.gsql",
    "disease_progression_risk.gsql",
    "comorbidity_cluster.gsql",
    "contraindication_safety_check.gsql",
]

def connect():
    print(f"Connecting to TigerGraph at {HOST} …")
    conn = tg.TigerGraphConnection(
        host=HOST,
        graphname=GRAPH,
        gsPort=GS_PORT,
        restppPort=RESTPP,
        username=USERNAME,
        password=PASSWORD,
    )
    try:
        token = conn.getToken(SECRET)
        print(f"  Token obtained: {str(token)[:30]}…")
    except Exception as e:
        print(f"  Warning: could not get token: {e}")
    return conn


def run_gsql_file(conn, path, label):
    with open(path) as f:
        gsql = f.read()
    print(f"  Running {label} …", end=" ", flush=True)
    try:
        result = conn.gsql(gsql)
        print("OK")
        if result:
            print(f"    {str(result)[:200]}")
        return True
    except Exception as e:
        print(f"FAILED: {e}")
        return False


def step_schema(conn):
    print("\n[1/3] Creating schema …")
    return run_gsql_file(conn, SCHEMA_FILE, "create_schema.gsql")


def step_queries(conn):
    print("\n[2/3] Installing queries …")
    ok = True
    for qf in QUERY_FILES:
        path = os.path.join(QUERIES_DIR, qf)
        if not os.path.exists(path):
            print(f"  SKIP {qf} (file not found)")
            continue
        ok &= run_gsql_file(conn, path, qf)
    return ok


def step_install(conn):
    print("\n[3/3] Compiling & installing all queries …")
    try:
        result = conn.gsql(f"USE GRAPH {GRAPH}\nINSTALL QUERY ALL")
        print("  OK")
        if result:
            print(f"  {str(result)[:300]}")
    except Exception as e:
        print(f"  FAILED: {e}")


def main():
    if not PASSWORD:
        print("ERROR: TG_PASSWORD is not set.")
        print("Run:  TG_PASSWORD=yourpassword python tigergraph/setup.py")
        sys.exit(1)

    conn = connect()
    schema_ok = step_schema(conn)
    if not schema_ok:
        print("\nSchema creation failed. The graph may already exist — continuing with queries.")
    step_queries(conn)
    step_install(conn)
    print("\nDone.")


if __name__ == "__main__":
    main()
