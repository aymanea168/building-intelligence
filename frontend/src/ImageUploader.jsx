/**
 * ImageUploader Component
 * 
 * Allows users to select and upload inspection images.
 * Validates file type and size before uploading to the server.
 * Provides visual feedback during the upload process.
 */

import { useState } from "react";
import { uploadImage } from "./ragApi";

const ALLOWED_FILE_TYPES = ["image/jpeg", "image/png", "image/jpg"];
const MAX_FILE_SIZE_MB = 10;

/**
 * @param {Object} props
 * @param {Function} props.setImagePath - Callback to update parent with uploaded image path
 */
export default function ImageUploader({ setImagePath }) {
  const [file, setFile] = useState(null);
  const [preview, setPreview] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");

  /**
   * Validates file before upload
   * Checks: file type, file size
   */
  function validateFile(selectedFile) {
    if (!selectedFile) return false;

    // Check file type
    if (!ALLOWED_FILE_TYPES.includes(selectedFile.type)) {
      setError("Only JPEG and PNG files are allowed");
      return false;
    }

    // Check file size
    if (selectedFile.size > MAX_FILE_SIZE_MB * 1024 * 1024) {
      setError(`File must be smaller than ${MAX_FILE_SIZE_MB}MB`);
      return false;
    }

    return true;
  }

  /**
   * Handles file selection from input
   */
  function handleFileSelect(e) {
    const selectedFile = e.target.files?.[0];
    setError("");

    if (!selectedFile) return;

    if (validateFile(selectedFile)) {
      setFile(selectedFile);
      // Create preview
      const reader = new FileReader();
      reader.onload = (event) => {
        setPreview(event.target.result);
      };
      reader.readAsDataURL(selectedFile);
    } else {
      setFile(null);
      setPreview(null);
    }
  }

  /**
   * Handles image upload to the server
   */
  async function handleUpload() {
    if (!file) {
      setError("Please select an image first");
      return;
    }

    setIsLoading(true);
    setError("");

    try {
      const result = await uploadImage(file);
      setImagePath(result.path);
      // Keep preview visible after upload
    } catch (err) {
      setError(err.message || "Upload failed. Please try again.");
      console.error("Upload error:", err);
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <div className="panel">
      <label>
        <span className="section-title">Upload Inspection Image</span>
        <input
          type="file"
          accept="image/jpeg,image/png,image/jpg"
          onChange={handleFileSelect}
          disabled={isLoading}
        />
      </label>

      {/* Image preview */}
      {preview && (
        <div
          style={{
            marginTop: "12px",
            borderRadius: "8px",
            overflow: "hidden",
            maxHeight: "200px",
          }}
        >
          <img
            src={preview}
            alt="Preview"
            style={{ width: "100%", height: "auto", display: "block" }}
          />
        </div>
      )}

      {/* Error message */}
      {error && <p style={{ color: "#f87171", fontSize: "0.9rem" }}>{error}</p>}

      {/* File info */}
      {file && (
        <p style={{ color: "#cbd5e1", fontSize: "0.9rem" }}>
          {file.name} ({(file.size / 1024 / 1024).toFixed(2)}MB)
        </p>
      )}

      <button onClick={handleUpload} disabled={!file || isLoading}>
        {isLoading ? "Uploading..." : "Upload Image"}
      </button>
    </div>
  );
}