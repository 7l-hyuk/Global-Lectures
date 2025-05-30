import React from 'react';
import { Link } from 'react-router-dom';
import styles from '../css/VideoStack.module.css';

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
            <span className={styles.videoTitle}>{video.title}</span>
            <span className={styles.videoLength}>{video.length}</span>
          </Link>
        </div>
      ))}
    </div>
  );
};

export default VideoStack;