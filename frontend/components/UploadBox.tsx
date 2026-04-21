"use client";

import { useRef, useState } from "react";
import { uploadPdfs } from "../lib/api";

type UploadBoxProps = {
  onUploadSuccess: () => void;
};

export default function UploadBox({ onUploadSuccess }: UploadBoxProps) {
  const fileInputRef = useRef<HTMLInputElement | null>(null);

  const [selectedFiles, setSelectedFiles] = useState<File[]>([]);
  const [uploading, setUploading] = useState(false);
  const [message, setMessage] = useState("");

  const handleUpload = async () => {
    if (selectedFiles.length === 0) {
      setMessage("Please select at least one PDF first.");
      return;
    }

    try {
      setUploading(true);
      setMessage("");

      const result = await uploadPdfs(selectedFiles);
      setMessage(
        `Uploaded ${result.files_count} file(s): ${result.uploaded_files.join(", ")}`
      );
      onUploadSuccess();
    } catch (error) {
      setMessage("Upload failed. Please try again.");
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="w-full rounded-2xl border border-gray-200 bg-white p-6 shadow-sm">
      <h2 className="mb-4 text-2xl font-semibold text-gray-900">Upload PDFs</h2>

      <input
        ref={fileInputRef}
        type="file"
        accept="application/pdf"
        multiple
        onChange={(e) => {
          const files = Array.from(e.target.files || []);
          setSelectedFiles(files);
          setMessage("");
        }}
        className="hidden"
      />

      <div className="rounded-xl border border-gray-200 bg-gray-50 p-4">
        <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
          <button
            type="button"
            onClick={() => fileInputRef.current?.click()}
            className="rounded-lg border border-gray-300 bg-white px-4 py-2 text-sm font-medium text-gray-900 hover:bg-gray-100"
          >
            Choose PDFs
          </button>

          <div className="text-sm text-gray-600 sm:text-right">
            {selectedFiles.length > 0 ? (
              <div className="space-y-1">
                {selectedFiles.map((file, index) => (
                  <p key={index} className="break-all">
                    {file.name}
                  </p>
                ))}
              </div>
            ) : (
              <p>No file selected</p>
            )}
          </div>
        </div>
      </div>

      <button
        onClick={handleUpload}
        disabled={uploading}
        className="mt-4 rounded-xl bg-black px-5 py-3 text-sm font-medium text-white transition hover:opacity-90 disabled:cursor-not-allowed disabled:opacity-50"
      >
        {uploading ? "Uploading..." : "Upload and Process"}
      </button>

      {message && (
        <p className="mt-4 text-sm text-gray-700">{message}</p>
      )}
    </div>
  );
}