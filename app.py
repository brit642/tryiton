import streamlit as st
from google.cloud import aiplatform
import PIL.Image
import io
import base64

# --- Configuration ---

# App layout
st.set_page_config(
    page_title="Virtual Try-On AI",
    page_icon="👕",
    layout="wide"
)

# --- Authentication and Initialization ---

# NOTE: This application requires authentication with Google Cloud.
# For local development, you can authenticate by running the following command in your terminal:
# gcloud auth application-default login
#
# Your Project ID is set below.
PROJECT_ID = "fonsi-gcp-demos"
LOCATION = "us-central1"

# Initialize Vertex AI SDK
try:
    aiplatform.init(project=PROJECT_ID, location=LOCATION)
except Exception as e:
    st.error(f"""
        **Error initializing Google Cloud AI Platform.** Please make sure you have:
        1. Set your `PROJECT_ID` in the script.
        2. Authenticated with Google Cloud by running `gcloud auth application-default login` in your terminal.
        
        *Details: {e}*
    """)
    st.stop()

# --- Core Functions ---

@st.cache_resource
def get_prediction_client():
    """
    Initializes and returns the PredictionServiceClient.
    The client is cached to avoid re-initialization on every run.
    """
    api_regional_endpoint = f"{LOCATION}-aiplatform.googleapis.com"
    client_options = {"api_endpoint": api_regional_endpoint}
    # Initialize client that will be used to send requests.
    client = aiplatform.gapic.PredictionServiceClient(client_options=client_options)
    return client

def generate_virtual_try_on_image(person_image_bytes, garment_image_bytes):
    """
    Generates an image of a person wearing a garment using the Virtual Try-On model.

    Args:
        person_image_bytes (bytes): The image of the person in bytes.
        garment_image_bytes (bytes): The image of the garment in bytes.

    Returns:
        PIL.Image.Image or None: The generated image, or None if an error occurs.
    """
    # The specific Virtual Try-On model endpoint
    model_endpoint = (
        f"projects/{PROJECT_ID}/locations/{LOCATION}/publishers/google/models/virtual-try-on-exp-05-31"
    )

    # Encode images to base64, which is required by this model endpoint
    person_image_b64 = base64.b64encode(person_image_bytes).decode("utf-8")
    garment_image_b64 = base64.b64encode(garment_image_bytes).decode("utf-8")

    # --- CORRECTED PAYLOAD STRUCTURE ---
    # This structure now exactly matches the format specified in the Colab notebook.
    instance = {
        "personImage": {"image": {"bytesBase64Encoded": person_image_b64}},
        "productImages": [{"image": {"bytesBase64Encoded": garment_image_b64}}],
    }
    instances = [instance]
    
    # No specific parameters are needed for this model
    parameters = {}

    try:
        prediction_client = get_prediction_client()
        
        # Send the prediction request
        response = prediction_client.predict(
            endpoint=model_endpoint,
            instances=instances,
            parameters=parameters,
        )
        
        # Check if the response has predictions
        if response.predictions:
            # --- CORRECTED RESPONSE KEY ---
            # Using 'bytesBase64Encoded' as shown in the Colab notebook's helper function.
            generated_image_b64 = response.predictions[0]['bytesBase64Encoded']
            generated_image_bytes = base64.b64decode(generated_image_b64)
            
            # Convert the image bytes into a displayable PIL Image
            result_image = PIL.Image.open(io.BytesIO(generated_image_bytes))
            return result_image
        else:
            st.error("The model did not return a valid prediction. Please try again with different images.")
            return None

    except Exception as e:
        st.error(f"An error occurred while calling the prediction model: {e}")
        return None

# --- Streamlit UI ---

st.title("👕 AI Virtual Try-On")
st.markdown("Upload a photo of a person and a photo of a garment to see the magic happen!")

st.divider()

col1, col2 = st.columns(2)

with col1:
    st.subheader("1. Upload Person's Image")
    person_image_file = st.file_uploader(
        "Select a clear, front-facing photo of a person.",
        type=['png', 'jpg', 'jpeg'],
        key="person_uploader"
    )
    if person_image_file:
        st.image(person_image_file, caption="Person's Image", use_column_width=True)

with col2:
    st.subheader("2. Upload Garment's Image")
    garment_image_file = st.file_uploader(
        "Select a clear photo of the clothing item.",
        type=['png', 'jpg', 'jpeg'],
        key="garment_uploader"
    )
    if garment_image_file:
        st.image(garment_image_file, caption="Garment's Image", use_column_width=True)

st.divider()

if st.button("✨ Generate Try-On Image", use_container_width=True, type="primary"):
    if person_image_file and garment_image_file:
        with st.spinner("Our AI stylist is at work... Please wait a moment."):
            # Get bytes from uploaded files
            person_bytes = person_image_file.getvalue()
            garment_bytes = garment_image_file.getvalue()

            # Generate the image
            result_image = generate_virtual_try_on_image(person_bytes, garment_bytes)

            if result_image:
                st.subheader("🎉 Here's Your Virtual Try-On!")
                st.image(result_image, caption="Generated Image", use_column_width=True)
    else:
        st.warning("Please upload both a person's image and a garment's image.")
