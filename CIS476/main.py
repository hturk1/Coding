from abc import ABC, abstractmethod  # import for abstract base class 

# define abstract product panel
class Panel(ABC):

    @abstractmethod
    def display(self):
        pass  

# define abstract product button
class Button(ABC):

    @abstractmethod
    def display(self):
        pass  

# define abstract product textbox
class Textbox(ABC):

    @abstractmethod
    def display(self):
        pass 


# concrete products for word96 below...
# concrete product for panel
class Word96Panel(Panel):

    def display(self):
        print("Panel Word96")  # print panel message for word96

# concrete product for button
class Word96Button(Button):

    def display(self):
        print("Button Word96")  # print button message for word96

# concrete product for textbox
class Word96Textbox(Textbox):

    def display(self):
        print("Textbox Word96")  # print textbox message for word96



# concrete products for word06 below...
# concrete product for panel
class Word06Panel(Panel):

    def display(self):
        print("Panel Word06")  # print panel message for word06

# concrete product for button
class Word06Button(Button):

    def display(self):
        print("Button Word06")  # print button message for word06

# concrete product for textbox
class Word06Textbox(Textbox):

    def display(self):
        print("Textbox Word06")  # print textbox message for word06



# concrete products for word16 below...
# concrete product for panel
class Word16Panel(Panel):

    def display(self):
        print("Panel Word16")  # print panel message for word16

# concrete product for button
class Word16Button(Button):

    def display(self):
        print("Button Word16")  # print button message for word16

# concrete product for textbox
class Word16Textbox(Textbox):

    def display(self):
        print("Textbox Word16")  # print textbox message for word16



# concrete product for word26 below...
# concrete product for panel
class Word26Panel(Panel):

    def display(self):
        print("Panel Word26")  # print panel message for word26

# concrete product for button
class Word26Button(Button):

    def display(self):
        print("Button Word26")  # print button message for word26

# concrete product for textbox
class Word26Textbox(Textbox):

    def display(self):
        print("Textbox Word26")  # print textbox message for word26



# abstract factory that declares creation methods
class GUIFactory(ABC):

    @abstractmethod
    def create_panel(self):
        pass  # return a panel object

    @abstractmethod
    def create_button(self):
        pass  # return a button object

    @abstractmethod
    def create_textbox(self):
        pass  # return a textbox object



# concrete factory for word96 with limited singleton behavior
class Word96Factory(GUIFactory):

    _instances = 0  # track number of created instances

    def __init__(self):
        Word96Factory._instances += 1  # increase counter when object is created

    @classmethod
    def get_instance(cls):
        if cls._instances >= 2:  # check if already created twice
            print("Warning: Word96 already instantiated twice.\n")
            return None  # prevent more than two instances
        return cls()  # create and return new instance

    def create_panel(self):
        return Word96Panel()  # create word96 panel

    def create_button(self):
        return Word96Button()  # create word96 button

    def create_textbox(self):
        return Word96Textbox()  # create word96 textbox


# concrete factory for word06 with limited singleton behavior
class Word06Factory(GUIFactory):

    _instances = 0  # track number of created instances

    def __init__(self):
        Word06Factory._instances += 1  # increase counter when object is created

    @classmethod
    def get_instance(cls):
        if cls._instances >= 2:  # check if already created twice
            print("Warning: Word06 already instantiated twice.\n")
            return None
        return cls()

    def create_panel(self):
        return Word06Panel()

    def create_button(self):
        return Word06Button()

    def create_textbox(self):
        return Word06Textbox()


# concrete factory for word16 with limited singleton behavior
class Word16Factory(GUIFactory):

    _instances = 0  # track number of created instances

    def __init__(self):
        Word16Factory._instances += 1  # increase counter when object is created

    @classmethod
    def get_instance(cls):
        if cls._instances >= 2: # check if already created twice
            print("Warning: Word16 already instantiated twice.\n")
            return None
        return cls()

    def create_panel(self):
        return Word16Panel()

    def create_button(self):
        return Word16Button()

    def create_textbox(self):
        return Word16Textbox()


# concrete factory for word26 with limited singleton behavior
class Word26Factory(GUIFactory):

    _instances = 0  # track number of created instances

    def __init__(self):
        Word26Factory._instances += 1  # increase counter when object is created

    @classmethod
    def get_instance(cls):
        if cls._instances >= 2: # check if already created twice
            print("Warning: Word26 already instantiated twice.\n")
            return None
        return cls()

    def create_panel(self):
        return Word26Panel()

    def create_button(self):
        return Word26Button()

    def create_textbox(self):
        return Word26Textbox()


# function to choose correct factory based on version name
def get_factory(version):

    factories = {
        "Word96": Word96Factory,
        "Word06": Word06Factory,
        "Word16": Word16Factory,
        "Word26": Word26Factory
    }  # dictionary mapping version names to factory classes

    if version not in factories:  # check if version is supported
        print(f"Warning: {version} is not supported.\n")
        return None

    return factories[version].get_instance()  # return factory instance


# function that reads config file and runs the test
def run_test(config_file):

    with open(config_file, "r") as file:  # open file
        for line in file:  # read each line
            version = line.strip()  # remove whitespace
            factory = get_factory(version)  # get appropriate factory

            if factory:  # only proceed if factory is valid
                panel = factory.create_panel()  # create panel
                button = factory.create_button()  # create button
                textbox = factory.create_textbox()  # create textbox

                panel.display()  # display panel message
                button.display()  # display button message
                textbox.display()  # display textbox message
                print()  # print blank line for formatting


# program starting point
if __name__ == "__main__":
    run_test("config.txt")  # call main test function