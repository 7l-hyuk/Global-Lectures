import React, { useState } from "react";
import { Outlet } from "react-router-dom";

import Navbar from "./Navbar";
import styles from "../../styles/global.module.css";


const Layout: React.FC = () => {
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);

  const toggleSidebar = () => {
    setIsSidebarOpen(!isSidebarOpen);
  }

  return (
    <>
      <div>
        <Navbar toggleSidebar={toggleSidebar} />
        <main className={styles.MainContainer}>
          <Outlet />
        </main>
      </div>
      
    </>
  )
}


export default Layout;