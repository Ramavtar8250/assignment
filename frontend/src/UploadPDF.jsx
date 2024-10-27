import React, { useState } from "react";
import axios from "axios";

const UploadPDF = ({ setFilename }) => {
  const [file, setFile] = useState(null);

  const handleUpload = async (e) => {
    e.preventDefault();
    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await axios.post("http://localhost:8000/upload_pdf/", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      setFilename(response.data.filename);
    } catch (error) {
      console.error("File upload error:", error);
    }
  };

  return (
    <form onSubmit={handleUpload}>
      <input type="file" onChange={(e) => setFile(e.target.files[0])} />
      <button type="submit">Upload PDF</button>
    </form>
  );
};

export default UploadPDF;
