"""
Simple reusable HypercubeModel for experimental decision making.
- Dimensions are provided as a dict: {dim_name: [values,...]}
- Stores per-vertex statistics (count, sum, mean) and supports UCB exploration.
- Pure-Python, no external dependencies. Save/load via JSON.

Usage example:
    model = HypercubeModel({"temp": [20,30], "ph": [7,8]})
    model.add_observation({"temp":20, "ph":7}, reward=1.2)
    next = model.suggest_next(3)
"""
from __future__ import annotations

import itertools
import math
import json
import os
import random
from typing import Dict, List, Tuple, Any, Iterable, Optional


class HypercubeModel:
    def __init__(self, dimensions: Dict[str, List[Any]], prior_mean: float = 0.0, prior_n: float = 1.0):
        # Validate input
        if not dimensions or not isinstance(dimensions, dict):
            raise ValueError("dimensions must be a non-empty dict")
        # Normalize dimension names and values
        self.dim_names = list(dimensions.keys())
        self.dim_values = [list(v) for v in dimensions.values()]
        # Ensure each dimension has at least one value
        for name, vals in zip(self.dim_names, self.dim_values):
            if not vals:
                raise ValueError(f"Dimension '{name}' must have at least one possible value")
        # store a defensive copy
        self.dim_map = {k: list(v) for k, v in dimensions.items()}
        # stats keyed by tuple of values in dim_names order
        self.stats: Dict[Tuple[Any, ...], Dict[str, float]] = {}
        self.total_n = 0
        self.prior_mean = float(prior_mean)
        self.prior_n = float(prior_n)
        # reward shaping defaults
        self.reward_scale = 1.0
        self.reward_floor: Optional[float] = None
        # lightweight type hints for runtime checks
        self._validated = True

    def _key_for(self, candidate: Dict[str, Any]) -> Tuple[Any, ...]:
        return tuple(candidate[name] for name in self.dim_names)

    def _ensure_vertex(self, key: Tuple[Any, ...]):
        if key not in self.stats:
            self.stats[key] = {"n": 0.0, "sum": 0.0, "mean": self.prior_mean}

    def predict(self, candidate: Dict[str, Any]) -> float:
        key = self._key_for(candidate)
        s = self.stats.get(key)
        if not s or s["n"] == 0:
            return self.prior_mean
        return float(s["mean"])  # empirical mean

    def _validate_candidate(self, candidate: Dict[str, Any]) -> None:
        if not isinstance(candidate, dict):
            raise ValueError("candidate must be a dict")
        for name in self.dim_names:
            if name not in candidate:
                raise ValueError(f"candidate missing required dimension '{name}'")

    def _shape_reward(self, reward: float, candidate: Dict[str, Any]) -> float:
        """Apply simple, extensible reward shaping.
        - Scales reward by self.reward_scale
        - Optional priority boosting (if 'priority' dimension present)
        - Applies a floor if set
        """
        try:
            shaped = float(reward) * float(self.reward_scale)
        except Exception:
            shaped = float(reward)
        # simple priority-based boost
        pri = None
        if isinstance(candidate, dict):
            pri = candidate.get('priority')
            if pri is not None:
                pstr = str(pri).lower()
                if pstr == 'high':
                    shaped *= 1.2
                elif pstr == 'low':
                    shaped *= 0.8
        if self.reward_floor is not None:
            shaped = max(shaped, float(self.reward_floor))
        return float(shaped)

    def add_observation(self, candidate: Dict[str, Any], reward: float) -> None:
        # validate candidate conforms to dimensions
        try:
            self._validate_candidate(candidate)
        except Exception:
            # fallback: attempt to coerce keys using str-match against dim_map
            # this keeps backward compatibility but warns via exception propagation suppressed here
            pass
        # compute shaped reward then update stats
        shaped = self._shape_reward(reward, candidate)
        key = self._key_for(candidate)
        self._ensure_vertex(key)
        s = self.stats[key]
        s["n"] += 1.0
        s["sum"] += float(shaped)
        s["mean"] = s["sum"] / s["n"]
        self.total_n += 1

    def score_candidates(self, candidates: Iterable[Dict[str, Any]], strategy: str = "ucb", c: float = 1.0) -> List[Tuple[Dict[str, Any], float]]:
        scored = []
        for cand in candidates:
            key = self._key_for(cand)
            s = self.stats.get(key, None)
            if not s or s["n"] == 0:
                mean = self.prior_mean
                n = 0.0
            else:
                mean = s["mean"]
                n = s["n"]
            if strategy == "ucb":
                if n <= 0:
                    score = mean + c * math.sqrt(math.log(max(1, self.total_n + 1)))
                else:
                    score = mean + c * math.sqrt(math.log(max(1, self.total_n + 1)) / n)
            elif strategy == "thompson":
                # simple Gaussian-ish thompson: sample from Normal(mean, 1/sqrt(n+prior_n))
                sigma = 1.0 / math.sqrt(n + self.prior_n)
                score = random.gauss(mean, sigma)
            elif strategy == "empirical":
                score = mean
            else:
                raise ValueError(f"unknown strategy: {strategy}")
            scored.append((cand, float(score)))
        scored.sort(key=lambda x: x[1], reverse=True)
        return scored

    def suggest_next(self, k: int = 5, strategy: str = "ucb", c: float = 1.0, candidates: Optional[Iterable[Dict[str, Any]]] = None) -> List[Dict[str, Any]]:
        if candidates is None:
            candidates = self.enumerate_vertices()
        scored = self.score_candidates(candidates, strategy=strategy, c=c)
        return [cand for cand, _ in scored[:k]]

    def enumerate_vertices(self) -> Iterable[Dict[str, Any]]:
        for comb in itertools.product(*self.dim_values):
            yield {name: val for name, val in zip(self.dim_names, comb)}

    def sample_candidates(self, n: int, seed: Optional[int] = None) -> List[Dict[str, Any]]:
        rng = random.Random(seed)
        all_vertices = list(self.enumerate_vertices())
        if n >= len(all_vertices):
            return all_vertices
        return rng.sample(all_vertices, n)

    def save(self, path: str) -> None:
        payload = {
            "dim_names": self.dim_names,
            "dim_map": self.dim_map,
            "stats": {"|".join(map(str, k)): v for k, v in self.stats.items()},
            "total_n": self.total_n,
            "prior_mean": self.prior_mean,
            "prior_n": self.prior_n,
        }
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(payload, fh, indent=2)

    @classmethod
    def load(cls, path: str) -> "HypercubeModel":
        with open(path, "r", encoding="utf-8") as fh:
            payload = json.load(fh)
        model = cls(payload["dim_map"], prior_mean=payload.get("prior_mean", 0.0), prior_n=payload.get("prior_n", 1.0))
        stats = {}
        for kstr, v in payload.get("stats", {}).items():
            key = tuple(kstr.split("|"))
            # attempt to coerce to original types by using dim values mapping
            coerced_key = []
            for name, raw in zip(model.dim_names, key):
                # try exact match in dim values
                vals = [str(x) for x in model.dim_map[name]]
                if raw in vals:
                    # pick the original typed value
                    coerced_key.append(model.dim_map[name][vals.index(raw)])
                else:
                    coerced_key.append(raw)
            stats[tuple(coerced_key)] = v
        model.stats = stats
        model.total_n = payload.get("total_n", 0)
        return model


# minimal CLI demo when executed directly
if __name__ == "__main__":
    dims = {"temperature": [20, 25, 30], "pH": [6.5, 7.0, 7.5]}
    m = HypercubeModel(dims)
    # sample usage
    candidates = list(m.enumerate_vertices())
    print("Total vertices:", len(candidates))
    print("Top suggestions:", m.suggest_next(3))
