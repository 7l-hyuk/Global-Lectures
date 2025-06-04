import {axiosVideoInstance} from "./axiosInstance";
import { AxiosResponse } from "axios";


export interface SubtitleEntry {
  time: number;
  end: number;
  text: string;
}


export interface VideoUpdate {
  title: string;
  description: string;
}


interface MediaBundle {
  audio: string;
  subtitle: SubtitleEntry[];
}


export const getVideos = async () => {
    return await axiosVideoInstance.get("/");
};


export const getVideoPresignedUrl = async (id: string) => {
    return await axiosVideoInstance.get(`/${id}`);
};


export const updateVideo = async (id: string, video: VideoUpdate) => {
  return await axiosVideoInstance.patch(`/${id}`, video);
}


export const getMediaBundle = async (
  id: string,
  lang_code: string
): Promise<AxiosResponse<MediaBundle>> => {
  return await axiosVideoInstance.get<MediaBundle>(`/bundle/${id}/${lang_code}`);
};
