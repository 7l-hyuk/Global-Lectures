import React, { useEffect, useRef, useState } from 'react';
import axios from 'axios';

interface VideoPlayerProps {
  src: string;
  videoId: string;
}

interface SubtitleEntry {
  time: number;
  text: string;
}

const formatTime = (seconds: number): string => {
  const m = Math.floor(seconds / 60);
  const s = Math.floor(seconds % 60);
  return `${m}:${s.toString().padStart(2, '0')}`;
};

const VideoPlayer: React.FC<VideoPlayerProps> = ({ src, videoId }) => {
  const videoRef = useRef<HTMLVideoElement | null>(null);
  const [subtitles, setSubtitles] = useState<SubtitleEntry[]>([]);
  const [currentSubtitle, setCurrentSubtitle] = useState<string>("");

  useEffect(() => {
    axios.get<[number, string][]>(`http://localhost:8000/api/videos/subtitle/${videoId}`)
      .then(res => {
        const parsed = res.data.map(([time, text]) => ({ time, text }));
        setSubtitles(parsed);
      })
      .catch(console.error);
  }, [videoId]);

  useEffect(() => {
    const interval = setInterval(() => {
      if (videoRef.current) {
        const currentTime = videoRef.current.currentTime;
        const current = subtitles.reduce((acc, sub) => {
          return currentTime >= sub.time ? sub.text : acc;
        }, "");
        setCurrentSubtitle(current);
      }
    }, 500);
    return () => clearInterval(interval);
  }, [subtitles]);

  const handleSubtitleClick = (time: number) => {
    if (videoRef.current) {
      videoRef.current.currentTime = time;
      videoRef.current.play();
    }
  };

  return (
    <div style={{ display: 'flex', gap: '20px', marginTop: '20px', alignItems: 'flex-start' }}>
      <video ref={videoRef} src={src} controls style={{ width: '50%' }} />
      <div style={{ width: '50%', height: '100%', maxHeight: videoRef.current?.clientHeight ?? 'auto', border: '1px solid #ccc', padding: '10px', borderRadius: '5px', background: '#f9f9f9', display: 'flex', flexDirection: 'column' }}>
        <strong>자막</strong>
        <div style={{ marginTop: '10px', overflowY: 'auto', flexGrow: 1 }}>
          {subtitles.map((sub, index) => (
            <div
              key={index}
              onClick={() => handleSubtitleClick(sub.time)}
              style={{
                display: 'flex',
                alignItems: 'flex-start',
                cursor: 'pointer',
                padding: '5px 10px',
                backgroundColor: currentSubtitle === sub.text ? '#f2f2fa' : 'transparent'
              }}
            >
              <span style={{ fontSize: '12px', color: '#888', marginRight: '8px', minWidth: '40px' }}>{formatTime(sub.time)}</span>
              <span style={{ wordBreak: 'break-word' }}>{sub.text}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default VideoPlayer;
