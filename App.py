import pandas as pd
from pandasai import SmartDataframe
from pandasai.llm import OpenAI
from PIL import Image
import matplotlib.pyplot as plt
import streamlit as st
import streamlit.components.v1 as components
import pygwalker as pyg

# Configure Matplotlib to use the TkAgg backend
st.set_option('deprecation.showPyplotGlobalUse', False)  # Disable warning
plt.switch_backend('TkAgg')  # Set the backend

st.set_page_config(layout="wide")

llm = OpenAI(api_token="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")

# Add a logo or header
#logo = Image.open("your_logo.png")  # Replace with your logo file
#st.image(logo, use_column_width=True)



# Main app
def main():
    st.sidebar.title("MagicAnalyser")
    uploaded_file = st.sidebar.file_uploader("Upload a CSV or Excel file", type=["csv", "xlsx"], key="file_uploader")
    
    if uploaded_file:
        st.session_state.uploaded_data = pd.read_csv(uploaded_file)
    else:
        st.warning("Please upload a CSV or Excel file.")

    st.sidebar.title("Menu")
    page = st.sidebar.radio("Go to", ("QA Analysis", "Visual Analysis", "User Manual"))

    if page == "QA Analysis":
        analysis_page()
    elif page == "Visual Analysis":
        visual_analysis_page()
    elif page == "User Manual":
        usage_page()

def visual_analysis_page():
    if hasattr(st.session_state, 'uploaded_data'):
        pyg_html = pyg.to_html(st.session_state.uploaded_data)
        # Embed the HTML into the Streamlit app
        components.html(pyg_html, height=1000, scrolling=True)
    else:
        image = Image.open("upload.jpg")
        # Display the image
        st.image("upload.jpg", caption="Upload a file on the menu panel", use_column_width=True)

def analysis_page():
    if hasattr(st.session_state, 'uploaded_data'):
        st.write("Uploaded file content:")
        df = SmartDataframe(st.session_state.uploaded_data, config={"llm": llm})
        st.write("Column names:")
        column_names = list(st.session_state.uploaded_data.columns)
        st.write(column_names)

        question = st.text_input("Enter your analysis question:", key="analysis_question")

        # Use a button to trigger analysis
        if st.button('Submit Analysis'):
            if question:
                with st.spinner('Generating response...'):
                    answer = df.chat(question)
                    st.write(answer)
            else:
                st.warning('Please ask a question')
    else:
        st.image("upload.jpg", caption="Upload a file on the menu panel", use_column_width=True)

def usage_page():
    st.header("How to Use MagicAnalyser:")
    st.subheader("Step 1: Upload Data")
    st.write("📂 Start on the 'Home' page.")
    st.write("📎 Upload your data file (CSV or Excel) using the 'Upload a CSV or Excel file' section on the left panel.")
    st.write("🔄 Once the file is uploaded, it will be stored in the application.")

    st.subheader("Step 2: Perform Analysis")
    st.write("📊 Go to the 'Analysis' page using the left panel.")
    st.write("🔍 View the column names of the uploaded data.")
    st.write("❓ Enter an analysis question in the text input box under 'Enter your analysis question:'.")

    st.subheader("Step 3: Submit Analysis")
    st.write("🚀 Click the 'Submit' button to perform the analysis.")
    st.write("📝 The application will provide insights or visualizations based on your question.")

    st.subheader("Step 4: Explore Data")
    st.write("🔍 Explore the uploaded data and the results of your analysis.")
    st.write("ℹ️ View the uploaded data's content, number of rows, and file size.")

    st.subheader("Additional Information")
    st.write("1. You can navigate between different pages using the left panel.")
    st.write("2. The 'Home' page displays an image, introductory content, and sample charts.")
    st.write("3. The 'Usage' page provides this user manual.")

    st.write("Enjoy using MagicAnalyser to analyze your data and discover valuable insights!")

if __name__ == "__main__":
    main()
