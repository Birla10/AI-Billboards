import React, { useState } from 'react';
import "../index.css";
import "./UploadForm.css";

const UploadForm = () => {
  const [file, setFile] = useState(null);
  const [keywords, setKeywords] = useState("");
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
   
    // Process the form data and call backend API
    const backendUrl = process.env.REACT_APP_BACKEND_URL;
    console.log("Backend URL:", backendUrl);
    const formData = new FormData();
    formData.append('file', file);
    formData.append('keywords', keywords);

    console.log(keywords);
    try {
      const response = await fetch(`${backendUrl}`, {
        method: 'POST',
        body: formData,
      });
      // Handle the response as needed
      const result = await response.json();
      console.log("API response:", result);
      if (response.ok) {
        setLoading(false);
        setMessage("File uploaded successfully!");
      } else {
        setLoading(false);
        setMessage("Failed to upload file!");
      }
    } catch (error) {
      console.error("Error during API call", error);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="upload-form">
      <div className="form-group">
        <label>Upload File:</label>
        <input type="file" onChange={(e) => setFile(e.target.files[0])} />
      </div>
      <div className="form-group">
        <label>Enter Keywords (comma separated):</label>
        <input 
          type="text" 
          value={keywords}
          onChange={(e) => setKeywords(e.target.value)}
        />
      </div>
      <button type="submit" className="submit-button" disabled={loading}>
        Submit
      </button>
      {loading && <p className="loading-text">Uploading and processing Ad...</p>}
      {message && <p className="message-text">{message}</p>}
    </form>
  );
};

export default UploadForm;