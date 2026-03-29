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

    cropduster = director.construct(CropDusterBuilder())
    cropduster.show()

    fighter = director.construct(FighterJetBuilder())
    fighter.show()

    glider = director.construct(GliderBuilder())
    glider.show()