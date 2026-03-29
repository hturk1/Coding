from abc import ABC, abstractmethod

# -------------------
# Vendor 1 sensors
# -------------------
class TS1:
    def get_temperature(self):
        return "return to TS1 with Temp in Fahrenheit: 75"

class TS2:
    def get_temperature(self):
        return "return to TS2 with Temp in Fahrenheit: 80"

# -------------------
# Vendor 2 sensor
# -------------------
class TS3:
    def get_temperature_celsius(self):
        return "return to TS3 with Temp in Celsius: 24"

# -------------------
# Adapter Interface
# -------------------
class TemperatureSensor(ABC):
    @abstractmethod
    def get_temperature(self):
        pass

# -------------------
# Adapters for TS1 and TS2
# -------------------
class TS1Adapter(TemperatureSensor):
    def __init__(self, sensor: TS1):
        self.sensor = sensor

    def get_temperature(self):
        return self.sensor.get_temperature()

class TS2Adapter(TemperatureSensor):
    def __init__(self, sensor: TS2):
        self.sensor = sensor

    def get_temperature(self):
        return self.sensor.get_temperature()

# -------------------
# TS3 Adapter with Singleton (print-and-block)
# -------------------
class TS3AdapterSingleton(TemperatureSensor):
    _instance = None

    def __new__(cls, sensor: TS3):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        else:
            print("Only one TS3 sensor can be used in the system! Cannot create another.")
            return None
        return cls._instance

    def __init__(self, sensor: TS3):
        self.sensor = sensor

    def get_temperature(self):
        msg = self.sensor.get_temperature_celsius()
        celsius = float(msg.split(": ")[1])
        fahrenheit = celsius * 9/5 + 32
        return f"return to TS3 with Temp in Fahrenheit: {fahrenheit:.1f}"

# -------------------
# Client Code
# -------------------
if __name__ == "__main__":
    sensors = [
        TS1Adapter(TS1()),
        TS2Adapter(TS2())
    ]

    # First TS3 works
    ts3_single = TS3AdapterSingleton(TS3())
    if ts3_single:
        sensors.append(ts3_single)

    for sensor in sensors:
        print(sensor.get_temperature())

    # Attempt second TS3 (blocked)
    ts3_second = TS3AdapterSingleton(TS3())
    if ts3_second:
        sensors.append(ts3_second)