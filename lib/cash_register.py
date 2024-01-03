#!/usr/bin/env python3

class CashRegister:
    def __init__(self, discount=0):
        self.items = []
        self.discount = discount
        self.last_transaction = 0

    def add_item(self, item, price, quantity=1):
        for _ in range(quantity):
            self.items.append((item, price))
        self.last_transaction = price * quantity

    def calculate_total(self):
        return sum(item[1] for item in self.items)

    def apply_discount(self):
        if self.discount > 0:
            discount_amount = (self.discount / 100) * self.calculate_total()
            return int(self.calculate_total() - discount_amount)
        else:
            return self.calculate_total()

    def void_last_transaction(self):
        if self.items:
            self.items.pop()
            self.last_transaction = 0
        else:
            print("No transactions to void.")

# Example usage
register = CashRegister(discount=10)
register.add_item("Apple", 2.5, 3)
register.add_item("Banana", 1.2, 2)

print(f"Total before discount: ${register.calculate_total()}")
print(f"Total after discount: ${register.apply_discount()}")

register.void_last_transaction()
print(f"Total after voiding last transaction: ${register.calculate_total()}")

class CashRegister:
    def __init__(self, discount=0):
        self.items = []
        self.discount = discount
        self.total = 0
        self.last_transaction = 0

    def add_item(self, title, price, quantity=1):
        for _ in range(quantity):
            self.items.append((title, price))
        self.last_transaction = price * quantity
        self.total += self.last_transaction

    def apply_discount(self):
        if self.discount > 0:
            discount_amount = (self.discount / 100) * self.total
            self.total = int(self.total - discount_amount)
            print(f"After the discount, the total comes to ${self.total}.")
        else:
            print("There is no discount to apply.")

    def void_last_transaction(self):
        if self.items:
            self.items.pop()
            self.total -= self.last_transaction
            self.last_transaction = 0
        else:
            print("No transactions to void.")

    def items_list(self):
        return [item[0] for item in self.items]

# Example usage
register = CashRegister(discount=10)
register.add_item("Apple", 2.5, 3)
register.add_item("Banana", 1.2, 2)

print(f"Total before discount: ${register.total}")
register.apply_discount()

register.void_last_transaction()
print(f"Total after voiding last transaction: ${register.total}")
print(f"Items in the register: {register.items_list()}")

import io
import sys
import pytest
from cash_register import CashRegister

class TestCashRegister:

    def setup_method(self, method):
        self.cash_register = CashRegister()
        self.cash_register_with_discount = CashRegister(20)

    def test_total_attribute(self):
        '''sets an instance variable total to zero on initialization.'''
        assert self.cash_register.total == 0

    def test_add_item(self):
        '''accepts a title and a price and increases the total.'''
        self.cash_register.add_item("eggs", 0.98)
        assert self.cash_register.total == 0.98

    def test_add_item_optional_quantity(self):
        '''also accepts an optional quantity.'''
        self.cash_register.add_item("book", 5.00, 3)
        assert self.cash_register.total == 15.00

    def test_add_item_with_multiple_items(self):
        '''doesn't forget about the previous total'''
        self.cash_register.add_item("Lucky Charms", 4.5)
        assert self.cash_register.total == 4.5

    def test_apply_discount(self):
        '''applies the discount to the total price.'''
        self.cash_register_with_discount.add_item("macbook air", 1000)
        self.cash_register_with_discount.apply_discount()
        assert self.cash_register_with_discount.total == 800

    def test_apply_discount_success_message(self):
        '''prints success message with updated total'''
        captured_out = io.StringIO()
        sys.stdout = captured_out
        self.cash_register_with_discount.add_item("macbook air", 1000)
        self.cash_register_with_discount.apply_discount()
        sys.stdout = sys.__stdout__
        assert captured_out.getvalue() == "After the discount, the total comes to $800.\n"

    def test_apply_discount_reduces_total(self):
        '''reduces the total'''
        self.cash_register_with_discount.add_item("macbook air", 1000)
        self.cash_register_with_discount.apply_discount()
        assert self.cash_register_with_discount.total == 800

    def test_apply_discount_when_no_discount(self):
        '''prints a string error message that there is no discount to apply'''
        captured_out = io.StringIO()
        sys.stdout = captured_out
        self.cash_register.apply_discount()
        sys.stdout = sys.__stdout__
        assert captured_out.getvalue() == "There is no discount to apply.\n"

    def test_items_list_without_multiples(self):
        '''returns an array containing all items that have been added'''
        new_register = CashRegister()
        new_register.add_item("eggs", 1.99)
        new_register.add_item("tomato", 1.76)
        assert set(new_register.items_list()) == set(["eggs", "tomato"])

    def test_items_list_with_multiples(self):
        '''returns an array containing all items that have been added, including multiples'''
        new_register = CashRegister()
        new_register.add_item("eggs", 1.99, 2)
        new_register.add_item("tomato", 1.76, 3)
        assert set(new_register.items_list()) == set(["eggs", "eggs", "tomato", "tomato", "tomato"])

    def test_void_last_transaction(self):
        '''subtracts the last item from the total'''
        self.cash_register.add_item("apple", 0.99)
        self.cash_register.add_item("tomato", 1.76)
        self.cash_register.void_last_transaction()
        assert self.cash_register.total == 0.99

    def test_void_last_transaction_with_multiples(self):
        '''returns the total to 0.0 if all items have been removed'''
        self.cash_register.add_item("tomato", 1.76, 2)
        self.cash_register.void_last_transaction()
        assert self.cash_register.total == 0.0
