import streamlit as st
import pandas as pd
import os

# Path to save project information
PROJECTS_FILE = 'projects.csv'

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
    projects = projects.append(new_project, ignore_index=True)
    projects.to_csv(PROJECTS_FILE, index=False)

# Function to display the project creation form
def project_creation_page():
    st.title("Create a New Project")
    
    project_name = st.text_input("Project Name")
    description = st.text_area("Project Description")
    
    st.write("Optional Fields:")
    image = st.file_uploader("Upload an Image", type=["png", "jpg", "jpeg"])
    link = st.text_input("Link to Project (e.g., GitHub, Website)")

    if st.button("Create Project"):
        if project_name and description:
            # Save the image file if uploaded
            if image:
                image_path = os.path.join("images", image.name)
                with open(image_path, "wb") as f:
                    f.write(image.getbuffer())
            else:
                image_path = None

            # Save the project details
            save_project(project_name, description, image_path, link)
            st.success(f"Project '{project_name}' created successfully!")
        else:
            st.error("Please provide at least the project name and description.")

# Function to display existing projects
def explore_projects():
    st.title("Explore Projects")
    
    projects = load_projects()
    
    if not projects.empty:
        for index, row in projects.iterrows():
            st.subheader(row["Project Name"])
            st.write(row["Description"])
            
            # Display image if available
            if row["Image"]:
                st.image(row["Image"], use_column_width=True)
            
            # Display link if available
            if row["Link"]:
                st.markdown(f"[View Project]({row['Link']})", unsafe_allow_html=True)
    else:
        st.write("No projects available yet. Create one!")

# Main app flow
def main():
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox("Go to", ["Create Project", "Explore Projects"])

    if page == "Create Project":
        project_creation_page()
    elif page == "Explore Projects":
        explore_projects()

# Run the app
if __name__ == "__main__":
    # Ensure 'images' folder exists for storing uploaded images
    if not os.path.exists("images"):
        os.makedirs("images")
    
    main()
