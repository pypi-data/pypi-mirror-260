from dataclasses import dataclass, field
from typing import Set, List, Optional, Dict, Any

import numpy as np
import pandas as pd
import pyomo.environ as pyo
# noinspection PyPackageRequirements
from descriptors import classproperty

from powerplantsim.datatypes.node import Node
from powerplantsim.utils.typing import Flow, State


@dataclass(frozen=True, repr=False, eq=False, unsafe_hash=False, kw_only=True)
class Storage(Node):
    """A node in the plant that stores certain commodities."""

    commodity: str = field(kw_only=True)
    """The commodity stored by the machine."""

    capacity: float = field(kw_only=True)
    """The storage capacity, which must be a strictly positive and finite number."""

    dissipation: float = field(kw_only=True)
    """The dissipation rate of the storage at every time unit, which must be a float in [0, 1]."""

    charge_rate: float = field(kw_only=True)
    """The maximal charge rate (input flow) in a time unit."""

    discharge_rate: float = field(kw_only=True)
    """The maximal discharge rate (output flow) in a time unit."""

    _storage: List[float] = field(init=False, default_factory=list)
    """The series of actual commodities storage, which is filled during the simulation."""

    def __post_init__(self):
        self._info['current_storage'] = None
        assert self.capacity != float('inf'), "Capacity should be a finite number, got inf"
        assert self.capacity > 0.0, f"Capacity should be strictly positive, got {self.capacity}"
        assert self.charge_rate > 0.0, f"Charge rate should be strictly positive, got {self.charge_rate}"
        assert self.discharge_rate > 0.0, f"Discharge rate should be strictly positive, got {self.discharge_rate}"
        assert 0.0 <= self.dissipation <= 1.0, f"Dissipation should be in range [0, 1], got {self.dissipation}"

    @classproperty
    def kind(self) -> str:
        return 'storage'

    @classproperty
    def _properties(self) -> List[str]:
        properties = super(Storage, self)._properties
        return properties + [
            'commodity',
            'capacity',
            'dissipation',
            'charge_rate',
            'discharge_rate',
            'storage',
            'current_storage'
        ]

    @property
    def storage(self) -> pd.Series:
        """The series of actual commodities storage, which is filled during the simulation."""
        return pd.Series(self._storage, dtype=float, index=self._horizon[:len(self._storage)])

    @property
    def current_storage(self) -> Optional[float]:
        """The current storage of the node for this time step."""
        return self._info['current_storage']

    @property
    def commodities_in(self) -> Set[str]:
        return {self.commodity}

    @property
    def commodities_out(self) -> Set[str]:
        return {self.commodity}

    # noinspection PyTypeChecker
    def to_pyomo(self, mutable: bool = False) -> pyo.Block:
        # start from the default node block and create aliases for the flows of the (unique) commodity
        node = super(Storage, self).to_pyomo(mutable=mutable)
        in_flow, out_flow = node.in_flows[self.commodity], node.out_flows[self.commodity]
        # add a parameter representing the current storage (and initialize it if needed)
        kwargs = dict(mutable=True) if mutable else dict(initialize=self.current_storage)
        node.current_storage = pyo.Param(domain=pyo.NonNegativeReals, **kwargs)
        # model the storage as the sum of between the current storage and the input and output flows
        node.storage = node.current_storage + in_flow - out_flow
        node.capacity_lb = pyo.Constraint(rule=node.storage >= 0)
        node.capacity_ub = pyo.Constraint(rule=node.storage <= self.capacity)
        # impose constraints on either input or output flows
        #  - create a binary variable where 0 means that there is an output flow, 1 means that there is an input flow
        #  - impose big-M constraints on input and output flows using the change/discharge rates as M
        #  - charge/discharge rates are lower bounded by remaining storage (capacity - current storage) and current
        #    storage (or total capacity if not available) to account for the fact that they can have infinite values
        #  - this definition automatically allow to impose the charge/discharge rate upper bounds
        charge_rate = min(self.capacity - (0 if mutable else self.current_storage), self.charge_rate)
        discharge_rate = min(self.capacity if mutable else self.current_storage, self.discharge_rate)
        node.flow_selector = pyo.Var(domain=pyo.Binary, initialize=0)
        node.input_flow_cst = pyo.Constraint(rule=in_flow <= node.flow_selector * charge_rate)
        node.output_flow_cst = pyo.Constraint(rule=out_flow <= (1 - node.flow_selector) * discharge_rate)
        return node

    def update(self, rng: np.random.Generator, flows: Dict[Any, Flow], states: Dict[Any, State]):
        self._info['current_storage'] = 0.0 if len(self._storage) == 0 else (1 - self.dissipation) * self._storage[-1]

    def step(self, flows: Dict[Any, Flow], states: Dict[Any, State]):
        # compute total input and output flows from respective edges
        in_flow, out_flow = 0.0, 0.0
        for edge, flow in flows.items():
            in_flow += flow if edge.destination == self.name else 0.0
            out_flow += flow if edge.source == self.name else 0.0
        # check that at least one of the two is null as from the constraints
        assert in_flow == 0.0 or out_flow == 0.0, \
            f"Storage node '{self.name}' can have either input or output flows in a single time step, got both"
        # check that the input and output flows are compatible with the charge rates
        assert in_flow <= self.charge_rate + self.eps, \
            f"Storage node '{self.name}' should have maximal input flow {self.charge_rate}, got {in_flow}"
        assert out_flow <= self.discharge_rate + self.eps, \
            f"Storage node '{self.name}' should have maximal output flow {self.discharge_rate}, got {out_flow}"
        # compute and check new storage from previous one (discounted by 1 - dissipation) and difference between flows
        storage = self._info['current_storage'] + in_flow - out_flow
        assert storage >= -self.eps, f"Storage node '{self.name}' cannot contain negative amount, got {storage}"
        assert storage <= self.capacity + self.eps, \
            f"Storage node '{self.name}' cannot contain more than {self.capacity} amount, got {storage}"
        self._storage.append(np.clip(storage, a_min=0, a_max=self.capacity))
        self._info['current_storage'] = None
