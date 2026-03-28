from fastapi import FastAPI, UploadFile, File,Body
from fastapi.middleware.cors import CORSMiddleware
import pdfplumber
import docx
from typing import List
from db import SessionLocal, engine
from models import Base, Resume, JobDescription
from parser import parse_resume
from scorer import calculate_score

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)


def extract_text(file: UploadFile):
    if file.filename.endswith(".pdf"):
        with pdfplumber.open(file.file) as pdf:
            return "\n".join([page.extract_text() or "" for page in pdf.pages])

    elif file.filename.endswith(".docx"):
        doc = docx.Document(file.file)
        return "\n".join([para.text for para in doc.paragraphs])

    return ""

@app.get("/health")
def get_health():
    return {
        "message": "health"
    }



@app.post("/upload-resumes/")
async def upload_resumes(files: List[UploadFile] = File(...)):
    db = SessionLocal()
    results = []

    jd = db.query(JobDescription).first()

    if not jd:
        db.close()
        return {"error": "No JD set"}
    
    jd_text = jd.content

    print("JD text: ",jd_text)

    for file in files:
        text = extract_text(file)

        parsed_data = parse_resume(text)
        print(parsed_data)

        score = calculate_score(parsed_data, jd_text)

        print("Score: ",score)

        resume = Resume(
            name=parsed_data["name"],
            email=parsed_data["email"],
            phone=parsed_data["phone"],
            skills=parsed_data["skills"],
            education=parsed_data["education"],
            experience=parsed_data["experience"],
            score=score,
            raw_text=text
        )

        db.add(resume)

        results.append({
            "name": parsed_data["name"],
            "score": score
        })

    db.commit()
    db.close()

    print("results: ",results)

    return {
        "message": "Resumes processed successfully",
        "results": results
    }

@app.post("/set-jd/")
async def set_jd(data: dict = Body(...)):
    db = SessionLocal()

    title = data.get("title", "")
    content = data.get("jd", "")

    # 👉 Option 1: Replace existing JD (simple approach)
    db.query(JobDescription).delete()

    jd = JobDescription(
        title=title,
        content=content
    )

    db.add(jd)
    db.commit()
    db.refresh(jd)
    db.close()

    return {
        "message": "Job Description saved",
        "title": jd.title,
        "jd": jd.content
    }

@app.get("/get-jd/")
async def get_jd():
    db = SessionLocal()

    jd = db.query(JobDescription).first()

    db.close()

    if not jd:
        return {
            "title": "",
            "jd": ""
        }

    return {
        "title": jd.title,
        "jd": jd.content
    }

@app.get("/rankings/")
async def get_rankings():

    db = SessionLocal()
    
    resumes = db.query(Resume).all()
    print("Resumes: ",resumes)

    db.close()

    results = []

    for r in resumes:

        if r.score >= 75:
            status = "Shortlist"
        elif r.score >= 50:
            status = "Maybe"
        else:
            status = "Reject"

        results.append({
            "name": r.name,
            "email": r.email,
            "score": r.score,
            "status": status,
            "skills": r.skills,
            "experience": r.experience,
            "education": r.education
        })
    results.sort(key = lambda x: x["score"],reverse=True)
    return results


@app.delete("/delete-all/")
def delete_all():
    db = SessionLocal()
    
    db.query(Resume).delete()
    db.commit()
    db.close()

    return {"message": "All resumes deleted"}

