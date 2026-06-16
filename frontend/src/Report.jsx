/**
 * Report Component
 * 
 * Displays the AI-generated inspection report with defect analysis,
 * severity classification, root causes, and recommendations.
 * Features collapsible/expandable box with toggle functionality.
 */

import { useState } from "react";

/**
 * @param {Object} props
 * @param {string} props.text - The generated inspection report text
 */
export default function Report({ text }) {
  const [isExpanded, setIsExpanded] = useState(true);
  const [isCopied, setIsCopied] = useState(false);

  if (!text) {
    return null; // Don't render if no report
  }

  /**
   * Toggles the report box expansion
   */
  function toggleExpand() {
    setIsExpanded(!isExpanded);
  }

  /**
   * Copies report text to clipboard
   */
  function copyToClipboard() {
    navigator.clipboard.writeText(text);
    setIsCopied(true);
    setTimeout(() => setIsCopied(false), 2000); // Reset after 2 seconds
  }

  /**
   * Downloads report as text file
   */
  function downloadReport() {
    const element = document.createElement("a");
    const file = new Blob([text], { type: "text/plain" });
    element.href = URL.createObjectURL(file);
    element.download = "inspection_report.txt";
    document.body.appendChild(element);
    element.click();
    document.body.removeChild(element);
  }

  return (
    <div
      className="card"
      style={{
        display: "flex",
        flexDirection: "column",
        transition: "all 0.3s ease",
      }}
    >
      {/* Header with Toggle and Actions */}
      <div
        style={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          marginBottom: isExpanded ? "16px" : "0",
          paddingBottom: "12px",
          borderBottom: isExpanded ? "1px solid rgba(148, 163, 184, 0.18)" : "none",
        }}
      >
        <div style={{ display: "flex", alignItems: "center", gap: "12px" }}>
          <h2 style={{ margin: 0, fontSize: "1.1rem" }}>Inspection Report</h2>
          <button
            onClick={toggleExpand}
            style={{
              width: "32px",
              height: "32px",
              padding: "0",
              background: "rgba(99, 102, 241, 0.15)",
              border: "1px solid rgba(148, 163, 184, 0.18)",
              borderRadius: "6px",
              color: "#93c5fd",
              cursor: "pointer",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              fontSize: "18px",
              transition: "all 0.2s ease",
              minWidth: "32px",
            }}
            title={isExpanded ? "Collapse" : "Expand"}
          >
            {isExpanded ? "−" : "+"}
          </button>
        </div>

        {/* Action Buttons */}
        {isExpanded && (
          <div style={{ display: "flex", gap: "8px" }}>
            <button
              onClick={copyToClipboard}
              style={{
                width: "auto",
                padding: "6px 12px",
                fontSize: "0.85rem",
                background: isCopied ? "rgba(34, 197, 94, 0.2)" : "rgba(99, 102, 241, 0.15)",
                border: `1px solid ${
                  isCopied ? "rgba(34, 197, 94, 0.5)" : "rgba(148, 163, 184, 0.18)"
                }`,
                color: isCopied ? "#22c55e" : "#cbd5e1",
                borderRadius: "6px",
                cursor: "pointer",
                transition: "all 0.2s ease",
              }}
              title="Copy to clipboard"
            >
              {isCopied ? "✓ Copied" : "Copy"}
            </button>
            <button
              onClick={downloadReport}
              style={{
                width: "auto",
                padding: "6px 12px",
                fontSize: "0.85rem",
                background: "rgba(99, 102, 241, 0.15)",
                border: "1px solid rgba(148, 163, 184, 0.18)",
                color: "#cbd5e1",
                borderRadius: "6px",
                cursor: "pointer",
                transition: "all 0.2s ease",
              }}
              title="Download report"
            >
              Download
            </button>
          </div>
        )}
      </div>

      {/* Report Content - Collapsible */}
      <div
        style={{
          maxHeight: isExpanded ? "600px" : "0",
          overflow: "hidden",
          transition: "max-height 0.3s ease, opacity 0.3s ease",
          opacity: isExpanded ? 1 : 0,
        }}
      >
        <pre
          style={{
            whiteSpace: "pre-wrap",
            wordWrap: "break-word",
            fontSize: "0.95rem",
            lineHeight: "1.6",
            color: "#cbd5e1",
            margin: 0,
            padding: "12px 0",
            overflowY: "auto",
            maxHeight: "500px",
          }}
        >
          {text}
        </pre>
      </div>

      {/* Collapsed State Indicator */}
      {!isExpanded && (
        <div
          style={{
            fontSize: "0.85rem",
            color: "#64748b",
            fontStyle: "italic",
            padding: "8px 0",
          }}
        >
          Report collapsed • Click + to expand
        </div>
      )}
    </div>
  );
}