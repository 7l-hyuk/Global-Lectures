import React, { useEffect, useRef, useState } from 'react';
import { getSubtitle } from '../api/video';
import styles from "../css/Video.module.css"


interface VideoPlayerProps {
  presignedUrl: string;
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

const VideoPlayer: React.FC<VideoPlayerProps> = ({ presignedUrl, videoId }) => {
  const videoRef = useRef<HTMLVideoElement | null>(null);
  const [subtitles, setSubtitles] = useState<SubtitleEntry[]>([]);
  const [currentTimeIndex, setCurrentTimeIndex] = useState<number | null>(null);
  useEffect(() => {
    getSubtitle(videoId)
      .then(res => {
        setSubtitles(res.data);

      })
      .catch(console.error);
  }, [videoId]);

  useEffect(() => {
    const interval = setInterval(() => {
      if (videoRef.current) {
        const currentTime = videoRef.current.currentTime;
        let latestIndex: number | null = null;

        for (let i = 0; i < subtitles.length; i++) {
          if (currentTime >= subtitles[i].time) {
            latestIndex = i;
          } else {
            break;
          }
        }

        setCurrentTimeIndex(latestIndex);
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
      <video ref={videoRef} src={presignedUrl} controls style={{ width: '50%' }} />
      <div
        style={{
          width: '50%',
          maxHeight: videoRef.current?.clientHeight ?? 'auto',
          border: '1px solid #ccc',
          padding: '10px',
          borderRadius: '5px',
          background: '#f9f9f9',
          display: 'flex',
          flexDirection: 'column'
        }}
      >
        <strong>자막</strong>
        <div style={{ marginTop: '10px', overflowY: 'auto', flexGrow: 1 }}>
          {subtitles.map((sub, index) => (
            <div
              key={index}
              className={styles.subtitle}
              onClick={() => handleSubtitleClick(sub.time)}
              style={{
                backgroundColor: currentTimeIndex === index ? '#e2e2e2' : 'transparent'
              }}
            >
              <span
                style={{
                  fontSize: '12px',
                  color: '#888',
                  marginRight: '8px',
                  minWidth: '40px'
                }}
              >
                {formatTime(sub.time)}
              </span>
              <span style={{ wordBreak: 'break-word' }}>{sub.text}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default VideoPlayer;
