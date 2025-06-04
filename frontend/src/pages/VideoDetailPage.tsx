import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import VideoPlayer from '../components/VideoPlayer';
import { getVideoPresignedUrl } from '../api/video';


const VideoDetailPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const [videoSrc, setVideoSrc] = useState<string | null>(null);
  const [supportedLang, setSupportedLang] = useState<string[] | null>(null);
  const [title, setTitle] = useState<string | null>(null);

  useEffect(() => {
  if (id) {
    const fetchPresignedUrl = async () => {
      try {
        const res = await getVideoPresignedUrl(id);
        setVideoSrc(res.data.url);
        setSupportedLang(res.data.languages);
        setTitle(res.data.title);
      } catch (error) {
        console.error("Failed to get video URL", error);
        setVideoSrc(null);
        setSupportedLang(null);
      }
    };

    fetchPresignedUrl();
  }
}, [id]);

  return (
    <div style={{ maxWidth: '1000px', margin: '60px auto', padding: '20px' }}>
      <h1 style={{ fontSize: '24px', fontWeight: 'bold', marginBottom: '40px', color: "#5a5a5a"}}>
        {title}
      </h1>
      {
        videoSrc && supportedLang && id && title &&
          <VideoPlayer 
            presignedUrl={videoSrc} 
            videoId={id} 
            supportedLang={supportedLang} 
          />
      }
    </div>
  );
};

export default VideoDetailPage;