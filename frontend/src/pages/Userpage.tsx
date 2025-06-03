import React, {useEffect, useState} from "react";

import styles from "../css/VideoStack.module.css";
import VideoStack, {VideoItem} from "../components/VideoStack";
import { getVideos } from "../api/video";

const Userpage: React.FC = () => {
  const [videos, setVideos] = useState<VideoItem[]>([]);;

  useEffect(() => {
    getVideos()
      .then(res => setVideos(res.data))
      .catch(console.error);
  }, []);

  return (
    <div className={styles.VideoStackContainer}>
      <VideoStack videos={videos} />
    </div>
  );
};

export default Userpage;
