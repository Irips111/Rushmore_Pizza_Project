import json
from datetime import datetime
import os
import random

# --- PIZZA MENU DATABASE ---
pizza_data = {
    "1": {"name": "Classic", "price": 3.4},
    "2": {"name": "Chicken", "price": 4.5},
    "3": {"name": "Pepperoni", "price": 4.0},
    "4": {"name": "Deluxe", "price": 6.0},
    "5": {"name": "Vegetable", "price": 4.0},
    "6": {"name": "Chocolate", "price": 12.0},
    "7": {"name": "Cheese", "price": 5.0},
    "8": {"name": "Hawaiian", "price": 7.0},
    "9": {"name": "Greek", "price": 8.0}
}

ORDERDB_FILE = 'pizza_orders.json'

# Randomly assign a Pizza of the Day with 25% discount
pizza_of_day_key = random.choice(list(pizza_data.keys()))
pizza_of_day = pizza_data[pizza_of_day_key]["name"]

def save_order_to_json(pizza_type, order_type, quantity, price, discount):
    """
    Save order details into a local JSON database file.
    """
    order = {
        'order_datetime': datetime.now().strftime('%Y-%m-%d-%H:%M:%S'),
        'pizza_type': pizza_type,
        'order_type': order_type,
        'quantity': quantity,
        'total_price': price,
        'discount_applied': discount
    }

    if os.path.exists(ORDERDB_FILE):
        with open(ORDERDB_FILE, 'r+', encoding='utf-8') as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError:
                data = []
            data.append(order)
            file.seek(0)
            json.dump(data, file, indent=4)
    else:
        with open(ORDERDB_FILE, 'w', encoding='utf-8') as file:
            json.dump([order], file, indent=4)

def calculate_payment(price, quantity, discount_rate=0.0):
    """
    Calculate total price with discount if applicable.
    """
    total = price * quantity
    discount = total * discount_rate
    return total - discount

def handle_box_order(pizza_name, price):
    """
    Handles ordering pizza by the box.
    Applies:
      - 10% discount for 5-9 boxes
      - 20% discount for 10+ boxes
      - Additional 25% if pizza is Pizza of the Day
    Saves order to JSON.
    """
    while True:
        qty_input = input("How many Box(es) do you want? (or type 'q' to cancel): ").strip()
        if qty_input.lower() == 'q':
            print('Box Order Cancelled')
            return
        elif qty_input.isdigit():
            quantity = int(qty_input)
            break
        else:
            print("Please enter a valid number.")

    # Determine discount rate
    discount_rate = 0.0
    if 5 <= quantity < 10:
        discount_rate = 0.10
    elif quantity >= 10:
        discount_rate = 0.20

    # Additional 25% discount if it’s Pizza of the Day
    if pizza_name == pizza_of_day:
        discount_rate += 0.25

    discount_applied = discount_rate > 0.0
    total = calculate_payment(price, quantity, discount_rate)

    print(f"Your payment is ${total:.2f} for {quantity} box(es) of {pizza_name}.")
    if discount_applied:
        print(f"Discount applied: {int(discount_rate * 100)}%")

    # Save to database
    save_order_to_json(pizza_name, 'Box', quantity, total, discount_applied)

def handle_slice_order(pizza_name, slice_price):
    """
    Handles ordering pizza by the slice.
    Applies:
      - 5% discount for 8 or more slices
      - Max limit: 16 slices per order
      - Additional 25% discount if Pizza of the Day
    Saves order to JSON.
    """
    while True:
        qty_input = input("How many slices do you want? (or type 'q' to cancel): ").strip()
        if qty_input.lower() == 'q':
            print('Slice Order Cancelled')
            return
        elif qty_input.isdigit():
            quantity = int(qty_input)
            if quantity > 16:
                print("Maximum of 16 slices per order. Please try again.")
                continue
            break
        else:
            print("Please enter a valid number.")

    # Discount logic
    discount_rate = 0.05 if quantity >= 8 else 0.0
    if pizza_name == pizza_of_day:
        discount_rate += 0.25

    discount_applied = discount_rate > 0.0
    total = calculate_payment(slice_price, quantity, discount_rate)

    print(f"Your payment is ${total:.2f} for {quantity} slice(s) of {pizza_name}.")
    if discount_applied:
        print(f"Discount applied: {int(discount_rate * 100)}%")

    save_order_to_json(pizza_name, 'Slice', quantity, total, discount_applied)

def pizza_selection_order(pizza_type):
    """
    Given the user's pizza choice key (1-9),
    shows pizza info and lets them choose between
    box or slice order.
    """
    if pizza_type in pizza_data:
        pizza = pizza_data[pizza_type]
        name = pizza["name"]
        price = pizza['price']
        slice_price = round(price / 8, 2)

        print(f"\nYou selected {name} Pizza")
        print(f"Price - ${price:.2f} per box | ${slice_price:.2f} per slice")
        
        # Notify if Pizza of the Day
        if name == pizza_of_day:
            print("*** Pizza of the Day! Enjoy an extra 25% discount! ***")

        # Choose box or slice
        while True:
            choice = input("Select 'B' for Box or 'S' for Slice (or 'q' to cancel): ").strip().upper()
            if choice == 'B':
                handle_box_order(name, price)
                break
            elif choice == 'S':
                handle_slice_order(name, slice_price)
                break
            elif choice == 'Q':
                print("Order Cancelled!")
                break
            else:
                print("Select either B, S or Q")
    else:
        print("We do not have this Pizza Flavour for now.")

def main_system():
    """
    Displays the menu and handle all users interactions.
    Announces Pizza of the Day on startup.
    """
    print("\n" + "=" * 40)
    print("🍕 Welcome to RushMore Pizzeria 🍕")
    print(f"👉 Today's Pizza of the Day: {pizza_of_day} (25% off!)")
    print("=" * 40)

    while True:
        print("\nHere is our menu:")
        for key, value in pizza_data.items():
            print(f"{key}: {value['name']} - ${value['price']}")

        # Make a selection.
        choice = input("\nPick your choice (1-9) or 'q' to quit: ").strip().lower()
        if choice == 'q':
            print("Thank you for visiting RushMore! Come again soon.")
            break
        elif choice in pizza_data:
            pizza_selection_order(choice)
        else:
            print("Invalid input. Please try again.")

if __name__ == "__main__":
    main_system()
