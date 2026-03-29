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

    @abstractmethod
    def get_quantity(self):
        pass

    @abstractmethod
    def get_unit_price(self):
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

    def get_quantity(self):
        return self.quantity

    def get_unit_price(self):
        return self.unit_price

class StudentTicket(Ticket):
    def __init__(self, quantity=1):
        self.quantity = quantity
        self.unit_price = 8

    def get_name(self):
        return "Student Ticket"

    def get_cost(self):
        return self.quantity * self.unit_price

    def get_quantity(self):
        return self.quantity

    def get_unit_price(self):
        return self.unit_price

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

    def get_quantity(self):
        return self.component.get_quantity()

    def get_unit_price(self):
        return self.component.get_unit_price()

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

    def get_quantity(self):
        return self.quantity

    def get_unit_price(self):
        return self.unit_price

class Chips(TicketDecorator):
    def __init__(self, component: Ticket, quantity=1.0):
        super().__init__(component)
        self.quantity = quantity
        self.unit_price = 4

    def get_name(self):
        return self.component.get_name() + " + Chips"

    def get_cost(self):
        return self.component.get_cost() + self.quantity * self.unit_price

    def get_quantity(self):
        return self.quantity

    def get_unit_price(self):
        return self.unit_price

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

    def get_quantity(self):
        return self.quantity

    def get_unit_price(self):
        return self.unit_price

class Gift(TicketDecorator):
    def __init__(self, component: Ticket):
        super().__init__(component)
        self.unit_price = 0
        self.quantity = 1

    def get_name(self):
        return self.component.get_name() + " + Free Gift"

    def get_cost(self):
        return self.component.get_cost() + self.unit_price

    def get_quantity(self):
        return self.quantity

    def get_unit_price(self):
        return self.unit_price

# -------------------
# Client Code – Normal Version
# -------------------
if __name__ == "__main__":
    # Create tickets
    ticket1 = AdultTicket()
    ticket2 = StudentTicket()

    # Decorate ticket1 with 0.6 popcorn, 0.4 chips, 2 coke, 1 gift
    ticket1 = Popcorn(ticket1, 0.6)
    ticket1 = Chips(ticket1, 0.4)
    ticket1 = Drink(ticket1, "Coke", 2)
    ticket1 = Gift(ticket1)

    # Decorate ticket2
    ticket2 = Popcorn(ticket2, 0.6)
    ticket2 = Chips(ticket2, 0.4)
    ticket2 = Drink(ticket2, "Coke", 2)
    ticket2 = Gift(ticket2)

    # Print receipt
    tickets = [ticket1, ticket2]
    total = 0
    for t in tickets:
        print(f"Item: {t.get_name()}, Quantity: {t.get_quantity()}, Unit Price: ${t.get_unit_price()}, Cost: ${t.get_cost()}")
        total += t.get_cost()
    print(f"Total: ${total}")