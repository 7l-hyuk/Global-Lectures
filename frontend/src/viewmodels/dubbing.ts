import { dubbingVideo as dubbingAPI } from "../models/dubbing";
import { DubbingRequest } from "../types/dubbing";


export const dubbingVideo = async (dubbingRequest: DubbingRequest) => {
    try {
        await dubbingAPI(dubbingRequest)
    } catch (err) {
        console.error(err)
    }
};
