#Imports
import streamlit as st
import pandas as pd
import os
import hashlib
from SheSync_Discovery import discovery

# Paths to save account and project information
DATA_FILE = 'accounts_with_passwords.csv'
PROJECTS_FILE = 'projects.csv'

# Function to hash passwords
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Function to load existing accounts from the CSV file
def load_accounts():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    else:
        return pd.DataFrame(columns=["Name", "Password", "Description", "Traits", "Written Response"])

# Function to save account information (with hashed password)
def save_account(name, password, description, traits, written_response):
    hashed_password = hash_password(password)
    new_account = {
        "Name": name,
        "Password": hashed_password,
        "Description": description,
        "Traits": ', '.join(traits),
        "Written Response": written_response
    }
    accounts = load_accounts()
    
    if name in accounts['Name'].values:
        accounts.loc[accounts['Name'] == name, ['Password', 'Description', 'Traits', 'Written Response']] = hashed_password, description, ', '.join(traits), written_response
    else:
        accounts = pd.concat([accounts, pd.DataFrame([new_account])], ignore_index=True)
    
    accounts.to_csv(DATA_FILE, index=False)

# Function to check password during sign in
def check_password(name, password):
    accounts = load_accounts()
    if name in accounts['Name'].values:
        stored_password_hash = accounts[accounts['Name'] == name]['Password'].values[0]
        return stored_password_hash == hash_password(password)
    return False

# Function to display the home page after sign-in or account creation
def homepage():
    st.title(f"Welcome, {st.session_state.current_user}")

    # Tabs for navigation
    tab1, tab2, tab3, tab4 = st.tabs(["Discovery", "Explore", "Account Settings", "Help"])

    with tab1:
        discovery()

    with tab2:
        explore_projects_page()

    with tab3:
        account_settings()

    with tab4:
        help_page()

# Function to edit account settings
def account_settings():
    st.title("Account Settings")
    accounts = load_accounts()
    
    if st.session_state.current_user in accounts['Name'].values:
        user_data = accounts[accounts['Name'] == st.session_state.current_user].iloc[0]
        description = st.text_area("Description", user_data["Description"])
        traits = user_data["Traits"].split(", ") if user_data["Traits"] else []
        
        st.write("Select your traits:")
        traits_list = ["Adventurous", "Creative", "Empathetic", "Logical", "Curious"]
        traits_selected = []
        
        for trait in traits_list:
            if trait in traits:
                if st.checkbox(trait, value=True):
                    traits_selected.append(trait)
            else:
                if st.checkbox(trait):
                    traits_selected.append(trait)
        
        if st.button("Save Changes"):
            save_account(st.session_state.current_user, user_data["Password"], description, traits_selected, user_data["Written Response"])
            st.success("Account updated successfully!")
    else:
        st.write("User not found.")

# Function to display help information
def help_page():
    st.title("Help")
    st.write("For any inquiries, please contact us at support@example.com.")

# Run the app
if __name__ == "__main__":
    main()
