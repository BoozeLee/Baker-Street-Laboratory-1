Connecting Ollama and Credential Broker (Baker Street Lab)

This document describes steps to connect a real Ollama model and the local credential broker so the ResearchOrchestrator can run end-to-end.

1. Ollama model
- Install and run Ollama according to its docs.
- Ensure Ollama HTTP API is reachable from the application host.
- Configure any model names in core/config or environment variables (e.g., OLLAMA_URL, OLLAMA_MODEL).

2. Credential Broker
- Deploy a local credential broker that exposes /api/v1/broker/token to mint ephemeral tokens for agents.
- The orchestrator expects the broker at http://localhost:5000 by default; change in core.config as needed.
- The token endpoint should accept JSON {"agent_id": "...", "scope": "..."} and return {"token": "..."}.

3. ResearchOrchestrator configuration
- Update core/config to include broker URL and Ollama settings.
- Ensure network access and any API keys are set in environment variables.

4. Running end-to-end
- Start broker and Ollama services.
- Run the orchestrator: set PYTHONPATH=implementation/src and execute a script that calls ResearchOrchestrator.conduct_research.

5. Security
- Protect broker endpoints and tokens.
- Use TLS for production deployments.
