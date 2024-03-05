import logging

import numpy as np

from .fpt import FixedPointType as FPT


class Component:
    """
    Base class for simulation component models. Implements basic operations like logging, processing pipeline, etc.
    """

    def __init__(self, bwin: int, bwout: int, loglevel: str = "error"):
        self.bwin = bwin
        self.bwout = bwout
        self.logger = self.get_logger(loglevel)
        self.bdataout = None

        self.connected = []

    def connect(self, component: "Component"):
        if component.bwin != self.bwout:
            raise RuntimeError(f"Cannot connect  components with different port bit widths. {self.__class__.__name__} "
                               f"has output bit width {self.bwout} and {component.__class__.__name__} has input bit "
                               f"width {component.bwin}.")
        if component not in self.connected:
            self.connected.append(component)

    def step(self, bdatain: np.ndarray = None):
        # if bdatain is None and self._impl.__code__.co_kwonlyargcount:
        #     raise ValueError(f"{self.__class__.__name__} requires data input.")

        self._impl(bdatain)

        for conn in self.connected:
            self.logger.debug(f"{self.__class__.__name__} sending data {self.bdataout} to {conn.__class__.__name__}")
            conn.step(self.bdataout)

    def _impl(self, datain: np.ndarray = None):
        """
        A placeholder method that is expected to be overridden by subclasses. Accepts the input at simulation step and
        updates the output data_ in self.dataout.
        :param datain: The input data_ to be processed.
        """
        self.logger.warning(f"The core of the {self.__class__.__name__} was not implemented yet. Returning input.")
        self.dataout = datain

    def get_logger(self, loglevel: str = "error"):
        numeric_level = getattr(logging, loglevel.upper(), None)
        if not isinstance(numeric_level, int):
            raise ValueError(f"Invalid log level: {loglevel}. Use of {list(logging._nameToLevel.keys())}")

        ch = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s %(levelname)8s %(name)s | %(message)s')
        ch.setFormatter(formatter)

        logger = logging.getLogger(self.__class__.__name__)
        logger.addHandler(ch)
        logger.setLevel(numeric_level)
        return logger
