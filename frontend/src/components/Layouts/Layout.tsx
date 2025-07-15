import React, { useState } from "react";
import { Outlet } from "react-router-dom";

import Navbar from "./Navbar";


const Layout: React.FC = () => {
    const [isSidebarOpen, setIsSidebarOpen] = useState(false);

    const toggleSidebar = () => {
        setIsSidebarOpen(!isSidebarOpen);
    }

    return (
        <div>
            <Navbar toggleSidebar={toggleSidebar}/>
            <main>
                <Outlet />
            </main>
        </div>
    )
}


export default Layout;