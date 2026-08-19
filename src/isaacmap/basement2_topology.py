"""Canonical ORIGINAL Basement II topology composition."""

from __future__ import annotations

from dataclasses import dataclass

from .floor_init import Basement2TopologyInputs, derive_basement2_topology_inputs
from .topology import TopologyResearchResult, generate_topology_research


BASEMENT2_TOPOLOGY_STATUS = "BASEMENT2_TOPOLOGY_CONFIRMED_BINARY"


@dataclass(frozen=True)
class Basement2TopologyResult:
    generation_status: str
    inputs: Basement2TopologyInputs
    topology: TopologyResearchResult


def generate_basement2_topology(
    start_seed: int, difficulty: str
) -> Basement2TopologyResult:
    inputs = derive_basement2_topology_inputs(start_seed, difficulty)
    return Basement2TopologyResult(
        BASEMENT2_TOPOLOGY_STATUS,
        inputs,
        generate_topology_research(inputs),
    )
