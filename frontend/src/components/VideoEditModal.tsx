import React, { useState } from 'react';
import Modal from 'react-modal';
import { updateVideo } from '../api/video';
import styles from "../css/VideoEditModal.module.css"
import { BaseButton, VideoUpdateInput } from "../components/Form";
import { faTrash, faTimes, faMagnifyingGlass, faMessage, faRotate } from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';



interface Props {
  isOpen: boolean;
  onClose: () => void;
  id: number;
  title: string;
  description: string;
  onUpdateSuccess?: () => void;
}

Modal.setAppElement('#root');

const VideoEditModal: React.FC<Props> = ({ isOpen, onClose, id, title, description, onUpdateSuccess }) => {
  const [newTitle, setNewTitle] = useState(title);
  const [newDescription, setNewDescription] = useState(description);

  const handleUpdate = async () => {
    try {
      await updateVideo(String(id), { title: newTitle, description: newDescription });
      onUpdateSuccess?.();
      onClose();
    } catch (err) {
      alert('Update failed');
      console.error(err);
    }
  };

  return (
    <Modal
      isOpen={isOpen}
      onRequestClose={onClose}
      contentLabel="Edit Video"
      style={{
        content: {
          width: '460px',
          height: '430px',
          margin: 'auto',
          padding: '20px 10px',
          borderRadius: '12px',
        },
        overlay: {
          backgroundColor: 'rgba(0, 0, 0, 0.6)',
        },
      }}
    >
    <div style={{display: "flex", justifyContent: "center"}}>
      <div className={styles.LoginFormContainer}>
        <div style={{display: "flex", justifyContent: "flex-end"}}>
          <button onClick={onClose} className={styles.CloseButton}>
            <FontAwesomeIcon icon={faTimes} />
          </button>
        </div>
          <VideoUpdateInput
            label="Title"
            value={newTitle}
            type="text"
            onChange={setNewTitle}
            styles={styles}
            icon={faMagnifyingGlass}
          />
          <VideoUpdateInput
            label="Description"
            value={newDescription}
            type="text"
            onChange={setNewDescription}
            styles={styles}
            icon={faMessage}
          />
          <div className={styles.LoginButtonContainer}>
              <BaseButton label="Update" icon={faRotate} buttonStyle={styles.UpdateButton} onClick={handleUpdate} disabled={false} />
              <BaseButton label="Delete" icon={faTrash} buttonStyle={styles.DeleteButton} onClick={() => alert('Delete not implemented')} disabled={false} />
          </div>
      </div>
    </div>
    </Modal>
  );
};

export default VideoEditModal;
