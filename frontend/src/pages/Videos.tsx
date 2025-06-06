import React, { useEffect, useState } from "react";
import styles from "../css/VideoStack.module.css";
import VideoStack, { VideoItem } from "../components/VideoStack";
import { getVideos } from "../api/video";

const Videos: React.FC = () => {
  const [videos, setVideos] = useState<VideoItem[]>([]);
  const [currentPage, setCurrentPage] = useState(1);
  const videosPerPage = 5;

  const fetchVideos = async () => {
    try {
      const res = await getVideos();
      setVideos(res.data);
    } catch (err) {
      console.error("Failed to fetch videos:", err);
    }
  };

  useEffect(() => {
    fetchVideos();
  }, []);

  const indexOfLastVideo = currentPage * videosPerPage;
  const indexOfFirstVideo = indexOfLastVideo - videosPerPage;
  const currentVideos = videos.slice(indexOfFirstVideo, indexOfLastVideo);
  const totalPages = Math.ceil(videos.length / videosPerPage);

  return (
    <div className={styles.VideoStackContainer} style={{flexDirection: "column"}}>
      <VideoStack videos={currentVideos} onRefresh={fetchVideos} />

      {/* Pagination Buttons */}
      <div className={styles.Pagination}>
        {[...Array(totalPages)].map((_, idx) => (
          <button
            key={idx}
            onClick={() => setCurrentPage(idx + 1)}
            className={`${styles.PageButton} ${currentPage === idx + 1 ? styles.ActivePage : ""}`}
          >
            {idx + 1}
          </button>
        ))}
      </div>
    </div>
  );
};

export default Videos;
