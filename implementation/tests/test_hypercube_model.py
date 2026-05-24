import unittest
import importlib.util
import os
import tempfile

HYPER_PATH = '/home/kilisan/bakerstreet-labs-repos/Baker-Street-Laboratory-1/tools/research/hypercube_model.py'

class TestHypercubeModel(unittest.TestCase):
    def load_model(self):
        spec = importlib.util.spec_from_file_location('hypercube_model', HYPER_PATH)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return mod.HypercubeModel

    def test_add_predict_save_load(self):
        HypercubeModel = self.load_model()
        dims = {'temperature': [20,25], 'pH': [6.5,7.0]}
        m = HypercubeModel(dims, prior_mean=0.0, prior_n=1.0)
        m.add_observation({'temperature':20,'pH':6.5}, 1.2)
        m.add_observation({'temperature':25,'pH':7.0}, 0.8)
        self.assertAlmostEqual(m.predict({'temperature':20,'pH':6.5}), 1.2)
        self.assertAlmostEqual(m.predict({'temperature':25,'pH':7.0}), 0.8)

        # test save/load
        with tempfile.TemporaryDirectory() as td:
            path = os.path.join(td, 'hc.json')
            m.save(path)
            self.assertTrue(os.path.exists(path))
            loaded = HypercubeModel.load(path)
            self.assertAlmostEqual(loaded.predict({'temperature':20,'pH':6.5}), 1.2)

if __name__ == '__main__':
    unittest.main()
