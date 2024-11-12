class User:
    def __init__(self, username, password, role):
        self.username = username
        self.password = password
        self.role = role
        
    def authenticate(self, password):
        return self.password == password
    
    def has_permission(self, action):
        if self.role == "admin":
            return True
        elif self.role == "user" and action == "view":
            return True
        return False
        
        
class Product:
    def __init__(self, product_id, name, category, price, stock_quantity):
        self.product_id = product_id
        self.name = name
        self.category = category
        self.price = price
        self.stock_quantity = stock_quantity
        
    def update_stock(self, quantity):
        self.stock_quantity += quantity
        if self.stock_quantity < 0:
            self.stock_quantity = 0
            
    def display_info(self):
        return f"ID: {self.product_id}, Name: {self.name}, Category: {self.category}, " \
               f"Price: ${self.price}, Stock: {self.stock_quantity}"


class Inventory:
    def __init__(self):
        self.products = {}
        self.users = {
            "admin": User("admin", "admin123", "admin"),
            "user": User("user", "user123", "user")
        }
    
    def add_product(self, product, current_user):
        if current_user.has_permission("add"):
            self.products[product.product_id] = product
            print(f"Product {product.name} added to inventory.")
        else:
            print("Permission Denied: You don't have the right to add products.")
        
    def update_product(self, product_id, name=None, category=None, price=None, stock_quantity=None, current_user=None):
        if current_user.has_permission("update"):
            product = self.products.get(product_id)
            if product:
                if name is not None: product.name = name
                if category is not None: product.category = category
                if price is not None: product.price = price
                if stock_quantity is not None: product.update_stock(stock_quantity)
                print("Product updated successfully!")
            else:
                print("Product not found.")
        else:
            print("Permission Denied: You don't have the right to update products.")
            
    def remove_product(self, product_id, current_user):
        if current_user.has_permission("delete"):
            if product_id in self.products:
                del self.products[product_id]
                print("Product removed successfully!")
            else:
                print("Product not found.")
        else:
            print("Permission Denied: You don't have the right to remove products.")

    def search_product(self, product_id):
        return self.products.get(product_id)
    
    def view_inventory(self, current_user):
        if current_user.has_permission("view"):
            for product in self.products.values():
                print(product.display_info())
        else:
            print("Permission Denied: You don't have the right to view inventory.")
            
def login(ims):
    username = input("Enter username: ")
    password = input("Enter password: ")
    user = ims.users.get(username)
    if user and user.authenticate(password):
        print(f"Welcome, {user.username}!")
        return user
    else:
        print("Invalid login credentials.")
        return None
    
def main():
    ims = Inventory()  # Corrected class name here
    current_user = login(ims)
    if not current_user:
        return  # Exit if login fails

    while True:
        print("\n--- Inventory Management System ---")
        print("1. View Inventory")
        print("2. Add Product")
        print("3. Update Product")
        print("4. Delete Product")
        print("5. Exit")
        
        choice = input("Choose an option: ")

        if choice == "1":
            ims.view_inventory(current_user)

        elif choice == "2":
            try:
                product_id = input("Enter Product ID: ")
                name = input("Enter Product Name: ")
                category = input("Enter Product Category: ")
                price = float(input("Enter Product Price: "))
                stock_quantity = int(input("Enter Stock Quantity: "))
                new_product = Product(product_id, name, category, price, stock_quantity)
                ims.add_product(new_product, current_user)
            except ValueError:
                print("Invalid input! Please enter valid data.")

        elif choice == "3":
            try:
                product_id = input("Enter Product ID to Update: ")
                name = input("Enter new name (or press Enter to skip): ") or None
                category = input("Enter new category (or press Enter to skip): ") or None
                price_input = input("Enter new price (or press Enter to skip): ")
                stock_quantity_input = input("Enter new stock quantity (or press Enter to skip): ")
                
                price = float(price_input) if price_input else None
                stock_quantity = int(stock_quantity_input) if stock_quantity_input else None
                
                ims.update_product(product_id, name=name, category=category,
                                   price=price, stock_quantity=stock_quantity,
                                   current_user=current_user)
            except ValueError:
                print("Invalid input!")

        elif choice == "4":
            product_id = input("Enter Product ID to Delete: ")
            ims.remove_product(product_id, current_user)

        elif choice == "5":
            print("Exiting Inventory Management System.")
            break
            
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()