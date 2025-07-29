import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { SubtitleEntry } from "../types/components";
import LecturePlayer from "../components/Video";
import { getUserVideoBundle, getUserVideo } from "../viewmodels/video";


const VideoPlayPage: React.FC = () => {
    const { id } = useParams<{ id: string }>();
    const [title, setTitle] = useState<string | null>(null);
    const [langList, setLangList] = useState<string[] | null>(null);
    const [videoPath, setVideoPath] = useState<string | null>(null);
    const [audioPath, setAudioPath] = useState<string | null>(null);
    const [scriptSource, setScriptSource] = useState<SubtitleEntry[] | null>(null);
    const [selectedLang, setSelectedLang] = useState<string>("ko") 

    useEffect(() => {
        if (id) {
            const _getUserVideo = async () => {
                const res = await getUserVideo(id);

                if (res) {
                    setVideoPath(res.data.url);
                    setLangList(res.data.languages);
                    setTitle(res.data.title);
                }
            };
            _getUserVideo();
        }
    }, [id]);

    useEffect(() => {
        if (id) {
            const _getVideoBundle = async () => {
                const res = await getUserVideoBundle(id, selectedLang);

                if (res) {
                    setAudioPath(res.data.audio);
                    setScriptSource(res.data.subtitle);
                }
            }
            _getVideoBundle();
        }
    }, [id, selectedLang]);

    return (
        <div>
            {title}
            {videoPath && audioPath && scriptSource && (
                <LecturePlayer videoPath={videoPath} id={id} langList={["Korean", "English"]} />
            )}
        </div>
    );

};


export default VideoPlayPage;