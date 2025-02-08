import streamlit as st
import pandas as pd
from PIL import Image
import warnings
warnings.filterwarnings("ignore")
# Load CSV file
csv_path = "/mnt/commonfolder/genAIllm/prasad/Pulkit/Open_domain_data.csv"  # Update with the actual path

df = pd.read_csv(csv_path)

# Streamlit UI
st.set_page_config(layout="wide")

st.title("Visual Question Answering App")

# Session state to track current index
if "current_index" not in st.session_state:
    st.session_state.current_index = 0

# Get current question
index = st.session_state.current_index
if index < len(df):
    row = df.iloc[index]
    question = row["Question"]
    answer = row["Answer"]
    image_paths = list(eval(row["Image_list"]))  # Convert string representation of set to list
    image_paths=image_paths[0:5]
    st.write(question)
    
    cols = st.columns(3)  # Display images in two columns
    
    for i, path in enumerate(image_paths):
        try:
            img = Image.open(path)
            with cols[i % 3]:  # Arrange images in two columns
                st.image(img, caption=f"Image {i+1}", use_container_width=True)
        except Exception as e:
            st.write(f"Error loading Image {i+1}: {e}")
    
    # Answer input
    user_answer = st.text_input("Your Answer:")
    
    # Submit button
    # Submit button
    if st.button("Submit Answer"):
        if user_answer.strip():
            st.success(f"Your answer has been recorded: {user_answer}")
            
            # Save the user's response in the DataFrame
            df.at[index, "User_Answer"] = user_answer  # Add a new column for responses if not exists
            
            # Save back to the CSV file
            df.to_csv(csv_path, index=False)
            
            # Move to the next question
            st.session_state.current_index += 1
            st.experimental_rerun()  # Refresh the app to show the next entry
        else:
            st.warning("Please enter an answer before submitting.")

else:
    st.write("### All questions have been answered!")