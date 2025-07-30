import { dubbingVideo as dubbingAPI, getProgress as getProgressAPI } from "../models/dubbing";
import { DubbingRequest } from "../types/dubbing";


export const getDubbingTaskId = async (dubbingRequest: DubbingRequest) => {
    try {
        const res = await dubbingAPI(dubbingRequest);
        return res.data.taskId
    } catch (err) {
        console.error(err)
    }
};


export const getProgress = async (taskId: string) => {
    const res = await getProgressAPI(taskId);
    return res.data;
};
