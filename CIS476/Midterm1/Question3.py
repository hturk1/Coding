from abc import ABC, abstractmethod

# Base Component

class Coffee(ABC):
    @abstractmethod
    def get_name(self):
        pass

    @abstractmethod
    def get_cost(self):
        pass

    @abstractmethod
    def get_quantity(self):
        pass

    @abstractmethod
    def get_unitcost(self):
        pass


# Concrete Coffee

class Latte(Coffee):
    def __init__(self, quantity=1):
        self.quantity = quantity
        self.unit_price = 4.5

    def get_name(self):
        return "Latte"

    def get_cost(self):
        return self.quantity * self.unit_price

    def get_quantity(self):
        return self.quantity
    
    def get_unitcost(self):
        return self.unit_price



class Cappuccino(Coffee):
    def __init__(self, quantity=1):
        self.quantity = quantity
        self.unit_price = 5

    def get_name(self):
        return "Cappuccino"

    def get_cost(self):
        return self.quantity * self.unit_price
    
    def get_quantity(self):
        return self.quantity
    
    def get_unitcost(self):
        return self.unit_price

    
class Black(Coffee):
    def __init__(self, quantity=1):
        self.quantity = quantity
        self.unit_price = 4

    def get_name(self):
        return "Black"

    def get_cost(self):
        return self.quantity * self.unit_price
    
    def get_quantity(self):
        return self.quantity
    
    def get_unitcost(self):
        return self.unit_price



# Decorator

class OrderDecorator(Coffee):
    def __init__(self, component: Coffee):
        self.component = component

    def get_name(self):
        return self.component.get_name()

    def get_cost(self):
        return self.component.get_cost()
    

    def get_quantity(self):
        return self.component.get_quantity()
    

    def get_unitcost(self):
        return self.component.get_unitcost()
    


# Concrete Decorators

class Cookie(OrderDecorator):
    def __init__(self, component: Coffee, quantity=1.0):
        super().__init__(component)
        self.quantity = quantity
        self.unit_price = 1.5

    def get_name(self):
        return self.component.get_name() + f' + {self.quantity} Cookie (unit cost is {self.unit_price})'

    def get_cost(self):
        return self.component.get_cost() + self.quantity * self.unit_price

class Muffins(OrderDecorator):
    def __init__(self, component: Coffee, quantity=1.0):
        super().__init__(component)
        self.quantity = quantity
        self.unit_price = 1.3

    def get_name(self):
        return self.component.get_name() + f' + {self.quantity} Muffins (unit cost is {self.unit_price})'

    def get_cost(self):
        return self.component.get_cost() + self.quantity * self.unit_price


class ExtraSugar(OrderDecorator):
    def __init__(self, component: Coffee, quantity=1.0):
        super().__init__(component)
        self.quantity = quantity
        self.unit_price = 1.0

    def get_name(self):
        return self.component.get_name() +f' + {self.quantity} Extra Sugar (unit cost is {self.unit_price})'

    def get_cost(self):
        return self.component.get_cost() + self.quantity * self.unit_price
    

class Butter(OrderDecorator):
    def __init__(self, component: Coffee, quantity=1.0):
        super().__init__(component)
        self.quantity = quantity
        self.unit_price = 1.2

    def get_name(self):
        return self.component.get_name()  + f' + {self.quantity} Butter (unit cost is {self.unit_price})' 

    def get_cost(self):
        return self.component.get_cost() + self.quantity * self.unit_price


# Singleton Coupon Decorator

class Coupon(OrderDecorator):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        else:
            print("Only one coupon can be applied")
            return None
        return cls._instance

    def __init__(self, component: Coffee):
        super().__init__(component)
        self.unit_price = 0.9

    def get_name(self):
        return self.component.get_name() + " + 10% Coupon"

    def get_cost(self):
        return self.component.get_cost() *  self.unit_price # Free gift adds $0


# Main Client 

def main():

    # Create drinks
    coffee1 = Latte()
    coffee2 = Cappuccino()
    coffee3 = Black()

    # Decorate coffee
    coffee1 = Muffins(coffee1, 2)
    coffee1 = Butter(coffee1, 1.5)
    coupon1 = Coupon(coffee1)  # First coupon works
    if coupon1:
        coffee1 = coupon1

    # Print receipt
    coffees = [coffee3, coffee1]
    total = 0
    for t in coffees:
        print(f"Item: {t.get_quantity()} coffee with cost of ${t.get_unitcost()}: {t.get_name()}, Cost: ${t.get_cost():.2f}")
        total += t.get_cost()
    print(f"Total: ${total:.2f}")

if __name__ == "__main__":
    main()