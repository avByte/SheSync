import streamlit as st
import pandas as pd
import os

# Path to save account information
DATA_FILE = 'accounts.csv'

# Function to load existing accounts from the CSV file
def load_accounts():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    else:
        return pd.DataFrame(columns=["Name", "Description", "Traits", "Written Response"])

# Function to save account information
def save_account(name, description, traits, written_response):
    new_account = {
        "Name": name,
        "Description": description,
        "Traits": ', '.join(traits),
        "Written Response": written_response
    }
    accounts = load_accounts()
    accounts = accounts.append(new_account, ignore_index=True)
    accounts.to_csv(DATA_FILE, index=False)

# Streamlit UI
st.title("Account Creation Page")

# Name input
name = st.text_input("Name")

# Description input
description = st.text_area("Description")

# Traits input (checkboxes)
st.write("Select your traits:")
traits = []
if st.checkbox("Adventurous"):
    traits.append("Adventurous")
if st.checkbox("Creative"):
    traits.append("Creative")
if st.checkbox("Empathetic"):
    traits.append("Empathetic")
if st.checkbox("Logical"):
    traits.append("Logical")
if st.checkbox("Curious"):
    traits.append("Curious")

# Written response input
written_response = st.text_area("Written Response")

# Submit button
if st.button("Create Account"):
    if name and description and written_response:
        # Save account data
        save_account(name, description, traits, written_response)
        st.success(f"Account created successfully for {name}!")
    else:
        st.error("Please fill in all required fields.")

# Show saved accounts
st.subheader("Saved Accounts")
accounts_df = load_accounts()
st.dataframe(accounts_df)
