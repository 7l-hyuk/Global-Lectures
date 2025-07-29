import { axiosAuthInstance } from "./axiosInstances";
import { UserSignup, UserSignin } from "../types/auth";


const userSignup = async (payload: UserSignup) => {
    return await axiosAuthInstance.post("/signup", payload);
};


const userSignin = async (payload: UserSignin) => {
    const res = await axiosAuthInstance.post("/signin", payload);
    return res
};


const fetchMe = async () => {
    return await axiosAuthInstance.get("/me");
};


const userSignout = async () => {
    return await axiosAuthInstance.post("/signout", {});
};


export {userSignup, userSignin, userSignout, fetchMe};
