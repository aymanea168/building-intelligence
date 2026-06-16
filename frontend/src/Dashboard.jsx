/**
 * Dashboard Component
 * 
 * Main layout component that orchestrates the inspection workflow.
 * Manages state for uploaded images and generated reports.
 * Coordinates communication between child components.
 */

import { useState } from "react";
import ImageUploader from "./ImageUploader";
import ChatBox from "./ChatBox";
import Report from "./Report";

export default function Dashboard() {
  const [imagePath, setImagePath] = useState("");
  const [report, setReport] = useState("");

  /**
   * Clears current analysis and allows new inspection
   */
  function handleNewAnalysis() {
    setImagePath("");
    setReport("");
  }

  return (
    <div className="page">
      <div className="shell">
        {/* Header */}
        <div className="hero">
          <p className="eyebrow">Construction Defect Analysis</p>
          <h1>Building Intelligence AI</h1>
          <p className="muted">
            Analyze building defects with AI-powered inspection reports.
            Upload an image and describe the defect to get expert analysis.
          </p>
        </div>

        {/* Main content layout */}
        <div className="layout">
          {/* Left column: Input components */}
          <div>
            <ImageUploader setImagePath={setImagePath} />

            {/* Show uploaded image path */}
            {imagePath && (
              <div className="card">
                <p style={{ margin: 0, fontSize: "0.9rem", color: "#cbd5e1" }}>
                  <strong>Image:</strong> {imagePath}
                </p>
              </div>
            )}

            <ChatBox imgPath={imagePath} setReport={setReport} />
          </div>

          {/* Right column: Report output */}
          <div>
            {report ? (
              <>
                <Report text={report} />
                <button
                  onClick={handleNewAnalysis}
                  style={{
                    marginTop: "16px",
                    width: "100%",
                    padding: "12px",
                    background: "rgba(100, 100, 100, 0.3)",
                    border: "1px solid rgba(148, 163, 184, 0.18)",
                    borderRadius: "8px",
                    color: "#cbd5e1",
                    cursor: "pointer",
                  }}
                >
                  New Analysis
                </button>
              </>
            ) : (
              <div
                className="card"
                style={{
                  minHeight: "300px",
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                  textAlign: "center",
                }}
              >
                <p style={{ color: "#64748b" }}>
                  Upload an image and describe the defect to see the analysis report
                </p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}