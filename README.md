# AI Quiz Genie – Generate AI-Powered Quizzes

ai-quizgenie is an **Apify Actor** that extracts content from **webpages and PDFs** to generate **multiple-choice quiz questions (MCQs)** using **LLMs (GPT-3.5, GPT-4, etc.)**.

✅ **Supports Web & PDF Extraction**  
✅ **Dynamic Model Selection** (GPT-3.5, GPT-4, etc.)  
✅ **LangGraph for Workflow Automation**  
✅ **Apify-Compatible for Deployment**  

---

## 📂 Project Structure
```
/ai-quizgenie/
│── src/
│   ├── __main__.py       # Executes main.py
│   ├── main.py           # Apify Actor Execution and Langgraph flow
│   ├── tools.py          # Web & PDF Extraction
│   ├── utils.py          # Quiz Generation Logic
│   ├── models.py         # Pydantic Schema
│── dataset_schema.json   # Defines Output Format
│── requirements.txt      # Python Dependencies
│── Dockerfile            # Containerized Deployment
│── input.json            # Example Input
│── README.md             # Documentation
```

---

## 🛠 Installation & Setup
### 1️⃣ Clone the Repository
```bash
git clone https://github.com/yourusername/ai-quizgenie.git
cd ai-quizgenie
```

### 2️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 3️⃣ Set API Keys (Optional)
If using OpenAI, set your API keys:
```bash
export OPENAI_API_KEY="your-api-key-here"
export OPENAI_API_BASE="your-base-url"
```

---

## 🚀 Running the Actor Locally
### Run with Sample Input
```bash
apify run -i input.json
```

### Example `input.json`
```json
{
    "url": "https://en.wikipedia.org/wiki/Artificial_intelligence",
    "num_questions": 5,
    "difficulty": "Medium",
    "model": "gpt-4-turbo"
}
```

---

## 🔧 How It Works
1. **Extracts content** from webpage/PDF  
2. **Uses LLM** to generate quiz questions  
3. **Outputs structured MCQs** in JSON format  

---

## 📜 Example Output (`dataset_schema.json`)
```json
{
    "model": "gpt-4-turbo",
    "questions": [
        {
            "question": "Who is considered the father of AI?",
            "options": ["Alan Turing", "John McCarthy", "Geoffrey Hinton", "Yann LeCun"],
            "answer": "John McCarthy",
            "explanation": "John McCarthy coined the term 'Artificial Intelligence' in 1956."
        }
    ]
}
```

---

## 📦 Deploying to Apify
### 1️⃣ Push to Apify
```bash
apify push
```

### 2️⃣ Run on Apify Cloud
```bash
apify call ball-ceg/ai-quizgenie -i input.json
```

---

## 📜 Customization
- **Modify `input.json`** to change the difficulty, number of questions, or LLM model  
- **Edit `utils.py`** to tweak the quiz generation prompt  
- **Extend `graph.py`** to add more processing steps  

---
## 🤝 Contributing
Want to improve AI QuizGenie? Open a PR or suggest features! 🚀  

---
## Apify Screenshots

<img width="1518" alt="Screenshot 2025-03-07 at 9 43 06 PM" src="https://github.com/user-attachments/assets/13610ef1-9fce-42da-b0fa-fe1d88e43ee3" />

---

<img width="1508" alt="Screenshot 2025-03-07 at 9 39 04 PM" src="https://github.com/user-attachments/assets/2a4d9129-3940-4c8d-a401-f23bc29762a0" /> 

---
<img width="1518" alt="Screenshot 2025-03-07 at 9 41 08 PM" src="https://github.com/user-attachments/assets/3d9af545-7450-40f1-9265-50aa528ef48f" />

---


 
