
# lockers.py
from __future__ import annotations
from _typeshed import Self
import abc
from collections import defaultdict
from dataclasses import dataclass
from enum import Enum
from typing import List


@dataclass
class Location:
    street_address: str
    postal_code: str
    city: str
    country: str


class Size(Enum):
    small: 1
    medium: 2
    large: 3


def generate_locker_id() -> str:
    raise NotImplementedError


class Locker:
    def __init__(self, location: Location,
                    s_units: int, m_units: int, l_units: int):
        self.id = generate_locker_id()
        self.location = location
        self.s_units = s_units
        self.m_units = m_units
        self.l_units = l_units

        self._units = defaultdict(list)
        self.__build_units()

    @property
    def is_full(self) -> bool:
        pass

    def unlock_unit(self, unit_id, code) -> bool:
        pass

    def add_package(self, unit_id, package: Package):
        pass

    def __build_units(self):
        for _ in range(self.s_units):
            self._units[Size.small].append(UnitFactory.new_small_unit())
        
        for _ in range(self.m_units):
            self._units[Size.medium].append(UnitFactory.new_small_unit())

        for _ in range(self.l_units):
            self._units[Size.large].append(UnitFactory.new_small_unit())


class LockerFactory:
    @staticmethod
    def new_standard_locker(self, location):
        # Set def for number of S, M, L units
        return Locker(location)

    
    @staticmethod
    def new_custom_locker(self, id, location, s_units, m_units, l_units):
        return(location, s_units, m_units, l_units)


def generate_unit_id():
    pass


class Unit:
    def __init__(self, size: Size):
        self.id = generate_unit_id()
        self.size = size
        self.package = None
    
    @property
    def has_package(self) -> bool:
        return self.package is not None
    
    def insert_package(self, package: Package):
        self.package = Package
        self.__lock_unit()
        pass

    def remove_package(self, code: str):
        self.__unlock_unit()
        self.package = None
        pass

    def __lock_unit(self):
        pass

    def __unlock_unit(self):
        pass

    
class UnitFactory:
    @staticmethod
    def new_small_unit(self):
        return Unit(Size.small)

    @staticmethod
    def new_med_unit(self):
        return Unit(Size.medium)

    @staticmethod
    def new_large_unit(self):
        return Unit(Size.large)


class PackageStatus(Enum):
    ToBeShipped: 1
    OnTheWay: 2
    InLocker: 3
    Received: 4 
    Cancelled: 5

@dataclass
class Dimensions:
    width: float
    height: float
    length: float

    @property
    def volume(self):
        return self.width * self.height * self.length


@dataclass
class Package:
    package_id: str
    customer_id: str
    contents: str
    locker: Locker
    status: PackageStatus
    dimensions: Dimensions
    size: Size
    fragile: bool


@dataclass
class Person:
    name: str
    address: Location
    email: str
    phone: str

class AccountStatus(Enum):
    Active: 0
    Closed: 1
    Blacklisted: 2


class AbstractAccount(abc.ABC):
    def __init__(self, id, password, status: AccountStatus, person: Person):
        self.id = id
        self.password = password
        self.status = status
        self.person = person

    def reset_password(self, new_password) -> bool:
        if new_password == self.password:
            return False

        self.password = new_password
        return True


class EmployeeAccount(AbstractAccount):
    def __init__(self, id, password, status: AccountStatus, person: Person,
                employee_id: int, date_joined: str):
        super().__init__(id, password, status, person)
        self.employee_id =  employee_id
        self.date_joined = date_joined

    @property
    def annual_salary(self):
        pass


class DeliveryPerson(EmployeeAccount):
    def __init__(self, id, password, status: AccountStatus, person: Person,
                    employee_id: int, date_joined: str):
        super().__init__(id, password, status, person, employee_id, date_joined)

    def pick_up_packages(self):
        pass

    def insert_package_into_locker(self, locker: Locker, package: Package):
        pass

    def get_remaining_packages(self):
        # Show pending deliveries
        pass


class Customer(AbstractAccount):
    def __init__(self, id, password, status: AccountStatus, person: Person):
        super().__init__(id, password, status, person)

    def receive_package(self):
        pass

    def get_active_packages(self):
        pass


class AbstractNotification(abc.ABC):
    def __init__(self):
        self.id
        self.created_on
        self.content  # include pin-code

    @abc.abstractmethod
    def send_notification(self, recipient: Person):
        raise NotImplementedError


class EmailNotification(AbstractNotification):
    def send_notification(self):
        pass


class SmsNotification(AbstractNotification):
    def send_notification(self):
        pass


def singleton(_class):
    # Wrapper to turn a class into a singleton
    pass


@singleton
class LockerSystem:
    def __init__(self):
        pass

    def add_locker(self, location: Location, locker: Locker):
        # add to database
        pass

    def add_delivery_person(self, delivery_person: DeliveryPerson):
        # add to database
        pass

    def add_customer(self, customer: Customer):
        # add to database
        pass

    def assign_package_to_locker(self, customer: Customer, package: Package):
        # Find closest vacant locker for customer
        pass

    def assign_package_to_delivery_person(self, package:Package):
        pass






        