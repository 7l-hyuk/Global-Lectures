import React from "react";

import { NavbarProps } from "./props";
import { IsLogin } from "./IsLogin";
import styles from "../css/Navbar.module.css"


const Navbar: React.FC<NavbarProps> = ({ toggleSidebar }) => {
  return (
    <nav className={styles.navbar}>
      <div className={styles.navbarLeft}>
        <button className={styles.menuButton} onClick={toggleSidebar}>☰</button>
        <span className={styles.logo} >
          <a
            href="http://localhost:3000"
            style={{ textDecoration: 'none', color: 'inherit', paddingRight: '50px' }}
          >
            Global Lectures
          </a>
        </span>
        <div className={styles.navbarLinks}>
          <a href="http://localhost:3000">Service</a>
          <a href="http://localhost:3000">Pricing</a>
          <a href="http://localhost:3000">Contact</a>
        </div>
      </div>
      <IsLogin />
    </nav>
  );
};


export default Navbar;
