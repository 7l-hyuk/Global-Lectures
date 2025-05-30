import React, {useEffect, useState} from "react";

import IntroStyles from "../css/Intro.module.css";
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
    <div className={IntroStyles.contentWrapper}>
      <VideoStack videos={videos} />
    </div>
  );
};

export default Userpage;
