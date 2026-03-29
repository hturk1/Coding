from abc import ABC, abstractmethod

# Product

class Coffee(ABC):

    @abstractmethod
    def prepare(self):
        pass

    def get_type(self):
        pass

    def get_size(self):
        pass

    def get_extras(self):
        pass



# Concrete Products

class Latte(Coffee):
    def prepare(self):
        print("Order 1:")
    
    def get_type(self):
        print ("Type: Latte")
        
    def get_size(self):
        print ("Size: Medium ")
    
    def get_extras(self):
        print ("Extras: No sugar, Extra shot ")


class Cappuccino(Coffee):

    def prepare(self):
        print("Order 2:")

    def get_type(self):
        print ("Type: Cappuccino")
        
    def get_size(self):
        print ("Size: Small")
    
    def get_extras(self):
        print ("Extras: Extra sugar, No cream")



# Creator
class CoffeeShop(ABC):

    @abstractmethod
    def create_coffee(self, type_):
        pass

    def order_coffee(self, type_):

        coffee = self.create_coffee(type_)


        coffee.prepare()
        coffee.get_type()
        coffee.get_size()
        coffee.get_extras()


# Concrete Creator

class CoffeeShop1(CoffeeShop):

    def create_coffee(self, type_):

        if type_ == "1":
            return Latte()

        elif type_ == "2":
            return Cappuccino()

        else:
            raise ValueError("Unknown coffee type")



# Main Test

def main():

    print ("Welcome, what would you like to order? Please choose 1 or 2." )
    
    choice = int(input())

    store = CoffeeShop1()

    if (choice == 1): 
        coffee1 = store.order_coffee("1")
        print()

    if (choice == 2): 
        coffee2 = store.order_coffee("2")
        print()


if __name__ == "__main__":
    main()
