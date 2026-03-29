from abc import ABC, abstractmethod

# -------------------
# Product
# -------------------
class Pizza(ABC):
    @abstractmethod
    def prepare(self):
        pass

    def bake(self):
        print("Baking pizza")

    def cut(self):
        print("Cutting pizza")

    def box(self):
        print("Boxing pizza")


# -------------------
# Concrete Products
# -------------------
class CheesePizza(Pizza):
    def prepare(self):
        print("Preparing Cheese Pizza")


class PepperoniPizza(Pizza):
    def prepare(self):
        print("Preparing Pepperoni Pizza")


# -------------------
# Singleton Pizza (only one allowed)
# -------------------
class GoldenPizza(Pizza):
    _instance = None  # store the single instance

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        else:
            print("Sorry, only one Golden Pizza allowed! Cannot create another.")
            return None  # Block creation instead of raising an exception
        return cls._instance

    def prepare(self):
        print("Preparing the ONE Golden Pizza!")


# -------------------
# Creator (Factory Method)
# -------------------
class PizzaStore(ABC):
    @abstractmethod
    def create_pizza(self, type_):
        pass

    def order_pizza(self, type_):
        pizza = self.create_pizza(type_)
        if pizza is None:
            print("Order could not be completed.")
            return None
        pizza.prepare()
        pizza.bake()
        pizza.cut()
        pizza.box()
        return pizza


# -------------------
# Concrete Creator
# -------------------
class NYPizzaStore(PizzaStore):
    def create_pizza(self, type_):
        if type_ == "cheese":
            return CheesePizza()
        elif type_ == "pepperoni":
            return PepperoniPizza()
        elif type_ == "golden":
            return GoldenPizza()
        else:
            print("Unknown pizza type")
            return None


# -------------------
# MAIN TEST
# -------------------
if __name__ == "__main__":
    store = NYPizzaStore()

    pizza1 = store.order_pizza("cheese")
    print()
    
    pizza2 = store.order_pizza("golden")
    print()
    
    # This will no longer raise an exception
    pizza3 = store.order_pizza("golden")
    print()
    
    pizza4 = store.order_pizza("pepperoni")