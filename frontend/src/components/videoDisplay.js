import React, { useEffect, useState, useRef } from 'react';

const VideoDisplay = () => {
    const [videoUrls, setVideoUrls] = useState([]); // Queue of videos
    const videoRef = useRef(null);
    const wsRef = useRef(null); // WebSocket reference

    useEffect(() => {
        const url = process.env.REACT_APP_WEBSOCKET_URL;
        wsRef.current = new WebSocket(url);

        wsRef.current.onopen = () => {
            console.log("WebSocket Connected");
        };

        wsRef.current.onmessage = (event) => {
            const newUrl = event.data;
            console.log("Received video URL:", newUrl);

            if (newUrl && !videoUrls.includes(newUrl) && newUrl.startsWith("https")) {
                setVideoUrls(prevUrls => [...prevUrls, newUrl]); // Append new video URL
            } else {
                console.warn("Ignored duplicate or invalid URL:", newUrl);
            }
        };

        wsRef.current.onerror = (error) => {
            console.error("WebSocket Error: ", error);
        };

        wsRef.current.onclose = () => {
            console.log("WebSocket Disconnected");
        };

        return () => {
            if (wsRef.current) {
                wsRef.current.close();
            }
        };
    }, []); // WebSocket setup runs once on mount

    useEffect(() => {
        if (videoUrls.length > 0 && videoRef.current) {
            const videoElement = videoRef.current;
            videoElement.src = videoUrls[videoUrls.length - 1]; // Always play the latest video

            videoElement.oncanplay = () => {
                console.log("Video ready to play:", videoElement.src);

                const playPromise = videoElement.play();

                if (playPromise !== undefined) {
                    playPromise
                        .then(() => {
                            console.log("Video playback started successfully.");
                        })
                        .catch(error => {
                            if (error.name !== "NotAllowedError" && error.name !== "AbortError") {
                                console.error("Unexpected video playback error:", error);
                            }
                            // Retry with mute
                            videoElement.muted = true;
                            videoElement.play().catch(err => console.error("Retry play failed:", err));
                        });
                }
            };
        }
    }, [videoUrls]); // Dependency fixed

    return (
        <div style={{ width: '100vw', height: '100vh', overflow: 'hidden', background: 'black' }}>
            {videoUrls.length > 0 ? (
                <video
                    ref={videoRef}
                    style={{ width: '100%', height: '100%' }}
                    controls
                    autoPlay
                    muted
                    playsInline
                />
            ) : (
                <p style={{ color: 'white', textAlign: 'center', paddingTop: '20px' }}>
                    Waiting for video stream...
                </p>
            )}
        </div>
    );
};

export default VideoDisplay;
