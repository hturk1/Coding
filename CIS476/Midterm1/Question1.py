from abc import ABC, abstractmethod

# Product

class Coffee:
    def __init__(self):
        self.parts = {}

    def add_part(self, name, value):
        self.parts[name] = value

    def show(self):
        for part, value in self.parts.items():
            print(f"  {part}: {value}")
        print()


# Builder interface

class CoffeeBuilder(ABC):
    @abstractmethod

    def set_type(self):
        pass

    def set_size(self):
        pass

    @abstractmethod
    def set_sugar(self):
        pass

    @abstractmethod
    def set_cream(self):
        pass

    @abstractmethod
    def get_result(self):
        pass


# Concrete Builders

class LatteBuilder(CoffeeBuilder):
    def __init__(self):
        self.coffee = Coffee()

    def set_type(self):
        self.coffee.add_part("Type", "Latte")

    def set_size(self):
        self.coffee.add_part("Size", "Medium")

    def set_sugar(self):
        self.coffee.add_part("Sugar", "None")

    def set_cream(self):
        self.coffee.add_part("Cream", "Extra Shot")

    def get_result(self):
        return self.coffee


class CappuccinoBuilder(CoffeeBuilder):
    def __init__(self):
        self.coffee = Coffee()

    def set_type(self):
        self.coffee.add_part("Type", "Cappuccino")

    def set_size(self):
        self.coffee.add_part("Size", "Small")

    def set_sugar(self):
        self.coffee.add_part("Sugar", "Extra")

    def set_cream(self):
        self.coffee.add_part("Cream", "No Cream")

    def get_result(self):
        return self.coffee



# Director

class Director:
    def construct(self, builder: CoffeeBuilder):
        builder.set_type()
        builder.set_size()
        builder.set_sugar()
        builder.set_cream()
        return builder.get_result()



# Main Test

def main():
    director = Director()


    print ("Welcome, what would you like to order? Please choose 1 or 2." )
    
    choice = int(input())

    if (choice == 1): 
        print ("Order 1:")
        latte = director.construct(LatteBuilder())
        latte.show()


    if (choice == 2):
        print ("Order 2:")
        cappuccino = director.construct(CappuccinoBuilder())
        cappuccino.show()

    

if __name__ == "__main__":
    main()

