import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.feature_extraction.text import CountVectorizer
from scipy.sparse import csr_matrix, hstack
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import pickle

# Load and preprocess data
data = pd.read_excel(r"C:\Users\R.SANTOSH\Downloads\water.xlsx")

# Define the expected column names
rename_dict = {
    'Column1': 'CropCode',
    'Column2': 'ProductDescription',
    'Column3': 'GreenWaterFootprint',
    'Column4': 'BlueWaterFootprint',
    'Column5': 'GreyWaterFootprint',
    'Column6': 'TotalWaterFootprint'
}

# Rename the columns
data = data.rename(columns=rename_dict)

# Ensure the DataFrame has exactly the columns we expect
expected_columns = ['CropCode', 'ProductDescription', 'GreenWaterFootprint', 'BlueWaterFootprint', 'GreyWaterFootprint', 'TotalWaterFootprint']
data = data[expected_columns]

# Handle non-numeric entries in numeric columns
numeric_features = ['GreenWaterFootprint', 'BlueWaterFootprint', 'GreyWaterFootprint']
for feature in numeric_features:
    # Convert non-numeric values to NaN
    data[feature] = pd.to_numeric(data[feature], errors='coerce')

# Handle missing values in 'ProductDescription'
data['ProductDescription'] = data['ProductDescription'].fillna('Unknown')

# Handle missing values in numeric columns by imputing
imputer = SimpleImputer(strategy='mean')  # Use mean imputation
data[numeric_features] = imputer.fit_transform(data[numeric_features])

# Convert target column to numeric and drop non-numeric entries
data['TotalWaterFootprint'] = pd.to_numeric(data['TotalWaterFootprint'], errors='coerce')
data = data.dropna(subset=['TotalWaterFootprint'])

# Vectorization
vectorizer = CountVectorizer()
X_product_description = vectorizer.fit_transform(data['ProductDescription'])

# Numeric features
X_numeric = csr_matrix(data[numeric_features].values)

# Combine features
X = hstack([X_product_description, X_numeric])

# Target
y = data['TotalWaterFootprint']

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = LinearRegression()
model.fit(X_train, y_train)

# Save vectorizer and model
with open("vectorizer.pkl", "wb") as f:
    pickle.dump(vectorizer, f)

with open("model.pkl", "wb") as f:
    pickle.dump(model, f)

print("Model and vectorizer saved successfully.")
