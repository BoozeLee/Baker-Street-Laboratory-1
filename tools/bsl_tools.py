"""Baker Street Laboratory Custom Tools for parllama"""
import json
import os
import subprocess
from datetime import datetime
from pathlib import Path

# Baker Street Lab research directory
RESEARCH_DIR = Path("/home/kilisan/bakerstreet-labs-repos/Baker-Street-Laboratory-1/research")
IMPLEMENTATION_DIR = Path("/home/kilisan/bakerstreet-labs-repos/Baker-Street-Laboratory-1/implementation")

def list_research_reports():
    """List all research reports in the research directory."""
    reports = []
    for f in RESEARCH_DIR.glob("research_report_*.md"):
        reports.append({
            "name": f.name,
            "size": f.stat().st_size,
            "created": datetime.fromtimestamp(f.stat().st_ctime).isoformat()
        })
    return reports

def read_research_report(report_name):
    """Read a specific research report."""
    report_path = RESEARCH_DIR / f"research_report_{report_name}.md"
    if report_path.exists():
        return report_path.read_text()
    return f"Report not found: {report_name}"

def run_research_query(query):
    """Run a research query through the Baker Street API."""
    import urllib.request
    import urllib.error
    try:
        url = "http://localhost:5000/api/v1/research/conduct"
        data = json.dumps({"query": query}).encode("utf-8")
        req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.URLError as e:
        return {"error": str(e)}

def check_system_status():
    """Check Baker Street Lab system status."""
    try:
        url = "http://localhost:5000/api/v1/system/health"
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=5) as resp:
            return json.loads(resp.read().decode())
    except Exception as e:
        return {"error": str(e)}

def list_ollama_models():
    """List all downloaded Ollama models."""
    try:
        import urllib.request
        url = "http://localhost:11434/api/tags"
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode())
            return data.get("models", [])
    except Exception as e:
        return {"error": str(e)}

def get_weather_info():
    """Placeholder for weather API integration."""
    return "Weather integration placeholder - configure API key in .env"

TOOLS = {
    "list_research_reports": list_research_reports,
    "read_research_report": read_research_report,
    "run_research_query": run_research_query,
    "check_system_status": check_system_status,
    "list_ollama_models": list_ollama_models,
}
