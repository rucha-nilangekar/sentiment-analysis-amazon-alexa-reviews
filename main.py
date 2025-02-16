'''import streamlit as st
import pandas as pd
import requests
from io import BytesIO

# flask --app api.py run --port=5000
prediction_endpoint = "http://127.0.0.1:5000/predict"

st.title("Text Sentiment Predictor")

uploaded_file = st.file_uploader(
    "Choose a CSV file for bulk prediction - Upload the file and click on Predict",
    type="csv",
)

# Text input for sentiment prediction
user_input = st.text_input("Enter text and click on Predict", "")

# Prediction on single sentence
if st.button("Predict"):
    if uploaded_file is not None:
        file = {"file": uploaded_file}
        response = requests.post(prediction_endpoint, files=file)
        response_bytes = BytesIO(response.content)
        response_df = pd.read_csv(response_bytes)

        st.download_button(
            label="Download Predictions",
            data=response_bytes,
            file_name="Predictions.csv",
            key="result_download_button",
        )

    else:
        response = requests.post(prediction_endpoint, json ={"text": user_input})  # here replacing "data" with "json"
        response = response.json()
        st.write(f"Predicted sentiment: {response['prediction']}") '''



import streamlit as st
import pandas as pd
import requests
from io import BytesIO
import base64

# Define Flask API endpoint
prediction_endpoint = "http://127.0.0.1:5000/predict"

# App title
st.title("Text Sentiment Predictor")

# File uploader for bulk prediction
uploaded_file = st.file_uploader(
    "Choose a CSV file for bulk prediction", type="csv"
)

# Text input for single prediction
user_input = st.text_input("Or enter text for single prediction", "")

# Predict button logic
if st.button("Predict"):
    if not uploaded_file and not user_input.strip():
        st.warning("Please upload a file or enter text before clicking Predict.")
    else:
        try:
            if uploaded_file is not None:  # Bulk prediction logic
                with st.spinner("Processing bulk predictions..."):
                    file = {"file": uploaded_file}
                    response = requests.post(prediction_endpoint, files=file)

                if response.status_code == 200:
                    # Read predictions from response and display download button
                    response_bytes = BytesIO(response.content)
                    response_df = pd.read_csv(response_bytes)
                    st.download_button(
                        label="Download Predictions",
                        data=response_bytes,
                        file_name="Predictions.csv",
                        key="result_download_button",
                    )

                    # Display graph if included in response headers
                    if 'X-Graph-Exists' in response.headers and response.headers['X-Graph-Exists'] == 'true':
                        graph_data = base64.b64decode(response.headers['X-Graph-Data'])
                        st.image(graph_data, caption="Sentiment Distribution")

                else:
                    st.error(f"Error: {response.status_code} - {response.text}")

            elif user_input.strip():  # Single sentence prediction logic
                with st.spinner("Processing single prediction..."):
                    response = requests.post(prediction_endpoint, json={"text": user_input})

                if response.status_code == 200:
                    result = response.json()
                    st.write(f"Predicted sentiment: {result['prediction']}")
                else:
                    st.error(f"Error: {response.status_code} - {response.text}")

        except requests.RequestException as e:
            st.error(f"Error connecting to server: {str(e)}")
