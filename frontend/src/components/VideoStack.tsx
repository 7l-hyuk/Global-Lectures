import React from 'react';
import { Link } from 'react-router-dom';
import styles from '../css/VideoStack.module.css';
import { faPenToSquare, faPlay } from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';

export interface VideoItem {
  id: number;
  title: string;
  length: string;
}

interface VideoStackProps {
  videos: VideoItem[];
}

const VideoStack: React.FC<VideoStackProps> = ({ videos }) => {
  return (
      <div className={styles.VideoStack}>
        {videos.map((video) => (
            <div className={styles.videoCard}>
              <Link
                to={`/videos/${video.id}`}
                key={video.id}
                className={styles.videoItem}
              >
                <FontAwesomeIcon icon={faPlay} style={{margin: "20px", alignSelf: "center", fontSize: "20px"}}/>
                <div style={{display: "flex", flexDirection: "column", justifyContent: "space-evenly", paddingLeft: "10px", paddingRight: "30px", overflow: "hidden", textOverflow: "ellipsis", width: "100%"}}>
                  <span className={styles.videoTitle}>{video.title}</span>
                  <span className={styles.videoLength}>{video.length}</span>
                </div>
                <div style={{textAlign: "right"}}>
                  <button style={{borderColor: "transparent", backgroundColor: "transparent"}} onClick={(e) => {
                      e.preventDefault();
                    }}>
                    <FontAwesomeIcon icon={faPenToSquare} className={styles.UpdateButton}/>
                  </button>
                </div>
              </Link>
            </div>
        ))}
      </div>
    
  );
};

export default VideoStack;