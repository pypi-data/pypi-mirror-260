from typing import List

import numpy as np
from tqdm import tqdm
from .base import Component
from .fpt import FixedPointType as FPT


class Serial:
    def __init__(self, components: List[Component], fpt_out: FPT, generator: Component = None):
        self.components = components
        self.first_node = components[0]
        self.last_node = components[-1]
        self.generator = generator
        self.fpt_out = fpt_out

        if fpt_out.bw != self.last_node.bwout:
            raise ValueError("Specified FPT output does not match last node's output bit width")

        for i in range(1, len(self.components)):
            self.components[-i-1].connect(components[-i])

        if self.generator:
            self.generator.connect(self.first_node)

    def run_generator(self, clocks: int, pb: bool = True):
        if not self.generator:
            raise RuntimeError(f"{self.__class__.__name__}.generator is not specified")
        output = []
        for _ in tqdm(range(clocks), disable=not pb):
            self.generator.step()
            output.append(
                self.fpt_out.to_float(self.last_node.bdataout)
            )
        return np.asarray(output)

    def run(self, data: np.ndarray = None):
        raise NotImplementedError

