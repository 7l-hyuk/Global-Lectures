import React, { createContext, useContext, useState, useEffect } from "react";

import { fetchMe, userSignout as signoutAPI } from "../models/auth";
import { AuthContextType } from "../types/auth";
import { User } from "../types/auth";


const AuthContext = createContext<AuthContextType | undefined>(undefined);


export const AuthProvider: React.FC<{children: React.ReactNode}> = ({ children }) => {
    const [user, setUser] = useState<User | null>(null);
    const [isLoading, setIsLoding] = useState(true);

    const fetchCurrentUser = async () => {
        console.log("try fetch user");
        try {
            setIsLoding(true);
            const user = await fetchMe();
            const username = user?.data?.username;
            if (username) {
                setUser({username});
                setIsLoding(false);
            } else {
                setUser(null);
                setIsLoding(false);
            }
            console.log("end fetch user");
        } catch {
            setUser(null);
            setIsLoding(false);
            console.log("end fetch user");
        } finally {
            setIsLoding(false);
            console.log("end fetch user");
        }
    };

    const userSignout = async () => {
        try {
            await signoutAPI();
            setUser(null);
        } catch (err) {
            console.error("Signout fail", err);
        }
    };

    useEffect(() => {
        setIsLoding(true);
        fetchCurrentUser();
    }, []);

    return (
        <AuthContext.Provider value={{user, setUser, fetchCurrentUser, userSignout, isLoading}}>
            {children}
        </AuthContext.Provider>
    );
};


export const useAuth = () => {
    const context = useContext(AuthContext);
    
    if (!context) {
        throw new Error("useAuth must be used within an AuthProvider")
    }
    return context;
};
