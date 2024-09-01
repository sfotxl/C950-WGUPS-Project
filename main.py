# C950 Task 2 - Kalani Man - km6 - 000775194

import csv
from datetime import timedelta
from package import Package, DeliveryStatus
from hashtable import HashTable
from truck import Truck


# Open the necessary files
with open('data/packages.csv') as packages_csv:
    PackagesCSV = list(csv.reader(packages_csv))

with open('data/distances.csv') as distances_csv:
    DistancesCSV = list(csv.reader(distances_csv))

with open('data/addresses.csv') as addresses_csv:
    AddressesCSV = list(csv.reader(addresses_csv))


# Create packages from the PackagesCSV file and load them into the HashTable
def create_packages(file, hashtable):
    for package in PackagesCSV:
        package_id = int(package[0])
        address = package[1]
        city = package[2]
        state = package[3]
        zipcode = package[4]
        deadline = package[5]
        weight = package[6]
        status = DeliveryStatus.AT_HUB

        # Create the package object
        temp_package = Package(package_id, address, city, state, zipcode, deadline, weight, status)

        # Insert the package object into the hashtable
        hashtable.insert(package_id, temp_package)


# Function to calculate distance between two addresses
def distance_between(address_x, address_y):
    distance = DistancesCSV[address_x][address_y]
    # If this produces no value, then swap x and y
    if distance == '':
        distance = DistancesCSV[address_y][address_x]
    return float(distance)


# Function to find the distance between addresses in the addresses list
def get_address_row(address):
    for r in AddressesCSV:
        if address in r[2]:
            return int(r[0])


# Create the HashTable for packages
projectHashTable = HashTable()

# Create packages from the csv file
create_packages('data/packages.csv', projectHashTable)

# Create three trucks with initial loads at the hub
Truck1 = Truck(16, [1, 13, 14, 15, 16, 19, 20, 21, 23, 29, 30, 37, 40],0.0, '4001 South 700 East',
               timedelta(hours=8))
Truck2 = Truck(16, [3, 6, 7, 18, 22, 24, 25, 31, 32, 34, 36, 38], 0.0, '4001 South 700 East',
               timedelta(hours=9, minutes=5))
# Truck 3 is loaded with Package 8, for which we will receive the correct address at 10:20am
Truck3 = Truck(16, [2, 4, 5, 8, 9, 10, 11, 12, 17, 26, 27, 28, 33, 35, 39], 0.0, '4001 South 700 East',
               timedelta(hours=10, minutes=20))


# Function for selecting packages via nearest neighbor
def package_selection(truck):
    # Create an empty list for undelivered packages
    undelivered_packages = []
    # Move all packages into the undelivered packages list
    for package in truck.packages:
        package = projectHashTable.get(package)
        undelivered_packages.append(package)

    # Clear the packages list for the truck so we can load the truck in order
    truck.packages.clear()

    # Add packages to the list using nearest neighbor
    while len(undelivered_packages) > 0:
        # Set nearest_address to 20 since 14.2 is the maximum distance between two addresses
        nearest_address = 20
        nearest_package = None
        for package in undelivered_packages:
            if distance_between(get_address_row(truck.address), get_address_row(package.address)) <= nearest_address:
                nearest_address = distance_between(get_address_row(truck.address), get_address_row(package.address))
                nearest_package = package

        # Add nearest package to the truck's delivery route
        truck.packages.append(nearest_package.package_id)

        # Remove the selected package from the undelivered list
        undelivered_packages.remove(nearest_package)

        # Update truck location to next package address
        truck.address = nearest_package.address

        # Update truck mileage
        truck.mileage += nearest_address

        # Update the time it took for the truck to drive to the nearest package
        truck.time += timedelta(hours=nearest_address / truck.speed)

        # Update delivery time
        nearest_package.delivery_time = truck.time
        nearest_package.departure_time = truck.departure_time


# Load each truck with package_selection
package_selection(Truck1)
package_selection(Truck2)
# There are only 2 drivers, so Truck 3 cannot leave until Truck1 or Truck2 is finished
driver_free = min(Truck1.time, Truck2.time)
# Truck 3 must also wait until the correct address for Package 8 is received
Truck3.departure_time = max(Truck3.departure_time, driver_free)
package_selection(Truck3)


class Main:
    # Display a welcome message to the user
    print('Welcome to the WGUPS Tracking Application!')

    while True:
        # Get the time in HH:MM from the user
        print('Enter a time (HH:MM) you would like a status update for.')
        print('Or type "exit" to quit this application.')
        user_input = input()

        if user_input.lower() == 'exit':
            break

        try:
            # Parse the input time
            (hours, minutes) = user_input.split(':')
            user_time = timedelta(hours=int(hours), minutes=int(minutes))

            # Calculate and display truck mileage for the day
            truck_mileage = Truck1.mileage + Truck2.mileage + Truck3.mileage
            print(f'Total truck mileage for today is {truck_mileage} miles.')

            # Update delivery statuses based on the requested time
            print('Here are package statuses at the requested time.')
            for packageID in range(1, 41):
                package = projectHashTable.get(packageID)

                # Update statuses for packages
                truck_departure_time = 0
                while truck_departure_time == 0:
                    for loaded_package in Truck1.packages:
                        if loaded_package == packageID:
                            truck_departure_time = Truck1.departure_time
                    for loaded_package in Truck2.packages:
                        if loaded_package == packageID:
                            truck_departure_time = Truck2.departure_time
                    for loaded_package in Truck3.packages:
                        if loaded_package == packageID:
                            truck_departure_time = Truck3.departure_time
                package.update_status(user_time, truck_departure_time)

            # Display package statuses by truck
            print('Packages in Truck 1: ')
            for package in Truck1.packages:
                print(projectHashTable.get(package))
            print('Packages in Truck 2: ')
            for package in Truck2.packages:
                print(projectHashTable.get(package))
            print('Packages in Truck 3: ')
            for package in Truck3.packages:
                print(projectHashTable.get(package))

        except ValueError:
            print('Invalid time format. Please enter a time in HH:MM format.')


if __name__ == "__main__":
    Main()
