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

    @property
    def value(self):
        return self.cost * self.quantity

    def add_quantity(self, quantity_to_add: int):
        self.quantity += quantity_to_add

    def __str__(self):
        """String representation of the shoe class as a table row."""
        return f"| {self.country:<20} | {self.code:<9} | {self.product:<25} | {self.cost:>6} | {self.quantity:>4} | {self.value:>9,} |"


class Inventory:
    """Blueprint for the shoe inventory."""

    def __init__(self, file_path: Path):
        """
        Initialise the Inventory class.

        :param file_path: Path object of the inventory file path
        :type file_path: Path
        """
        self.file_path = file_path
        self.shoes: list[Shoe] = []

    def load_data(self):
        has_formatting_errors = False

        try:
            with Path.open(self.file_path) as inv_file:
                # Using readline() to skip the header and at the same time get the number of columns in the file
                num_of_inv_columns = len(inv_file.readline().split(","))
                for item in inv_file:
                    item_list = item.strip("\n").split(",")

                    # Skip if not enough columns of data to avoid error,
                    # then at the end of function let the user know
                    if len(item_list) != num_of_inv_columns:
                        has_formatting_errors = True
                        continue

                    shoe = Shoe(
                        country=item_list[0],
                        code=item_list[1],
                        product=item_list[2],
                        cost=int(item_list[3]),
                        quantity=int(item_list[4]),
                    )
                    self.shoes.append(shoe)
        except FileNotFoundError:
            self.file_not_found_exit()

        if has_formatting_errors:
            print("\n!!! Check inventory file for incorrect formatting !!!\n")

    def save_data(self):
        """Save current shoes list to a file."""
        with Path.open(self.file_path, "w") as inv_file:
            inv_file.write("Country,Code,Product,Cost,Quantity\n")
            for shoe in self.shoes:
                inv_file.write(
                    f"{shoe.country},{shoe.code},{shoe.product},{shoe.cost},{shoe.quantity}\n",
                )

    def view_all(self):
        """
        Print out all the shoes in the shoe list.

        Relying on the string representation of the Shoe object.
        """
        header = f"| {'Country':<20} | {'Code':<9} | {'Product Name':<25} | {'Cost':<6} | {'Qty':<4} | {'Value':<9} |"
        table_width = len(header)
        print("_" * table_width)
        print(header)
        print("-" * table_width)
        for shoe in self.shoes:
            print(shoe)
        print("-" * table_width)

    def capture_shoes(self):
        """Ask the user for 5 inputs; country, code, product, cost, and quantity to add a Shoe object to the shoe list."""
        while True:
            print("\nPlease enter shoe details...")
            country = input("\tCountry: ")
            code = input("\tCode: SKU")
            code = f"SKU{code}"
            product = input("\tProduct Name: ")

            # This logic will make sure only an int value is entered for cost and quantity
            while True:
                try:
                    cost = int(input("\tCost: "))
                    quantity = int(input("\tQuantity: "))
                    break
                except ValueError:
                    print("Enter a number value for cost and quantity. Try again...\n")

            print("\nYou've entered the following details...")
            print(
                f"\tCountry:    {country}\n"
                f"\tCode:       {code}\n"
                f"\tProduct:    {product}\n"
                f"\tCost:       {cost}\n"
                f"\tQuantity:   {quantity}\n",
            )
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
                    self.shoes.append(shoe)

                    # Append shoe to the inventory file
                    self.save_data()

                    print(
                        f"\nNew product: {product} with code {code} entered into inventory\n"
                        "Inventory file updated...",
                    )
                    return
                if user_input.lower() == "n":
                    break
                print("Try again...\n")

    def re_stock(self):
        """
        Prints the shoe with the lowest quantity in the inventory and asks user for quantity input.

        Updates the inventory file.
        """
        lowest_quantity_product = min(
            self.shoes,
            key=lambda shoe: shoe.quantity,
            default=None,
        )
        if not lowest_quantity_product:
            self.file_not_found_exit()

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

        # Write the new shoe to the inventory file
        self.save_data()

        print("Inventory file updated...")

    def search_shoe(self):
        """Search for a shoe using the shoe code."""
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
                for shoe in self.shoes:
                    if user_input == shoe.code:
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

    def highest_qty(self):
        """View the highest quantity shoe in the inventory."""
        print("Shoe with the highest quantity in stock...")
        highest_quantity_product = max(
            self.shoes,
            key=lambda shoe: shoe.quantity,
            default=None,
        )
        if not highest_quantity_product:
            self.file_not_found_exit()

        print(highest_quantity_product)
        print(f"\n{highest_quantity_product.product} is now for sale!")

    def file_not_found_exit(self):
        """Print the error for path file not found and then exit the program."""
        print(
            f"\n\t{self.file_path.name} not found, please fix and run this program again"
            "\n\tProgram shutting down...",
        )
        sys.exit()


# ==========Functions outside the class==============


# Menu Constants
MENU_VIEW_ALL = 1
MENU_SEARCH = 2
MENU_INPUT_NEW_SHOE = 3
MENU_RESTOCK = 4
MENU_HIGHEST_QUANTITY = 5


# ==========Main Menu=============
def main():
    print("Shoe Inventory Program")

    inventory = Inventory(INVENTORY_PATH)
    inventory.load_data()

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
    \t5) View highest quantity of a shoe in inventory

    \t0) Quit program

    \tEnter selection: """,
                    ),
                )
                break
            except ValueError:
                print("\nEnter a number from the list, please try again...")

        if user_choice == MENU_VIEW_ALL:
            inventory.view_all()
        elif user_choice == MENU_SEARCH:
            inventory.search_shoe()
        elif user_choice == MENU_INPUT_NEW_SHOE:
            inventory.capture_shoes()
        elif user_choice == MENU_RESTOCK:
            inventory.re_stock()
        elif user_choice == MENU_HIGHEST_QUANTITY:
            inventory.highest_qty()
        elif user_choice == 0:
            print("\nThank you for using the Shoe Inventory Program!")
            break
        else:
            print("Please enter a number from the menu list, try again...")


if __name__ == "__main__":
    main()
