import React from "react";
import styles from "../../styles/Navbar.module.css";


interface NavbarProps {
  toggleSidebar: () => void;
}

const Navbar: React.FC<NavbarProps> = ({toggleSidebar}) => {
    return (
        <nav className={styles.Navbar}>

        </nav>
    );
};

export default Navbar;