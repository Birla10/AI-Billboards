import React from "react";
import ReactDOM from "react-dom/client";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import App from "./App";
import VideoDisplay from "./components/videoDisplay";

const root = ReactDOM.createRoot(document.getElementById("root"));

root.render(
  <React.StrictMode>
    <Router>
      <Routes>
        <Route path="/" element={<App />} />
        <Route path="/video-display" element={<VideoDisplay />} />
      </Routes>
    </Router>
  </React.StrictMode>
);
