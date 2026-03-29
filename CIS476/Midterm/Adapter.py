from abc import ABC, abstractmethod

# Vendor 1 sensors
class TS1:
    def get_temperature(self):
        return "return to TS1 with Temp in Fahrenheit: 75"

class TS2:
    def get_temperature(self):
        return "return to TS2 with Temp in Fahrenheit: 80"

# Vendor 2 sensor
class TS3:
    def get_temperature_celsius(self):
        return "return to TS3 with Temp in Celsius: 24"

# Adapter Interface
class TemperatureSensor(ABC):
    @abstractmethod
    def get_temperature(self):
        pass

# Adapters
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

class TS3Adapter(TemperatureSensor):
    def __init__(self, sensor: TS3):
        self.sensor = sensor
    def get_temperature(self):
        # Convert Celsius to Fahrenheit
        msg = self.sensor.get_temperature_celsius()
        celsius = float(msg.split(": ")[1])
        fahrenheit = celsius * 9/5 + 32
        return f"return to TS3 with Temp in Fahrenheit: {fahrenheit:.1f}"

# Client Code
if __name__ == "__main__":
    sensors = [
        TS1Adapter(TS1()),
        TS2Adapter(TS2()),
        TS3Adapter(TS3())
    ]
    for sensor in sensors:
        print(sensor.get_temperature())