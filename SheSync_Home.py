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
    
    # If the account already exists (same name), update it
    if name in accounts['Name'].values:
        accounts.loc[accounts['Name'] == name, ['Description', 'Traits', 'Written Response']] = description, ', '.join(traits), written_response
    else:
        accounts = accounts.append(new_account, ignore_index=True)
    
    accounts.to_csv(DATA_FILE, index=False)

# Function to show explore page (similar to account viewer)
def explore_page():
    st.title("Explore User Accounts")
    
    accounts = load_accounts()

    # If no accounts exist, show a message
    if accounts.empty:
        st.write("No accounts available.")
        return

    st.write("Click on any account to view more details.")

    # Scrollable container for previews
    with st.container():
        for index, account in accounts.iterrows():
            st.subheader(account["Name"])
            st.write(f"Description: {account['Description'][:100]}...")  # Show only first 100 chars
            st.write(f"Traits: {account['Traits']}")

            if st.button(f"View {account['Name']}", key=index):
                st.session_state.selected_account = index
                st.experimental_rerun()

# Function to display and edit account settings
def account_settings():
    st.title("Account Settings")

    # Load account info for current user
    if "current_user" in st.session_state:
        accounts = load_accounts()
        user_account = accounts[accounts['Name'] == st.session_state.current_user].iloc[0]
        
        # Name is fixed, can't be edited
        st.subheader(f"Name: {user_account['Name']}")
        
        # Editable fields
        description = st.text_area("Description", user_account['Description'])
        written_response = st.text_area("Written Response", user_account['Written Response'])
        
        st.write("Select your traits:")
        traits_list = ["Adventurous", "Creative", "Empathetic", "Logical", "Curious"]
        traits = user_account['Traits'].split(", ")
        traits_selected = []
        
        for trait in traits_list:
            if st.checkbox(trait, value=(trait in traits)):
                traits_selected.append(trait)

        # Save changes
        if st.button("Save Changes"):
            save_account(st.session_state.current_user, description, traits_selected, written_response)
            st.success("Account details updated!")

    else:
        st.warning("Please sign in to access account settings.")

# Function to display help information
def help_page():
    st.title("Help & Contact Information")
    st.write("""
        **Need assistance?**  
        Contact us at:  
        - Email: support@example.com  
        - Phone: +1-800-123-4567  
        
        **Business Hours**:  
        Monday to Friday: 9:00 AM - 5:00 PM (EST)
    """)

# Account creation/sign-in page
def account_creation_or_sign_in():
    st.title("Sign In or Create an Account")
    name = st.text_input("Name")
    description = st.text_area("Description")
    written_response = st.text_area("Written Response")

    st.write("Select your traits:")
    traits_list = ["Adventurous", "Creative", "Empathetic", "Logical", "Curious"]
    traits_selected = []
    
    for trait in traits_list:
        if st.checkbox(trait):
            traits_selected.append(trait)

    if st.button("Create/Sign In"):
        if name and description and written_response:
            save_account(name, description, traits_selected, written_response)
            st.session_state.current_user = name  # Store current user in session state
            st.success(f"Welcome, {name}!")
            st.experimental_rerun()  # Redirect to homepage
        else:
            st.error("Please fill in all fields.")

# Main homepage with tabs
def homepage():
    st.title(f"Welcome, {st.session_state.current_user}")

    # Tabs for navigation
    tab1, tab2, tab3 = st.tabs(["Explore", "Account Settings", "Help"])

    with tab1:
        explore_page()

    with tab2:
        account_settings()

    with tab3:
        help_page()

# Main app flow
def main():
    if "current_user" not in st.session_state:
        account_creation_or_sign_in()  # User must sign in or create an account
    else:
        homepage()  # Display homepage after sign-in/account creation

if __name__ == "__main__":
    main()
