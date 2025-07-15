import React, { createContext, useContext, useState, useEffect } from "react";
import { fetchMe, userSignout as signoutAPI } from "../models/auth";
import { AuthContextType } from "../types/auth";
import { User } from "../types/auth";


const AuthContext = createContext<AuthContextType | undefined>(undefined);


export const AuthProvider: React.FC<{children: React.ReactNode}> = ({children}) => {
    const [user, setUser] = useState<User | null>(null);
    
    const fetchCurrentUser = async () => {
        try {
            const user = await fetchMe();
            const username = user?.data?.username;

            if (username) {
                setUser({username});
            } else {
                setUser(null);
            }
        } catch {
            setUser(null);
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

    useEffect(
        () => {fetchCurrentUser()},
        []
    );

    return (
        <AuthContext.Provider value={{user, setUser, fetchCurrentUser, userSignout}}>
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
