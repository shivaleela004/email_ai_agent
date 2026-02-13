# AI Email Agent

## Setup

1. Create virtual environment
python -m venv venv

2. Activate
Windows:
venv\Scripts\activate

Mac/Linux:
source venv/bin/activate

3. Install dependencies
pip install -r requirements.txt

4. Add .env file with your keys

5. Run server
uvicorn app.main:app --reload

6. Open browser
http://127.0.0.1:8000
