"""
In the supply chain, a product typically starts as raw materials that are sourced from various suppliers.
These raw materials are then transformed into finished goods through manufacturing processes. Once the
finished product is ready, it is packaged and shipped to distributors, wholesalers, or retailers who
sell it to end customers.
"""

import math
from abc import ABC
from typing import Union
from decimal import Decimal

from cost import Cost, Costs


class Product(ABC):
    """
    In the supply chain, a product typically starts as raw materials that are sourced from various suppliers.
    These raw materials are then transformed into finished goods through manufacturing processes. Once the
    finished product is ready, it is packaged and shipped to distributors, wholesalers, or retailers who
    sell it to end customers.
    """

    def __init__(
        self,
        name: str,
        price: Union[str, int, float, Decimal] = 0,
        demand: Union[str, int, float, Decimal] = 0,
        lead_time: Union[str, int, float, Decimal] = 0,
        inventory: Union[str, int, float, Decimal] = 0,
        **kwargs,
    ) -> None:
        """
        Product constructor.
        """
        self.name: str = name
        self.inventory: Decimal = inventory
        self.demand: Decimal = demand
        self.lead_time: Decimal = lead_time
        self.price: Decimal = price
        self.storage_costs: Costs = Costs()

    def __repr__(self) -> str:
        """
        String serializer.
        """
        return f'<Product: {self.name} - {self.inventory}>'

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
            raise AttributeError('Invalid product name:', value)
        self.__name = value

    @property
    def inventory(self) -> Decimal:
        """
        Inventory getter.
        """
        return self.__inventory

    @inventory.setter
    def inventory(self, value: str) -> None:
        """
        Inventory setter.
        """
        if not isinstance(value, (str, float, Decimal, int)):
            raise AttributeError('Invalid product inventory:', value)
        self.__inventory = Decimal(value)
        if self.__inventory < 0:
            raise ValueError('The inventory can not be negative:', value)

    @property
    def demand(self) -> Decimal:
        """
        Demand getter.
        """
        return self.__demand

    @demand.setter
    def demand(self, value: str) -> None:
        """
        Demand setter.
        """
        if not isinstance(value, (str, float, Decimal, int)):
            raise AttributeError('Invalid demand:', value)
        self.__demand = Decimal(value)
        if self.__demand < 0:
            raise ValueError('The demand can not be negative:', value)

    @property
    def lead_time(self) -> Decimal:
        """
        Lead time getter.
        """
        return self.__lead_time

    @lead_time.setter
    def lead_time(self, value: str) -> None:
        """
        Lead time setter.
        """
        if not isinstance(value, (str, float, Decimal, int)):
            raise AttributeError('Invalid lead time:', value)
        self.__lead_time = Decimal(value)
        if self.__lead_time < 0:
            raise ValueError('The lead time can not be negative:', value)

    @property
    def price(self) -> Decimal:
        """
        Price getter.
        """
        return self.__price

    @price.setter
    def price(self, value: str) -> None:
        """
        Price setter.
        """
        if not isinstance(value, (str, float, Decimal, int)):
            raise AttributeError('Invalid product price:', value)
        self.__price = Decimal(value)
        if self.__price < 0:
            raise ValueError('The price can not be negative:', value)

    @property
    def total_storage_cost(self) -> Decimal:
        """
        Returns the total storage cost.
        """
        return self.storage_costs.total

    @property
    def total_variable_cost(self) -> Decimal:
        """
        Returns the total variable cost.
        """
        raise NotImplementedError('Method not overrided!')

    @property
    def optimum_inventory_level(self) -> Decimal:
        """
        Returns the total estimated cost.

        This method calculates the optimum inventory level using the Economic Order Quantity (EOQ) formula,
        which balances the holding cost of inventory against the ordering cost and the stockout cost.
        The formula assumes that demand for the product is constant and that lead time for replenishing
        inventory is known.

        >>> T = KD/Q + hQ/2

        With:
        - T = total annual inventory cost
        - Q = order quantity
        - D = annual demand quantity
        - K = fixed cost per order, setup cost (not per unit, typically cost of ordering and shipping
              and handling. This is not the cost of goods)
        - h = annual holding cost per unit, also known as carrying cost or storage cost (capital cost,
              warehouse space, refrigeration, insurance, opportunity cost (price x interest), etc.
              usually not related to the unit production cost)

        To determine the minimum point of the total cost curve, calculate the derivative of the total
        cost with respect to Q (assume all other variables are constant) and set it equal to 0:

        >>> Q^2 = 2DK/h
        """
        if not self.demand:
            raise RuntimeError('The demand must be positive.')
        if not self.total_storage_cost:
            raise RuntimeError('The total storage cost must be positive.')
        if not self.total_variable_cost:
            raise RuntimeError('The total variable cost must be positive.')
        return Decimal(math.sqrt(2 * self.demand * self.total_variable_cost / self.total_storage_cost))


class ProducedProduct(Product):
    """
    A Product that is produced by the company in one of their factories.
    """

    def __init__(self, *args, **kwargs) -> None:
        """
        Product constructor.
        """
        Product.__init__(self, *args, **kwargs)
        self.production_costs: Costs = Costs()

    @property
    def total_variable_cost(self) -> Decimal:
        """
        Returns the total variable cost.
        """
        return self.production_costs.total


class PurchasedProduct(Product):
    """
    A Product that is purchased to an external company.
    """

    def __init__(self, *args, **kwargs) -> None:
        """
        Product constructor.
        """
        Product.__init__(self, *args, **kwargs)
        self.purchase_costs: Costs = Costs()

    @property
    def total_variable_cost(self) -> Decimal:
        """
        Returns the total variable cost.
        """
        return self.purchase_costs.total


if __name__ == '__main__':

    from simulator import Simulator

    with Simulator(title='Product Variable Cost', times=10) as simulator:

        @simulator.simulate()
        def main() -> Decimal:

            product: Product = ProducedProduct(name='Product I', inventory=100)

            product.production_costs.add(Cost('Energy Costs', simulator.normal(mean=2, std=1, upper=5, lower=0)))
            product.production_costs.add(Cost('Labor Costs', simulator.normal(mean=7, std=2, upper=10, lower=5)))

            return product.total_variable_cost

    with Simulator(title='Product Storage Cost', times=10) as simulator:

        @simulator.simulate()
        def main() -> Decimal:

            product: Product = PurchasedProduct(name='Product II', inventory=100)

            product.storage_costs.add(Cost('Warehousing', simulator.normal(mean=0.1, std=0.1, upper=0.5, lower=0)))
            product.storage_costs.add(Cost('Utilities', simulator.normal(mean=0.1, std=0.1, upper=0.5, lower=0)))
            product.storage_costs.add(Cost('Insurance', simulator.normal(mean=0.1, std=0.1, upper=0.5, lower=0)))
            product.storage_costs.add(Cost('Taxes', simulator.normal(mean=0.1, std=0.1, upper=0.5, lower=0)))
            product.storage_costs.add(Cost('Freight', simulator.normal(mean=0.1, std=0.1, upper=0.5, lower=0)))
            product.storage_costs.add(Cost('Placement', simulator.normal(mean=0.1, std=0.1, upper=0.5, lower=0)))
            product.storage_costs.add(Cost('Ordering', simulator.normal(mean=0.1, std=0.1, upper=0.5, lower=0)))
            product.storage_costs.add(Cost('Obsolescence', simulator.normal(mean=0.1, std=0.1, upper=0.5, lower=0)))

            return product.total_storage_cost

    with Simulator(title='Product Optimum Inventory Level', times=10) as simulator:

        @simulator.simulate()
        def main() -> Decimal:

            product: Product = ProducedProduct(
                name='Product III',
                inventory=100,
                demand=simulator.normal(mean=1000, std=1000, upper=3000, lower=0),
            )

            product.production_costs.add(Cost('Energy Costs', simulator.normal(mean=2, std=1, upper=5, lower=0)))
            product.production_costs.add(Cost('Labor Costs', simulator.normal(mean=7, std=2, upper=10, lower=5)))

            product.storage_costs.add(Cost('Warehousing', simulator.normal(mean=0.1, std=0.1, upper=0.5, lower=0)))
            product.storage_costs.add(Cost('Utilities', simulator.normal(mean=0.1, std=0.1, upper=0.5, lower=0)))
            product.storage_costs.add(Cost('Insurance', simulator.normal(mean=0.1, std=0.1, upper=0.5, lower=0)))
            product.storage_costs.add(Cost('Taxes', simulator.normal(mean=0.1, std=0.1, upper=0.5, lower=0)))
            product.storage_costs.add(Cost('Freight', simulator.normal(mean=0.1, std=0.1, upper=0.5, lower=0)))
            product.storage_costs.add(Cost('Placement', simulator.normal(mean=0.1, std=0.1, upper=0.5, lower=0)))
            product.storage_costs.add(Cost('Ordering', simulator.normal(mean=0.1, std=0.1, upper=0.5, lower=0)))
            product.storage_costs.add(Cost('Obsolescence', simulator.normal(mean=0.1, std=0.1, upper=0.5, lower=0)))
            product.storage_costs.add(Cost('Refrigeration', simulator.normal(mean=0.1, std=0.1, upper=0.5, lower=0)))

            return product.optimum_inventory_level
