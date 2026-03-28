import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import spacy

nlp = spacy.load("en_core_web_sm")

with open("technical_skills_list.txt") as f:
    skills = [line.strip().lower() for line in f.readlines()]


def clean_text(text):
    if not text:
        return ""
    text = text.lower()
    text = text.replace(".js", " js")
    text = re.sub(r'[^a-z0-9\s]', ' ', text)
    return text


def extract_jd_skills(jd_text):
    jd_text = clean_text(jd_text)
    return [skill for skill in skills if skill in jd_text]


def calculate_similarity(text1, text2):
    text1 = clean_text(text1)
    text2 = clean_text(text2)

    if not text1.strip() or not text2.strip():
        return 0

    vectorizer = TfidfVectorizer(stop_words="english")
    tfidf_matrix = vectorizer.fit_transform([text1, text2])

    score = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
    return score


def experience_score(exp_text):
    match = re.findall(r'(\d+)', exp_text)
    years = max([int(x) for x in match], default=0)

    if years >= 5:
        return 1
    elif years >= 3:
        return 0.8
    elif years >= 1:
        return 0.6
    return 0.3



def calculate_score(resume, jd_text):

    jd_skills = extract_jd_skills(jd_text)
    resume_skills = [skill.strip().lower().replace(".js","") for skill in resume["skills"].split(",")] 
    print("JD Skills:", jd_skills)
    print("Resume Skills:", resume_skills)


    exact_matches = list(set(jd_skills) & set(resume_skills))
    print("exact: ",exact_matches)

    if jd_skills:
        skill_overlap = len(exact_matches) / len(jd_skills)
    else:
        skill_overlap = 0

    jd_skill_text = " ".join(jd_skills)
    resume_skill_text = " ".join(resume_skills)

    tfidf_skill = calculate_similarity(jd_skill_text, resume_skill_text)

    resume_text = resume.get("projects", "") + " " + resume.get("experience", "")
    text_score = calculate_similarity(resume_text, jd_text)

    exp_score = experience_score(resume.get("experience", ""))

    final_score = (
        0.6 * skill_overlap +
        0.2 * tfidf_skill +
        0.1 * text_score +
        0.1 * exp_score
    )

    final_score = round(final_score * 100, 2)

    print("Skill Overlap:", skill_overlap)
    print("TF-IDF Skill:", tfidf_skill)
    print("Text Score:", text_score)
    print("Experience Score:", exp_score)
    print("Final Score:", final_score)

    return final_score