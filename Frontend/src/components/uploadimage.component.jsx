import React, { useState } from "react";

const UploadImage = () => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [preview, setPreview] = useState(null);
  const [uploadResult, setUploadResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [askNew, setAskNew] = useState(false); // New state for asking new prediction

  const handleFileChange = (event) => {
    const file = event.target.files[0];
    if (!file) return;

    setSelectedFile(file);
    setPreview(URL.createObjectURL(file));
    setUploadResult(null);
    setAskNew(false);
  };

  const handleCancelImage = () => {
    setSelectedFile(null);
    setPreview(null);
    setUploadResult(null);
    setAskNew(false);
  };

  const handleSubmit = async () => {
    if (!selectedFile) {
      alert("Please select an image first!");
      return;
    }

    const formData = new FormData();
    formData.append("file", selectedFile);

    try {
      setLoading(true);
      setUploadResult(null);

      const response = await fetch("http://localhost:8000/predict/upload/", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        throw new Error(`Server error: ${response.status}`);
      }

      const result = await response.json();
      setUploadResult({ name: result.class_name });
      setAskNew(true); // Ask for a new prediction
    } catch (error) {
      console.error("Error uploading image:", error);
      setUploadResult({ error: "Prediction failed. Please try again." });
      setAskNew(true);
    } finally {
      setLoading(false);
    }
  };

  const handleNewPrediction = () => {
    setSelectedFile(null);
    setPreview(null);
    setUploadResult(null);
    setAskNew(false);
  };

  return (
    <div className="mb-4 ">
      {!selectedFile && !askNew && (
        <input
          type="file"
          accept="image/*"
          onChange={handleFileChange}
          className="form-control mb-3 img-predict-input"
        />
      )}

      {preview && (
        <div className="mb-3 position-relative d-inline-block">
          <h5 className="text-white">Preview:</h5>
          <img
            src={preview}
            alt="Preview"
            className="img-fluid rounded shadow"
            style={{ maxHeight: "300px" }}
          />
          <button
            type="button"
            className="btn btn-danger btn-cancel-predict btn-sm position-absolute end-0"
            onClick={handleCancelImage}
          >
            ❌
          </button>
        </div>
      )}

      {selectedFile && !askNew && (
        <div>
          <button
            className="btn btn-primary mt-2"
            onClick={handleSubmit}
            disabled={loading}
          >
            {loading ? "Predicting..." : "Submit for Prediction"}
          </button>
        </div>
      )}

      {uploadResult && (
        <div
          className={`alert mt-3 ${
            uploadResult.error ? "alert-danger" : "alert-info"
          }`}
        >
          {uploadResult.error ? (
            <p>{uploadResult.error}</p>
          ) : (
            <p>
              <strong>Predicted Class:</strong> {uploadResult.name}
            </p>
          )}
        </div>
      )}

      {/* Ask for new prediction */}
      {askNew && (
        <div className="mt-3">
          <button className="btn btn-success" onClick={handleNewPrediction}>
            Predict Another Image
          </button>
        </div>
      )}
    </div>
  );
};

export default UploadImage;
