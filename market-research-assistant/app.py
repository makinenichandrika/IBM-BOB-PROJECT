"""
app.py — Flask entry point for the Intelligent Market Research Assistant.
Exposes REST API endpoints consumed by the SPA frontend.
"""

import os
import logging
from datetime import datetime
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

# ─── Logging Setup ────────────────────────────────────────────────────────────
os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.FileHandler("logs/app.log"),
        logging.StreamHandler(),
    ]
)
logger = logging.getLogger(__name__)

# ─── Flask App ────────────────────────────────────────────────────────────────
app = Flask(__name__, static_folder="static", static_url_path="")
app.secret_key = os.getenv("FLASK_SECRET_KEY", "imra-secret-key-change-in-production")
CORS(app)

# ─── Lazy-load orchestrator (avoids slow import at startup) ───────────────────
_orchestrator = None

def get_orchestrator():
    global _orchestrator
    if _orchestrator is None:
        from agent.orchestrator import MarketResearchOrchestrator
        _orchestrator = MarketResearchOrchestrator()
    return _orchestrator


# ─── Routes ───────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    """Serve the main SPA."""
    return send_from_directory("static", "index.html")


@app.route("/api/health", methods=["GET"])
def health():
    """Health check endpoint."""
    orchestrator = get_orchestrator()
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "model": orchestrator.llm.model_id,
        "mode": "demo" if orchestrator.llm._demo_mode else "live",
        "tools": list(orchestrator.tools.keys())
    })


@app.route("/api/research", methods=["POST"])
def research():
    """
    Full market research pipeline endpoint.
    Accepts: industry, product, target_audience, location, competitors
    Returns: structured report with reasoning steps and ethics check
    """
    from agent.guardrails import validate_inputs, GuardrailViolation

    try:
        data = request.get_json(force=True)
        if not data:
            return jsonify({"status": "error", "message": "Request body must be JSON"}), 400

        # Guardrail: validate and sanitize inputs
        cleaned_inputs = validate_inputs(data)

        logger.info(
            f"Research request | industry={cleaned_inputs.get('industry')} "
            f"| location={cleaned_inputs.get('location')}"
        )

        # Run the agentic research pipeline
        orchestrator = get_orchestrator()
        result = orchestrator.run_research(cleaned_inputs)

        return jsonify(result)

    except GuardrailViolation as e:
        logger.warning(f"Guardrail violation: {e}")
        return jsonify({
            "status": "error",
            "message": str(e),
            "error_type": "guardrail_violation"
        }), 400

    except Exception as e:
        logger.error(f"Research pipeline error: {e}", exc_info=True)
        return jsonify({
            "status": "error",
            "message": "An unexpected error occurred. Please try again.",
            "error_type": "internal_error"
        }), 500


@app.route("/api/query", methods=["POST"])
def query():
    """
    Single Q&A endpoint for market research questions.
    Accepts: question (string)
    Returns: answer, warnings, elapsed_seconds
    """
    from agent.guardrails import validate_question, GuardrailViolation

    try:
        data = request.get_json(force=True)
        if not data or not data.get("question"):
            return jsonify({"status": "error", "message": "Field 'question' is required"}), 400

        # Guardrail: validate question
        clean_question = validate_question(data["question"])

        logger.info(f"Query request | question={clean_question[:60]}...")

        orchestrator = get_orchestrator()
        result = orchestrator.run_query(clean_question)

        return jsonify(result)

    except GuardrailViolation as e:
        logger.warning(f"Guardrail violation (query): {e}")
        return jsonify({
            "status": "error",
            "message": str(e),
            "error_type": "guardrail_violation"
        }), 400

    except Exception as e:
        logger.error(f"Query error: {e}", exc_info=True)
        return jsonify({
            "status": "error",
            "message": "An unexpected error occurred. Please try again.",
            "error_type": "internal_error"
        }), 500


# ─── Entry Point ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    port = int(os.getenv("FLASK_PORT", 5000))
    debug = os.getenv("FLASK_DEBUG", "False").lower() == "true"
    logger.info(f"Starting IMRA on http://localhost:{port}")
    logger.info("Press Ctrl+C to stop the server")
    app.run(host="0.0.0.0", port=port, debug=debug)
