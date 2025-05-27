import { createContext, useContext, useState, useEffect } from "react";
import { fetchMe, logout as logoutAPI } from "../api/auth";
import { AuthContextType, User } from "./types";


const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  const fetchCurrentUser = async () => {
    try {
      const res = await fetchMe();
      setUser({ username: res.data.username });
    } catch {
      setUser(null);
    } finally {
      setIsLoading(false);
    }
  };

  const logout = async () => {
    try {
        await logoutAPI();
        setUser(null);
    } catch (err) {
        console.error("logout fail", err)
    }
  };

  useEffect(() => {
    fetchCurrentUser();
  }, []);

  return (
    <AuthContext.Provider value={{ user, isLoading, setUser, fetchCurrentUser, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
};
