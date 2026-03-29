from abc import ABC, abstractmethod

# -------------------
# Abstract Products
# -------------------
class Button(ABC):
    @abstractmethod
    def render(self):
        pass

class TextField(ABC):
    @abstractmethod
    def render(self):
        pass

# -------------------
# Concrete Products – Windows
# -------------------
class PushButtonWindow(Button):
    def render(self):
        print("This is Window Button as PushButtonWindow")

class TextFieldWindow(TextField):
    def render(self):
        print("This is Window TextField as TextFieldWindow")

# -------------------
# Concrete Products – Mac
# -------------------
class PushButtonMac(Button):
    def render(self):
        print("This is Mac Button as PushButtonMac")

class TextFieldMac(TextField):
    def render(self):
        print("This is Mac Text Field as TextFieldMac")

# -------------------
# Abstract Factory
# -------------------
class WidgetFactory(ABC):
    @abstractmethod
    def create_button(self) -> Button:
        pass

    @abstractmethod
    def create_textfield(self) -> TextField:
        pass

# -------------------
# Concrete Factories with Singleton enforced
# -------------------
class WindowsFactory(WidgetFactory):
    _instance = None  # Singleton storage

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        else:
            print("Only one WindowsFactory can exist! Cannot create another.")
            return None
        return cls._instance

    def create_button(self) -> Button:
        return PushButtonWindow()

    def create_textfield(self) -> TextField:
        return TextFieldWindow()


class MacFactory(WidgetFactory):
    _instance = None  # Singleton storage

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        else:
            print("Only one MacFactory can exist! Cannot create another.")
            return None
        return cls._instance

    def create_button(self) -> Button:
        return PushButtonMac()

    def create_textfield(self) -> TextField:
        return TextFieldMac()


# -------------------
# MAIN TEST
# -------------------
if __name__ == "__main__":
    # First Windows factory (works)
    windows_factory1 = WindowsFactory()
    if windows_factory1:
        btn_win = windows_factory1.create_button()
        txt_win = windows_factory1.create_textfield()
        btn_win.render()
        txt_win.render()

    print()

    # Attempt to create second WindowsFactory (blocked)
    windows_factory2 = WindowsFactory()
    if windows_factory2:
        btn_win2 = windows_factory2.create_button()
        txt_win2 = windows_factory2.create_textfield()
        btn_win2.render()
        txt_win2.render()

    print()

    # First Mac factory (works)
    mac_factory1 = MacFactory()
    if mac_factory1:
        btn_mac = mac_factory1.create_button()
        txt_mac = mac_factory1.create_textfield()
        btn_mac.render()
        txt_mac.render()

    print()

    # Attempt to create second MacFactory (blocked)
    mac_factory2 = MacFactory()
    if mac_factory2:
        btn_mac2 = mac_factory2.create_button()
        txt_mac2 = mac_factory2.create_textfield()
        btn_mac2.render()
        txt_mac2.render()