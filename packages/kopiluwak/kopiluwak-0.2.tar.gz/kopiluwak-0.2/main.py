# extended_code.py

class ShoppingCart:
    def __init__(self):
        self.items = []

    def add_item(self, item, quantity):
        self.items.append({"item": item, "quantity": quantity})

    def remove_item(self, item_name):
        for item in self.items:
            if item["item"] == item_name:
                self.items.remove(item)
                return
        print(f"{item_name} not found in the cart.")

    def total(self):
        total_cost = sum(item["item"].price * item["quantity"] for item in self.items)
        return total_cost

class Item:
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def __str__(self):
        return f"{self.name}: ${self.price:.2f}"

def main():
    # Creating items
    apple = Item("Apple", 1.50)
    banana = Item("Banana", 0.75)
    orange = Item("Orange", 1.25)

    # Creating shopping cart
    cart = ShoppingCart()

    # Adding items to the cart
    cart.add_item(apple, 2)
    cart.add_item(banana, 4)
    cart.add_item(orange, 1)

    # Displaying items in the cart
    print("Items in the shopping cart:")
    for item in cart.items:
        print(f"{item['item']} - Quantity: {item['quantity']}")

    # Removing an item from the cart
    cart.remove_item("Banana")

    # Displaying total cost
    print(f"Total cost: ${cart.total():.2f}")

if __name__ == "__main__":
    main()
