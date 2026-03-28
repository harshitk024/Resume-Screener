import { useState, useEffect } from "react";
import { setJD, getJD } from "../api/api";

export default function JDInput() {
  const [title, setTitle] = useState("");
  const [jd, setJDText] = useState("");

  useEffect(() => {
    fetchJD();
  }, []);

  const fetchJD = async () => {
    try {
      const data = await getJD();
      if (data) {
        setTitle(data.title || "");
        setJDText(data.jd || "");
      }
    } catch (err) {
      console.error("Error fetching JD:", err);
    }
  };

  const handleSubmit = async () => {
    await setJD(title, jd);
    alert("JD submitted");
  };

  return (
    <div>
      <h2>Job Description</h2>

      <input
        type="text"
        placeholder="Enter Job Title"
        value={title}
        onChange={(e) => setTitle(e.target.value)}
        style={{ width: "300px", marginBottom: "10px" }}
      />

      <br />

      <textarea
        rows="6"
        cols="50"
        value={jd}
        onChange={(e) => setJDText(e.target.value)}
      />

      <br />

      <button onClick={handleSubmit}>Submit JD</button>
    </div>
  );
}