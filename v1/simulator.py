"""
Monte Carlo simulation is a computational technique used in probability theory and statistics to model
and analyze complex systems or processes that involve uncertainty. It involves using random sampling and
statistical analysis to generate a range of possible outcomes for a given system or process.

References:
- https://realpython.com/python-with-statement/
"""

import sys
import logging
from decimal import Decimal
from typing import List, Optional

import numpy as np
from scipy.stats import truncnorm

logger: logging.RootLogger = logging.getLogger(__name__)


class Simulator:
    """
    In supply chain management, storage refers to the physical locations where goods or materials
    are stored before they are transported to their final destination. Storage facilities can include
    warehouses, distribution centers, and other types of storage facilities, such as refrigerated
    or climate-controlled environments.

    References:
    - https://realpython.com/python-with-statement/
    """

    def __init__(self, times: int = 1, title: str = 'Example') -> None:
        """
        Simulator constructor.
        """
        if not isinstance(times, int) or times < 0:
            raise AttributeError("Invalid simulator run times:", times)
        if not title or not isinstance(title, str):
            raise TypeError('Invalid simulator title:', title)
        self.times = times
        self.title : str = title
        self.results: List[Decimal] = []

    def __repr__(self) -> str:
        """
        String serializer.
        """
        return '<Simulator>'

    def normal(self, mean: float, std: float, upper: float, lower: float) -> Decimal:
        """
        The truncnorm function creates a truncated normal distribution, which is a normal distribution
        that is bounded by a lower and an upper limit.
        """
        if mean > upper:
            raise ValueError('Mean is too high:', mean)
        if mean < lower:
            raise ValueError('Mean is too low:', mean)
        return Decimal(truncnorm((lower - mean) / std, (upper - mean) / std, loc=mean, scale=std).rvs())

    def simulate(self) -> callable:
        """
        Decorator to run a piece of code multiple times.

        Reference:
        - https://stackoverflow.com/questions/4930386/python-is-there-a-way-to-get-the-code-inside-the-with-statement
        """

        def decorated(fn: callable):
            """
            Decorated function to execute multiple times.
            """
            for test_number in range(self.times):
                logger.info('Simulator | Test[%s]: Starting...', test_number)
                result: Decimal = fn()
                if not isinstance(result, Decimal):
                    raise TypeError('Expecting a Decimal, got:', result)
                logger.info('Simulator | Test[%s]: %s', test_number, result)
                self.results.append(result)

        return decorated

    @property
    def average(self) -> Decimal:
        """
        Calculates the average of the simulation tests.
        """
        return sum(self.results) / len(self.results) if self.results else Decimal(0)

    def __enter__(self) -> 'Simulator':
        """
        Context manager initialization.
        """
        return self

    def __exit__(self, exc_type: Optional[Exception], exc_value: Optional[Exception], exc_tb: Optional['traceback']):
        """
        Context manager finalization.
        """
        if exc_type is None:
            self.summary()
        else:
            raise RuntimeError('Failed to run simulator!', exc_value, exc_tb) from exc_type

    @property
    def maximum(self) -> Decimal:
        """
        Calculates the maximum of the simulation tests.
        """
        return max(self.results) if self.results else Decimal(0)

    @property
    def minimum(self) -> Decimal:
        """
        Calculates the minimum of the simulation tests.
        """
        return min(self.results) if self.results else Decimal(0)

    def summary(self) -> None:
        """
        Prints the summary of the simulator to STDOUT.
        """
        print('-' * 50)
        print(self.title, 'Summary:')
        print('- Simulated:', self.times, 'times')
        print('- Average:', self.average)
        print('- Maximum:', self.maximum)
        print('- Minimum:', self.minimum)
        print('-' * 50)


if __name__ == '__main__':
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)

    with Simulator(times=10) as simulator:

        @simulator.simulate()
        def main() -> Decimal:
            """
            Sample simulator case.
            """
            return simulator.normal(mean=3, std=1, upper=10, lower=1)
