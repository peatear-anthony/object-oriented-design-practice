import enum
import datetime
from abc import ABC, abstractmethod
from collections import defaultdict
from dataclasses import dataclass
from typing import List


@dataclass
class Location:
    address: str
    city: str
    postal_code: str
    country: str


class MachineStatus(enum.Enum):
    Active: 1
    LowStock: 2
    OutOfOrder: 3


# inside product.py
class AbstractProduct(ABC):
    def __init__(self, id, price, name, barcode):
        self.id = id
        self.price = price
        self.name = name
        self.barcode = barcode

    def __str__(self):
        raise NotImplementedError
    

class ConsumableProduct(AbstractProduct):
    def __init__(self, id, price, name, barcode, expiry_date):
        super().__init__(id, price, name, barcode)
        self.expiry_date = expiry_date
    
    def is_expired(self):
        return self.expiry_date > datetime.date.today()

# rack.py
class Rack:
    def __init__(self, id, max_capacity, status):
        self.id = id
        self.max_capacity = max_capacity
        self.status = MachineStatus.Active
        self.products = []

    @property
    def top_product(self):
        if len(self):
            return self.products[-1]
        else:
            return None

    def __len__(self):
        return self.max_capacity - len(self.products)

    def get_current_capacity(self):
        return len(self)

    def is_full(self) -> bool:
        return self.max_capacity == len(self)

    def load(self, product: AbstractProduct):
        if self.max_capacity > len(self):
            self.products.append(product)
            return True
        else:
            return False

    def has_expired_products(self):
        # Make this query at most once a day
        for product in self.products:
            if type(product) is ConsumableProduct and product.is_expired():
                return True

        return False

    def dispense(self):
        if self.status == MachineStatus.Active and len(self):
            dispensed_product = self.products.pop()
            print(f'Rack {self.id} dispensed: {str(dispensed_product)} ')
            return True
        
        else:
            return False


# coin_system.py
class InvalidCoinError(Exception):
    pass


class CoinBank:
    denoms = [1, 5, 10, 25]

    def __init__(self, max_capacity: int):
        self.max_capacity
        self.coin_bank = {coin: 0 for coin in CoinBank.denoms}

    @property
    def total(self):
        return sum(coin*count for coin, count in self.coin_bank.items()) // 100
    
    def add_coin(self, coin):
        if coin not in CoinBank.denoms:
            raise InvalidCoinError(f'{coin} not valid denomination.')
        
        elif self.coin_bank[coin] < self.max_capacity:
            self.coin_bank[coin] += 1
        else:
            return False

    def dispense_coin(self, coin):
        if self.coin_bank[coin] > 0:
            self.coin_bank[coin] -= 1
        else:
            # Handle lack of change case
            raise Exception

    def dispense_coins(self):
        # Assume it will dispense coins to collect profit
        # But will leave a specificed amount to return change to customers
        raise NotImplementedError
    

class CoinSystem:
    def __init__(self):
        self.status = MachineStatus.Active
        self.coin_bank = CoinBank(max_capacity=500)
        self.currently_loaded_coins = []

    @property
    def total_loaded(self):
        return sum(self.currently_loaded_coins) // 100

    def load_coin(self, coin):
        if coin not in CoinBank.denoms:
            self.dispense_coin(coin)
        else:
            self.currently_loaded_coins.append(coin)

    def charge(self, cost):
        change = cost - self.total_loaded

        for coin in self.currently_loaded_coins:
            self.coin_bank.add_coin(coin)

        for coin in self.__calc_optimal_coin_combo(change):
            self.coin_bank.dispense_coin(coin)
            print('Dispensing ', str(coin))

    def return_coins_loaded(self):
        for coin in self.currently_loaded_coins:
            print('Returning ', str(coin))
    
    def __calc_optimal_coin_combo(self, amount) -> List[int]:
        # Use greedy algorithm to determine the coin combination to return
        raise NotImplementedError


# Inside display.py

class AbstractDisplay(ABC):
    @abstractmethod
    def update_display(self):
        raise NotImplementedError


class MaintainceDisplay(AbstractDisplay):
    def show_product_stock(self):
        raise NotImplementedError

    def show_coin_stock(self):
        raise NotImplementedError

    def update_display(self):
        self.show_coin_stock()
        self.show_product_stock()


class ExternalDisplay(AbstractDisplay):
    def show_total_amount(self):
        raise NotImplementedError

    def show_currently_selected(self):
        raise NotImplementedError

    def show_total_change_inserted(self):
        raise NotImplementedError

    def show_products_available(self):
        raise NotImplementedError

    def update_display(self):
        self.show_currently_selected()
        self.show_total_amount()
        self.show_total_change_inserted()
        self.show_products_available()


# Inside interface.py

class Interface:
    def __init__(self):
        self.current_selections = []

    def select_deselect_rack(self, rack_id):
        raise NotImplementedError
    
    def purchase(self):
        raise NotImplementedError
    
    def return_change(self):
        raise NotImplementedError
    
    def insert_change(self):
        raise NotImplementedError

    def check_for_input(self):
        raise NotImplementedError

    def get_action(self):
        raise NotImplementedError


# Inside vending_machine.py
class DuplicateRackError(Exception):
    pass


# Might want to make this class a singleton
class VendingMachine:
    def __init__(self, id, location: Location):
        self.id = id
        self.location = location
        self.status = MachineStatus.Active

        self.__maintenance_display = MaintainceDisplay()
        self.__external_display = ExternalDisplay()
        self.__interface = Interface()
        self.__coin_system = CoinSystem()

        self.__racks = {}

    def add_new_rack(self, rack:Rack):
        if rack.id in self.__racks:
            raise DuplicateRackError

        self.__racks[rack.id] = rack

    def set_status(self, updated_status: MachineStatus):
        self.status = updated_status

    def __run_active(self):
        self.__external_display.update_display()

        if self.__interface.check_for_input():
            action = self.__interface.get_action()

            if action == 'insert_change':
                self.__coin_system.load_coin()

            elif action == 'return_coins':
                self.__coin_system.return_coins_loaded()

            elif action == 'purchase':
                selected_racks = [self.__racks[id]
                    for id in self.__interface.selected_racks] 

                total_cost = sum(rack.top_product.price
                    for rack in selected_racks)

                if self.__coin_system.total_loaded >= total_cost:
                    self.__coin_system.charge(total_cost)

                for rack in selected_racks:
                    rack.dispense()


    def __run_out_of_order(self):
        self.__maintenance_display.update_display()
        # Load products, load change, collect change here.


    def run(self):
        while True:
            if self.status == MachineStatus.Active:
                self.__run_active(self)
            
            elif self.stauts == MachineStatus.LowStock:
                self.__run_active(self)
                # send notification to maintenance staff  
            
            elif self.status == MachineStatus.OutOfOrder:
                self.__run_out_of_order(self)