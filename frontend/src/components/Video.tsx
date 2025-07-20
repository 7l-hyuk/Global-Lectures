import React, { useRef, useState, useEffect } from 'react';
import { faPlay, faPause, faClosedCaptioning, faVolumeXmark, faVolumeLow, faVolumeHigh, faEllipsisVertical, faTimes } from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';

import { VideoProps, ScriptContentRowProps, SubtitleEntry } from '../types/components';
import styles from '../styles/Video.module.css';


const formatTime = (seconds: number): string => {
  const m = Math.floor(seconds / 60);
  const s = Math.floor(seconds % 60);
  return `${m}:${s.toString().padStart(2, '0')}`;
};


const LecturePlayer: React.FC<VideoProps> = ({videoPath, audioPath, scriptPath}) => {
  const [isPlaying, setIsPlaying] = useState(false);
  const [showSubtitle, setShowSubtitle] = useState(false);
  const [currentTime, setCurrentTime] = useState(0);
  const [duration, setDuration] = useState(0);
  const [volume, setVolume] = useState(0.8);
  const [showVolumeControl, setShowVolumeControl] = useState(false);
  const [scripts, setScripts] = useState<SubtitleEntry[]>([])

  const videoRef = useRef<HTMLVideoElement>(null);
  const audioRef = useRef<HTMLAudioElement>(null);


  const ScriptContentRow: React.FC<ScriptContentRowProps> = ({ script }) => {
    const video = videoRef.current;
    const audio = audioRef.current;
  
    return (
      <li 
        style={script.start <= currentTime && currentTime <= script.end ? {backgroundColor: "#505050"} : {}}
        onClick={() => {
          if (video && audio) {
            video.currentTime = script.start + 0.01;
            audio.currentTime = script.start + 0.01;
          }
        }}
      >
        <div>
        <span className={styles.ScriptContentRowTime}>{formatTime(script.start)}</span>
        </div>
        <div className={styles.ScriptContentRowText}>
          <span>{script.text}</span>
        </div>
      </li>
    );
  };

  const togglePlay = () => {
    const video = videoRef.current;
    const audio = audioRef.current;
  
    if (!video || !audio) return;

    if (video.paused) {
      video.play();
      audio.play();
      setIsPlaying(true);
    } else {
      video.pause();
      audio.pause();
      setIsPlaying(false);
    }
  };

  const handleTimeUpdate = () => {
    const video = videoRef.current;

    if (video) {
      setCurrentTime(video.currentTime);
    }
  };

  const handleLoadedMetadata = () => {
    const video = videoRef.current;

    if (video) {
      setDuration(video.duration);
    }
  };

  const handleVolumeChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const value = parseFloat(event.target.value);
    setVolume(value);

    if (audioRef.current) {
      audioRef.current.volume = value;
    }
  };

  const handleSeek = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = parseFloat(e.target.value);
    const video = videoRef.current;
    const audio = audioRef.current;
  
    if (video && audio) {
      video.currentTime = value;
      audio.currentTime = value;
    }
  };

  useEffect(() => {
    const audio = audioRef.current;

    if (!audio || !isPlaying) return;
    
    audio.load();
    audio.play().catch((e) => {
      console.warn("Autoplay blocked or failed:", e);
    });
  }, [audioPath]);

  useEffect(() => {
    const video = videoRef.current;
    const audio = audioRef.current;

    if (!video || !audio) return;

    const sync = () => {
      const drift = Math.abs(video.currentTime - audio.currentTime);
      if (drift > 0.2) {
        audio.currentTime = video.currentTime;
      }
    };

    video.addEventListener('timeupdate', sync);
    return () => video.removeEventListener('timeupdate', sync);
  }, []);

  useEffect(() => {
    fetch(scriptPath)
      .then(res => res.json())
      .then(setScripts)
      .catch(err => console.error(err));
  }, [scriptPath]);

  const progressPercent = (currentTime / duration) * 100;

  return (
    <div className={styles.container}>
      <div className={styles.content}>
        <video
          ref={videoRef}
          src={videoPath}
          className={styles.video}
          onTimeUpdate={handleTimeUpdate}
          onLoadedMetadata={handleLoadedMetadata}
        />
        <audio ref={audioRef} src={audioPath} />
        <div className={styles.controls}>
          <input
            type="range"
            min={0}
            max={duration}
            step={0.01}
            value={currentTime}
            onChange={handleSeek}
            className={styles.progress}
            style={{
              background: `linear-gradient(to right, #7d2020ff ${progressPercent}%, #333 ${progressPercent}%)`,
            }}
          />
          <div className={styles.controlButtonContainer}>
            <button onClick={togglePlay} className={styles.playButton}>
              <FontAwesomeIcon icon={isPlaying ? faPause : faPlay} />
            </button>
            <div className={styles.videoSettingControl}>
              <button onClick={() => {setShowVolumeControl(!showVolumeControl)}} className={styles.subtitleButton}>
                <FontAwesomeIcon icon={(volume == 0) ? faVolumeXmark : (volume < 0.5) ? faVolumeLow : faVolumeHigh} />
              </button>
              <input
                type="range"
                min={0}
                max={1}
                step={0.01}
                value={volume}
                onChange={handleVolumeChange}
                className={`${styles.volumeSlider} ${showVolumeControl ? styles.show : styles.hide}`}
                style={{
                  background: `linear-gradient(to right, #ffffff ${volume * 100}%, #333 ${volume * 100}%)`,
                }}
              />
              <button onClick={() => {setShowSubtitle(!showSubtitle)}} className={styles.subtitleButton}>
                <FontAwesomeIcon icon={faClosedCaptioning} />
              </button>
            </div>
          </div>
        </div>
      </div>
      {showSubtitle && (
        <div className={styles.ScriptContainer}>
          <div className={styles.Script}>
            <div className={styles.ScriptHeader}>
              <h1>Script</h1>
              <button onClick={() => {setShowSubtitle(false)}}><FontAwesomeIcon icon={faTimes} /></button>
            </div>
            <ul>
              {scripts.map((script, index) => (
                <ScriptContentRow script={script}/>
              ))}
            </ul>
          </div>
        </div>
      )}
    </div>
  );
};


export default LecturePlayer;
