import streamlit as st
import json
import requests
import matplotlib.pyplot as plt
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

# Streamlit UI - Custom Styling
st.markdown(
    """
    <style>
    .stApp {
        background-color: #1e1e1e;
        color: #ffffff;
    }
    .stTitle, .stMarkdown h1, .stMarkdown h2 {
        color: #FFA500;
        text-align: center;
    }
    .stButton>button {
        background-color: #007BFF;
        color: white;
        font-size: 16px;
        border-radius: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

def main():
    st.title("📊 Social Media Analyser Tool")
    st.write("### Select a Post Type to Generate Insights")

    # User Input
    post_types = ['Carousel', 'Reels', 'Static image']
    message = st.selectbox("Select post type",post_types)

    # Generate Response Button
    if st.button("🚀 Generate AI Insights"):
        if not message:
            st.error("⚠️ Please select a post type.")
            return

        # Run the flow
        try:
            with st.spinner("✨ Generating response..."):
                response = run_flow(message)
                
                if "outputs" in response:
                    output_text = response["outputs"][0]["outputs"][0]["results"]["message"]["text"]
                    st.success("✅ Insights Generated Successfully!")
                    st.markdown(f"<p>{output_text}</p>", unsafe_allow_html=True)
                    
                    # Extract engagement data from the text
                    engagement_data = extract_metrics(output_text)
                    
                    # Generate Graph
                    plot_engagement_graph(engagement_data)
                    
                else:
                    st.error("❌ No 'outputs' found in the response. Please check the API or input.")

        except Exception as e:
            st.error(f"❌ Error: {str(e)}")

# Function to extract engagement metrics from response text
def extract_metrics(text):
    data = {}
    try:
        lines = text.split('\n')
        for line in lines:
            if 'Likes' in line:
                data['likes'] = int(line.split(': ')[1])
            elif 'Comments' in line:
                data['comments'] = int(line.split(': ')[1])
            elif 'Shares' in line:
                data['shares'] = int(line.split(': ')[1])
            elif 'Impressions' in line:
                data['impressions'] = int(line.split(': ')[1])
    except Exception as e:
        st.error(f"")
    return data

# Graph Plotting Function
def plot_engagement_graph(data):
    if not data:
        st.warning("No engagement data available to plot.")
        return
    
    metrics = list(data.keys())
    values = list(data.values())

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.bar(metrics, values, color=['#FFA500', '#007BFF', '#00BFFF', '#4BFF00'])
    ax.set_title('Social Media Engagement Metrics')
    ax.set_ylabel('Count')
    ax.set_xlabel('Engagement Type')
    ax.grid(axis='y', linestyle='--', alpha=0.7)

    for i, v in enumerate(values):
        ax.text(i, v + 100, str(v), ha='center', va='bottom', fontsize=12)

    st.pyplot(fig)

if __name__ == "__main__":
    main()
