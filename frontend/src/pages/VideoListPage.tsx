// @ts-ignore
import Modal from "react-modal";
import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faTrashCan, faPen, faEllipsisH, faStopwatch, faCalendar, faTimes } from "@fortawesome/free-solid-svg-icons";
import { getUserVideos, patchUserVideo } from "../viewmodels/video";
import { BasicButton } from "../components/Button";
import styles from "../styles/VideoListPage.module.css";

Modal.setAppElement('#root');

export type VideoItem = {
  id: number;
  title: string;
  description: string;
  length: string;
  created_at: string;
};


export interface VideoRowProps {
  videoItem: VideoItem;
};


interface EditModalProps {
  isOpen: boolean;
  onClose: () => void;
  id: number;
  title: string;
  description: string;
  onUpdateSuccess?: () => void;
}

interface EditModalInputProps {
  height?: string;
  value: string;
  setValue: (value: string) => void;
  children: React.ReactNode;
}


const EditModalInput: React.FC<EditModalInputProps> = ({height = "20rem", value, setValue, children}) => {  
  return (
    <div className={styles.EditModalInput}>
      <span>{children}</span>
      <textarea value={value} style={{height: height}} onChange={(event) => {setValue(event.target.value)}}/>
    </div>
  );
};


const EditModal: React.FC<EditModalProps> = ({ isOpen, onClose, id, title, description, onUpdateSuccess }) => {
  const [newTitle, setNewTitle] = useState(title);
  const [newDescription, setNewDescription] = useState(description);

  return (
    <Modal
      isOpen={isOpen}
      onRequestClose={onClose}
      contentLabel="Edit Video"
      style={{
        content: {
          display: "flex",
          width: '460px',
          height: "27rem",
          margin: 'auto',
          padding: '1.5rem .7rem',
          border: "none",
          borderRadius: '.5em',
          backgroundColor: 'var(--bg-color)'
        },
        overlay: {
          backgroundColor: 'rgba(0, 0, 0, 0.6)',
        },
      }}
    >
      <div style={{display: "flex", justifyContent: "center", alignContent: "center", flexDirection: "column", width: "100%", gap: "1.5rem"}}>
        <EditModalInput height="5rem" value={newTitle} setValue={setNewTitle}>Title (required)</EditModalInput>
        <EditModalInput height="10rem" value={newDescription} setValue={setNewDescription}>Description</EditModalInput>
        <div style={{display: "flex", justifyContent: "flex-end", width: "100%", gap: "1rem"}}>
          <BasicButton 
            label="Cancel"
            onClick={onClose}
          />
          <BasicButton 
            label="Save"
            onClick={async () => {
              await patchUserVideo(id, {title: newTitle, description: newDescription});
              onClose();
              onUpdateSuccess?.();
            }}
          />
        </div>
      </div>

    </Modal>
  );
};


const VideoListPage: React.FC = () => {
  const [videoItems, setVideoItems] = useState<VideoItem[]>([]);

  const fetchVideos = async () => {
    try {
      const _videoItems = await getUserVideos();
      setVideoItems(_videoItems);
    } catch (error) {
      console.error("비디오 로딩 실패:", error);
    }
  };

  const VideoRow: React.FC<VideoRowProps> = ({ videoItem }) => {
    const [isModalOpen, setIsModalOpen] = useState(false);
    const date = new Date(videoItem.created_at);
    const formattedDate = date.toLocaleDateString("en-US", {
      month: "short",
      day: "numeric",
      year: "numeric",
    });

    const VideoControls: React.FC = () => {
      const [isDropdownOpen, setIsDropdownOpen] = useState(false);
  
      return (
        <div className={styles.controls}>
          <button onClick={() => {
            setIsDropdownOpen(!isDropdownOpen);
          }}>
            <FontAwesomeIcon icon={faEllipsisH} />
          </button>
          {isDropdownOpen && (
            <ul>
              <li onClick={() => setIsModalOpen(true)}>
                <FontAwesomeIcon icon={faPen} />
                Edit title and description
              </li>
              <li style={{ color: "var(--red-btn-color)" }}>
                <FontAwesomeIcon icon={faTrashCan} />
                Delete forever
              </li>
            </ul>
          )}
        </div>
      );
    };

    return (
      <div className={styles.RowContainer}>
        <div className={styles.VideoCell}>
          <div className={styles.title}>
            <a href={`/videos/${videoItem.id}`}>{videoItem.title}</a>
            <VideoControls />
          </div>
          <div className={styles.BodyContainer}>
            <div className={styles.description}>
              {videoItem.description}
            </div>
            <div className={styles.meta}>
              <span>
                <FontAwesomeIcon icon={faStopwatch} />
                {videoItem.length}
              </span>
              <span>
                <FontAwesomeIcon icon={faCalendar} />
                {formattedDate}
              </span>
            </div>
          </div>
        </div>
        <EditModal
          isOpen={isModalOpen}
          onClose={() => setIsModalOpen(false)}
          id={videoItem.id}
          title={videoItem.title}
          description={videoItem.description}
          onUpdateSuccess={() => {
            fetchVideos();
          }}
        />
      </div>
    );
  };

  useEffect(() => {
    fetchVideos();
  }, []);

  return (
    <div className={styles.VideoListContent}>
      {videoItems.map((videoItem, _) => (
        <VideoRow videoItem={videoItem} />
      ))}
    </div>
  );
};


export default VideoListPage;