import streamlit as st
import hashlib

# Define model data (replace with actual source)
models = [
    {"name": "Chair", "type": "Furniture", "format": "FBX", "description": "A comfortable chair for relaxing."},
    {"name": "Car", "type": "Vehicle", "format": "OBJ", "description": "A fast and sleek car."},
    # ... more models
]

# Define model criteria options (using conditional checks for missing keys)
criteria_options = {
    "Type": list(set(model.get("type", "Unknown") for model in models)),
    "Format": list(set(model.get("format", "Unknown") for model in models)),
    # Add more criteria options here (e.g., software compatibility)
}

# Load user credentials from a text file (create one if it doesn't exist)
user_credentials_file = "user_credentials.txt"
try:
    with open(user_credentials_file, "r") as file:
        user_credentials = eval(file.read())  # Insecure, but simple for the example
except FileNotFoundError:
    user_credentials = {}

# List to store uploaded models during the session
uploaded_models = []

# List to store user activities log
user_activities_log = []

# Initialize SessionState class
class SessionState:
    def __init__(self, **kwargs):
        for key, val in kwargs.items():
            setattr(self, key, val)

# Create a session_state object
session_state = SessionState(username=None)

# Main content area title
st.title("3D Model Library")

# Sidebar for navigation
menu = st.sidebar.selectbox("Menu", ["Home", "Filter Models", "Upload 3D Model", "Sign-Up/Login", "Admin Panel"])

if menu == "Filter Models":
    st.title("Filter Models")
    selected_criteria = st.multiselect("Filter by:", criteria_options.keys())

    # Display and apply filters based on selections
    for criterion, options in criteria_options.items():
        if criterion in selected_criteria:
            selected_value = st.selectbox(criterion, options)
            models = [model for model in models if model.get(criterion, "Unknown") == selected_value]

elif menu == "Upload 3D Model":
    st.title("Upload 3D Model")
    uploaded_model = st.file_uploader("Upload 3D Model (FBX, OBJ, STL, etc.)", type=["fbx", "obj", "stl"])
    model_description = st.text_area("Enter Model Description", key="model_description")
    
    if uploaded_model:
        # Create a dictionary to store model information
        new_model = {
            "name": uploaded_model.name,
            "format": uploaded_model.type,
            "description": model_description,
            # Add more fields as needed
        }
        uploaded_models.append(new_model)
        st.success("3D Model uploaded successfully!")

elif menu == "Sign-Up/Login":
    st.title("Sign-Up/Login")
    username_input = st.text_input("Enter your Username", key="username_input")
    password_input = st.text_input("Enter your Password", type="password", key="password_input")
    login_button = st.button("Login")

    if login_button:
        # Check if the entered username exists and the hashed password matches
        if username_input in user_credentials and \
                user_credentials[username_input] == hashlib.sha256(password_input.encode()).hexdigest():
            session_state.username = username_input  # Set the session_state variable
            st.success(f"Login successful! Welcome, {username_input}.")
            # Log the user activity
            user_activities_log.append(f"{username_input} logged in.")
        else:
            st.error("Invalid username or password. Please try again.")

    st.write("---")
    st.subheader("Sign-Up")
    new_username = st.text_input("Enter a unique Username", key="new_username")
    new_password = st.text_input("Enter a Password", type="password", key="new_password")
    sign_up_button = st.button("Sign Up")

    if sign_up_button:
        if new_username in user_credentials:
            st.error("Username already exists. Please choose a different username.")
        else:
            # Hash the password before storing
            hashed_password = hashlib.sha256(new_password.encode()).hexdigest()
            user_credentials[new_username] = hashed_password

            # Save the updated user credentials to the file
            with open(user_credentials_file, "w") as file:
                file.write(str(user_credentials))

            st.success("Sign-up successful!")

elif menu == "Admin Panel":
    st.title("Admin Panel")

    st.subheader("Manage Users")

    # Display a list of signed-up users
    st.write("Users who have signed up:")
    for user in user_credentials.keys():
        st.write(f"- {user}")

    # Allow admin to delete a user
    user_to_delete = st.text_input("Enter username to delete:", key="user_to_delete")
    delete_user_button = st.button("Delete User")

    if delete_user_button:
        st.write(f"Entered username: {user_to_delete}")
        st.write("Admins can delete any user.")

        if user_to_delete in user_credentials:
            # Remove the user from the stored credentials
            del user_credentials[user_to_delete]

            # Save the updated user credentials to the file
            with open(user_credentials_file, "w") as file:
                file.write(str(user_credentials))

            st.success(f"User '{user_to_delete}' deleted successfully.")
        else:
            st.error("User not found. Please enter a valid username.")

    st.subheader("View User Activities")

    # Display a simple log of user activities (replace this with a more sophisticated logging system)
    st.write("User Activities Log:")
    # Display the activities log (add more details based on your actual log)
    for log_entry in user_activities_log:
        st.write(f"- {log_entry}")

    # Add more admin functionalities here

# ... (rest of the code remains unchanged)

# Display filtered model information (without images or download links)
st.title("Available Models")
for model in models + uploaded_models:
    st.write("*Name:*", model["name"])
    st.write("*Format:*", model["format"])
    st.write("*Description:*", model.get("description", "No description available"))

# Display signed-up users
st.write("---")
st.subheader("Signed-Up Users")
if user_credentials:
    st.write("Users who have signed up:")
    for user in user_credentials.keys():
        st.write(f"- {user}")
else:
    st.write("No users have signed up yet.")
