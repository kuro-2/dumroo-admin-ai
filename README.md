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

![image](https://github.com/user-attachments/assets/3f469572-9d85-482a-90b2-56d1e7ecfa22)
![image-1](https://github.com/user-attachments/assets/848eaff0-dd32-4d22-b681-195b37ee4626)
![image-2](https://github.com/user-attachments/assets/8cf53cdf-2c51-482d-a730-0c696f8ebb76)
![image-3](https://github.com/user-attachments/assets/b5a81dfe-de9e-40ce-8f09-4b992ce6b9fc)
![image-4](https://github.com/user-attachments/assets/4cd0f6b9-edd4-47fc-8b16-1750a8323576)
![image-5](https://github.com/user-attachments/assets/b7a2def7-42e7-4d4c-9123-f17c9851c809)
![image-6](https://github.com/user-attachments/assets/b4b76fce-26e9-4d31-accf-8d496dc517f4)
![image-7](https://github.com/user-attachments/assets/a0085ce7-29a1-4afb-af5f-3a5b7d5c24be)




