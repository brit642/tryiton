👕 AI Virtual Try-On Application
This is an interactive web application that uses Google Cloud's cutting-edge generative AI to perform a "virtual try-on". Users can upload an image of a person and an image of a garment (like a t-shirt, pants, or shoes), and the application will generate a new, realistic image of the person wearing the selected item.

This project is built with Python and Streamlit, and it leverages the powerful Virtual Try-On model available on Google's Vertex AI platform.


(Feel free to replace the image above with a screenshot of your running application!)

✨ Features
Interactive UI: Simple and intuitive web interface powered by Streamlit.

Person Image Upload: Upload a clear, front-facing photo of a person.

Garment Image Upload: Upload a clear photo of a clothing item.

AI-Powered Generation: Generates a high-quality image of the person wearing the garment naturally.

Direct Image Handling: Processes local image uploads directly without needing Google Cloud Storage.

⚙️ How It Works
The application captures the two uploaded images (person and garment) and converts them into base64-encoded strings. These strings are then sent as a request to a specific, pre-trained Virtual Try-On model endpoint hosted on Google Cloud's Vertex AI. The AI model processes these images and returns a new, generated image, which is then decoded and displayed to the user.

🚀 Setup and Installation
Follow these steps to set up and run the project on your local machine.

Prerequisites
Python 3.8+

Google Cloud SDK installed and authenticated.

A Google Cloud Project with the Vertex AI API enabled.

1. Clone the Repository
First, clone the repository to your local machine.

git clone [https://github.com/brit642/try-it.git](https://github.com/brit642/try-it.git)
cd try-it

2. Create a Virtual Environment
It is highly recommended to use a virtual environment to manage project dependencies.

# Create the virtual environment
python -m venv .venv

# Activate the virtual environment
# On macOS/Linux:
source .venv/bin/activate

# On Windows:
# .venv\Scripts\activate

3. Install Dependencies
Install all the required Python packages from the requirements.txt file.

pip install -r requirements.txt

4. Authenticate with Google Cloud
You need to authenticate your local environment to allow the application to access Google Cloud services.

gcloud auth application-default login

Follow the instructions in your browser to complete the login process.

5. Configure Your Project ID
Open the app.py file and replace the placeholder with your actual Google Cloud Project ID.

# Find this line in app.py
PROJECT_ID = "MyProject-ID" # <-- Replace with your project ID

▶️ How to Run the App
Once you have completed the setup, you can run the Streamlit application with a single command:

streamlit run app.py

Your web browser will automatically open a new tab with the running application.

📂 Project Structure
try-it/
├── .venv/                # Virtual environment folder (ignored by git)
├── .gitignore            # Specifies files for Git to ignore
├── app.py                # The main Streamlit application script
├── README.md             # This README file
└── requirements.txt      # Python package dependencies

📄 License
This project is licensed under the Apache 2.0 License. See the LICENSE file for details.

🙏 Acknowledgments
This project is based on the official Google Cloud Platform Virtual Try-On notebook. A big thank you to the original authors for providing the foundation and the powerful AI model.
