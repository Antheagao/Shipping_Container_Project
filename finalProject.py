import pandas as pd
import numpy as np

def main():
    # Declare variables
    file_name = ''
    
    # Get the manifest file from the user
    file_name = str(input('Enter the name of the manif file: '))
    
    # Read the manifest file into a dataframe
    manif = pd.read_csv(file_name, sep=',', header=None, 
                     names=['X', 'Y', 'Weight', 'Info'])
    df = pd.read_csv(file_name, sep=',', header=None, 
                     names=['X', 'Y', 'Weight', 'Info'])
    print(df)
    
    # Remove the curly braces from the weight column and convert to int
    df["Weight"] = df['Weight'].str.replace(r'{|}', '', regex=True)
    df = df.astype({'Weight': 'int32'})
    print(df)
    
    # Create the updated manifest file
    file_name = file_name.replace(".txt", "OUTBOUND.txt")
    manif.to_csv(file_name, header=None, index=False)
    
main()