import pandas as pd

# Create a DataFrame
df = pd.DataFrame({
  'Name': ['Alice', 'Bob', 'Charlie'],
  'Age': [25, 30, 35],
  'Occupation': ['Engineer', 'Doctor', 'Artist']
})

# Convert DataFrame to dictionary
dict_output = df.to_dict()

print(dict_output)