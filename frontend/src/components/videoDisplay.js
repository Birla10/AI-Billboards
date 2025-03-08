import React, { useEffect, useState, useRef } from 'react';

const VideoDisplay = () => {
    const [videoUrls, setVideoUrls] = useState([]);
    const videoRef = useRef(null);
    const wsRef = useRef(null); // Keep WebSocket reference stable

    useEffect(() => {
        const url = process.env.REACT_APP_WEBSOCKET_URL;
        wsRef.current = new WebSocket(url);
        wsRef.current.onopen = () => {
            console.log("WebSocket Connected");
        };
        
        wsRef.current.onmessage = (event) => {
            const newUrl = event.data;
            console.log('Received video URL:', newUrl);
            setVideoUrls([newUrl]); // Replace previous URLs to play only the latest one
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
    }, []);

    useEffect(() => {
        // Request camera access
        navigator.mediaDevices.getUserMedia({ video: true })
            .then((stream) => {
                if (videoRef.current) {
                    videoRef.current.srcObject = stream;
                }
                console.log("Camera access granted!");
            })
            .catch((error) => {
                console.error("Camera access denied:", error);
            });
    }, []);

    useEffect(() => {
        if (videoUrls.length > 0 && videoRef.current) {
            console.log("Setting video source:", videoUrls[0]);  
    
            videoRef.current.src = videoUrls[0];
    
            const playPromise = videoRef.current.play();
    
            if (playPromise !== undefined) {
                playPromise
                    .then(() => {
                        console.log(" Video playback started successfully.");
                    })
                    .catch(error => {
                        console.error("Video playback blocked. Trying manual play:", error);
                        videoRef.current.muted = true;
                        videoRef.current.play();
                    });
            }
        }
    }, [videoUrls]);
    

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
