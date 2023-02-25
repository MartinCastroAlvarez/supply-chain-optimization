"""
In supply chain management, cost refers to the amount of money that a company spends
on producing and delivering goods or services to customers.
"""

from typing import Union, Dict

from decimal import Decimal


class Cost:
    """
    In supply chain management, cost refers to the amount of money that a company spends
    on producing and delivering goods or services to customers.
    """

    def __init__(self, name: str, value: Union[str, int, Decimal, float]) -> None:
        """
        Cost constructor.
        """
        self.name: str = name
        self.value: Decimal = Decimal(value)

    @property
    def name(self) -> str:
        """
        Name getter.
        """
        return self.__name

    @name.setter
    def name(self, value: str) -> None:
        """
        Name setter.
        """
        if not value or not isinstance(value, str):
            raise AttributeError('Invalid cost name:', value)
        self.__name = value

    @property
    def value(self) -> Decimal:
        """
        Cost getter.
        """
        return self.__value

    @value.setter
    def value(self, value: str) -> None:
        """
        Cost setter.
        """
        if not isinstance(value, (str, float, Decimal, int)):
            raise AttributeError('Invalid cost:', value)
        self.__value = Decimal(value)
        if self.__value < 0:
            raise ValueError('The cost can not be negative:', value)


class Costs:
    """
    A data structure for storing costs associated with a Storage center or a Product.
    """

    def __init__(self) -> None:
        """
        Lazy constructor.
        """
        self.__costs: Dict[Cost, Decimal] = {}

    def __repr__(self) -> str:
        """
        String serializer.
        """
        return f'<Costs: {self.name} - {self.address}>'

    def add(self, cost: Cost) -> None:
        """
        Adding a new cost to the cost structure.
        """
        if not isinstance(cost, Cost):
            raise AttributeError("Expecting cost, got::", cost)
        self.__costs[cost.name] = cost

    def get(self, name: str) -> Cost:
        """
        Returns the cost associate with a given name.
        """
        return self.__costs.get(name, Cost(name))

    @property
    def total(self) -> Decimal:
        """
        Returns the total cost.
        """
        return sum([
            cost.value
            for cost in self.__costs.values()
        ])
