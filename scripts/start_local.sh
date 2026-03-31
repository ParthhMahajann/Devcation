#!/usr/bin/env bash
# ╔══════════════════════════════════════════════════════════════╗
# ║  MedGraph AI — Full Local Stack Startup                     ║
# ║  Run from the repo root: bash scripts/start_local.sh        ║
# ╚══════════════════════════════════════════════════════════════╝
set -e

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

echo "═══════════════════════════════════════════════"
echo " MedGraph AI — Local TigerGraph CE Setup"
echo "═══════════════════════════════════════════════"

# ── 1. Start TigerGraph container ────────────────────────────────
echo ""
echo "[1/5] Starting TigerGraph CE container …"
docker compose up -d tigergraph

echo "      Waiting for TigerGraph to be ready (up to 120s) …"
for i in $(seq 1 24); do
  if curl -sf http://127.0.0.1:9000/echo > /dev/null 2>&1; then
    echo "      ✓ TigerGraph is ready."
    break
  fi
  sleep 5
  echo "      … still waiting ($((i*5))s)"
done

# ── 2. Create schema ──────────────────────────────────────────────
echo ""
echo "[2/5] Creating MedGraph schema …"
cd "$ROOT"
python tigergraph/setup.py

# ── 3. Seed data ──────────────────────────────────────────────────
echo ""
echo "[3/5] Loading seed data …"
python tigergraph/seed_data.py

# ── 4. Start FastAPI backend ──────────────────────────────────────
echo ""
echo "[4/5] Starting FastAPI backend …"
docker compose up -d backend

# ── 5. Done ───────────────────────────────────────────────────────
echo ""
echo "[5/5] ✓ All services running."
echo ""
echo "  GraphStudio  →  http://localhost:14240"
echo "  REST API     →  http://localhost:9000"
echo "  FastAPI docs →  http://localhost:8000/docs"
echo ""
echo "  Stop all:    docker compose down"
echo "  View logs:   docker compose logs -f"
