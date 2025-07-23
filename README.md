


# 🤖 AI-Powered Q&A Chatbot API (FastAPI + Groq)

An intelligent and lightweight question-answering backend built with **FastAPI** and powered by **Groq's LLaMA 3** models. This API is capable of processing natural language queries and returning accurate, contextual responses — ideal for integration into chatbots, educational platforms, support assistants, and more.

Hosted on **[Railway](https://railway.app/)** for rapid deployment and scalability.

---

## 📌 Project Overview

This project serves as the backend for an AI-powered Q&A system. It accepts a question from the frontend, processes it using Groq's hosted large language models (like `llama3-70b-8192`), and returns a human-like response.

### ✅ Use Cases

- AI Chatbots
- Customer Support Assistants
- Educational Tutors
- Internal Knowledgebase Search
- Developer Assistants

---

## 🚀 Live API Endpoint

```

[https://test-production-d202.up.railway.app/query](https://test-production-d202.up.railway.app/query)

```

Use this endpoint to POST questions and receive AI-generated responses.

---

## 🧠 Technology Stack

| Layer        | Tech Used               |
|--------------|-------------------------|
| Language     | Python 3.12+            |
| Web Framework| FastAPI                 |
| AI Provider  | Groq API (LLaMA 3)      |
| Deployment   | Railway                 |
| Environment  | dotenv (.env) support   |

---

## 📂 Directory Structure

```

📁 ai-qa-backend/
├── main.py               # Core FastAPI app
├── requirements.txt      # Python dependencies
├── .env                  # Environment variables (Groq API key, model)

````

---

## ⚙️ Environment Setup

Create a `.env` file with the following values:

```env
GROQ_API_KEY=gsk_xxxxxxxxxxxxxxxxxxxxxx
GROQ_MODEL=llama3-70b-8192
````

Your API key can be obtained from: [https://console.groq.com](https://console.groq.com)

---

## 📦 Installation & Local Development

1. **Clone the repo**

   ```bash
   git clone https://github.com/your-username/ai-qa-backend.git
   cd ai-qa-backend
   ```

2. **Create a virtual environment**

   ```bash
   python -m venv venv
   source venv/bin/activate    # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Run the development server**

   ```bash
   uvicorn main:app --reload
   ```

   The app will be running at: [http://localhost:8000](http://localhost:8000)

---

## 🔐 CORS Configuration

For frontend consumption, CORS is pre-enabled for all origins. For production, consider restricting it:

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## 📤 API Usage

### 📍 Endpoint

```
POST /query
```

### 🔧 Request Body

```json
{
  "question": "What is machine learning?"
}
```

### ✅ Success Response

```json
{
  "answer": "Machine learning is a subset of artificial intelligence (AI)..."
}
```

### ❌ Error Response

```json
{
  "detail": "Failed to process query"
}
```

---

## 🌐 Frontend Integration (Example)

Using `fetch` in React or vanilla JavaScript:

```javascript
const fetchAnswer = async (question) => {
  const response = await fetch("https://test-production-d202.up.railway.app/query", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ question })
  });
  const data = await response.json();
  return data.answer;
};
```

---

## 📈 Deployment (via Railway)

1. Push your code to GitHub
2. Create a project on [Railway](https://railway.app/)
3. Link your GitHub repo
4. Set your environment variables:

   * `GROQ_API_KEY`
   * `GROQ_MODEL`
5. Deploy 🚀

---

## 🧾 `requirements.txt`

```txt
fastapi
uvicorn[standard]
python-dotenv
requests
```

Avoid unused packages like `logging`, `certifi`, or duplicate entries.

---

## 🤝 Contribution

Contributions, bug reports, and feature requests are welcome!

```bash
# Fork this repository
# Create a new branch
git checkout -b feature/your-feature-name

# Commit changes
git commit -m "Add: Your new feature"

# Push and create a PR
```

---

## 🛡️ License

Licensed under the **MIT License**. See [`LICENSE`](./LICENSE) for more information.

---

## 👨‍💻 Author

**Nimrod Omanga O.**
Prompt Engineer | Full Stack Developer | AI Systems Architect
[Portfolio](https://portfolio-rouge-zeta-36.vercel.app) · [LinkedIn](https://www.linkedin.com/in/nimrodomanga) · [GitHub](https://github.com/nimrod-omanga)

---

## 📸 Project Preview

```bash
[🧠 Q&A AI Backend]
      ↓
 Frontend App (React, Streamlit, etc.)
      ↓
  POST /query {"question": "Your query"}
      ↓
 Groq LLM API
      ↓
Response → Frontend
```

---

### 💬 Questions?

Feel free to open an [issue](https://github.com/your-username/ai-qa-backend/issues) or contact me directly.

---

```

---

### ✅ Next Steps

Would you like me to:
- Export this as a `.md` file?
- Push it directly to your GitHub repo?
- Style a frontend `README.md` to pair with this?
- Add diagrams or badges?

Let me know and I’ll get it done.
```
