import sys
from pathlib import Path

# Constants
# Using Path from pathlib because it is cleaner and easier to work with and is the recommended approach
INVENTORY_PATH: Path = Path(Path(__file__).parent / "inventory.txt")


# Class
class Shoe:
    """Blueprint for a shoe product."""

    def __init__(self, country: str, code: str, product: str, cost: int, quantity: int):
        """
        Initialise the Shoe class.

        :param country: Country shoe is located in
        :type country: str
        :param code: SKU code for the shoe
        :type code: str
        :param product: Name of the shoe
        :type product: str
        :param cost: How much the shoe costs
        :type cost: int
        :param quantity: Amount of shoes at location
        :type quantity: int
        """
        self.country = country
        self.code = code
        self.product = product
        self.cost = cost
        self.quantity = quantity

    def get_code(self):
        """
        Gets the shoe SKU code.

        :return: Shoe code
        :rtype: str
        """
        return self.code

    def get_cost(self):
        """
        Gets the cost of the shoe.

        :return: Cost of the shoe
        :rtype: int
        """
        return self.cost

    def get_quantity(self):
        """
        Gets the amount of the shoe at the location.

        :return: Quantity of the shoe
        :rtype: int
        """
        return self.quantity

    def add_quantity(self, quantity_to_add: int):
        self.quantity += quantity_to_add

    def __str__(self):
        """String representation of the shoe class."""
        return (
            f"\tProduct:    {self.product}\n"
            f"\tCode:       {self.code}\n"
            f"\tQuantity:   {self.quantity}\n"
            f"\tCost:       {self.cost}\n"
            f"\tCountry:    {self.country}\n"
        )


# ==========Functions outside the class==============
def read_shoes_data():
    """
    Open the inventory file and read its contents and populate the shoe list variable.

    There is also some logic to prevent a FileNotFoundError and to prevent some errors in
    the inventory file.

    :return: Returns list of shoe objects from the inventory
    :rtype: list[Shoe]
    """
    shoes = []
    check_file_formatting = False

    try:
        with Path.open(INVENTORY_PATH) as inv_file:
            # Using readline() to skip the header and at the same time get the number of columns in the file
            num_of_inv_columns = len(inv_file.readline().split(","))
            for item in inv_file:
                item_list = item.strip("\n").split(",")

                # Skip if not enough columns of data to avoid error,
                # then at the end of function let the user know
                if len(item_list) != num_of_inv_columns:
                    check_file_formatting = True
                    continue

                shoe = Shoe(
                    country=item_list[0],
                    code=item_list[1],
                    product=item_list[2],
                    cost=int(item_list[3]),
                    quantity=int(item_list[4]),
                )
                shoes.append(shoe)
    except FileNotFoundError:
        inventory_not_found_exit()

    if check_file_formatting:
        print("\n!!! Check inventory file for incorrect formatting !!!\n")

    return shoes


def capture_shoes(shoes: list[Shoe]):
    """
    Ask the user for 5 inputs; country, code, product, cost, and quantity to add a Shoe object to the shoe list.

    :param shoes: List of shoe objects
    :type shoes: list[Shoe]
    """
    while True:
        print("\nPlease enter shoe details...")
        country = input("Country: ")
        code = input("Code: SKU")
        code = f"SKU{code}"
        product = input("Product Name: ")

        # This logic will make sure only an int value is entered for cost and quantity
        while True:
            try:
                cost = int(input("Cost: "))
                quantity = int(input("Quantity: "))
                break
            except ValueError:
                print("Enter a number value for cost and quantity. Try again...\n")

        print("You've entered the following details...")
        print(f"""\tCountry:    {country}
\tCode:       {code}
\tProduct:    {product}
\tCost:       {cost}
\tQuantity:   {quantity}
""")
        # This loop is logic to give the user a chance to redo the details if any entered details are incorrect
        while True:
            user_input = input("Are these shoe details correct? (y/n): ")
            if user_input.lower() == "y":
                shoe = Shoe(
                    country=country,
                    code=code,
                    product=product,
                    cost=cost,
                    quantity=quantity,
                )
                shoes.append(shoe)

                # Append shoe to the inventory file
                try:
                    with Path.open(INVENTORY_PATH, "a") as inv_file:
                        inv_file.write(
                            f"{country},{code},{product},{cost},{quantity}\n",
                        )
                except FileNotFoundError:
                    inventory_not_found_exit()

                print(
                    f"\nNew product: {product} with code {code} entered into inventory\n"
                    "Inventory file updated...",
                )
                return
            if user_input.lower() == "n":
                break
            print("Try again...\n")


def view_all(shoes: list[Shoe]):
    """
    Print out all the shoes in the shoe list.

    Relying on the string representation of the Shoe object.

    :param shoes: List of shoe objects
    :type shoes: list[Shoe]
    """
    print("All shoes in the list...")
    for shoe in shoes:
        print(shoe)


def re_stock(shoes: list[Shoe]):
    """
    Prints the shoe with the lowest quantity in the inventory and asks user for quantity input.

    Updates the inventory file.

    :param shoes: List of shoe objects
    :type shoes: list[Shoe]
    """
    lowest_quantity_product = min(
        shoes,
        key=lambda shoe: shoe.get_quantity(),
        default=None,
    )
    if not lowest_quantity_product:
        inventory_not_found_exit()

    print(
        f"The shoe product with the lowest quantity in stock is...\n{lowest_quantity_product}\n",
    )

    while True:
        user_input = input("Would you like to add quantity? (y/n): ")
        if user_input.lower() == "y":
            try:
                quantity_to_add = int(input("How much would you like to add: "))
                lowest_quantity_product.add_quantity(quantity_to_add)
                break
            except ValueError:
                print("Enter a number value for the restock. Try again...\n")
        elif user_input.lower() == "n":
            break
        else:
            print("Try again...\n")

    print("\nNew details...")
    print(lowest_quantity_product)

    # Write the new shoe, including all other shoes into the inventory file
    try:
        with Path.open(INVENTORY_PATH, "w") as inv_file:
            inv_file.write("Country,Code,Product,Cost,Quantity\n")
            for shoe in shoes:
                inv_file.write(
                    f"{shoe.country},{shoe.code},{shoe.product},{shoe.cost},{shoe.quantity}\n",
                )
    except FileNotFoundError:
        inventory_not_found_exit()

    print("Inventory file updated...")


def search_shoe(shoes: list[Shoe]):
    """
    Search for a shoe using the shoe code.

    :param shoes: List of shoe objects
    :type shoes: list[Shoe]
    """
    # Looping for the ability to search again instead of going back to the main menu
    while True:
        while True:
            print(
                "\nEnter shoe code for the shoe details you're after...",
            )
            user_input = input("Code: SKU")
            user_input = f"SKU{user_input}"
            shoe_found = False
            target_shoe = None
            for shoe in shoes:
                if user_input == shoe.get_code():
                    shoe_found = True
                    target_shoe = shoe
            if shoe_found:
                print("Search result:")
                print(target_shoe)
                break

            print("\nShoe code not in the inventory list...")

        while True:
            # Logic to ask if the user wants to search again
            user_input = input("\nWould you like to search again? (y/n): ")
            if user_input.lower() == "y":
                break
            if user_input.lower() == "n":
                return
            print("Try again...\n")


def value_per_item(shoes: list[Shoe]):
    """
    Print all the shoes out with an added detail for the value of each shoe.

    Value = Cost * Quantity

    :param shoes: List of shoe objects
    :type shoes: list[Shoe]
    """
    print("Value per item for all shoes...")
    for shoe in shoes:
        value = shoe.get_cost() * shoe.get_quantity()
        print(shoe, end="")
        print(f"\tValue:      {value:,}", end="\n\n")


def highest_qty(shoes: list[Shoe]):
    """
    View the highest quantity shoe in the inventory.

    :param shoes: List of shoe objects
    :type shoes: list[Shoe]
    """
    print("Shoe with the highest quantity in stock...")
    highest_quantity_product = max(
        shoes,
        key=lambda shoe: shoe.get_quantity(),
        default=None,
    )
    if not highest_quantity_product:
        inventory_not_found_exit()

    print(highest_quantity_product)
    print(f"\n{highest_quantity_product.product} is now for sale!")


def inventory_not_found_exit():
    """Print the error for inventory file not found and then exit the program."""
    print(
        "\n\tInventory file not found, please add it and run this program again"
        "\n\tProgram shutting down...",
    )
    sys.exit()


# Menu Constants
MENU_VIEW_ALL = 1
MENU_SEARCH = 2
MENU_INPUT_NEW_SHOE = 3
MENU_RESTOCK = 4
MENU_VALUE_PER = 5
MENU_HIGHEST_QUANTITY = 6


# ==========Main Menu=============
def main():
    print("Shoe Inventory Program")

    shoes = read_shoes_data()

    while True:
        while True:
            try:
                user_choice = int(
                    input(
                        """\nPlease select from the following menu:
    \t1) View whole inventory
    \t2) Search for a shoe in inventory using SKU code
    \t3) Input new shoe detail into inventory
    \t4) Restock the lowest quantity of a shoe in inventory
    \t5) View value per item for the whole inventory
    \t6) View highest quantity of a shoe in inventory

    \t0) Quit program

    \tEnter selection: """,
                    ),
                )
                break
            except ValueError:
                print("\nEnter a number from the list, please try again...")

        if user_choice == MENU_VIEW_ALL:
            view_all(shoes)
        elif user_choice == MENU_SEARCH:
            search_shoe(shoes)
        elif user_choice == MENU_INPUT_NEW_SHOE:
            capture_shoes(shoes)
        elif user_choice == MENU_RESTOCK:
            re_stock(shoes)
        elif user_choice == MENU_VALUE_PER:
            value_per_item(shoes)
        elif user_choice == MENU_HIGHEST_QUANTITY:
            highest_qty(shoes)
        elif user_choice == 0:
            print("\nThank you for using the Shoe Inventory Program!")
            break
        else:
            print("Please enter a number from the menu list, try again...")


if __name__ == "__main__":
    main()
