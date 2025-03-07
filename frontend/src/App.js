import React, { useRef, useEffect } from 'react';
import { useNavigate } from "react-router-dom";
import NavBar from './components/NavBar';
import UploadForm from './components/UploadForm';

function App() {
  const videoWindowRef = useRef(null);
  const navigate = useNavigate();

  useEffect(() => {
    // Ensure the video window is only opened once
    if (!videoWindowRef.current || videoWindowRef.current.closed) {
      videoWindowRef.current = window.open(
        "/video-display", // Opens the video route
        "VideoDisplayWindow",
        "width=1920,height=1080,toolbar=no,menubar=no,scrollbars=no,resizable=no"
      );

      // Ensure the window is brought to fullscreen (if allowed)
      setTimeout(() => {
        if (videoWindowRef.current) {
          videoWindowRef.current.focus();
          videoWindowRef.current.document.body.requestFullscreen?.();
        }
      }, 1000);
    }

    return () => {
      if (videoWindowRef.current) {
        videoWindowRef.current.close();
      }
    };
  }, []);

  return (
    <div>
      <NavBar />
      <main style={{ padding: "20px" }}>
        <UploadForm />
      </main>
    </div>
  );
}

export default App;
