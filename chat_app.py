import streamlit as st
from google import genai
from google.genai import types # Import types for structured content formatting

# --- CUSTOM CSS FOR THEME ---
st.markdown("""
<style>
/* 1. Overall Page and Background */
body {
    background-color: #FAEE8ED; /* Lavender Blush - a very light pink for the page background */
}
.main .block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}

/* 2. Custom Header Bar Styling */
/* Hide the default Streamlit header bar */
.stApp > header {
    visibility: hidden; 
}
/* Style the container where the logo and title are placed */
.stApp .main [data-testid="stVerticalBlock"] > div:first-child { 
    background-color: #FFB2C5; /* Cherry Blossom Pink - custom header background */
    padding: 15px 10px;
    border-radius: 0px 0px 15px 15px; 
    margin-bottom: 20px;
    
    /* Ensure content inside the header is centered */
    display: flex;
    align-items: center;
    justify-content: center;
}

/* 3. Title Text Styling */
h1 {
    color: #444444; /* Darker text for readability on pink background */
    font-size: 2.0em; /* Slightly smaller for a tighter look */
    margin: 0;
    line-height: 1.0;
}

/* 4. General Chat Container Reset */
div[data-testid="stChatMessage"] {
    background-color: transparent !important;
    padding: 0px 10px;
    margin-bottom: 10px;
    border: none;
}

/* 5. User Chat Bubble (Right-aligned, Amaranth Pink) */
.stChatMessage:has([data-testid="stChatMessageAvatarUser"]) {
    flex-direction: row-reverse; 
    text-align: right;
}
.stChatMessage:has([data-testid="stChatMessageAvatarUser"]) [data-testid="stMarkdownContainer"] {
    background-color: #FFA2B9; /* Amaranth Pink for User */
    color: white; 
    border-radius: 18px 18px 0px 18px; 
    padding: 10px 15px;
    max-width: 70%; /* Allows width to shrink for small messages */
    box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
    display: inline-block; /* Crucial: Shrink-wraps the container to the text size */
    text-align: left; 
}

/* 6. Assistant Chat Bubble (Left-aligned, Mimi Pink) */
.stChatMessage:has([data-testid="stChatMessageAvatarAssistant"]) {
    flex-direction: row; 
    text-align: left;
}
.stChatMessage:has([data-testid="stChatMessageAvatarAssistant"]) [data-testid="stMarkdownContainer"] {
    background-color: #FDD5DF; /* Mimi Pink for Assistant */
    color: #333333; 
    border-radius: 18px 18px 18px 0px; 
    padding: 10px 15px;
    max-width: 70%; /* Allows width to shrink for small messages */
    box-shadow: -2px 2px 5px rgba(0,0,0,0.1);
    display: inline-block; /* Crucial: Shrink-wraps the container to the text size */
    text-align: left; 
}

/* 7. Input Box Styling */
.stChatInputContainer input {
    border-radius: 12px;
    border: 1px solid #FFB2C5 !important; /* Cherry Blossom Pink border */
    padding: 10px 15px;
    box-shadow: 0px 2px 5px rgba(0,0,0,0.1);
}
</style>
""", unsafe_allow_html=True)


# --- HEADER WITH IMAGE AND TITLE ---
# Use columns to place the logo and title side-by-side
# Adjust ratios to center the combined image/title block
col1, col2, col3 = st.columns([0.38, 0.30, 0.32]) # Tighter inner columns, wider outer columns

with col1:
    # Use st.image for the logo (must be in the images/ folder)
    # The image width (60) is sized to match the title height
    st.image("images/robot_logo_pink.png", width=100) 

with col2:
    # Added a left margin of 15px to push the text away from the image slightly
    st.markdown("<h1 style='color:#561530; margin:0 0 0 10px;'>Chatbot</h1>", unsafe_allow_html=True)

# The third column (col3) is left empty for alignment


# --- REST OF THE CHAT APP LOGIC ---

# Fetch the GEMINI_API_KEY from secrets.toml
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
except KeyError:
    st.error("GEMINI_API_KEY not found. Please add your Gemini key to .streamlit/secrets.toml")
    st.stop()
    
# Initialize the Gemini client
client = genai.Client(api_key=API_KEY)


# 2. Session State Management (Initializing Variables)
if "gemini_model" not in st.session_state:
    st.session_state["gemini_model"] = "gemini-2.5-flash-lite"

if "messages" not in st.session_state:
    st.session_state.messages = []

# 3. Display Existing Messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. Handle User Input
if prompt := st.chat_input("Wassup?"):
    
    # Add user message to the stored chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display the user's message
    with st.chat_message("user"):
        st.markdown(prompt)

    # 5. Get and Display Assistant Response (The Core API Call)
    with st.chat_message("assistant"):
        
        # --- Format History for Gemini API ---
        formatted_contents = [
            types.Content(
                role="user" if m["role"] == "user" else "model",
                parts=[types.Part.from_text(text=m["content"])]
            )
            for m in st.session_state.messages
        ]
        
        # Call the Gemini API's streaming function
        response_stream = client.models.generate_content_stream(
            model=st.session_state["gemini_model"],
            contents=formatted_contents,
        )
        
        # Stream the response chunks using st.write_stream
        full_response = st.write_stream(
            (chunk.text for chunk in response_stream)
        )
        
    # Store the full, final assistant response in the chat history
    st.session_state.messages.append({"role": "assistant", "content": full_response})