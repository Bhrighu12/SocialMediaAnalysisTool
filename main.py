import streamlit as st
import json
import requests
from typing import Optional

# Langflow Configurations
BASE_API_URL = "https://api.langflow.astra.datastax.com"
LANGFLOW_ID = "1dc1ae5a-c517-4716-b853-2a6fb964d6e0"
FLOW_ID = "d1be4736-446f-41b4-a106-afad17e4e506"
APPLICATION_TOKEN = st.secrets["api_keys"]["langflow_token"]
ENDPOINT = FLOW_ID

# Function to run Langflow
def run_flow(message: str) -> dict:
    api_url = f"{BASE_API_URL}/lf/{LANGFLOW_ID}/api/v1/run/{ENDPOINT}"
    payload = {
        "input_value": message,
        "output_type": "chat",
        "input_type": "chat",
    }
    headers = {"Authorization": "Bearer " + APPLICATION_TOKEN, "Content-Type": "application/json"}
    
    response = requests.post(api_url, json=payload, headers=headers)
    return response.json()

# Streamlit UI
def main():
    st.title("Social Media Analyser Tool")
    st.write("Select a Post Type to Generate Insights")

    # User Input
    post_types = ['Carousel', 'Reels', 'Static image']
    message = st.selectbox("Select Type",post_types)

    # Generate Response Button
    if st.button("Generate AI Insights"):
        if not message:
            st.error("Please enter a message.")
            return

        # Run the flow
        try:
            with st.spinner("Generating response..."):
                response = run_flow(message)
                
                # Check if "outputs" exist in response
                if "outputs" in response:
                    output_text = response["outputs"][0]["outputs"][0]["results"]["message"]["text"]
                    st.write(output_text)
                else:
                    st.error("No 'outputs' found in the response. Please check the API or input.")

        except Exception as e:
            st.error(f"Error: {str(e)}")

if __name__ == "__main__":
    main()
