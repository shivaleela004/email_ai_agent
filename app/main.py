from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.ai_generator import generate_email
from app.email_sender import send_email

app = FastAPI(debug=True)

templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/send", response_class=HTMLResponse)
def send(
    request: Request,
    to_email: str = Form(...),
    receiver_name: str = Form(...),
    sender_name: str = Form(...),
    message: str = Form(...)
):
    try:
        email_content = generate_email(receiver_name, sender_name, message)

        if not email_content:
            raise ValueError("Gemini returned empty response")

        # Extract Subject
        subject = "AI Generated Email"
        lines = email_content.split("\n")

        clean_body_lines = []

        for line in lines:
            if line.lower().startswith("subject:"):
                subject = line.replace("Subject:", "").strip()
            elif line.lower().startswith("greeting:"):
                clean_body_lines.append(line.replace("Greeting:", "").strip())
            elif line.lower().startswith("body:"):
                continue
            elif line.lower().startswith("closing:"):
                continue
            else:
                clean_body_lines.append(line)

        clean_body = "\n".join(clean_body_lines).strip()

        send_email(to_email, subject, clean_body)

        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "success": "Email sent successfully!",
                "preview": clean_body
            }
        )

    except Exception as e:
        return templates.TemplateResponse(
            "index.html",
            {"request": request, "error": str(e)}
        )
