# Dumroo Admin Panel AI Assistant

A Streamlit-based AI assistant for school administrators to interact with student data using natural language queries. Powered by Google Gemini (Gemini 2.0 Flash) via LangChain, it supports role-based access control and answers questions about student performance, submissions, and quizzes.

---

## 🚀 Features

- **Natural Language Queries:** Ask questions about student data (e.g., "Show me performance data for Grade 8 from last week").
- **Role-Based Access Control:** Admins see only the data relevant to their role (Super Admin, Grade Admin, Class Admin, Region Admin).
- **Gemini AI Integration:** Uses Google Gemini 2.0 Flash model for fast, accurate responses.
- **Streamlit UI:** Simple web interface for interaction.

---

## 🛠️ Installation

1. **Clone the repository:**
    ```bash
    git clone https://github.com/kuro-2/dumroo-admin-ai.git
    cd dumroo-admin-ai
    ```

2. **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
    Or manually:
    ```bash
    pip install streamlit pandas python-dotenv langchain langchain-experimental langchain-google-genai tabulate
    ```

3. **Set up your Gemini API key:**
    - Create a `.env` file in the project root:
      ```
      GOOGLE_API_KEY=your-gemini-api-key-here
      ```
    - Get your Gemini API key from [Google AI Studio](https://aistudio.google.com/app/apikey).

4. **Add your data:**
    - Place your `data.json` file (student data) in the project directory.

---

## ▶️ Usage

Run the Streamlit app:

```bash
streamlit run main.py
```

Open the provided local URL in your browser.  
Select your admin role, view accessible data, and ask questions in natural language!

---

## 📄 Example Queries

- Which students haven't submitted their homework yet?
- Show me performance data for Grade 8 from last week.
- List all upcoming quizzes scheduled for next week.
- What is the average quiz score for students in 8A?
- How many students are in the North region?
- Show me all students with a quiz score less than 75.

---

## 📝 About

This project demonstrates how AI can empower school administrators to gain insights from student data quickly and securely, using the latest in generative AI and data

## 🖼️ Screenshot

![alt text](image.png)
![alt text](image-1.png)
![alt text](image-2.png)
![alt text](image-3.png)
![alt text](image-4.png)
![alt text](image-5.png)
![alt text](image-6.png)
![alt text](image-7.png)



