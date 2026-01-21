# Вам необходимо реализовать систему управления складом (InventoryManager)
# для магазина, которая поддерживает различные типы операций с товарами:
# AddItem (добавление),
# RemoveItem (удаление),
# TransferItem (перемещение между складами)
# AdjustPrice (изменение цены). Каждая операция должна:
# Иметь метод execute(InventoryItem item, BigDecimal amount).
# Менять состояние товара на складе.
# Могла быть отменена (undo операция).
# Все изменения состояния товаров должны происходить только через эти операции
# Реализуйте систему управления складом с привязкой к пользователям.
# В качестве ответа: ссылка на репозиторий с решением
from decimal import Decimal


class User:
    """
    Represents a user in the system.
    Attributes:
        username (str): The username of the user.
        role (str): The role of the user.
    """
    def __init__(self, username: str, role: str = "staff") -> None:
        self.username = username
        self.role = role

    def __str__(self) -> str:
        return f"User - {self.username}, role - {self.role}"


class InventoryItem:
    """
    Represents an item.
    Attributes:
        name (str): The name of the item.
        amount (Decimal): The amount of the item.
        price (Decimal): The price of the item.
        location (str): The storage location of the item.
    """
    def __init__(self, name: str, amount: Decimal, price: Decimal) -> None:
        """
        Initializes inventory
        """
        self.name = name
        self.amount = amount
        self.price = price
        self.location = "Main Storage"

    def __str__(self) -> str:
        """
        Returns string representation of inventory item
        """
        return (
            f"Name - {self.name}, amount - {self.amount}, " +
            f"price - {self.price}, location - {self.location}"
            )


class InventoryOperation:
    """
    Base class for inventory operations.
    """
    def execute(self, item: InventoryItem, amount: Decimal) -> None:
        """
        Execute the operation on the inventory item
        args:
            item (InventoryItem): The inventory item to operate on.
            amount (Decimal): The amount for the operation.
        Raises:
            NotImplementedError if not implemented
        """
        raise NotImplementedError("Execute not implemented")

    def undo(self, item: InventoryItem, amount: Decimal) -> None:
        """
        Undo the operation on the inventory item
        args:
            item (InventoryItem): The inventory item to operate on.
            amount (Decimal): The amount for the operation.
        Raises:
            NotImplementedError if not implemented
        """
        raise NotImplementedError("Undo not implemented")


class AddItem(InventoryOperation):
    """
    Adds items to inventory.
    """
    def execute(self, item: InventoryItem, amount: Decimal) -> None:
        """
        Execute add operation
        args:
            item (InventoryItem): The inventory item to operate on.
            amount (Decimal): The amount to add.
        """
        item.amount += int(amount)

    def undo(self, item: InventoryItem, amount: Decimal) -> None:
        """
        Undo add operation
        args:
            item (InventoryItem): The inventory item to operate on.
            amount (Decimal): The amount to remove.
        """
        item.amount -= int(amount)


class RemoveItem(InventoryOperation):
    """
    Removes items from inventory.
    """
    def execute(self, item: InventoryItem, amount: Decimal) -> None:
        """Execute remove operation
        args:
            item (InventoryItem): The inventory item to operate on.
            amount (Decimal): The amount to remove.
        """
        item.amount -= int(amount)

    def undo(self, item: InventoryItem, amount: Decimal) -> None:
        """Undo remove operation
        args:
            item (InventoryItem): The inventory item to operate on.
            amount (Decimal): The amount to add.
        """
        item.amount += int(amount)


class TransferItem(InventoryOperation):
    """
    Transfers items between storages
    """
    def __init__(self, new_location: str) -> None:
        """
        Initializes transfer operation
        args:
            new_location (str): The new location to transfer the item.
        """
        self.new_location = new_location
        self.old_location = None

    def execute(self, item: InventoryItem, amount: Decimal) -> None:
        """Execute transfer operation
        args:
            item (InventoryItem): The inventory item to operate on.
            amount (Decimal): not used in this operation.
        """
        self.old_location = item.location
        item.location = self.new_location

    def undo(self, item: InventoryItem, amount: Decimal) -> None:
        """Undo transfer operation
        args:
            item (InventoryItem): The inventory item to operate on.
            amount (Decimal): not used in this operation.
        """
        item.location = self.old_location


class AdjustPrice(InventoryOperation):
    """
    Adjusts the price of an item.
    """
    def __init__(self) -> None:
        """
        Initializes adjust price operation
        """
        self.old_price = None

    def execute(self, item: InventoryItem, amount: Decimal) -> None:
        """Execute adjust price operation
        args:
            item (InventoryItem): The inventory item to operate on
            amount (Decimal): The amount to adjust the price
        """
        self.old_price = item.price
        item.price += amount

    def undo(self, item: InventoryItem, amount: Decimal) -> None:
        """Undo adjust price operation
        args:
            item (InventoryItem): The inventory item to operate on.
            amount (Decimal): not used in this operation.
        """
        item.price = self.old_price


class InventoryManager:
    """
    Manages inventory operations.
    Attributes:
        history (list): A list of already performed
        operations for undo functions
    """
    def __init__(self) -> None:
        """
        Initializes inventory manager
        """
        self.history = []

    def perform_operation(
            self,
            user: User,
            operation: InventoryOperation,
            item: InventoryItem,
            amount: Decimal
            ) -> None:
        """
        Perform an inventory operation
        args:
            user (User): The user performing the operation.
            operation (InventoryOperation): The operation to perform.
            item (InventoryItem): The inventory item to operate on.
            amount (Decimal): The amount for the operation.
        """
        if isinstance(operation, AdjustPrice) and user.role != "admin":
            print("Error! Only admins can adjust prices")
        else:
            operation.execute(item, amount)
            self.history.append((operation, item, amount))

    def undo_last_operation(self) -> None:
        """
        Undo the last performed operation
        """
        if self.history:
            operation, item, amount = self.history.pop()
            operation.undo(item, amount)


if __name__ == "__main__":
    admin = User("admin_user", "admin")
    staff = User("staff_user", "staff")

    item = InventoryItem("Iphone", 10, Decimal("1599.99"))
    manager = InventoryManager()

    print(item)

    add_op = AddItem()
    manager.perform_operation(staff, add_op, item, Decimal(5))
    print(item)

    remove_op = RemoveItem()
    manager.perform_operation(staff, remove_op, item, Decimal(3))
    print(item)

    transfer_op = TransferItem("Another Storage")
    manager.perform_operation(staff, transfer_op, item, Decimal(0))
    print(item)

    adjust_price_op = AdjustPrice()
    manager.perform_operation(admin, adjust_price_op, item, Decimal("50.00"))
    print(item)

    adjust_price_op = AdjustPrice()
    manager.perform_operation(staff, adjust_price_op, item, Decimal("50.00"))
    print(item)

    manager.undo_last_operation()
    print(item)

    manager.undo_last_operation()
    print(item)
  
