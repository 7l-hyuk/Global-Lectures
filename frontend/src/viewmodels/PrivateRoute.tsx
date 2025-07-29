import { Navigate } from "react-router-dom";
import { useAuth } from "./AuthContext";


const PrivateRoute = ({ children }: { children: React.ReactNode }) => {
  const { user, isLoading } = useAuth();
  if (isLoading) return null;
  if (!user) return <Navigate to="/signin" replace />;
  return <>{children}</>;
};


export default PrivateRoute;