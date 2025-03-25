import streamlit as st
import sqlite3
import google.generativeai as genai

# Configure Gemini AI
GEMINI_API_KEY = "AIzaSyDpBGGP40Km8D1_JH97jAw7jXlxqoq5Z7Q"  # Replace with actual API key
genai.configure(api_key=GEMINI_API_KEY)

# Database Setup
def init_db():
    conn = sqlite3.connect("chat_history.db", check_same_thread=False)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_input TEXT,
                    ai_response TEXT,
                    correction TEXT,
                    explanation TEXT,
                    mistake_analysis TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )''')
    conn.commit()
    return conn, c

# Store chat history
def store_chat(conn, c, user_input, ai_response, correction, explanation, mistake_analysis):
    c.execute("INSERT INTO history (user_input, ai_response, correction, explanation, mistake_analysis) VALUES (?, ?, ?, ?, ?)",
              (user_input, ai_response, correction, explanation, mistake_analysis))
    conn.commit()

# Retrieve chat history
def get_chat_history(conn, c):
    c.execute("SELECT * FROM history ORDER BY timestamp DESC")
    return c.fetchall()

# Clear chat history
def clear_history(conn, c):
    c.execute("DELETE FROM history")
    conn.commit()

# Generate response from Gemini AI
def generate_response(prompt):
    model = genai.GenerativeModel("gemini-1.5-pro")
    response = model.generate_content(prompt)
    return response.text if response else "No response generated."

# Generate mistake analysis in the user's native language
def generate_mistake_analysis(known_language, chat_history):
    prompt = f"User speaks {known_language}. Provide an easy-to-understand summary of common mistakes in the chat history and suggest improvement areas in {known_language}:\n\n"
    for chat in chat_history:
        prompt += f"User: {chat[1]}\nAI: {chat[2]}\nCorrection: {chat[3]}\nExplanation: {chat[4]}\n\n"
    
    return generate_response(prompt)

# Streamlit UI
st.set_page_config(page_title="AI Language Chatbot", page_icon="🗣️", layout="wide")
menu = st.sidebar.radio("📌 Navigation", ["🏠 Chatbot", "📂 Chat History", "📊 Mistake Analysis"])

conn, c = init_db()

if menu == "🏠 Chatbot":
    st.title("🗣️ AI Language Learning Chatbot")
    
    known_language = st.text_input("🏠 Your Native Language", "kannada")
    learning_language = st.text_input("🌍 Learning Language", "English")
    proficiency = st.selectbox("📊 Proficiency Level", ["Beginner", "Intermediate", "Advanced"])
    
    user_input = st.text_area("📝 Your message:")
    if st.button("💬 Send") and user_input.strip():
        prompt = f"User is learning {learning_language}, speaks {known_language}, and is {proficiency} level. Correct mistakes and provide explanations: {user_input}"
        response = generate_response(prompt)
        
        correction, explanation = "", ""
        if "[Correction]" in response:
            parts = response.split("[Correction]")
            correction = parts[1].strip().split("[Explanation]")[0] if "[Explanation]" in parts[1] else parts[1].strip()
            explanation = parts[1].split("[Explanation]")[1].strip() if "[Explanation]" in parts[1] else ""
        
        mistake_analysis = generate_mistake_analysis(known_language, [(None, user_input, response, correction, explanation)])
        store_chat(conn, c, user_input, response, correction, explanation, mistake_analysis)
        
        st.write(f"**🤖 AI:** {response}")
        st.write(f"✅ **Correction:** {correction}")
        st.write(f"ℹ️ **Explanation:** {explanation}")
        st.write(f"📊 **Mistake Analysis:** {mistake_analysis}")

if menu == "📂 Chat History":
    st.title("📂 Full Chat History")
    chat_history = get_chat_history(conn, c)
    
    if chat_history:
        for chat in chat_history:
            st.write(f"🔹 **ID:** {chat[0]}")
            st.write(f"   **User Input:** {chat[1]}")
            st.write(f"   **AI Response:** {chat[2]}")
            st.write(f"   ✅ **Correction:** {chat[3]}")
            st.write(f"   ℹ️ **Explanation:** {chat[4]}")
            st.write(f"   📊 **Mistake Analysis:** {chat[5]}")
            st.write("---")
    else:
        st.write("🗃️ No chat history available.")
    
    if st.button("🗑️ Clear Chat History"):
        clear_history(conn, c)
        st.write("✅ Chat history cleared!")

if menu == "📊 Mistake Analysis":
    st.title("📊 Mistake Analysis & Learning Insights")
    chat_history = get_chat_history(conn, c)
    if chat_history:
        overall_analysis = generate_mistake_analysis(chat_history[0][1], chat_history)
        st.write(f"📋 **Overall Mistake Summary:** {overall_analysis}")
    else:
        st.write("🗃️ No chat history available for analysis.")

st.write("🔹 Powered by **llm chatbot** 🚀")
