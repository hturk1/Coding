from abc import ABC, abstractmethod

# -------------------
# Base Component
# -------------------
class Ticket(ABC):
    @abstractmethod
    def get_name(self):
        pass

    @abstractmethod
    def get_cost(self):
        pass

# -------------------
# Concrete Tickets
# -------------------
class AdultTicket(Ticket):
    def __init__(self, quantity=1):
        self.quantity = quantity
        self.unit_price = 10

    def get_name(self):
        return "Adult Ticket"

    def get_cost(self):
        return self.quantity * self.unit_price

class StudentTicket(Ticket):
    def __init__(self, quantity=1):
        self.quantity = quantity
        self.unit_price = 8

    def get_name(self):
        return "Student Ticket"

    def get_cost(self):
        return self.quantity * self.unit_price

# -------------------
# Decorator
# -------------------
class TicketDecorator(Ticket):
    def __init__(self, component: Ticket):
        self.component = component

    def get_name(self):
        return self.component.get_name()

    def get_cost(self):
        return self.component.get_cost()

# -------------------
# Concrete Decorators
# -------------------
class Popcorn(TicketDecorator):
    def __init__(self, component: Ticket, quantity=1.0):
        super().__init__(component)
        self.quantity = quantity
        self.unit_price = 6

    def get_name(self):
        return self.component.get_name() + " + Popcorn"

    def get_cost(self):
        return self.component.get_cost() + self.quantity * self.unit_price

class Chips(TicketDecorator):
    def __init__(self, component: Ticket, quantity=1.0):
        super().__init__(component)
        self.quantity = quantity
        self.unit_price = 4

    def get_name(self):
        return self.component.get_name() + " + Chips"

    def get_cost(self):
        return self.component.get_cost() + self.quantity * self.unit_price

class Drink(TicketDecorator):
    def __init__(self, component: Ticket, drink_type="Coke", quantity=1):
        super().__init__(component)
        self.quantity = quantity
        self.unit_price = 2
        self.drink_type = drink_type

    def get_name(self):
        return self.component.get_name() + f" + {self.drink_type}"

    def get_cost(self):
        return self.component.get_cost() + self.quantity * self.unit_price

# -------------------
# Singleton Gift Decorator
# -------------------
class Gift(TicketDecorator):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        else:
            print("Only one free gift allowed per order! Cannot add another.")
            return None
        return cls._instance

    def __init__(self, component: Ticket):
        super().__init__(component)
        self.unit_price = 0

    def get_name(self):
        return self.component.get_name() + " + Free Gift"

    def get_cost(self):
        return self.component.get_cost()  # Free gift adds $0

# -------------------
# MAIN CLIENT
# -------------------
if __name__ == "__main__":
    # Create tickets
    ticket1 = AdultTicket()
    ticket2 = StudentTicket()

    # Decorate ticket1
    ticket1 = Popcorn(ticket1, 0.6)
    ticket1 = Chips(ticket1, 0.4)
    ticket1 = Drink(ticket1, "Coke", 2)
    gift1 = Gift(ticket1)  # First gift works
    if gift1:
        ticket1 = gift1

    # Decorate ticket2
    ticket2 = Popcorn(ticket2, 0.6)
    ticket2 = Chips(ticket2, 0.4)
    ticket2 = Drink(ticket2, "Coke", 2)
    gift2 = Gift(ticket2)  # Attempt second gift (blocked)
    if gift2:
        ticket2 = gift2


    # Print receipt
    tickets = [ticket1, ticket2]
    total = 0
    for t in tickets:
        print(f"Item: {t.get_name()}, Cost: ${t.get_cost():.2f}")
        total += t.get_cost()
    print(f"Total: ${total:.2f}")