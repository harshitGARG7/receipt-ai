this is made by harsht garg

## Screenshots

| Screenshot 1                           | Screenshot 2                           |
| -------------------------------------- | -------------------------------------- |
| ![Screenshot1](assets/screenshot1.png) | ![Screenshot2](assets/screenshot2.png) |

# Receipt AI

A simple AI-powered receipt scanning application using OCR + LLMs to extract structured data from receipts.

---

## 🚀 Features

- Upload receipt images (JPG/PNG)
- Extract text using OCR (Tesseract)
- Use LLM to convert raw text to structured JSON
- Save parsed data to a database (JSON file for now)
- CLI/API interface

---

## 🧠 Tech Stack

| Component  | Technology                                       |
| ---------- | ------------------------------------------------ |
| Backend    | Python + Flask/FastAPI (specify soon)            |
| OCR        | Tesseract OCR                                    |
| AI Model   | OpenAI / Custom model                            |
| Database   | JSON file (local), optional Mongo/Postgres later |
| Deployment | Render / Railway                                 |

---

## 📦 Installation

```bash
git clone https://github.com/harshitGARG7/receipt-ai.git
cd receipt-ai
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
# OR
.venv\\Scripts\\activate  # Windows
pip install -r requirements.txt
```

---

## ▶ Run the Application

```bash
python app.py
```

The app will start at:

```
http://localhost:5000
```

---

## 🚢 Deployment (Render / Railway)

### Render (recommended)

1. Go to render.com
2. Click **New Web Service**
3. Connect GitHub repo
4. Pick `main` branch
5. Set **Build Command**:

```bash
pip install -r requirements.txt
```

6. Set **Start Command**:

```bash
python app.py
```

7. Choose **Free plan**
8. Deploy 🎉

---

## 📁 Project Structure

```
receipt-ai/
│── app.py
│── llm.py
│── ocr.py
│── db.json
│── requirements.txt
│── .gitignore
│── images/ (ignored in git)
```

---

## 📝 TODO / Next Steps

- Add UI to upload receipts
- Store parsed expenses by category
- Support multiple formats & currencies
- Deploy frontend on Vercel

---

## 🤝 Contributing

PRs and issues are welcome!

---

## 📄 License

MIT License

---

## ⭐ Support

If you like this project, please star the repository on GitHub 🙂
