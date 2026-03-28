import { useState } from "react";

export default function Dashboard({ data }) {
  const [activeId, setActiveId] = useState(null);

  const toggleCandidate = (id) => {
    setActiveId((prev) => (prev === id ? null : id));
  };

  if (!data || data.length === 0) {
    return <p>No candidates available</p>;
  }

  return (
    <div>
      <h2>Candidate Rankings</h2>

      {data.map((candidate) => {
        const isActive = activeId === candidate.id;

        return (
          <div
            key={candidate.id}
            style={{
              border: "1px solid gray",
              margin: "10px",
              padding: "10px",
              background: isActive ? "#eef" : "white",
              transition: "0.2s",
            }}
          >
            {/* 🔹 Clickable Summary */}
            <div
              onClick={() => toggleCandidate(candidate.id)}
              style={{ cursor: "pointer" }}
            >
              <h3>{candidate.name || "Unknown"}</h3>
              <p>Score: {candidate.score ?? 0}%</p>
              <p>Status: {candidate.status || "N/A"}</p>

              {/* Preview skills */}
              <p>
                Skills:{" "}
                {candidate.skills
                  ? candidate.skills.slice(0, 60) + "..."
                  : "N/A"}
              </p>

              <p style={{ fontSize: "12px", color: "gray" }}>
                {isActive ? "Click to collapse" : "Click to expand"}
              </p>
            </div>

            {/* 🔥 Expanded Section */}
            {isActive && (
              <div
                style={{
                  marginTop: "10px",
                  padding: "10px",
                  borderTop: "1px solid #ccc",
                  background: "#f9f9f9",
                }}
              >
                <p><strong>Email:</strong> {candidate.email || "N/A"}</p>
                <p><strong>Phone:</strong> {candidate.phone || "N/A"}</p>

                <p>
                  <strong>Skills (Full):</strong>{" "}
                  {candidate.skills || "N/A"}
                </p>

                <p>
                  <strong>Education:</strong>{" "}
                  {candidate.education || "N/A"}
                </p>

                <p>
                  <strong>Experience:</strong>{" "}
                  {candidate.experience || "N/A"}
                </p>

                <button
                  onClick={() => setActiveId(null)}
                  style={{
                    marginTop: "10px",
                    padding: "5px 10px",
                    cursor: "pointer",
                  }}
                >
                  Close
                </button>
              </div>
            )}
          </div>
        );
      })}
    </div>
  );
}