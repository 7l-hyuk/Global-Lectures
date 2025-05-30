import {axiosVideoInstance} from "./axiosInstance";


export const getVideos = async () => {
    return await axiosVideoInstance.get("/");
};


export const getVideoPresignedUrl = async (id: string) => {
    return await axiosVideoInstance.get(`/${id}`);
};

export const getSubtitle = async (id: string) => {
    return await axiosVideoInstance.get(`/subtitle/${id}`);
};

