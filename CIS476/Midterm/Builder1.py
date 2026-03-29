from abc import ABC, abstractmethod

# -------------------
# Product
# -------------------
class Plane:
    def __init__(self):
        self.parts = {}

    def add_part(self, name, value):
        self.parts[name] = value

    def show(self):
        print("Plane configuration:")
        for part, value in self.parts.items():
            print(f"  {part}: {value}")
        print()


# -------------------
# Builder interface
# -------------------
class PlaneBuilder(ABC):
    @abstractmethod
    def build_engine(self):
        pass

    @abstractmethod
    def build_wings(self):
        pass

    @abstractmethod
    def build_weapons(self):
        pass

    @abstractmethod
    def build_paint(self):
        pass

    @abstractmethod
    def get_result(self):
        pass


# -------------------
# Concrete Builders
# -------------------
class CropDusterBuilder(PlaneBuilder):
    def __init__(self):
        self.plane = Plane()

    def build_engine(self):
        self.plane.add_part("Engine", "Small piston engine")

    def build_wings(self):
        self.plane.add_part("Wings", "Standard wings with sprayers")

    def build_weapons(self):
        self.plane.add_part("Weapons", "None")

    def build_paint(self):
        self.plane.add_part("Paint", "Yellow with red stripes")

    def get_result(self):
        return self.plane


class FighterJetBuilder(PlaneBuilder):
    _instance = None  # Singleton storage for FighterJet

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        else:
            print("Sorry, only one Fighter Jet can exist! Cannot create another.")
            return None  # Block creation
        return cls._instance

    def __init__(self):
        self.plane = Plane()

    def build_engine(self):
        self.plane.add_part("Engine", "Turbojet engine")

    def build_wings(self):
        self.plane.add_part("Wings", "Swept wings with missile hardpoints")

    def build_weapons(self):
        self.plane.add_part("Weapons", "Missiles, Guns")

    def build_paint(self):
        self.plane.add_part("Paint", "Camouflage grey")

    def get_result(self):
        return self.plane


class GliderBuilder(PlaneBuilder):
    def __init__(self):
        self.plane = Plane()

    def build_engine(self):
        self.plane.add_part("Engine", "None")

    def build_wings(self):
        self.plane.add_part("Wings", "Extra long glider wings")

    def build_weapons(self):
        self.plane.add_part("Weapons", "None")

    def build_paint(self):
        self.plane.add_part("Paint", "White")

    def get_result(self):
        return self.plane


# -------------------
# Director
# -------------------
class Director:
    def construct(self, builder: PlaneBuilder):
        if builder is None:
            print("Cannot construct: Builder instance is not available.")
            return None
        builder.build_engine()
        builder.build_wings()
        builder.build_weapons()
        builder.build_paint()
        return builder.get_result()


# -------------------
# MAIN TEST
# -------------------
if __name__ == "__main__":
    director = Director()

    # Normal planes
    cropduster = director.construct(CropDusterBuilder())
    if cropduster:
        cropduster.show()

    glider = director.construct(GliderBuilder())
    if glider:
        glider.show()

    # Singleton plane (only one Fighter Jet allowed)
    fighter1 = director.construct(FighterJetBuilder())
    if fighter1:
        fighter1.show()

    # Attempting to build a second Fighter Jet
    fighter2 = director.construct(FighterJetBuilder())
    if fighter2:
        fighter2.show()