FastAPI for building REST API
Axios for making API requests
Vue.js for frontend framework
Hugging face transformer for pegasus model used to summarize


Utilizes caching and chunk processing to handle large text inputs, splits into manageable chunks
Vue.js frontend is served directly through FastAPI

Uses pytest and httpx for backend testing
For frontend testing use Jest

1. Clone Repository

```bash
git clone https://github.com/mnothman/NLPsummarizer
cd NLPsummarizer
```

# 2. Setup Backend

```bash
cd backend
```

Create and activate virtual environment 
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

Install dependencies for backend

```bash
pip install -r requirements.txt
```

Optional for preprocessing spacy model 
python -m spacy download en_core_web_sm

3. Start FastAPI server
```bash
uvicorn app.main:app --reload
```
Debug mode: uvicorn app.main:app --reload --log-level debug


Project run at:
http://127.0.0.1:8000

To see docs:
http://127.0.0.1:8000/docs

# 4. Frontend

Navigate to frontend directory

```bash
cd frontend
```
Install dependencies

```bash
npm install
```

Build Vue app

```bash
npm run build
```

Copy created dist/ folder from npm run build into backend/app/

```bash
cp -r dist ../backend/app/
```

Access application after frontend built

```bash
uvicorn app.main:app --reload
```

Visit the frontend at http://127.0.0.1:8000/

![Image](https://github.com/user-attachments/assets/6db8b05e-f862-4c97-9f6a-16bab094759c)

![Image](https://github.com/user-attachments/assets/43c9d492-fed4-4b0e-8b1d-8c6e2fecfd4f)


# For testing:
Uses pytest and httpx for backend testing
For frontend testing use Jest


Backend Testing
backend/tests

```bash
cd backend
pytest tests/
```

Frontend Testing 
rontend/tests
```bash
cd frontend
npm run test:unit
```
![Image](https://github.com/user-attachments/assets/e7207eee-2b77-4e45-b266-4543c1666d3d)
![Image](https://github.com/user-attachments/assets/2c5d78cf-fb47-44a3-802d-cddbd88d8f28)

NLPproject/ <br/>
├── backend/ <br/>
│   ├── app/ <br/>
│   │   ├── dist/              # Compiled Vue.js frontend <br/>
│   │   ├── main.py            # FastAPI backend entry point <br/>
│   │   ├── summarizer.py      # Text summarization logic <br/>
│   │   ├── utils.py           # Utility functions <br/>
│   │   └── __init__.py <br/>
│   ├── static/                # Static assets (optional) <br/>
│   └── tests/                 # Test files <br/>
├── frontend/                  # Vue.js project source files <br/>
│   ├── public/                # Public assets <br/>
│   ├── src/                   # Vue.js components and logic <br/>
│   └── vue.config.js          # Vue.js configuration <br/>
├── requirements.txt           # Python dependencies <br/>
└── README.md    <br/>
