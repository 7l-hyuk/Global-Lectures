import React, {useEffect, useState} from "react";
import { faCirclePlay, faUser, faCartShopping } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";

import styles from "../css/VideoStack.module.css";
import VideoStack, {VideoItem} from "../components/VideoStack";
import { getVideos } from "../api/video";


const Videos: React.FC = () => {
  const [videos, setVideos] = useState<VideoItem[]>([]);

  const fetchVideos = async () => {
    try {
      const res = await getVideos();
      setVideos(res.data);
    } catch (err) {
      console.error('Failed to fetch videos:', err);
    }
  };

  useEffect(() => {
    fetchVideos();
  }, []);

  return (
      <div className={styles.VideoStackContainer}>
        <VideoStack videos={videos} onRefresh={fetchVideos}/>
      </div>
  );
};

export default Videos;
