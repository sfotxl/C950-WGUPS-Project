# Truck class

class Truck:
    # Constructor
    def __init__(self, capacity, packages, mileage, address, departure_time):
        self.capacity = capacity
        self.packages = packages
        self.mileage = mileage
        self.address = address
        self.departure_time = departure_time
        self.speed = 18
        self.time = departure_time

    # Method for displaying truck info (mainly for debugging)
    def __str__(self):
        return (f'Capacity: {self.capacity}'
                f'\nPackages: {self.packages}'
                f'\nAddress: {self.address}'
                f'\nDeparture time: {self.departure_time}')
