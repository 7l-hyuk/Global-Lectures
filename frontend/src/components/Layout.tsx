import React, { useState } from "react";
import Navbar from "./Navbar";
import Sidebar from "./Sidebar";
import { Outlet } from "react-router-dom";
import { useAuth } from "../context/AuthContext";


const Layout: React.FC = () => {
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);
  // const { user } = useAuth();

  const toggleSidebar = () => {
    setIsSidebarOpen(!isSidebarOpen);
  };

  return (
    <div style={{ minWidth: '768px', maxWidth: '1280px', margin: '0 auto' }}>
      <Navbar toggleSidebar={toggleSidebar} />
      <Sidebar isOpen={isSidebarOpen} user={{username: "7lhyuk"}} toggleSidebar={toggleSidebar} />
      <main>
        <Outlet />
      </main>
    </div>
  );
};

export default Layout;