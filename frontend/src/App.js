import React, { useRef, useEffect, useState } from 'react';
import NavBar from './components/NavBar';
import UploadForm from './components/UploadForm';

function App() {
  const videoWindowRef = useRef(null);
  const [fullscreenRequested, setFullscreenRequested] = useState(false);

  useEffect(() => {
    if (!videoWindowRef.current || videoWindowRef.current.closed) {
      videoWindowRef.current = window.open(
        "/video-display",
        "VideoDisplayWindow",
        "width=1920,height=1080,toolbar=no,menubar=no,scrollbars=no,resizable=no"
      );

      setTimeout(() => {
        if (videoWindowRef.current) {
          videoWindowRef.current.focus();
        }
      }, 1000);
    }

    return () => {
      if (videoWindowRef.current) {
        videoWindowRef.current.close();
      }
    };
  }, []);

  const requestFullscreen = () => {
    if (videoWindowRef.current) {
      videoWindowRef.current.document.documentElement.requestFullscreen?.();
      setFullscreenRequested(true);
    }
  };

  return (
    <div onClick={!fullscreenRequested ? requestFullscreen : null} style={{ height: "100vh", cursor: "pointer" }}>
      <NavBar />
      <main style={{ padding: "20px" }}>
        <UploadForm />
        {!fullscreenRequested && (
          <p style={{ textAlign: "center", color: "red" }}>
            Click anywhere to enable fullscreen mode.
          </p>
        )}
      </main>
    </div>
  );
}

export default App;
