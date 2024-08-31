import pickle
import pandas as pd
from scipy.sparse import csr_matrix, hstack
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LinearRegression
import re

# Load the vectorizer and model
with open("vectorizer.pkl", "rb") as f:
    vectorizer = pickle.load(f)

with open("model.pkl", "rb") as f:
    model = pickle.load(f)

# Load the cleaned dataset for reference
data = pd.read_excel(r"C:\Users\R.SANTOSH\Downloads\water.xlsx")

# Rename the columns to match what your code expects
rename_dict = {
    'Column1': 'CropCode',
    'Column2': 'ProductDescription',
    'Column3': 'GreenWaterFootprint',
    'Column4': 'BlueWaterFootprint',
    'Column5': 'GreyWaterFootprint',
    'Column6': 'TotalWaterFootprint'
}
data = data.rename(columns=rename_dict)

# Confirm the renaming worked
print("Columns after renaming:", data.columns)

def parse_input(user_input):
    # Use regex to extract product description and quantity
    match = re.search(r'(?P<quantity>\d+)\s*(?P<product_description>[a-zA-Z\s]+)', user_input)
    
    if match:
        quantity = float(match.group('quantity'))
        product_description = match.group('product_description').strip()
        return product_description, quantity
    else:
        # If regex fails, try to split assuming "product description quantity" format
        try:
            product_description, quantity = user_input.rsplit(' ', 1)
            quantity = float(quantity)
            return product_description, quantity
        except ValueError:
            return None, None

def predict_water_footprint(product_description, quantity):
    # Find the matching product in the dataset
    product_data = data[data['ProductDescription'].str.lower() == product_description.lower()]
    
    if not product_data.empty:
        # Get the numeric features directly from the dataset
        green_water = product_data['GreenWaterFootprint'].values[0]
        blue_water = product_data['BlueWaterFootprint'].values[0]
        grey_water = product_data['GreyWaterFootprint'].values[0]
    else:
        # Handle missing or unknown products
        green_water = 0
        blue_water = 0
        grey_water = 0

    # Create a dummy dataframe for numeric features
    dummy_df = pd.DataFrame({
        'GreenWaterFootprint': [green_water], 
        'BlueWaterFootprint': [blue_water], 
        'GreyWaterFootprint': [grey_water]
    })
    
    # Ensure the numeric features are in the correct sparse matrix format
    numeric_features = csr_matrix(dummy_df.values)
    
    # Vectorize the input description
    product_vector = vectorizer.transform([product_description])
    
    # Ensure product_vector is a sparse matrix
    if not isinstance(product_vector, csr_matrix):
        product_vector = csr_matrix(product_vector)
    
    # Combine the product vector with numeric features
    X_input = hstack([product_vector, numeric_features])
    
    # Predict the water footprint using the model
    predicted_footprint = model.predict(X_input)[0]
    
    # Calculate the total footprint based on quantity
    total_footprint = predicted_footprint * quantity
    
    return total_footprint

# Main chatbot loop
print("Welcome to the Water Footprint Chatbot!")
print("You can ask about the water footprint of any product.")
print("For example, you can say 'Give me the water footprint for 5 units of rice' or 'rice 5'.")

while True:
    user_input = input("Enter a product description and quantity or type 'exit' to quit: ").strip()
    
    if user_input.lower() == 'exit':
        break

    product_description, quantity = parse_input(user_input)
    
    if product_description and quantity:
        try:
            # Predict the water footprint
            footprint = predict_water_footprint(product_description, quantity)
            print(f"The estimated water footprint for {quantity} units of {product_description} is {footprint:.2f} cubic meters.")
        except Exception as e:
            print(f"An error occurred: {e}")
    else:
        print("Sorry, I couldn't understand your input. Please provide the product and quantity in a clear format.")
