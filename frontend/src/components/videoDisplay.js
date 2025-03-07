import React, { useEffect, useState, useRef } from 'react';

const VideoDisplay = () => {
    const [videoUrls, setVideoUrls] = useState([]);
    const videoRef = useRef(null);
    const wsRef = useRef(null); // Keep WebSocket reference stable

    useEffect(() => {
        var url = process.env.WEBSOCKET_URL;
        wsRef.current = new WebSocket(url); 

        wsRef.current.onmessage = (event) => {
            const newUrl = event.data;
            console.log('Received video URL:', newUrl);

            setVideoUrls((prevUrls) => [...prevUrls, newUrl]);
        };

        wsRef.current.onerror = (error) => {
            console.error("WebSocket Error: ", error);
        };

        wsRef.current.onclose = () => {
            console.log("WebSocket Disconnected");
        };

        return () => {
            wsRef.current.close();
        };
    }, []);

    useEffect(() => {
        if (videoUrls.length > 0 && videoRef.current) {
            videoRef.current.src = videoUrls[0];
            videoRef.current.play().catch(error => console.error("Video playback failed:", error));
        }
    }, [videoUrls]);

    const handleVideoEnd = () => {
        setVideoUrls((prevUrls) => prevUrls.slice(1)); // Remove current video and move to the next
    };

    return (
        <div style={{ width: '100vw', height: '100vh', overflow: 'hidden', background: 'black' }}>
            {videoUrls.length > 0 ? (
                <video
                    ref={videoRef}
                    style={{ width: '100%', height: '100%' }}
                    onEnded={handleVideoEnd}
                    controls
                    autoPlay
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
