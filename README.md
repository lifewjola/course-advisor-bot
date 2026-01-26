# 🎓 Course Advisor AI (RAG Chatbot)

**Live Demo:** [Course Advisor AI](https://course-advisor-ai.streamlit.app/)

This project is an AI-powered **Course Advisor Chatbot** designed for Babcock University. It uses **Retrieval-Augmented Generation (RAG)** to answer student inquiries about course registration, CGPA rules, and academic regulations with high accuracy.

It includes a secure **Admin Dashboard** for managing the knowledge base and monitoring student questions.

---

## 🏗️ Architecture & Tech Stack

This project is built for **$0 cost** using generous free tiers:

* **Frontend:** [Streamlit](https://streamlit.io/) (Python-based UI)
* **Database & Vector Store:** [Supabase](https://supabase.com/) (PostgreSQL + `pgvector`)
* **LLM & Embeddings:** [Google Gemini](https://ai.google.dev/) (Gemini 2.5 Flash Lite + Text-Embedding-004)
* **Language:** Python 3.10+

### 📂 Project Structure

The project follows a modular "Model-View-Controller" style pattern:

```text
course-advisor-bot/
├── .streamlit/              # Streamlit configuration
│   ├── config.toml          # UI Theme & Settings
│   └── secrets.toml         # ⚠️ API KEYS (Do NOT commit to Git)
├── app/                     # Backend Logic & Assets
│   ├── clients.py           # Database & AI Connections (Singleton)
│   ├── utils.py             # Helper functions (CSS loader)
│   ├── styles.css           # Custom University Styling
│   └── modules/             # The Core Logic
│       ├── embedder.py      # Text -> Vector converter
│       ├── upserter.py      # Admin tools (Add/Edit/Delete)
│       ├── retriever.py     # Search Engine (RAG)
│       ├── generator.py     # LLM Response Generator
│       ├── bot_logger.py    # Analytics/Logging
│       └── prompts.py       # AI Persona & Rules
├── pages/                   # Streamlit Pages
│   └── admin_panel.py       # 🔒 Secure Admin Dashboard
├── streamlit_app.py         # 🏠 Main Entry Point (Student Chat)
├── requirements.txt         # Python Dependencies
└── README.md                # Documentation

```

---

## 🚀 Setup & Installation

### 1. Prerequisites

* Python 3.9 or higher installed.
* A **Supabase** account (Free).
* A **Google Cloud** account (for Gemini API Key).

### 2. Clone the Repository

```bash
git clone https://github.com/lifewjola/course-advisor-bot.git
cd course-advisor-bot

```

### 3. Install Dependencies

It is recommended to use a virtual environment:

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate

```

Install the required packages:

```bash
pip install -r requirements.txt

```

### 4. Database Setup (Supabase)

1. Create a new project on [Supabase](https://supabase.com/).
2. Go to the **SQL Editor** (sidebar) and run the following script to create the tables and vector search function:

```sql
-- 1. Enable Vector Extension
create extension if not exists vector;

-- 2. Knowledge Base Table
create table knowledge_base (
  id bigint primary key generated always as identity,
  content text not null,
  embedding vector(768),
  created_at timestamptz default now(),
  updated_at timestamptz default now()
);

-- 3. Chat Logs Table
create table chat_logs (
  id bigint primary key generated always as identity,
  user_question text,
  bot_answer text,
  created_at timestamptz default now()
);

-- 4. Vector Search Function
create or replace function match_documents (
  query_embedding vector(768),
  match_threshold float,
  match_count int
)
returns table (
  id bigint,
  content text,
  similarity float
)
language plpgsql
as $$
begin
  return query
  select
    knowledge_base.id,
    knowledge_base.content,
    1 - (knowledge_base.embedding <=> query_embedding) as similarity
  from knowledge_base
  where 1 - (knowledge_base.embedding <=> query_embedding) > match_threshold
  order by similarity desc
  limit match_count;
end;
$$;

```

### 5. Configure Secrets

Create a file named `secrets.toml` inside the `.streamlit/` folder.
**Do NOT upload this file to GitHub.**

```toml
# .streamlit/secrets.toml

[supabase]
url = "YOUR_SUPABASE_PROJECT_URL"
key = "YOUR_SUPABASE_SERVICE_ROLE_KEY" # Use the SECRET key, not public!

[gemini]
api_key = "YOUR_GOOGLE_GEMINI_API_KEY"

[admin]
password = "SetYourStrongPasswordHere"

```

---

## 🖥️ Usage Guide

### Running the App Locally

Run the application from the project root:

```bash
streamlit run streamlit_app.py

```

### 🔒 Accessing the Admin Panel

1. Open the app in your browser.
2. Click **"🔐 Admin Access"** in the sidebar (or go to `http://localhost:8501/admin_panel`).
3. Enter the password you set in `secrets.toml`.

**What you can do in Admin:**

* **Knowledge Base:** Add plain text chunks (e.g., "CGPA for First Class is 4.50-5.00"). The system automatically converts them to vectors.
* **Edit/Delete:** Fix typos or remove outdated rules.
* **Chat Logs:** See exactly what students are asking to improve the data.

### 🎓 The Student Chatbot

* Students can access the main page.
* The bot remembers conversation context (e.g., "What is probation?" -> "How do I get out of **it**?").
* It strictly refuses to answer questions not found in the database (to prevent hallucinations).

---

## Deployment (Streamlit Cloud)

1. Push your code to **GitHub**.
2. Log in to [Streamlit Community Cloud](https://share.streamlit.io/).
3. Click **"New App"** and select your repository.
4. **CRITICAL STEP:** Before clicking Deploy, click **"Advanced Settings"**.
5. Paste the contents of your `secrets.toml` into the **"Secrets"** box.
6. Click **Deploy**.

---

## 📝 Troubleshooting

* **Error: `ModuleNotFoundError**`: Make sure you run `streamlit run streamlit_app.py` from the **root** folder, not inside `app/`.
* **Database Error**: Ensure you enabled the `vector` extension in Supabase.
* **Auth Error**: Check that you are using the `service_role` (secret) key for Supabase, not the `anon` key.