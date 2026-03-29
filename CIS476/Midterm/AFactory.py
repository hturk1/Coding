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
# Concrete Factories
# -------------------
class WindowsFactory(WidgetFactory):
    def create_button(self) -> Button:
        return PushButtonWindow()

    def create_textfield(self) -> TextField:
        return TextFieldWindow()

class MacFactory(WidgetFactory):
    def create_button(self) -> Button:
        return PushButtonMac()

    def create_textfield(self) -> TextField:
        return TextFieldMac()

# -------------------
# MAIN TEST
# -------------------
if __name__ == "__main__":
    # Windows UI
    windows_factory = WindowsFactory()
    btn_win = windows_factory.create_button()
    txt_win = windows_factory.create_textfield()

    btn_win.render()
    txt_win.render()

    print()

    # Mac UI
    mac_factory = MacFactory()
    btn_mac = mac_factory.create_button()
    txt_mac = mac_factory.create_textfield()

    btn_mac.render()
    txt_mac.render()