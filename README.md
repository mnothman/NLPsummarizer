Get environment set up in backend

python -m venv venv
source venv/bin/activate  # For Linux/macOS
venv\Scripts\activate     # For Windows


remove backend/app/templates/ and make a dedicated frontend later


<!-- optional for preprocessing spacy model -->
python -m spacy download en_core_web_sm


![Image](https://github.com/user-attachments/assets/43c9d492-fed4-4b0e-8b1d-8c6e2fecfd4f)

1. Start FastAPI server

in backend/ directory run:
```bash
uvicorn app.main:app --reload
```

browser: http://127.0.0.1:8000


2. Build and run docker image

```bash
docker build -t text-summarizer .
docker run -p 8000:8000 text-summarizer
```
```
NLPproject
├─ Dockerfile
├─ README.md
├─ backend
│  ├─ app
│  │  ├─ __pycache__
│  │  │  ├─ main.cpython-311.pyc
│  │  │  └─ summarizer.cpython-311.pyc
│  │  ├─ main.py
│  │  ├─ summarizer.py
│  │  ├─ templates
│  │  │  └─ index.html
│  │  └─ utils.py
│  ├─ data
│  ├─ static
│  ├─ tests
│  │  └─ test_main.py
│  └─ 
├─ frontend
└─ requirements.txt

```