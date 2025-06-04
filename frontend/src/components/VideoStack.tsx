import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import styles from '../css/VideoStack.module.css';
import { faPenToSquare, faPlay } from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import VideoEditModal from './VideoEditModal';

export interface VideoItem {
  id: number;
  title: string;
  description: string;
  length: string;
}

interface VideoStackProps {
  videos: VideoItem[];
  onRefresh?: () => void;
}

const VideoStack: React.FC<VideoStackProps> = ({ videos, onRefresh }) => {
  const [editingVideo, setEditingVideo] = useState<VideoItem | null>(null);

  return (
    <div className={styles.VideoStack}>
      {videos.map((video) => (
        <div className={styles.videoCard} key={video.id}>
          <Link to={`/videos/${video.id}`} className={styles.videoItem}>
            <FontAwesomeIcon icon={faPlay} style={{ margin: '20px', alignSelf: 'center', fontSize: '20px' }} />
            <div style={{ display: 'flex', flexDirection: 'column', justifyContent: 'space-evenly', paddingLeft: '10px', paddingRight: '30px', overflow: 'hidden', textOverflow: 'ellipsis', width: '100%' }}>
              <span className={styles.videoTitle}>{video.title}</span>
              <span className={styles.videoDescription}>{video.description}</span>
              <span className={styles.videoLength}>{video.length}</span>
            </div>
            <div style={{ textAlign: 'right' }}>
              <button
                style={{ borderColor: 'transparent', backgroundColor: 'transparent' }}
                onClick={(e) => {
                  e.preventDefault();
                  setEditingVideo(video);
                }}
              >
                <FontAwesomeIcon icon={faPenToSquare} className={styles.UpdateButton} />
              </button>
            </div>
          </Link>
        </div>
      ))}
      {editingVideo && (
        <VideoEditModal
          isOpen={!!editingVideo}
          onClose={() => setEditingVideo(null)}
          id={editingVideo.id}
          title={editingVideo.title}
          description={editingVideo.description}
          onUpdateSuccess={() => {
            setEditingVideo(null);
            onRefresh?.();
          }}
        />
      )}
    </div>
  );
};

export default VideoStack;
