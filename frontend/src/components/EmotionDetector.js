// import React, { useEffect, useRef, useState } from "react";
// import * as faceapi from "face-api.js";

// const EmotionDetector = () => {
//     const videoRef = useRef(null);
//     const intervalRef = useRef(null); // ✅ Store interval reference
//     const [emotion, setEmotion] = useState("Detecting...");

//     useEffect(() => {
//         const loadModels = async () => {
//             await faceapi.nets.tinyFaceDetector.loadFromUri("/models");
//             await faceapi.nets.faceExpressionNet.loadFromUri("/models");
//             console.log("✅ Face-API.js models loaded");
//         };

//         const startVideo = async () => {
//             try {
//                 const stream = await navigator.mediaDevices.getUserMedia({ video: true });
//                 if (videoRef.current) {
//                     videoRef.current.srcObject = stream;
//                 }
//                 console.log("🎥 Camera access granted");
//             } catch (err) {
//                 console.error("❌ Camera access denied:", err);
//             }
//         };

//         // Load models first, then start video
//         loadModels().then(startVideo);
//     }, []);

//     useEffect(() => {
//         const detectEmotions = async () => {
//             if (!videoRef.current) return;

//             const detections = await faceapi.detectSingleFace(videoRef.current, new faceapi.TinyFaceDetectorOptions())
//                 .withFaceExpressions();

//             if (detections && detections.expressions) {
//                 const detectedEmotion = Object.entries(detections.expressions)
//                     .sort((a, b) => b[1] - a[1])[0][0]; // Get the most dominant emotion
//                 setEmotion(detectedEmotion);
//                 console.log(`😊 Detected Emotion: ${detectedEmotion}`);
//             }
//         };

//         // ✅ Clear existing interval before setting a new one
//         if (intervalRef.current) clearInterval(intervalRef.current);

//         // ✅ Run emotion detection at consistent 2-second intervals
//         intervalRef.current = setInterval(() => {
//             detectEmotions();
//         }, 2000);

//         return () => clearInterval(intervalRef.current); // ✅ Cleanup on unmount
//     }, []);

//     return (
//         <div>
//             {/* Hidden video feed */}
//             <video ref={videoRef} autoPlay muted playsInline style={{ display: "none" }} />

//             {/* Only show detected emotion (No video visible) */}
//             <h3>Detected Emotion: {emotion}</h3>
//         </div>
//     );
// };

// export default EmotionDetector;
