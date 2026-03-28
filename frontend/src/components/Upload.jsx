import { useState } from "react";
import { uploadResumes } from "../api/api";

export default function upload ({onUploadSuccess}) {

    const [files,setFiles] = useState([])

    const handleUpload = async () => {
        await uploadResumes(files);
        alert("uploaded")
        onUploadSuccess()
    }

    return (
        <div>
            <h2>Upload Resumes</h2>
            <input
            type="file"
            multiple
            onChange={(e) => setFiles([...e.target.files])}
            />
            <button onClick={handleUpload}>Upload</button>
        </div>
    )
}