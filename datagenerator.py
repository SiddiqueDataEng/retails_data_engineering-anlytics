import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
import pyodbc
import os
from faker import Faker
import argparse

class RetailDataGenerator:
    def __init__(self):
        self.fake = Faker()
        self.categories = []
        self.subcategories = []
        self.products = []
        self.customers = []
        self.stores = []
        
    def generate_categories(self):
        """Generate categories data"""
        categories_data = [
            (1, 'Electronics'),
            (2, 'Home Appliances'),
            (3, 'Clothing'),
            (4, 'Books & Media'),
            (5, 'Sports & Outdoors'),
            (6, 'Beauty & Personal Care'),
            (7, 'Toys & Games'),
            (8, 'Automotive')
        ]
        self.categories = categories_data
        return pd.DataFrame(categories_data, columns=['CategoryID', 'CategoryName'])
    
    def generate_subcategories(self):
        """Generate subcategories data"""
        subcategories_data = [
            (11, 'Smartphones', 1),
            (12, 'Laptops', 1),
            (13, 'Audio Devices', 1),
            (14, 'Tablets', 1),
            (15, 'Cameras', 1),
            (21, 'Kitchen Appliances', 2),
            (22, 'Home Comfort', 2),
            (23, 'Cleaning Appliances', 2),
            (31, "Men's Clothing", 3),
            (32, "Women's Clothing", 3),
            (33, "Kids' Clothing", 3),
            (41, 'Books', 4),
            (42, 'Movies & TV', 4),
            (43, 'Music', 4),
            (51, 'Exercise Equipment', 5),
            (52, 'Outdoor Gear', 5),
            (61, 'Skincare', 6),
            (62, 'Makeup', 6),
            (71, 'Board Games', 7),
            (72, 'Video Games', 7),
            (81, 'Car Accessories', 8),
            (82, 'Tools & Equipment', 8)
        ]
        self.subcategories = subcategories_data
        return pd.DataFrame(subcategories_data, columns=['SubcategoryID', 'SubcategoryName', 'CategoryID'])
    
    def generate_products(self, num_products=200):
        """Generate products data"""
        products = []
        brands_by_category = {
            1: ['Apple', 'Samsung', 'Sony', 'LG', 'Dell', 'Lenovo', 'HP', 'Bose', 'JBL'],
            2: ['KitchenAid', 'Ninja', 'Instant Pot', 'Dyson', 'Shark', 'Black+Decker', 'Cuisinart'],
            3: ['Nike', 'Adidas', 'Levi\'s', 'H&M', 'Zara', 'Gap', 'Under Armour'],
            4: ['Penguin', 'HarperCollins', 'Random House', 'Scholastic', 'Disney'],
            5: ['Nike', 'Adidas', 'Under Armour', 'The North Face', 'Columbia'],
            6: ['L\'Oreal', 'Maybelline', 'Neutrogena', 'Olay', 'Nivea'],
            7: ['Hasbro', 'Mattel', 'Nintendo', 'Sony', 'Microsoft'],
            8: ['3M', 'Bosch', 'Stanley', 'Black+Decker', 'Michelin']
        }
        
        product_id = 101
        for _ in range(num_products):
            category_id = random.choice([cat[0] for cat in self.categories])
            subcats = [sub for sub in self.subcategories if sub[2] == category_id]
            if not subcats:
                continue
                
            subcategory_id = random.choice(subcats)[0]
            brand = random.choice(brands_by_category.get(category_id, ['Generic']))
            
            # Generate realistic product names based on category and brand
            product_name = self.generate_product_name(category_id, brand)
            
            # Generate realistic prices based on category
            cost_price, selling_price = self.generate_prices(category_id)
            
            products.append((product_id, product_name, category_id, subcategory_id, brand, cost_price, selling_price))
            product_id += 1
        
        self.products = products
        return pd.DataFrame(products, columns=['ProductID', 'ProductName', 'CategoryID', 'SubcategoryID', 'Brand', 'CostPrice', 'SellingPrice'])
    
    def generate_product_name(self, category_id, brand):
        """Generate realistic product names"""
        base_names = {
            1: [f"{brand} Smartphone", f"{brand} Laptop", f"{brand} Headphones", f"{brand} Tablet", f"{brand} Smart Watch"],
            2: [f"{brand} Blender", f"{brand} Coffee Maker", f"{brand} Vacuum Cleaner", f"{brand} Air Purifier"],
            3: [f"{brand} T-Shirt", f"{brand} Jeans", f"{brand} Jacket", f"{brand} Dress", f"{brand} Sneakers"],
            4: [f"Book: {self.fake.catch_phrase()}", f"DVD: {self.fake.catch_phrase()}", f"CD: {self.fake.catch_phrase()}"],
            5: [f"{brand} Running Shoes", f"{brand} Yoga Mat", f"{brand} Tent", f"{brand} Basketball"],
            6: [f"{brand} Moisturizer", f"{brand} Foundation", f"{brand} Shampoo", f"{brand} Perfume"],
            7: [f"{brand} Board Game", f"{brand} Video Game", f"{brand} Action Figure", f"{brand} Puzzle"],
            8: [f"{brand} Car Mat", f"{brand} Tool Set", f"{brand} Tire", f"{brand} Battery"]
        }
        
        return random.choice(base_names.get(category_id, [f"{brand} Product"]))
    
    def generate_prices(self, category_id):
        """Generate realistic prices based on category"""
        price_ranges = {
            1: (50, 2000),  # Electronics - wide range
            2: (20, 500),   # Home Appliances
            3: (10, 200),   # Clothing
            4: (5, 50),     # Books & Media
            5: (15, 300),   # Sports
            6: (5, 100),    # Beauty
            7: (10, 100),   # Toys
            8: (10, 400)    # Automotive
        }
        
        min_price, max_price = price_ranges.get(category_id, (10, 100))
        selling_price = round(random.uniform(min_price, max_price), 2)
        cost_price = round(selling_price * random.uniform(0.5, 0.8), 2)  # Cost is 50-80% of selling price
        
        return cost_price, selling_price
    
    def generate_customers(self, num_customers=1000):
        """Generate customers data"""
        customers = []
        states = ['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 
                 'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD',
                 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ',
                 'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC',
                 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY']
        
        for i in range(1, num_customers + 1):
            first_name = self.fake.first_name()
            last_name = self.fake.last_name()
            email = f"{first_name.lower()}.{last_name.lower()}@{self.fake.free_email_domain()}"
            phone = self.fake.phone_number() if random.random() > 0.05 else ""  # 5% missing phones
            city = self.fake.city()
            state = random.choice(states)
            country = 'USA'
            created_date = self.fake.date_between(start_date='-2y', end_date='today')
            
            customers.append((i, first_name, last_name, email, phone, city, state, country, created_date))
        
        self.customers = customers
        return pd.DataFrame(customers, columns=['CustomerID', 'FirstName', 'LastName', 'Email', 'Phone', 'City', 'State', 'Country', 'CreatedDate'])
    
    def generate_stores(self):
        """Generate stores data"""
        stores_data = [
            (1, 'NYC Flagship', 'New York', 'NY', 'Northeast', 'Flagship'),
            (2, 'LA Downtown', 'Los Angeles', 'CA', 'West', 'Standard'),
            (3, 'Chicago Mall', 'Chicago', 'IL', 'Midwest', 'Standard'),
            (4, 'Houston Plaza', 'Houston', 'TX', 'South', 'Outlet'),
            (5, 'Miami Beach Store', 'Miami', 'FL', 'Southeast', 'Standard'),
            (6, 'Seattle Center', 'Seattle', 'WA', 'Northwest', 'Standard'),
            (7, 'Boston Commons', 'Boston', 'MA', 'Northeast', 'Flagship'),
            (8, 'Phoenix Mall', 'Phoenix', 'AZ', 'Southwest', 'Outlet'),
            (9, 'Denver Downtown', 'Denver', 'CO', 'Mountain', 'Standard'),
            (10, 'Atlanta Plaza', 'Atlanta', 'GA', 'Southeast', 'Standard')
        ]
        self.stores = stores_data
        return pd.DataFrame(stores_data, columns=['StoreID', 'StoreName', 'City', 'State', 'Region', 'StoreType'])
    
    def generate_sales_transactions(self, num_records, start_date, end_date):
        """Generate sales transactions data"""
        transactions = []
        
        start_dt = datetime.strptime(start_date, '%Y-%m-%d')
        end_dt = datetime.strptime(end_date, '%Y-%m-%d')
        date_range = (end_dt - start_dt).days
        
        payment_methods = ['Credit Card', 'Debit Card', 'Digital Wallet', 'Cash', 'Bank Transfer']
        
        for i in range(1, num_records + 1):
            customer_id = random.choice(self.customers)[0]
            product = random.choice(self.products)
            product_id = product[0]
            unit_price = product[6]  # Selling price
            
            quantity = random.randint(1, 5)
            discount = round(random.uniform(0, 0.3) * unit_price, 2) if random.random() > 0.2 else 0  # 20% no discount
            
            # Generate random date within range
            random_days = random.randint(0, date_range)
            transaction_date = start_dt + timedelta(days=random_days)
            
            store_id = random.choice(self.stores)[0]
            payment_method = random.choice(payment_methods)
            
            # Introduce some data quality issues
            if random.random() < 0.02:  # 2% chance of missing customer ID
                customer_id = None
            if random.random() < 0.01:  # 1% chance of negative quantity
                quantity = -1
            if random.random() < 0.03:  # 3% chance of unit price mismatch
                unit_price = round(unit_price * random.uniform(0.5, 1.5), 2)
            
            transactions.append((
                1000 + i, customer_id, product_id, quantity, unit_price, 
                discount, transaction_date.strftime('%Y-%m-%d'), store_id, payment_method
            ))
        
        return pd.DataFrame(transactions, columns=[
            'TransactionID', 'CustomerID', 'ProductID', 'Quantity', 'UnitPrice', 
            'Discount', 'TransactionDate', 'StoreID', 'PaymentMethod'
        ])
    
    def generate_historic_data(self, start_date, end_date, num_transactions):
        """Generate complete historic dataset"""
        print("Generating categories...")
        categories_df = self.generate_categories()
        
        print("Generating subcategories...")
        subcategories_df = self.generate_subcategories()
        
        print("Generating products...")
        products_df = self.generate_products()
        
        print("Generating customers...")
        customers_df = self.generate_customers()
        
        print("Generating stores...")
        stores_df = self.generate_stores()
        
        print(f"Generating {num_transactions} sales transactions...")
        sales_df = self.generate_sales_transactions(num_transactions, start_date, end_date)
        
        return {
            'Categories': categories_df,
            'Subcategories': subcategories_df,
            'Products': products_df,
            'Customers': customers_df,
            'Stores': stores_df,
            'SalesTransactions': sales_df
        }
    
    def save_to_csv(self, data_dict, sourcedata_folder='sourcedata'):
        """Save all dataframes to CSV files"""
        if not os.path.exists(sourcedata_folder):
            os.makedirs(sourcedata_folder)
        
        for name, df in data_dict.items():
            filename = os.path.join(sourcedata_folder, f"{name}.csv")
            df.to_csv(filename, index=False)
            print(f"Saved {filename} with {len(df)} records")
    
    def create_database_connection(self, server=None, database='RetailSales'):
        """Create SQL Server database connection"""
        if server is None:
            server = 'DESKTOP-A3PO7VB\\SQLEXPRESS'
        
        connection_string = f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'
        try:
            conn = pyodbc.connect(connection_string)
            return conn
        except Exception as e:
            print(f"Error connecting to database: {e}")
            return None
    
    def create_tables(self, conn):
        """Create database tables"""
        cursor = conn.cursor()
        
        # Drop tables if they exist
        tables = ['SalesTransactions', 'Products', 'Customers', 'Stores', 'Subcategories', 'Categories']
        for table in tables:
            try:
                cursor.execute(f"DROP TABLE IF EXISTS {table}")
            except:
                pass
        
        # Create tables
        cursor.execute("""
            CREATE TABLE Categories (
                CategoryID INT PRIMARY KEY,
                CategoryName VARCHAR(100)
            )
        """)
        
        cursor.execute("""
            CREATE TABLE Subcategories (
                SubcategoryID INT PRIMARY KEY,
                SubcategoryName VARCHAR(100),
                CategoryID INT FOREIGN KEY REFERENCES Categories(CategoryID)
            )
        """)
        
        cursor.execute("""
            CREATE TABLE Stores (
                StoreID INT PRIMARY KEY,
                StoreName VARCHAR(100),
                City VARCHAR(50),
                State VARCHAR(10),
                Region VARCHAR(50),
                StoreType VARCHAR(50)
            )
        """)
        
        cursor.execute("""
            CREATE TABLE Customers (
                CustomerID INT PRIMARY KEY,
                FirstName VARCHAR(50),
                LastName VARCHAR(50),
                Email VARCHAR(100),
                Phone VARCHAR(20),
                City VARCHAR(50),
                State VARCHAR(10),
                Country VARCHAR(50),
                CreatedDate DATE
            )
        """)
        
        cursor.execute("""
            CREATE TABLE Products (
                ProductID INT PRIMARY KEY,
                ProductName VARCHAR(200),
                CategoryID INT FOREIGN KEY REFERENCES Categories(CategoryID),
                SubcategoryID INT FOREIGN KEY REFERENCES Subcategories(SubcategoryID),
                Brand VARCHAR(50),
                CostPrice DECIMAL(10,2),
                SellingPrice DECIMAL(10,2)
            )
        """)
        
        cursor.execute("""
            CREATE TABLE SalesTransactions (
                TransactionID INT PRIMARY KEY,
                CustomerID INT FOREIGN KEY REFERENCES Customers(CustomerID),
                ProductID INT FOREIGN KEY REFERENCES Products(ProductID),
                Quantity INT,
                UnitPrice DECIMAL(10,2),
                Discount DECIMAL(10,2),
                TransactionDate DATE,
                StoreID INT FOREIGN KEY REFERENCES Stores(StoreID),
                PaymentMethod VARCHAR(50)
            )
        """)
        
        conn.commit()
        print("Database tables created successfully")
    
    def insert_data(self, conn, data_dict):
        """Insert data into database tables"""
        cursor = conn.cursor()
        
        for table_name, df in data_dict.items():
            print(f"Inserting data into {table_name}...")
            
            for _, row in df.iterrows():
                try:
                    placeholders = ', '.join(['?' for _ in range(len(row))])
                    columns = ', '.join(df.columns)
                    cursor.execute(f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})", *row)
                except Exception as e:
                    print(f"Error inserting row into {table_name}: {e}")
                    continue
            
            conn.commit()
            print(f"Inserted {len(df)} records into {table_name}")

def main():
    generator = RetailDataGenerator()
    
    print("Retail Sales Data Generator")
    print("1. Historic Data (CSV files)")
    print("2. Live Data (SQL Server)")
    
    choice = input("Choose option (1 or 2): ").strip()
    
    if choice == '1':
        start_date = input("Enter start date (YYYY-MM-DD): ").strip()
        end_date = input("Enter end date (YYYY-MM-DD): ").strip()
        num_records = int(input("Enter number of sales transactions to generate: "))
        
        data = generator.generate_historic_data(start_date, end_date, num_records)
        generator.save_to_csv(data)
        
        print(f"\nGenerated {num_records} sales transactions with related data")
        for name, df in data.items():
            print(f"  {name}: {len(df)} records")
    
    elif choice == '2':
        server = input("Enter SQL Server (press Enter for default): ").strip()
        if not server:
            server = None
        
        database = input("Enter database name (press Enter for 'RetailSales'): ").strip()
        if not database:
            database = 'RetailSales'
        
        start_date = input("Enter start date (YYYY-MM-DD): ").strip()
        end_date = input("Enter end date (YYYY-MM-DD): ").strip()
        num_records = int(input("Enter number of sales transactions to generate: "))
        
        conn = generator.create_database_connection(server, database)
        if conn:
            data = generator.generate_historic_data(start_date, end_date, num_records)
            generator.create_tables(conn)
            generator.insert_data(conn, data)
            conn.close()
            print("Data generation and insertion completed successfully!")
        else:
            print("Failed to connect to database")
    
    else:
        print("Invalid choice")

if __name__ == "__main__":
    # Install required packages: pip install pandas numpy pyodbc faker
    main()