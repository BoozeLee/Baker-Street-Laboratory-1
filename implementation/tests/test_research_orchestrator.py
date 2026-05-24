import unittest
import importlib.util
import sys
import os
import types
import asyncio
import tempfile

# ensure implementation src is on path
repo_src = os.path.join(os.path.dirname(__file__), '..', 'src')
if repo_src not in sys.path:
    sys.path.insert(0, repo_src)

# inject ai.ollama_client stub to avoid external dependency
ai_mod = types.ModuleType('ai')
ollama_mod = types.ModuleType('ai.ollama_client')
class OllamaClient:
    def __init__(self):
        pass
    async def initialize(self):
        return False
    async def analyze_research_query(self, query):
        return {'success': False}
    async def synthesize_research_findings(self, findings, query):
        return {'success': False}
ollama_mod.OllamaClient = OllamaClient
sys.modules['ai'] = ai_mod
sys.modules['ai.ollama_client'] = ollama_mod

OR_PATH = os.path.join(repo_src, 'orchestrator', 'research_orchestrator.py')

class TestResearchOrchestratorIntegration(unittest.TestCase):
    def load_orchestrator(self):
        spec = importlib.util.spec_from_file_location('research_orch', OR_PATH)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return mod.ResearchOrchestrator

    def test_conduct_research_saves_hypercube(self):
        ResearchOrchestrator = self.load_orchestrator()
        config = types.SimpleNamespace(agents=[], tools=[])
        orc = ResearchOrchestrator(config)

        async def _run():
            # monkeypatch token fetch
            async def _token(a,b):
                return 'dummy'
            orc._get_agent_token = _token
            orc.ollama_available = False
            with tempfile.TemporaryDirectory() as td:
                res = await orc.conduct_research('Unit test query', output_dir=td)
                self.assertIn('output_dir', res)
                files = os.listdir(td)
                # expect a hypercube_model json saved
                found = any(f.startswith('hypercube_model_') and f.endswith('.json') for f in files)
                self.assertTrue(found, f"Expected hypercube model saved in {td}, got: {files}")

        asyncio.run(_run())

if __name__ == '__main__':
    unittest.main()
