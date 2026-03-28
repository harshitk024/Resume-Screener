import re
import spacy
nlp = spacy.load("en_core_web_sm")

def extract_email(text):
    match = re.search(r"[a-zA-Z0-9+_.-]+@[a-zA-Z0-9.-]+", text)
    return match.group(0) if match else None

def extract_phone(text):
    match = re.search(r"\+?\d[\d -]{8,12}\d", text)
    return match.group(0) if match else None


def extract_name(text):
    lines = text.strip().split("\n")

    for line in lines[:5]:
        line = line.strip()

        if not line:
            continue

        if re.match(r"^[A-Za-z ]{3,50}$", line):
            words = line.split()

            if 1 < len(words) <= 3:
                return line

    doc = nlp(text[:1000])
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            return ent.text

    return None

def extract_skills(text):
    with open("technical_skills_list.txt") as f:
        skills_list = [line.strip().lower() for line in f]
    
    found = [skill for skill in skills_list if skill.lower() in text.lower()]
    return ", ".join(found)


def extract_sections(text):
    sections = {
        "education": "",
        "experience": "",
        "summary": "",
        "projects": ""
    }

    all_section_keywords = {
        "education": ["education", "academic", "qualifications", "academic background"],
        "experience": ["experience", "work experience", "professional experience", "employment history"],
        "skills": ["skills", "technical skills", "core competencies", "key skills"],
        "projects": ["projects", "personal projects", "academic projects"],
        "certifications": ["certifications", "certificates", "courses"],
        "summary": ["summary", "objective", "profile", "about me"],
        "awards": ["awards", "achievements", "honors"],
        "languages": ["languages"],
        "interests": ["interests", "hobbies"],
        "references": ["references"],
        "publications": ["publications"],
        "contact": ["contact", "contact information"],
    }

    lines = text.split("\n")
    current_section = None

    for line in lines:
        clean_line = line.strip()
        lower_line = clean_line.lower()

        if not clean_line:
            continue

        matched_section = None
        for section, keywords in all_section_keywords.items():
            if any(re.fullmatch(kw, lower_line) or re.search(rf"^\s*{re.escape(kw)}\s*[:\-]?\s*$", lower_line) for kw in keywords):
                matched_section = section
                break

        if matched_section:
            current_section = matched_section 
            continue

        if current_section in sections:
            sections[current_section] += clean_line + " "

    return {k: v.strip() for k, v in sections.items()}

def parse_resume(text):
    sections = extract_sections(text)

    return {
        "name": extract_name(text),
        "email": extract_email(text),
        "phone": extract_phone(text),
        "skills": extract_skills(text),
        "education": sections["education"],
        "experience": sections["experience"],
        "projects": sections["projects"],
        "summary": sections["summary"]
    }


