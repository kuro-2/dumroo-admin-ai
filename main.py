import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
import io 
import tabulate
from contextlib import redirect_stdout 

# LangChain imports
from langchain_experimental.agents import create_pandas_dataframe_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage

# --- Configuration ---
# Load environment variables from .env file
load_dotenv()

# Ensuring the API key is set
if "GOOGLE_API_KEY" not in os.environ:
    st.error("GOOGLE_API_KEY environment variable not set. Please create a .env file with GOOGLE_API_KEY='YOUR_API_KEY'.")
    st.stop()

# --- Data Loading ---
@st.cache_data
def load_data(file_path="data.json"):
    """Loads student data from a JSON file."""
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
        df = pd.DataFrame(data)
        # Convert quiz_date to datetime objects for easier filtering
        df['quiz_date'] = pd.to_datetime(df['quiz_date'], errors='coerce')
        return df
    except FileNotFoundError:
        st.error(f"Error: {file_path} not found. Please ensure data.json is in the same directory.")
        st.stop()
    except Exception as e:
        st.error(f"Error loading data: {e}")
        st.stop()

# --- Role-Based Access Control (RBAC) ---
def filter_data_by_role(df, admin_role):
    """
    Filters the DataFrame based on the admin's assigned role.
    Admins can only see data relevant to their grade, class, or region.
    """
    filtered_df = df.copy()

    if admin_role == "Super Admin":
        # Super Admin can see all data
        return filtered_df
    elif admin_role == "Grade 8 Admin":
        # Grade 8 Admin sees only Grade 8 data
        filtered_df = filtered_df[filtered_df['grade'] == 8]
    elif admin_role == "Grade 9 Admin":
        # Grade 9 Admin sees only Grade 9 data
        filtered_df = filtered_df[filtered_df['grade'] == 9]
    elif admin_role == "8A Class Admin":
        # 8A Class Admin sees only 8A class data
        filtered_df = filtered_df[filtered_df['class'] == '8A']
    elif admin_role == "North Region Admin":
        # North Region Admin sees only North region data
        filtered_df = filtered_df[filtered_df['region'] == 'North']
    else:
        st.warning("Invalid admin role selected. Displaying no data.")
        return pd.DataFrame() # Return empty DataFrame for unrecognized roles

    return filtered_df

# --- AI System with LangChain ---
def get_ai_response(df, query):
    """
    Uses LangChain's Pandas DataFrame agent to answer natural language queries.
    """
    
    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0)
    
    agent = create_pandas_dataframe_agent(
        llm,
        df,
        verbose=True, 
        agent_type="openai-tools", 
        extra_tools=[], 
        allow_dangerous_code=True # REQUIRED to allow the agent to execute code
    )

    # Define a custom prompt to guide the agent
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are an AI assistant for the Dumroo Admin Panel. "
                "You have access to student data in a pandas DataFrame. "
                "Your goal is to answer questions about student performance, "
                "submission status, and quizzes based on the provided data. "
                "When asked about dates like 'last week' or 'next week', assume 'last week' refers to "
                "the last 7 days from today's date, and 'next week' refers to the next 7 days from today's date. "
                "Today's date is assumed to be 2025-07-10 for consistent demo results. "
                "Provide clear and concise answers. "
                "If a specific student or data point is not found, state that clearly. "
                "If asked for a list, provide it in an easy-to-read format. "
                "**Do not show Python code or instructions. Only provide the answer based on the data.**"
            ),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ]
    )

    # Initialize chat history
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Prepare input for the agent
    full_input = {"input": query, "chat_history": st.session_state.chat_history}

    # Capture verbose output
    f = io.StringIO()
    with redirect_stdout(f):
        try:
            # Invoke the agent with the query
            response = agent.invoke(full_input)
            
            # Append current interaction to chat history
            st.session_state.chat_history.append(HumanMessage(content=query))
            st.session_state.chat_history.append(AIMessage(content=response["output"]))
            
            output_text = f.getvalue()
            st.subheader("Agent's Thought Process (for debugging):")
            st.code(output_text)
            
            return response["output"]
        except Exception as e:
            output_text = f.getvalue() 
            st.subheader("Agent's Thought Process (for debugging):")
            st.code(output_text) 
            st.error(f"An error occurred while processing your query: {e}")
            st.info("Please try rephrasing your question or check your Gemini API key and model availability.")
            return "Error processing query."

# --- Streamlit UI ---
def main():
    st.set_page_config(page_title="Dumroo Admin Panel AI Assistant", layout="wide")

    st.title("📚 Dumroo Admin Panel AI Assistant")
    st.markdown(
        """
        Welcome to the Dumroo Admin Panel AI Assistant!
        Ask questions about student data in natural language.
        Your access to data is controlled by your selected admin role.
        """
    )

    # Load data
    df = load_data()

    st.sidebar.header("Admin Settings")
    admin_roles = [
        "Super Admin",
        "Grade 8 Admin",
        "Grade 9 Admin",
        "8A Class Admin",
        "North Region Admin"
    ]
    selected_role = st.sidebar.selectbox("Select Admin Role:", admin_roles)

    st.sidebar.markdown("---")
    st.sidebar.info(
        "**Role-Based Access Control (RBAC) in Action:**\n\n"
        "- **Super Admin:** Sees all data.\n"
        "- **Grade 8 Admin:** Sees only Grade 8 students.\n"
        "- **Grade 9 Admin:** Sees only Grade 9 students.\n"
        "- **8A Class Admin:** Sees only students in class 8A.\n"
        "- **North Region Admin:** Sees only students from the North region."
    )

    # Filter data based on selected role
    filtered_df = filter_data_by_role(df, selected_role)

    st.subheader(f"Data Accessible to: {selected_role}")
    if not filtered_df.empty:
        st.dataframe(filtered_df, use_container_width=True)
    else:
        st.info("No data accessible for the selected admin role.")

    st.markdown("---")
    st.subheader("Ask a Question")

    user_query = st.text_input("Type your question here:", key="user_query",
                                placeholder="e.g., Which students haven't submitted their homework yet?")

    if st.button("Get Answer"):
        if user_query:
            if not filtered_df.empty:
                with st.spinner("Thinking..."):
                    response = get_ai_response(filtered_df, user_query)
                    st.success("Here's the answer:")
                    st.write(response)
            else:
                st.warning("Cannot answer query: No data available for your selected role.")
        else:
            st.warning("Please enter a question.")

    st.markdown("---")
    st.subheader("Example Queries:")
    st.markdown(
        """
        - "Which students haven't submitted their homework yet?"
        - "Show me performance data for Grade 8 from last week." (Assumes today is 2025-07-10 for 'last week' calculation)
        - "List all upcoming quizzes scheduled for next week." (Assumes today is 2025-07-10 for 'next week' calculation)
        - "What is the average quiz score for students in 8A?"
        - "How many students are in the North region?"
        - "Show me all students with a quiz score less than 75."
        """
    )
    st.info(
        "**Note on Dates:** For 'last week' and 'next week' queries, the system is configured to assume today's date is **2025-07-10** "
        "to provide consistent demo results. In a live environment, this would dynamically use the current date."
    )

if __name__ == "__main__":
    main()
