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
# Creator
# -------------------
class PizzaStore(ABC):

    @abstractmethod
    def create_pizza(self, type_):
        pass

    def order_pizza(self, type_):

        pizza = self.create_pizza(type_)

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

        else:
            raise ValueError("Unknown pizza type")


# -------------------
# MAIN TEST
# -------------------
if __name__ == "__main__":

    store = NYPizzaStore()

    pizza1 = store.order_pizza("cheese")
    print()

    pizza2 = store.order_pizza("pepperoni")