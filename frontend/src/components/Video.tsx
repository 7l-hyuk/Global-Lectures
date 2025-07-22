import React, { useRef, useState, useEffect } from 'react';
import { faPlay, faPause, faClosedCaptioning, faVolumeXmark, faVolumeLow, faVolumeHigh, faTimes } from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';

import { VideoProps, ScriptContentRowProps, ControlButtonProps ,SubtitleEntry } from '../types/components';
import styles from '../styles/Video.module.css';


const formatTime = (seconds: number): string => {
  const m = Math.floor(seconds / 60);
  const s = Math.floor(seconds % 60);
  return `${m}:${s.toString().padStart(2, '0')}`;
};


const ControlButton: React.FC<ControlButtonProps> = ({onClick, icon, style}) => {
  return (
    <button onClick={onClick} className={styles[style]}>
      <FontAwesomeIcon icon={icon} />
    </button>
  );
};


const LecturePlayer: React.FC<VideoProps> = ({videoPath, audioPath, scriptPath}) => {
  const [isPlaying, setIsPlaying] = useState(false);
  const [showScript, setShowScript] = useState(false);
  const [scripts, setScripts] = useState<SubtitleEntry[]>([])
  const [currentTime, setCurrentTime] = useState(0);
  const [duration, setDuration] = useState(0);
  const [volume, setVolume] = useState(0.8);
  const [showVolumeControl, setShowVolumeControl] = useState(false);

  const videoRef = useRef<HTMLVideoElement>(null);
  const audioRef = useRef<HTMLAudioElement>(null);

  const ScriptRow: React.FC<ScriptContentRowProps> = ({ script }) => {
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
          <span className={styles.ScriptTimeStamp}>{formatTime(script.start)}</span>
        </div>
        <div className={styles.ScriptText}>
          <span>{script.text}</span>
        </div>
      </li>
    );
  };

  const Script: React.FC = () => {
    return (
      <div className={styles.ScriptContainer}>
        <div className={styles.ScriptContent}>
          <div className={styles.ScriptHeader}>
            <h1>Script</h1>
            <button onClick={() => {setShowScript(false)}}>
              <FontAwesomeIcon icon={faTimes} />
            </button>
          </div>
          <ul>
            {scripts.map((script, _) => (
              <ScriptRow script={script}/>
            ))}
          </ul>
        </div>
      </div>
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

  const handleSeek = (event: React.ChangeEvent<HTMLInputElement>) => {
    const value = parseFloat(event.target.value);
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
    <div className={styles.LecturePlayerContainer}>
      <div className={styles.LecturePlayer}>
        <video
          ref={videoRef}
          src={videoPath}
          className={styles.Video}
          onTimeUpdate={handleTimeUpdate}
          onLoadedMetadata={handleLoadedMetadata}
        />
        <audio ref={audioRef} src={audioPath} />
        <div className={styles.VideoControlContainer}>
          <input
            type="range"
            min={0}
            max={duration}
            step={0.01}
            value={currentTime}
            onChange={handleSeek}
            className={styles.ProgressBar}
            style={{
              background: `linear-gradient(to right, #7d2020ff ${progressPercent}%, #333 ${progressPercent}%)`,
            }}
          />
          <div className={styles.VideoControlButtonContainer}>
            <ControlButton
              onClick={togglePlay}
              icon={isPlaying ? faPause : faPlay}
              style='PlayButton'
            />
            <div className={styles.VideoToolContainer}>
              <ControlButton
                onClick={() => {setShowVolumeControl(!showVolumeControl)}}
                icon={(volume == 0) ? faVolumeXmark : (volume < 0.5) ? faVolumeLow : faVolumeHigh}
                style='VideoToolButton'
              />
              <input
                type="range"
                min={0}
                max={1}
                step={0.01}
                value={volume}
                onChange={handleVolumeChange}
                className={`${styles.VolumeSlider} ${showVolumeControl ? styles.volumeSliderShow : styles.volumeSliderHide}`}
                style={{
                  background: `linear-gradient(to right, #ffffff ${volume * 100}%, #333 ${volume * 100}%)`,
                }}
              />
              <ControlButton
                onClick={() => {setShowScript(!showScript)}}
                icon={faClosedCaptioning}
                style='VideoToolButton'
              />
            </div>
          </div>
        </div>
      </div>
      {showScript && <Script />}
    </div>
  );
};


export default LecturePlayer;