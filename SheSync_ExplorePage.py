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

# Page to display full account details
def display_account_details(account):
    st.title(f"Account: {account['Name']}")
    st.subheader("Description")
    st.write(account['Description'])
    st.subheader("Traits")
    st.write(account['Traits'])
    st.subheader("Written Response")
    st.write(account['Written Response'])

# Function to display a scrollable list of account previews
def display_account_previews():
    st.title("User Accounts")

    accounts = load_accounts()

    # If no accounts exist, show a message
    if accounts.empty:
        st.write("No accounts available.")
        return

    st.write("Click on any account to view more details.")

    # Scrollable container for previews
    with st.container():
        for index, account in accounts.iterrows():
            # Display each account's preview (Name, Description, Traits)
            st.subheader(account["Name"])
            st.write(f"Description: {account['Description'][:100]}...")  # Show only the first 100 characters
            st.write(f"Traits: {account['Traits']}")

            # Create a button for each account
            if st.button(f"View {account['Name']}", key=index):
                st.session_state.selected_account = index  # Save selected account index to session state
                st.experimental_rerun()  # Rerun the app to display the selected account page

# Main function to handle navigation
def main():
    # Load the accounts
    accounts = load_accounts()

    # Check if an account is selected
    if "selected_account" in st.session_state:
        selected_index = st.session_state.selected_account
        account = accounts.iloc[selected_index]
        display_account_details(account)
        if st.button("Back to Account List"):
            del st.session_state.selected_account  # Reset selection
            st.experimental_rerun()  # Go back to the account list
    else:
        display_account_previews()

# Run the app
if __name__ == "__main__":
    main()