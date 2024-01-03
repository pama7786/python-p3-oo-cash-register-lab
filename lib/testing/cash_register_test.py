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
