import streamlit as st
import pandas as pd
import os
import hashlib

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

# Function to show the account creation form
def account_creation_page():
    st.title("Create an Account")
    name = st.text_input("Name")
    password = st.text_input("Password", type="password")
    description = st.text_area("Description")
    written_response = st.text_area("Written Response")

    st.write("Select your traits:")
    traits_list = ["Adventurous", "Creative", "Empathetic", "Logical", "Curious"]
    traits_selected = []
    
    for trait in traits_list:
        if st.checkbox(trait):
            traits_selected.append(trait)

    if st.button("Create Account"):
        if name and password and description and written_response:
            save_account(name, password, description, traits_selected, written_response)
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
def homepage():
    st.title(f"Welcome, {st.session_state.current_user}")

    # Tabs for navigation
    tab1, tab2, tab3, tab4 = st.tabs(["Discovery", "Explore", "Account Settings", "Help"])

    with tab1:
        discovery_page()

    with tab2:
        explore_projects_page()

    with tab3:
        account_settings()

    with tab4:
        help_page()

# Function for the account creation or sign-in decision page
def sign_in_or_create_page():
    st.title("Welcome! Please choose an option:")
    
    if st.button("Sign In"):
        st.session_state.page = "sign_in"  # Switch to sign in page

    if st.button("Create a New Account"):
        st.session_state.page = "create_account"  # Switch to account creation page

# Function to display the discovery page (user previews)
def discovery_page():
    st.subheader("Discovery Page")
    accounts = load_accounts()
    
    if not accounts.empty:
        for index, row in accounts.iterrows():
            st.write(f"**Name:** {row['Name']}")
            st.write(f"**Description:** {row['Description']}")
            st.write(f"**Traits:** {row['Traits']}")
            st.write(f"**Written Response:** {row['Written Response']}")
            st.write("---")
    else:
        st.write("No accounts available yet. Create one!")

# Function to display the explore projects page (project previews)
def explore_projects_page():
    st.title("Explore Projects")
    
    projects = load_projects()
    
    if not projects.empty:
        for index, row in projects.iterrows():
            st.subheader(row["Project Name"])
            st.write(row["Description"])
            
            if row["Image"]:
                st.image(row["Image"], use_column_width=True)
            
            if row["Link"]:
                st.markdown(f"[View Project]({row['Link']})", unsafe_allow_html=True)
            st.write("---")
    else:
        st.write("No projects available yet. Create one!")

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

# Function to load existing projects from the CSV file
def load_projects():
    if os.path.exists(PROJECTS_FILE):
        return pd.read_csv(PROJECTS_FILE)
    else:
        return pd.DataFrame(columns=["Project Name", "Description", "Image", "Link"])

# Function to save project information
def save_project(project_name, description, image, link):
    new_project = {
        "Project Name": project_name,
        "Description": description,
        "Image": image if image else "",
        "Link": link if link else ""
    }
    
    projects = load_projects()
    projects = pd.concat([projects, pd.DataFrame([new_project])], ignore_index=True)
    projects.to_csv(PROJECTS_FILE, index=False)

# Function to show the project creation form
def project_creation_page():
    st.title("Create a New Project")
    
    project_name = st.text_input("Project Name")
    description = st.text_area("Project Description")
    
    st.write("Optional Fields:")
    image = st.file_uploader("Upload an Image", type=["png", "jpg", "jpeg"])
    link = st.text_input("Link to Project (e.g., GitHub, Website)")

    if st.button("Create Project"):
        if project_name and description:
            if image:
                image_path = os.path.join("images", image.name)
                with open(image_path, "wb") as f:
                    f.write(image.getbuffer())
            else:
                image_path = None

            save_project(project_name, description, image_path, link)
            st.success(f"Project '{project_name}' created successfully!")
        else:
            st.error("Please provide at least the project name and description.")

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
