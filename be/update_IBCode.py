# -*- coding: utf-8 -*-
"""
Created on Fri Jun 30 14:27:29 2023

@author: yanminghao
"""

import json

# Step 1: Read the existing JSON config file
def read_config(file_path):
    with open(file_path, 'r') as file:
        config = json.load(file)
    return config

# Step 2: Update the dictionary with user input
def update_config(config):
    ib_code = input("Enter IB code: ")
    isin = input("Enter ISIN code: ")
    config[ib_code] = isin
    return config

# Step 3: Write the updated dictionary back to the JSON file
def write_config(config, file_path):
    with open(file_path, 'w') as file:
        json.dump(config, file, indent=4)
    print("Configuration file updated successfully!")

# Main program
def main_read():
    file_path = 'config.json'  # Replace with the actual path to your configuration file
    config = read_config(file_path)
    return config
    
def main_update():
    file_path = 'config.json'  # Replace with the actual path to your configuration file
    config = read_config(file_path)    
    updated_config = update_config(config)
    write_config(updated_config, file_path)

if __name__ == '__main__':
    main_read()
    main_update()