import { axiosVideoInstance } from "../models/axiosInstances";
import { VideoUpdate } from "../types/video";


export const getUserVideos = async () => {
    return await axiosVideoInstance.get("/");
};


export const getUserVideo = async (id: number | string) => {
    return await axiosVideoInstance.get(`/${id}`);
};


export const getUserVideoBundle = async (id: number | string, lang: string) => {
    return await axiosVideoInstance.get(`/bundle/${id}/${lang}`);
};


export const patchUserVideo = async (id: number, videoUpdate: VideoUpdate) => {
    return await axiosVideoInstance.patch(`/${id}`, videoUpdate);
};
