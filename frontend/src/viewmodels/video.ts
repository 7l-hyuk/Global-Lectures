import { promises } from "dns";
import {
    getUserVideos as getVideosAPI,
    patchUserVideo as patcVideoAPI,
    getUserVideo as getVideoAPI,
    getUserVideoBundle as getVideoBundleAPI
} from "../models/video";
import { VideoUpdate } from "../types/video";


export const getUserVideos = async () => {
    try {
        const res = await getVideosAPI();
        return res.data;
    } catch (err) {
        console.error("Failed to fetch videos:", err);
    }
};


export const patchUserVideo: (id: number, videoUpdate: VideoUpdate) => Promise<void> = async (id, videoUpdate) => {
    try {
        await patcVideoAPI(id, videoUpdate);
    } catch (err) {
        alert("Update fail");
        console.error(err);
    }
};


export const getUserVideo = async (id: number | string) => {
    try {
        return await getVideoAPI(id);
    } catch (err) {
        console.error("Fetch video fail", err);
    }
};


export const getUserVideoBundle = async (id: number | string, lang: string) => {
    try {
        return getVideoBundleAPI(id, lang);
    } catch (err) {
        console.error('Failed to load media bundle:', err);
    }
}