from enum import Enum


# enum for delivery statuses
class DeliveryStatus(Enum):
    AT_HUB = 'At the hub'
    EN_ROUTE = 'En route'
    DELIVERED = 'Delivered'


# Package class
class Package:
    def __init__(self, package_id, address, city, state, zipcode, deadline, weight, status: DeliveryStatus):
        self.package_id = package_id
        self.address = address
        self.city = city
        self.state = state
        self.zipcode = zipcode
        self.deadline = deadline
        self.weight = weight
        self.status = status
        self.departure_time = None
        self.delivery_time = None

    # This method defines how a Package object should look as a string
    def __str__(self):
        return (f'Package ID: {self.package_id}, '
                f'Address: {self.address}, {self.city}, {self.state} {self.zipcode}, '
                f'Deadline: {self.deadline}, '
                f'Weight: {self.weight}, '
                f'Status: {self.status.value}, '
                f'Expected Delivery time: {self.delivery_time}')

    # Method for updating delivery status as a particular time
    def update_status(self, time_requested, truck_departure_time):
        if time_requested < truck_departure_time:
            self.status = DeliveryStatus.AT_HUB
        elif self.delivery_time < time_requested:
            self.status = DeliveryStatus.DELIVERED
        elif self.delivery_time > time_requested:
            self.status = DeliveryStatus.EN_ROUTE
        else:
            self.status = DeliveryStatus.AT_HUB
