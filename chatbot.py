import pandas as pd
from fuzzywuzzy import process
import re

# Load dataset
df = pd.read_excel(r"C:\Users\R.SANTOSH\Documents\ai_bot\water.xlsx")

# Rename columns based on the dataset inspection
df.columns = ['Cropcode', 'Product', 'Green', 'Blue', 'Grey', 'Total']

# Drop rows with NaN in the 'Product' column
df.dropna(subset=['Product'], inplace=True)

# Convert columns to numeric, replacing non-numeric values with NaN
df['Green'] = pd.to_numeric(df['Green'], errors='coerce').fillna(0).astype(float)
df['Blue'] = pd.to_numeric(df['Blue'], errors='coerce').fillna(0).astype(float)
df['Grey'] = pd.to_numeric(df['Grey'], errors='coerce').fillna(0).astype(float)
df['Total'] = pd.to_numeric(df['Total'], errors='coerce').fillna(0).astype(float)

# Create a dictionary for water footprints
water_footprints = df.set_index('Product').to_dict(orient='index')

def get_product_info(product_name):
    # Extract and normalize product names from the dataset
    products = water_footprints.keys()
    
    # Find the best match using fuzzy matching
    best_match, score = process.extractOne(product_name, products)
    
    if score < 80:  # Adjust threshold as needed
        return None, "Product not found. Please try another one."
    
    return best_match, None

def calculate_water_footprint(product, quantity):
    product_info = water_footprints.get(product)
    
    if not product_info:
        return "Product not found. Please try another one."
    
    green = product_info['Green']
    blue = product_info['Blue']
    grey = product_info['Grey']
    total = product_info['Total']
    
    green_total = green * quantity
    blue_total = blue * quantity
    grey_total = grey * quantity
    total_total = total * quantity
    
    return (f"For {quantity} kg of {product}:\n"
            f"- Green Water Footprint: {green_total:.2f} liters\n"
            f"- Blue Water Footprint: {blue_total:.2f} liters\n"
            f"- Grey Water Footprint: {grey_total:.2f} liters\n"
            f"- Total Water Footprint: {total_total:.2f} liters")

print("Welcome to the Water Footprint Chatbot!")
print("You can ask about the water footprint of any product.")
print("For example, you can say 'Give me the water footprint for 5 kg of rice' or 'rice 5'.")

while True:
    user_input = input("Enter a product description and quantity or type 'exit' to quit: ").strip().lower()
    
    if user_input == 'exit':
        break
    
    # Extract product and quantity from the user input
    match = re.match(r'(.*?)(\d+)\s*kg$', user_input)
    
    if match:
        product_name = match.group(1).strip()
        try:
            quantity = float(match.group(2))
        except ValueError:
            print("Invalid quantity. Please enter a numeric value followed by 'kg'.")
            continue
        
        # Get the best matching product
        product_name, error = get_product_info(product_name)
        
        if error:
            print(error)
        else:
            result = calculate_water_footprint(product_name, quantity)
            print(result)
    else:
        print("Invalid input format. Please enter the product description followed by 'kg'.")

print("Thank you for using the Water Footprint Chatbot!")
