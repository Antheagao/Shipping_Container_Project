import pandas as pd
import numpy as np

def main():
    # Declare variables
    file_name = ''
    
    # Get the manifest file from the user
    '''file_name = str(input('Enter the name of the manifest file: '))'''
    
    # Read the manifeset file into a dataframe
    '''df = pd.read_csv(file_name, sep=',', header=None, 
                     names=['Coord', 'Weight', 'Container'])'''
    manifest = pd.read_csv('ShipCase1.txt', sep=' ', header=None, 
                     names=['XY', 'Weight', 'Info'])
    df = pd.read_csv('ShipCase1.txt', sep=',', header=None, 
                     names=['X', 'Y', 'Weight', 'Info'])
    print(df)
    
    # Remove the curly braces from the weight column
    df["Weight"] = df['Weight'].str.replace(r'{|}', '', regex=True)
    print(df)
    
    # Create the updated manifest file
    manifest.to_csv('ShipCase1Updated.txt', header=None, index=False)
    
main()