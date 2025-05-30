import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import VideoPlayer from '../components/VideoPlayer';
import { getVideoPresignedUrl } from '../api/video';


const VideoDetailPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const [videoSrc, setVideoSrc] = useState<string | null>(null);

  useEffect(() => {
  if (id) {
    const fetchPresignedUrl = async () => {
      try {
        const res = await getVideoPresignedUrl(id);
        setVideoSrc(res.data); 
      } catch (error) {
        console.error("Failed to get video URL", error);
        setVideoSrc(null);
      }
    };

    fetchPresignedUrl();
  }
}, [id]);

  return (
    <div style={{ maxWidth: '1000px', margin: '40px auto', padding: '20px' }}>
      <h1 style={{ fontSize: '24px', fontWeight: 'bold', marginBottom: '20px' }}>
        동영상 보기 (ID: {id})
      </h1>
      {videoSrc && <VideoPlayer presignedUrl={videoSrc} videoId={id as string} />}
    </div>
  );
};

export default VideoDetailPage;