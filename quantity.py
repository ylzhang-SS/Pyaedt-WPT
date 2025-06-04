from typing import List, Tuple

class BaseQuantity:
    def __init__(self, name: str, is_variable: bool):
        self.name = name
        self.is_variable = is_variable

    def __repr__(self):
        return f"{self.__class__.__name__}(name={self.name}, is_variable={self.is_variable})"

class DimensionTypeI(BaseQuantity):
    def __init__(self, name: str, initial_size: float, size_range: Tuple[float, float],
                 is_variable: bool, is_objective: bool, weight: float):
        super().__init__(name, is_variable)
        self.initial_size = initial_size
        self.size_range = size_range
        self.is_objective = is_objective
        self.weight = weight

    def __repr__(self):
        return (f"DimensionTypeI(name={self.name}, initial_size={self.initial_size}, "
                f"size_range={self.size_range}, is_variable={self.is_variable}, "
                f"is_objective={self.is_objective}, weight={self.weight})")

class DimensionTypeII(BaseQuantity):
    def __init__(self, name: str, sizes: Tuple[float, float, float]):
        super().__init__(name, is_variable=False)
        self.sizes = sizes

    def __repr__(self):
        return (f"DimensionTypeII(name={self.name}, sizes={self.sizes})")

class ConstantTypeI(BaseQuantity):
    def __init__(self, name: str, value: float):
        super().__init__(name, is_variable=False)
        self.value = value

    def __repr__(self):
        return f"ConstantTypeI(name={self.name}, value={self.value})"

class QuantityManager:
    def __init__(self):
        self.quantities = []

    def add_quantity(self, quantities: List[BaseQuantity]):
        """Adds multiple quantities at once."""
        if isinstance(quantities, list):
            self.quantities.extend(quantities)
        else:
            raise TypeError("The argument must be a list or other iterable of BaseQuantity objects.")

    def list_quantities(self):
        return self.quantities

    def set_initial_size(self, name: str, new_size: float):
        """Sets the initial size of a specific DimensionTypeI quantity by name."""
        for quantity in self.quantities:
            if isinstance(quantity, DimensionTypeI) and quantity.name == name:
                if quantity.size_range[0] <= new_size <= quantity.size_range[1]:
                    quantity.initial_size = new_size
                    return True
                else:
                    raise ValueError(f"New size {new_size} is out of range {quantity.size_range}.")
        raise KeyError(f"Quantity with name '{name}' not found.")

    def update_variable_sizes(self, scaling_factor: float):
        for quantity in self.quantities:
            if isinstance(quantity, DimensionTypeI) and quantity.is_variable:
                new_size = quantity.initial_size * scaling_factor
                if quantity.size_range[0] <= new_size <= quantity.size_range[1]:
                    quantity.initial_size = new_size

    def update_dimension_typeI(self, name: str, initial_size: float = None, size_range: Tuple[float, float] = None,
                               is_variable: bool = None, is_objective: bool = None, weight: float = None):
        """Update attributes of DimensionTypeI by name."""
        for quantity in self.quantities:
            if isinstance(quantity, DimensionTypeI) and quantity.name == name:
                if initial_size is not None:
                    if size_range and (size_range[0] <= initial_size <= size_range[1]):
                        quantity.initial_size = initial_size
                    else:
                        raise ValueError(f"Initial size {initial_size} is out of range {size_range}.")
                if size_range is not None:
                    quantity.size_range = size_range
                if is_variable is not None:
                    quantity.is_variable = is_variable
                if is_objective is not None:
                    quantity.is_objective = is_objective
                if weight is not None:
                    quantity.weight = weight
                return True
        raise KeyError(f"DimensionTypeI with name '{name}' not found.")

    def __repr__(self):
        return "\n".join([repr(quantity) for quantity in self.quantities])
test