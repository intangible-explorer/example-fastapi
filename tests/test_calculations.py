# import pytest
# from ..app.calculations import add, subtract, multiply, divide, BankAccount, InsufficientFundsException

# @pytest.fixture
# def zero_bank_account():
#     return BankAccount()

# @pytest.fixture
# def bank_account():
#     return BankAccount(50)

# @pytest.mark.parametrize("num1, num2, expected", [
#     (5, 3, 8),
#     (5, 5, 10),
#     (10, 5, 15),
#     (10, 10, 20),
# ])
# def test_add(num1, num2, expected):
#     print("testing add function")
#     assert add(num1,num2) == expected

# def test_subtract():
#     print("testing subtract function")
#     assert subtract(5,3) == 2

# def test_multiply():
#     print("testing multiply function")
#     assert multiply(5,3) == 15

# def test_divide():
#     print("testing divide function")
#     assert divide(5,3) == 1

# def test_bank_default_amount(zero_bank_account):
#     assert zero_bank_account.balance == 0

# def test_bank_set_initial_amount(bank_account):
#     assert bank_account.balance == 50

# def test_withdraw(bank_account):
#     bank_account.withdraw(20)
#     assert bank_account.balance == 30

# def test_deposit(bank_account):
#     bank_account.deposit(20)
#     assert bank_account.balance == 70

# def test_collect_interest(bank_account):
#     bank_account.collect_interest()
#     assert round(bank_account.balance, 2) == 55

# @pytest.mark.parametrize("deposit, withdraw, expected", [
#     (200, 100, 100),
#     (50, 10, 40),
#     (500, 200, 300)
# ])
# def test_bank_transaction(zero_bank_account, deposit, withdraw, expected):
#     zero_bank_account.deposit(deposit)
#     zero_bank_account.withdraw(withdraw)
#     assert zero_bank_account.balance == expected

# def test_insufficient_funds(zero_bank_account):
#     with pytest.raises(InsufficientFundsException):
#         zero_bank_account.withdraw(100)
    