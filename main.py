import streamlit as st
import google.generativeai as genai
from pytesseract import pytesseract
import uuid  

#IMAGE EXTRACTING CODE START
class OCR:
    def __init__(self):
        self.path = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

    def extract(self, filename):

        try:
            pytesseract.tesseract_cmd = self.path
            text = pytesseract.image_to_string(filename)
            return text

        except Exception as e:
            print(e)
            return "Error"
        
#IMAGE EXTRACTING CODE END

genai.configure(api_key="AIzaSyBGT3ai6i_IrBx-82W0PrVpumeWTMD4c6g")

# Set up the model
generation_config = {
  "temperature": 0,
  "top_p": 1,
  "top_k": 1,
  "max_output_tokens": 2048,
}

safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
]

model = genai.GenerativeModel(model_name="gemini-1.0-pro",
                              generation_config=generation_config,
                              safety_settings=safety_settings)
st.title("AI CHAT")
st.markdown("AI is here to assist you.")

def translate_role_for_streamlit(user_role):
    if user_role == "model":
        return "assistant"
    else:
        return user_role


# Initialize chat session in Streamlit if not already present
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])
    
    

# Display the chatbot's title on the page
st.title("🤖 Personal Assistant")

# Display the chat history

# for message in st.session_state.chat_session.history:
#     with st.chat_message(translate_role_for_streamlit(message.role)):
#         st.markdown(message.parts[0].text)

uploaded_file = st.file_uploader("Choose an image:", type=['jpg', 'png'])
user_prompt = st.chat_input("Ask me...")
text = ""
if uploaded_file is not None:
    # Generate a unique filename using uuid
    filename = f"{uuid.uuid4()}.png"
    # Save the uploaded image data to the server's filesystem 
    with open(filename, "wb") as f:
        f.write(uploaded_file.read())
    ocr = OCR()
    text = ocr.extract(filename)
    text = "summerize it : " + text
    print(text)
    
if text:
    # Send user's message to Gemini-Pro and get the response
    gemini_response = st.session_state.chat_session.send_message(text)

    # Display Gemini-Pro's response
    with st.chat_message("assistant"):
        st.markdown(gemini_response.text)

if user_prompt:
    # Add user's message to chat and display it
    st.chat_message("User").markdown(user_prompt)

    # Send user's message to Gemini-Pro and get the response
    gemini_response = st.session_state.chat_session.send_message(user_prompt)

    # Display Gemini-Pro's response
    with st.chat_message("assistant"):
        st.markdown(gemini_response.text)

# st.write(st.session_state.chat_session.history)