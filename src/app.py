import streamlit as st
import joblib
import os
import sys

# Add src to path to import local modules
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.preprocess import clean_log

# Page config
st.set_page_config(page_title="Log Anomaly Detection", page_icon="🔍")

# Title and description
st.title("🔍 Log Anomaly Detection")
st.markdown("Enter a log message below to check if it's an **Anomaly** or **Normal**.")

# Load models
@st.cache_resource
def load_models():
    try:
        model_path = os.path.join("models", "isolation_forest_model.pkl")
        vectorizer_path = os.path.join("models", "vectorizer.pkl")
        
        if not os.path.exists(model_path) or not os.path.exists(vectorizer_path):
            st.error("Models not found! Please run the training notebooks first.")
            return None, None

        model = joblib.load(model_path)
        vectorizer = joblib.load(vectorizer_path)
        return model, vectorizer
    except Exception as e:
        st.error(f"Error loading models: {e}")
        return None, None

model, vectorizer = load_models()

if model and vectorizer:
    # User input
    log_input = st.text_area("Log Message:", height=150, placeholder="081109 203615 148 INFO dfs.DataNode$PacketResponder: PacketResponder ...")

    if st.button("Analyze Log"):
        if log_input.strip():
            # Preprocess
            cleaned_log = clean_log(log_input)
            
            # Vectorize
            features = vectorizer.transform([cleaned_log])
            
            # Predict
            prediction = model.predict(features)
            # Isolation Forest: -1 for anomaly, 1 for normal
            
            # Display result
            st.subheader("Result")
            if prediction[0] == -1:
                st.error("🚨 **Anomaly Detected!**")
            else:
                st.success("✅ **Normal Log**")
                
            with st.expander("See processed log"):
                st.code(cleaned_log)
        else:
            st.warning("Please enter a log message.")
