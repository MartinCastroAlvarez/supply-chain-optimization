"""
In supply chain management, storage refers to the physical locations where goods or materials
are stored before they are transported to their final destination. Storage facilities can include
warehouses, distribution centers, and other types of storage facilities, such as refrigerated
or climate-controlled environments.
"""

from decimal import Decimal

from cost import Cost, Costs


class Center:
    """
    In supply chain management, storage refers to the physical locations where goods or materials
    are stored before they are transported to their final destination. Storage facilities can include
    warehouses, distribution centers, and other types of storage facilities, such as refrigerated
    or climate-controlled environments.
    """

    def __init__(self) -> None:
        """
        Cost center constructor.
        """
        self.__name: str = 'Sample Center'
        self.__address: str = ''
        self.costs: Costs = Costs()

    def __repr__(self) -> str:
        """
        String serializer.
        """
        return f'<Center: {self.name} - {self.address}>'

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
            raise AttributeError('Invalid center name:', value)
        self.__name = value

    @property
    def address(self) -> str:
        """
        Address getter.
        """
        return self.__address

    @address.setter
    def address(self, value: str) -> None:
        """
        Address setter.
        """
        if not value or not isinstance(value, str):
            raise AttributeError('Invalid center address:', value)
        self.__address = value

    @property
    def total_fixed_cost(self) -> Decimal:
        """
        Returns the total fixed cost.
        """
        return self.costs.total


if __name__ == '__main__':

    from simulator import Simulator

    with Simulator(title='Total Fixed Cost', times=100) as simulator:

        @simulator.simulate()
        def main() -> Decimal:

            center: Center = Center()
            center.name = 'My Center I'
            center.address = '450 Hawk St.'
            print('Center identifier:', center)

            center.costs.add(Cost('Quality Control Costs', simulator.normal(mean=100, std=20, upper=3000, lower=50)))
            center.costs.add(Cost('Labor Costs', simulator.normal(mean=500, std=100, upper=1000, lower=0)))
            center.costs.add(Cost('Energy Costs', simulator.normal(mean=150, std=180, upper=1000, lower=100)))
            center.costs.add(Cost('Equipment Costs', simulator.normal(mean=200, std=40, upper=320, lower=160)))
            center.costs.add(Cost('Overhead Costs', simulator.normal(mean=30, std=20, upper=300, lower=0)))
            center.costs.add(Cost('Warehouse Rent', simulator.normal(mean=300, std=50, upper=400, lower=200)))
            center.costs.add(Cost('Inventory Management Software', simulator.normal(mean=10, std=5, upper=80, lower=0)))

            return center.total_fixed_cost
