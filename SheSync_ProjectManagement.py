import streamlit as st
import pandas as pd
import os

PROJECTS_FILE = 'projects.csv'

# Function to load existing projects from the CSV file
def load_projects():
    if os.path.exists(PROJECTS_FILE):
        return pd.read_csv(PROJECTS_FILE)
    else:
        return pd.DataFrame(columns=["Project Name", "Description", "Image", "Tags"])

# Function to save a new project
def save_project(project_name, description, image_path, tags):
    new_project = {
        "Project Name": project_name,
        "Description": description,
        "Image": image_path,
        "Tags": ', '.join(tags)  # Storing tags as a comma-separated string
    }
    projects = load_projects()
    projects = pd.concat([projects, pd.DataFrame([new_project])], ignore_index=True)
    projects.to_csv(PROJECTS_FILE, index=False)

# Function to display the form for creating a new project
def project_creation_form():
    st.title("Create a New Project")

    # Input fields for project creation
    project_name = st.text_input("Project Title")
    description = st.text_area("Project Description")

    # Optional image upload
    image = st.file_uploader("Upload an image (optional)", type=["jpg", "jpeg", "png"])

    # Optional tags
    st.write("Enter tags (optional):")
    tags_input = st.text_input("Separate tags with commas")
    tags = [tag.strip() for tag in tags_input.split(",") if tag.strip()]

    # Button to submit the new project
    if st.button("Create Project"):
        if project_name and description:
            # Save image if uploaded
            image_path = None
            if image:
                image_path = os.path.join("images", image.name)
                with open(image_path, "wb") as f:
                    f.write(image.getbuffer())

            save_project(project_name, description, image_path, tags)
            st.success("Project created successfully!")
            st.session_state.show_form = False  # Hide form after submission
        else:
            st.error("Please fill out at least the project title and description.")

# Function to display project previews
def display_project_previews():
    projects = load_projects()

    if not projects.empty:
        for index, row in projects.iterrows():
            st.subheader(row["Project Name"])
            st.write(row["Description"])
            
            # Display image if it exists
            if pd.notna(row["Image"]):
                st.image(row["Image"], use_column_width=True)

            # Display tags if they exist
            if row["Tags"]:
                st.write(f"**Tags:** {row['Tags']}")
            st.write("---")
    else:
        st.write("No projects available yet. Create one!")

# Main function to manage the project page
def project_page():
    st.title("Projects")

    # Button to show the project creation form
    if st.button("Create New Project"):
        st.session_state.show_form = True

    # Show project creation form if the button was clicked
    if st.session_state.get("show_form", False):
        project_creation_form()

    # Scrollable project previews
    with st.container():
        st.subheader("Projects")
        st.write("Scroll down to view other user's projects!")
        display_project_previews()

# Initialize session state and display the project page
if __name__ == "__main__":
    if "show_form" not in st.session_state:
        st.session_state.show_form = False
    project_page()
