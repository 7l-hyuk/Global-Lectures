import React, { useEffect, useRef, useState } from 'react';
import { getMediaBundle } from '../api/video';
import styles from "../css/Video.module.css";

interface SubtitleEntry {
  time: number;
  text: string;
}

interface VideoPlayerProps {
  presignedUrl: string;
  videoId: string;
  supportedLang: string[];
}

const langLabels: Record<string, string> = {
  ko: "Korean",
  en: "English",
};

const formatTime = (seconds: number): string => {
  const m = Math.floor(seconds / 60);
  const s = Math.floor(seconds % 60);
  return `${m}:${s.toString().padStart(2, '0')}`;
};

const VideoPlayer: React.FC<VideoPlayerProps> = ({ presignedUrl, videoId, supportedLang }) => {
  const videoRef = useRef<HTMLVideoElement | null>(null);
  const audioRef = useRef<HTMLAudioElement | null>(null);

  const [subtitles, setSubtitles] = useState<SubtitleEntry[]>([]);
  const [currentTimeIndex, setCurrentTimeIndex] = useState<number | null>(null);
  const [selectedLang, setSelectedLang] = useState<string>(supportedLang[0]);
  const [audioUrl, setAudioUrl] = useState<string | null>(null);

  useEffect(() => {
    const loadMedia = async () => {
      try {
        const res = await getMediaBundle(videoId, selectedLang);
        setAudioUrl(res.data.audio);
        setSubtitles(res.data.subtitle);

        if (audioRef.current) {
          audioRef.current.load();
        }
      } catch (err) {
        console.error('Failed to load media bundle:', err);
      }
    };

    loadMedia();
  }, [selectedLang, videoId]);

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

  useEffect(() => {
    const syncPlayback = () => {
      if (videoRef.current && audioRef.current) {
        if (videoRef.current.paused) {
          audioRef.current.pause();
        } else {
          audioRef.current.currentTime = videoRef.current.currentTime;
          const playPromise = audioRef.current.play();
          if (playPromise !== undefined) {
            playPromise.catch((error) => {
              console.warn('Audio play interrupted:', error);
            });
          }
        }
      }
    };

    if (videoRef.current) {
      videoRef.current.addEventListener('play', syncPlayback);
      videoRef.current.addEventListener('pause', syncPlayback);
    }

    return () => {
      if (videoRef.current) {
        videoRef.current.removeEventListener('play', syncPlayback);
        videoRef.current.removeEventListener('pause', syncPlayback);
      }
    };
  }, [audioUrl]);

  const handleLanguageChange = async (lang: string) => {
    if (!videoRef.current) return;
    const currentTime = videoRef.current.currentTime;

    try {
      setSelectedLang(lang);
      const res = await getMediaBundle(videoId, lang);
      setAudioUrl(res.data.audio);
      setSubtitles(res.data.subtitle);

      setTimeout(() => {
        if (audioRef.current) {
          audioRef.current.currentTime = currentTime;
          if (!videoRef.current?.paused) {
            const playPromise = audioRef.current.play();
            if (playPromise !== undefined) {
              playPromise.catch((error) => {
                console.warn('Audio play interrupted:', error);
              });
            }
          }
        }
      }, 200);
    } catch (err) {
      console.error('Failed to switch language:', err);
    }
  };

  const handleSubtitleClick = (time: number) => {
    if (videoRef.current && audioRef.current) {
      videoRef.current.currentTime = time;
      audioRef.current.currentTime = time;
      videoRef.current.play();
      const playPromise = audioRef.current.play();
      if (playPromise !== undefined) {
        playPromise.catch((error) => {
          console.warn('Audio play interrupted:', error);
        });
      }
    }
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '16px', fontFamily: 'sans-serif' }}>
      <div style={{ display: 'flex', gap: '20px', alignItems: 'flex-start', minHeight: '300px', maxHeight: '500px', height: '100%', width: '100%' }}>
        <video ref={videoRef} src={presignedUrl} muted controls style={{ width: '50%', height: '100%', borderRadius: '12px', boxShadow: '0 4px 12px rgba(0,0,0,0.1)', objectFit: 'cover' }} />
        {audioUrl && (
          <audio ref={audioRef} key={audioUrl} src={audioUrl} />
        )}

        <div
          style={{ 
            width: '50%', 
            height: '100%',
            border: '1px solid #ddd',
            padding: '16px',
            borderRadius: '12px',
            maxHeight: '250px',
            background: '#ffffff',
            display: 'flex',
            flexDirection: 'column',
            boxShadow: '0 4px 12px rgba(0,0,0,0.05)',
          }}
        >
          <strong style={{ fontSize: '16px', marginBottom: '8px' }}>Subtitles ({langLabels[selectedLang] ?? selectedLang.toUpperCase()})</strong>
          <div key={selectedLang} style={{ overflowY: 'auto', flexGrow: 1, height: '100%' }}>
            {subtitles.map((sub, index) => (
              <div
                key={index}
                onClick={() => handleSubtitleClick(sub.time)}
                className={styles.subtitle}
                style={{
                  backgroundColor: currentTimeIndex === index ? '#dbdbdb' : 'transparent',
                  cursor: 'pointer',
                  padding: '6px 0',
                  transition: 'background 0.2s ease-in-out',
                }}
              >
                <span style={{ fontSize: '12px', color: '#888', marginRight: '8px', minWidth: '40px' }}>
                  {formatTime(sub.time)}
                </span>
                <span style={{ wordBreak: 'break-word', fontSize: '14px' }}>{sub.text}</span>
              </div>
            ))}
          </div>
        </div>
      </div>
      <div className={styles.ButtonContainer} style={{flexDirection: "row", justifyContent: "space-between"}}>
        <div  style={{ display: 'flex', gap: '8px' }}>
          {supportedLang.map((lang) => (
            <button
              className={styles.Button}
              key={lang}
              onClick={() => handleLanguageChange(lang)}
              style={{
                backgroundColor: selectedLang === lang ? "#b53836" : '#ccc',
                borderColor: selectedLang === lang ? "#b53836" : '#ccc'
              }}
            >
              {langLabels[lang] ?? lang.toUpperCase()}
            </button>
          ))}
        </div>
        <div style={{ display: 'flex', gap: '8px' }}>
          <button
            className={styles.Button}
            style={{backgroundColor: "#28a745", borderColor: "#28a745"}}
            onClick={() => {}}
          >
            Convert
          </button>
        </div>
      </div>
    </div>
  );
};

export default VideoPlayer;
