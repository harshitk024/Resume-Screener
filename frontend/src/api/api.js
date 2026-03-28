const BASE_URL = "http://localhost:8000"

export const uploadResumes = async (files) => {

    const formData = new FormData()
    files.forEach(file => formData.append("files",file))

    const res = await fetch(`${BASE_URL}/upload-resumes`, {
        method: "POST",
        body: formData
    })
    return res.json()
}

export const setJD = async (title,jd) => {
    const res = await fetch(`${BASE_URL}/set-jd`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({title,jd})
    })
    return res.json()
}

export const getJD = async () => {
    const res = await fetch(`${BASE_URL}/get-jd`)
    return res.json()
}

export const getRankings = async () => {
    const res = await fetch(`${BASE_URL}/rankings/`)
    return res.json()
}
