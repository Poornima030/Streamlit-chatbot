# 🌸 Streamlit Chatbot 

This is a **live, fully functional chatbot** application built using **Streamlit** and powered by the **Google Gemini API**. The interface is styled with a unique pink and purple theme inspired by a modern, friendly AI aesthetic.

## 🔗 Live Application

Experience the chatbot yourself by visiting the deployed link:

➡️ **[Launch the Gemini Chatbot App](https://app-chatbot-jwa3je6smqys7hpztey5jf.streamlit.app/)**

-----

## ✨ Features

  * **Custom Theme:** A unique UI styled with custom CSS and a vibrant pink color palette.
  * **Streaming:** Provides a fast, real-time "typing" effect for an engaging user experience.
  * **Chat History:** Maintains conversation context throughout the entire session.
  * **Secure:** Uses Streamlit Cloud's **Secrets** management for API key security.

-----

## 📸 Screenshots of the Working Model

<img width="1919" height="915" alt="image" src="https://github.com/user-attachments/assets/53336122-6c8f-489c-b9e1-ea4de25ff6b7" />

## 🚀 Getting Started (For Developers)

### Prerequisites

1.  **Python 3.8+**
2.  **A Gemini API Key** (Key used for this app is named `StreamlitChatbot`)

### 1\. Installation

Clone the repository and install the required Python packages:

```bash
git clone YOUR_REPO_URL
cd Streamlit-chatbot
pip install -r requirements.txt
```

### 2\. API Key Setup

This application is configured to read the API key from a variable named `GEMINI_API_KEY`.

  * **For Local Use:** Create a file named **`.streamlit/secrets.toml`** and add your key:
    ```ini, TOML
    GEMINI_API_KEY = "YOUR_ACTUAL_GEMINI_API_KEY_HERE"
    ```
  * **For Streamlit Cloud Deployment:** The key must be added manually to the **Secrets** section of the deployed app's settings.

### 3\. Run Locally

Launch the application from your terminal:

```bash
streamlit run chat_app.py
```

-----

## 📜 `requirements.txt`

```
streamlit
google-genai
```
