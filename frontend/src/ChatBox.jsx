/**
 * ChatBox Component
 * 
 * Allows users to enter a text description or query about a construction defect.
 * Sends the prompt (along with an optional image path) to the RAG backend
 * for analysis and generates an expert inspection report.
 */

import { useState } from "react";
import { sendChat } from "./ragApi";

/**
 * @param {Object} props
 * @param {string} props.imgPath - Path to the uploaded inspection image
 * @param {Function} props.setReport - Callback to update parent with analysis result
 */
export default function ChatBox({ imgPath, setReport }) {
  const [prompt, setPrompt] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");

  /**
   * Handles form submission: sends prompt and image path to RAG system
   */
  async function handleSubmit() {
    if (!prompt.trim()) {
      setError("Please enter a description");
      return;
    }

    setIsLoading(true);
    setError("");

    try {
      const result = await sendChat(prompt, imgPath);
      setReport(result.text);
      setPrompt(""); // Clear input after successful submission
    } catch (err) {
      setError(err.message || "Failed to analyze. Please try again.");
      console.error("Analysis error:", err);
    } finally {
      setIsLoading(false);
    }
  }

  /**
   * Handles Enter key to submit the form
   */
  function handleKeyPress(e) {
    if (e.key === "Enter" && e.ctrlKey) {
      handleSubmit();
    }
  }

  return (
    <div className="panel">
      <label>
        <span className="section-title">Inspection Notes</span>
        <textarea
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder="Describe the defect or enter your query..."
          disabled={isLoading}
        />
      </label>

      {error && <p style={{ color: "#f87171" }}>{error}</p>}

      <button
        onClick={handleSubmit}
        disabled={isLoading || !prompt.trim()}
        style={{
          opacity: isLoading || !prompt.trim() ? 0.5 : 1,
          cursor: isLoading || !prompt.trim() ? "not-allowed" : "pointer",
        }}
      >
        {isLoading ? "Analyzing..." : "Analyze"}
      </button>
    </div>
  );
}