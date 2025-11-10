import React, { useState, useRef } from "react";

type PredictionResult = {
  class_name: string;
  confidence?: number;
};

const UploadSection = () => {
  const [file, setFile] = useState<File | null>(null);
  const [preview, setPreview] = useState<string | null>(null);
  const [result, setResult] = useState<PredictionResult | null>(null);
  const [loading, setLoading] = useState(false);

  const fileInputRef = useRef<HTMLInputElement>(null);

  // Handle file selection
  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const selected = e.target.files?.[0];
    if (selected) {
      setFile(selected);
      setPreview(URL.createObjectURL(selected));
      setResult(null);
    }
  };

  // Upload to API and get prediction
  const handleUpload = async () => {
    if (!file) return alert("Please select an image first!");

    const formData = new FormData();
    formData.append("file", file);

    try {
      setLoading(true);
      const res = await fetch(
        "https://disease-detection-api-rutn.onrender.com/predict/upload/",
        {
          method: "POST",
          body: formData,
        }
      );

      if (!res.ok) throw new Error(`Server Error: ${res.status}`);
      const data: PredictionResult = await res.json();
      setResult(data);
    } catch (err) {
      console.error(err);
      setResult({ class_name: "Prediction failed. Try again." });
    } finally {
      setLoading(false);
    }
  };

  // Reset & open file picker for a new prediction
  const handlePredictAnother = () => {
    setFile(null);
    setPreview(null);
    setResult(null);
    setLoading(false);
    fileInputRef.current?.click(); // Open file picker
  };

  return (
    <section id="upload" className="py-16 px-6 bg-white text-center">
      <h2 className="text-3xl font-bold mb-4">Upload Your X-ray</h2>
      <p className="max-w-2xl mx-auto text-gray-600 mb-6">
        Upload a chest X-ray image to get an instant AI-based disease prediction.
      </p>

      {/* Hidden file input */}
      <input
        type="file"
        accept="image/*"
        onChange={handleFileChange}
        ref={fileInputRef}
        className="hidden"
      />

      {/* Show preview & buttons if a file is selected */}
      {preview && !result && (
        <div className="mt-6 flex flex-col items-center">
          <img
            src={preview}
            alt="Preview"
            className="w-72 h-72 object-cover rounded-lg shadow-md"
          />

          <div className="mt-4 flex gap-3">
            <button
              className="bg-blue-600 text-white px-6 py-2 rounded hover:bg-blue-700 transition disabled:opacity-50"
              onClick={handleUpload}
              disabled={loading}
            >
              Upload & Predict
            </button>

            <button
              className="bg-red-500 text-white px-6 py-2 rounded hover:bg-red-600 transition disabled:opacity-50"
              onClick={handlePredictAnother}
              disabled={loading}
            >
              Cancel
            </button>
          </div>

          {loading && (
            <div className="mt-4 flex items-center gap-3">
              <div className="w-10 h-10 border-4 border-blue-300 border-t-blue-600 rounded-full animate-spin"></div>
              <span className="text-blue-700 font-semibold">Predicting...</span>
            </div>
          )}
        </div>
      )}

      {/* Show result */}
      {result && (
        <div className="mt-8 flex flex-col items-center">
          <div className="bg-gray-100 p-4 rounded-lg max-w-md shadow transition-opacity duration-500 opacity-100">
            <p className="font-semibold text-blue-700 text-lg">
              Prediction: {result.class_name}
            </p>
            {result.confidence !== undefined && (
              <p className="text-gray-700 mt-1">
                Confidence: {(result.confidence * 100).toFixed(2)}%
              </p>
            )}
          </div>

          <button
            className="mt-4 bg-green-600 text-white px-6 py-2 rounded hover:bg-green-700 transition"
            onClick={handlePredictAnother}
            disabled={loading}
          >
            Predict Another
          </button>
        </div>
      )}

      {/* Show file picker if no preview yet */}
      {!preview && !result && (
        <button
          className="bg-gray-200 px-6 py-2 rounded hover:bg-gray-300 transition"
          onClick={() => fileInputRef.current?.click()}
        >
          Select Image
        </button>
      )}
    </section>
  );
};

export default UploadSection;
