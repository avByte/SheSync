#Imports
import streamlit as st
import pandas as pd
import os
import hashlib
from SheSync_Home import homepage

# Path to save account information
DATA_FILE = 'accounts_with_passwords.csv'

# Function to hash passwords
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Function to load existing accounts from the CSV file
def load_accounts():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    else:
        return pd.DataFrame(columns=["Name", "Password", "Description", "Interests", "Languages", "Tags"])

# Function to save account information (with hashed password)
def save_account(name, password, description, interests, languages, tags):
    hashed_password = hash_password(password)
    new_account = {
        "Name": name,
        "Password": hashed_password,
        "Bio": description,
        "Interests": ', '.join(interests),
        "Languages": ', '.join(languages),
        "Tags": ', '.join(tags)
    }
    accounts = load_accounts()
    
    # If the account already exists (same name), update it
    if name in accounts['Name'].values:
        accounts.loc[accounts['Name'] == name, ['Password', 'Bio', 'Interests', 'Languages', 'Tags']] = hashed_password, description, ', '.join(interests), ', '.join(languages), ', '.join(tags)
    else:
        # Use pd.concat to add new account
        accounts = pd.concat([accounts, pd.DataFrame([new_account])], ignore_index=True)
    
    accounts.to_csv(DATA_FILE, index=False)

# Function to check password during sign in
def check_password(name, password):
    accounts = load_accounts()
    if name in accounts['Name'].values:
        stored_password_hash = accounts[accounts['Name'] == name]['Password'].values[0]
        return stored_password_hash == hash_password(password)
    return False

# Function to show the account creation form
def account_creation_page():
    st.title("Create an Account")
    name = st.text_input("Name")
    password = st.text_input("Password", type="password")
    description = st.text_area("Bio")

    st.write("Select your interests:")
    interests_list = ["Web Development", "Data Science", "DevOps", "Mobile Developent", "Cybersecurity", "Game Development", "Hackathons", "Internships", "Conferences", "Workshops", "Competitions", "Full-Time Opportunities", "Networking"]
    interests_selected = []
    
    for interest in interests_list:
        if st.checkbox(interest):
            interests_selected.append(interest)

    st.write("Select your languages:")
    languages_list = ["Bash/Shell", "C/C++","C#", "Go" "HTML/CSS", "JavaScript", "Java", "PHP", "Python", "PowerShell", "Rust", "SQL", "TypeScript"]
    languages_selected = []
    
    for language in languages_list:
        if st.checkbox(language):
            languages_selected.append(language)

    tags_list = ["Tech Enthusiast", "Gamer", "Traveler", "Fitness Lover", "Foodie", "Entrepreneur", "Music Lover", "Artistic", "Movies/Shows", "Podcasts"]
    selected_tags = st.multiselect("Select your tags", options=tags_list)

    if st.button("Create Account"):
        if name and password and description:
            save_account(name, password, description, interests_selected, languages_selected, selected_tags)
            st.session_state.current_user = name  # Store current user in session state
            st.session_state.page = "homepage"  # Change to homepage after creating account
        else:
            st.error("Please fill in all fields.")

# Function to show the sign-in form
def sign_in_page():
    st.title("Sign In")
    name = st.text_input("Name")
    password = st.text_input("Password", type="password")

    if st.button("Sign In"):
        if name and password:
            if check_password(name, password):
                st.session_state.current_user = name  # Store current user in session state
                st.session_state.page = "homepage"  # Change to homepage after signing in
            else:
                st.error("Incorrect name or password.")
        else:
            st.error("Please fill in both fields.")

# Function to display the home page after sign-in or account creation
def home():
    homepage()

# Function for the account creation or sign-in decision page
def sign_in_or_create_page():
    st.title("Welcome! Please choose an option:")
    
    if st.button("Sign In"):
        st.session_state.page = "sign_in"  # Switch to sign in page

    if st.button("Create a New Account"):
        st.session_state.page = "create_account"  # Switch to account creation page

# Main app flow
def main():
    if "page" not in st.session_state:
        st.session_state.page = "choose"

    if "current_user" not in st.session_state:
        if st.session_state.page == "choose":
            sign_in_or_create_page()
        elif st.session_state.page == "sign_in":
            sign_in_page()
        elif st.session_state.page == "create_account":
            account_creation_page()
    else:
        homepage()  # Redirect to homepage if already logged in

# Run the app
if __name__ == "__main__":
    main()
