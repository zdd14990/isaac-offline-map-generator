"""Canonical ORIGINAL Caves-I topology composition."""

from __future__ import annotations

from dataclasses import dataclass

from .floor_init import Caves1TopologyInputs, derive_caves1_topology_inputs
from .topology import TopologyResearchResult, generate_topology_research


CAVES1_TOPOLOGY_STATUS = "CAVES1_TOPOLOGY_CONFIRMED_BINARY"


@dataclass(frozen=True)
class Caves1TopologyResult:
    generation_status: str
    inputs: Caves1TopologyInputs
    topology: TopologyResearchResult


def generate_caves1_topology(start_seed: int, difficulty: str) -> Caves1TopologyResult:
    inputs = derive_caves1_topology_inputs(start_seed, difficulty)
    return Caves1TopologyResult(
        CAVES1_TOPOLOGY_STATUS,
        inputs,
        generate_topology_research(inputs),
    )
