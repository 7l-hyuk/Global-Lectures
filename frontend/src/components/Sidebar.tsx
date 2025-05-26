import React from "react";

import { SidebarProps } from "./props";
import styles from "../css/Sidebar.module.css";


const Sidebar: React.FC<SidebarProps> = ({isOpen, toggleSidebar}) => {
    return (
        <div className={`${styles.sidebar} ${isOpen ? styles.open : ''}`}>
            <button className={styles.closeButton} onClick={toggleSidebar}>×</button>
            <ul className={styles.sidebarMenu}> 
                <li><a href="http://localhost:3000">Home</a></li>
                <li><a href="http://localhost:3000">About</a></li>
                <li><a href="http://localhost:3000">Contact</a></li>
            </ul>
        </div>
    );
};


export default Sidebar;