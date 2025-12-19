import React, { useState, useRef } from "react";
import { API_ROUTES } from "../config/api";

type PredictionResult = {
  id: string;
  predicted_label: string;
  confidence: number; // already in %
};

const UploadSection = () => {
  const [file, setFile] = useState<File | null>(null);
  const [preview, setPreview] = useState<string | null>(null);
  const [result, setResult] = useState<PredictionResult | null>(null);
  const [loading, setLoading] = useState(false);

  const [showReportForm, setShowReportForm] = useState(false);
  const [userInfo, setUserInfo] = useState({ name: "", email: "" });

  const fileInputRef = useRef<HTMLInputElement>(null);

  // ---------------- FILE SELECT ----------------
  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const selected = e.target.files?.[0];
    if (!selected) return;

    if (preview) URL.revokeObjectURL(preview); // cleanup

    setFile(selected);
    setPreview(URL.createObjectURL(selected));
    setResult(null);
  };

  // ---------------- UPLOAD & PREDICT ----------------
  const handleUpload = async () => {
    if (!file) return alert("Please select an image");

    const formData = new FormData();
    formData.append("file", file);

    try {
      setLoading(true);

      const res = await fetch(API_ROUTES.UPLOAD, {
        method: "POST",
        body: formData,
      });

      const data = await res.json();
      if (!res.ok) throw new Error("Prediction failed");

      setResult({
        id: data.id,
        predicted_label: data.predicted_label,
        confidence: data.confidence, // already %
      });
    } catch (err) {
      console.error(err);
      alert("Prediction failed");
    } finally {
      setLoading(false);
    }
  };

  // ---------------- DOWNLOAD REPORT ----------------
  const handleDownloadReport = async () => {
    if (!userInfo.name || !userInfo.email)
      return alert("Please enter name and email");

    if (!result?.id) return alert("Prediction ID missing");

    const formData = new FormData();
    formData.append("prediction_id", result.id);
    formData.append("name", userInfo.name);
    formData.append("email", userInfo.email);

    try {
      const res = await fetch(API_ROUTES.DOWNLOAD_REPORT, {
        method: "POST",
        body: formData,
      });

      if (!res.ok) throw new Error("Report failed");

      const blob = await res.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = "xray_report.pdf";
      a.click();
      window.URL.revokeObjectURL(url);

      setShowReportForm(false);
    } catch (err) {
      console.error(err);
      alert("Failed to download report");
    }
  };

  // ---------------- CLEAN RESET ----------------
  const resetForm = () => {
    if (preview) URL.revokeObjectURL(preview);

    setFile(null);
    setPreview(null);
    setResult(null);
    setShowReportForm(false);
    setUserInfo({ name: "", email: "" });

    if (fileInputRef.current) {
      fileInputRef.current.value = "";
      fileInputRef.current.click(); // auto open picker
    }
  };

  return (
    <section className="py-16 px-6 bg-white text-center">
      <h2 className="text-3xl font-bold mb-4">Upload Chest X-ray</h2>

      <input
        type="file"
        accept="image/*"
        ref={fileInputRef}
        onChange={handleFileChange}
        className="hidden"
      />

      {/* SELECT IMAGE */}
      {!preview && !result && (
        <button
          className="bg-gray-200 px-6 py-2 rounded"
          onClick={() => fileInputRef.current?.click()}
        >
          Select Image
        </button>
      )}

      {/* PREVIEW + UPLOAD */}
      {preview && !result && (
        <div className="mt-6 flex flex-col items-center">
          <img
            src={preview}
            alt="preview"
            className="w-72 h-72 object-cover rounded shadow"
          />

          <button
            onClick={handleUpload}
            disabled={loading}
            className="mt-4 bg-blue-600 text-white px-6 py-2 rounded"
          >
            Upload & Predict
          </button>

          {loading && <p className="mt-3 text-blue-600">Processing...</p>}
        </div>
      )}

      {/* RESULT */}
      {result && (
        <div className="mt-8 flex flex-col items-center">
          <div className="bg-gray-100 p-4 rounded shadow max-w-md">
            <p className="text-lg font-bold text-blue-700">
              Prediction: {result.predicted_label}
            </p>
            <p className="text-gray-700">
              Confidence: {result.confidence.toFixed(2)}%
            </p>
          </div>

          <div className="mt-6 flex gap-4">
            <button
              className="bg-green-600 text-white px-6 py-2 rounded"
              onClick={() => setShowReportForm(true)}
            >
              Download Report
            </button>

            <button
              className="bg-gray-400 text-white px-6 py-2 rounded"
              onClick={resetForm}
            >
              Predict Another
            </button>
          </div>
        </div>
      )}

      {/* REPORT FORM */}
      {showReportForm && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
          <div className="bg-white p-6 rounded w-80">
            <h3 className="font-bold mb-4">Enter Details</h3>

            <input
              type="text"
              placeholder="Name"
              className="w-full border px-3 py-2 rounded mb-3"
              value={userInfo.name}
              onChange={(e) =>
                setUserInfo({ ...userInfo, name: e.target.value })
              }
            />

            <input
              type="email"
              placeholder="Email"
              className="w-full border px-3 py-2 rounded mb-3"
              value={userInfo.email}
              onChange={(e) =>
                setUserInfo({ ...userInfo, email: e.target.value })
              }
            />

            <div className="flex justify-end gap-3">
              <button
                className="bg-gray-300 px-4 py-2 rounded"
                onClick={() => setShowReportForm(false)}
              >
                Cancel
              </button>
              <button
                className="bg-green-600 text-white px-4 py-2 rounded"
                onClick={handleDownloadReport}
              >
                Download
              </button>
            </div>
          </div>
        </div>
      )}
    </section>
  );
};

export default UploadSection;
