# Architecture Overview

## 1. Introduction

This document provides an overview of the architecture for the AI Language Learning Chatbot. The chatbot helps users improve their language skills by providing AI-driven corrections, explanations, and mistake analysis in a native language for better understanding.

## 2. System Components

### 2.1 User Interface

- **Technology**: Streamlit
- **Features**:
  - User inputs text in the learning language.
  - AI provides real-time corrections and explanations.
  - Mistake analysis is generated for each chat session.
  - Chat history is stored and accessible for review.
  - Users can clear chat history and mistake analysis.

### 2.2 AI Processing

- **Technology**: Google Gemini AI (Generative AI)
- **Process**:
  - Receives user input and processes it for language correction.
  - Returns the corrected version along with an explanation.
  - Generates mistake analysis after each chat session.
  - Provides mistake analysis in the user's native language for better comprehension.

### 2.3 Database

- **Technology**: SQLite
- **Schema**:
  - `history` table:
    - `id`: Unique identifier
    - `user_input`: User's original text
    - `ai_response`: AI-generated response
    - `correction`: Corrected version of the input
    - `explanation`: Explanation of mistakes
    - `mistake_analysis`: Summary of frequent mistakes and improvement areas
    - `timestamp`: Time of entry

### 2.4 Mistake Analysis Module

- **Functionality**:
  - Aggregates user mistakes from chat history.
  - Identifies patterns in errors.
  - Provides a summary of common mistakes.
  - Generates recommendations for improvement in the native language.

## 3. Workflow

1. **User Interaction**:

   - User inputs text in the learning language.
   - AI processes input and provides corrections and explanations.
   - Mistake analysis is generated after every chat session.

2. **Database Storage**:

   - Each chat session, including corrections and explanations, is stored in SQLite.
   - Mistake analysis is updated with each new interaction.

3. **Review and Improvement**:

   - Users can review chat history and mistake analysis.
   - Users can clear chat history and analysis as needed.

## 4. Conclusion

This architecture ensures an efficient and user-friendly language learning experience by combining AI-driven correction, real-time mistake analysis, and a persistent learning history. The integration of Google Gemini AI with Streamlit and SQLite enables a seamless workflow, making the chatbot an effective learning tool.

