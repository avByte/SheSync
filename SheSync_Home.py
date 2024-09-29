#Imports
import streamlit as st
import pandas as pd
import os
import hashlib
from SheSync_Discovery import discovery
from SheSync_ProjectManagement import project_page

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
        return pd.DataFrame(columns=["Name", "Password", "Bio", "Interests", "Languages", "Tags"])

# Function to save account information (with hashed password)
def save_account(name, password, description, interests, languages, tags):
    hashed_password = hash_password(password)
    new_account = {
        "Name": name,
        "Password": hashed_password,
        "Bio": description,
        "Interests": ', '.join(interests),
        "Languages": ', '.join(languages),
        "Tags": tags
    }
    accounts = load_accounts()
    
    if name in accounts['Name'].values:
        accounts.loc[accounts['Name'] == name, ['Password', 'Bio', 'Interests', 'Languages', 'Tags']] = hashed_password, description, ', '.join(interests), ', '.join(languages), tags
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

# Function to display the home page
def homepage():
    st.title(f"Hey hi, {st.session_state.current_user}!")

    # Tabs for navigation
    tab1, tab2, tab3, tab4 = st.tabs(["Discovery", "Explore", "Account Settings", "About Us"])

    with tab1:
        discovery()

    with tab2:
        project_page()

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
        description = st.text_area("Bio", user_data["Bio"])
        interests = user_data["Interests"].split(", ") if user_data["Interests"] else []
        languages = user_data["Languages"].split(", ") if user_data["Languages"] else []
        tags = user_data["Tags"].split(", ") if user_data["Tags"] else []

        st.write("Select your Interests:")
        interests_list = ["Web Development", "Data Science", "DevOps", "Mobile Developent", "Cybersecurity", "Game Development", "Hackathons", "Internships", "Conferences", "Workshops", "Competitions", "Full-Time Opportunities", "Networking"]
        interests_selected = []
        
        for interest in interests_list:
            if interest in interests:
                if st.checkbox(interest, value=True):
                    interests_selected.append(interest)
            else:
                if st.checkbox(interest):
                    interests_selected.append(interest)
        
        st.write("Select your languages:")
        languages_list = ["Bash/Shell", "C/C++","C#", "Go", "HTML/CSS", "JavaScript", "Java", "PHP", "Python", "PowerShell", "Rust", "SQL", "TypeScript"]
        languages_selected = []

        for language in languages_list:
            if language in languages:
                if st.checkbox(language, value=True):
                    languages_selected.append(language)
            else:
                if st.checkbox(language):
                    languages_selected.append(language)

        st.write("Select your Tags:")
        tags_list = ["Tech Enthusiast", "Gamer", "Traveler", "Fitness Lover", "Foodie", "Entrepreneur", "Music Lover", "Artistic", "Movies/Shows", "Podcasts"]
        tags_selected = st.multiselect("Choose your tags:", options=tags_list, default=tags)


        if st.button("Save Changes"):
            save_account(st.session_state.current_user, user_data["Password"], description, interests_selected, languages_selected, tags_selected)
            st.success("Account updated successfully!")
    else:
        st.write("User not found.")

# Function to display help information
def help_page():
    st.title("About Us")
    st.subheader("Our Mission")
    st.write("With women constantly being overlooked and neglected in tech, we bring you SheSync to connect women with women, to make working in tech feel a little less isolating.")
    st.write("")
    st.write("For any inquiries or technical support, please contact the LowKey team at #####@####.ca")

# Run the app
if __name__ == "__main__":
    homepage()