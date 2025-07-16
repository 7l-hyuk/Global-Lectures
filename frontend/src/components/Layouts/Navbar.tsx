import React, { useState, useRef, useEffect } from "react";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faBars, faAngleDown } from "@fortawesome/free-solid-svg-icons";

import { NavbarProps } from "../../types/components";
import { useAuth } from "../../viewmodels/AuthContext";
import styles from "../../styles/Navbar.module.css";


const Navbar: React.FC<NavbarProps> = ({toggleSidebar}) => {
    const [isDropdownOpen, setIsDropdownOpen] = useState(false);
    const dropdownRef = useRef<HTMLDivElement>(null);
    const {user, userSignout, isLoading} = useAuth();

    const UserMenu: React.FC = () => {
      const handleClickOutside = (event: MouseEvent) => {
        if (
          dropdownRef.current &&
          !dropdownRef.current.contains(event.target as Node)
        ) {
          setIsDropdownOpen(false);
        }
      };

      useEffect(() => {
        document.addEventListener("mousedown", handleClickOutside);
        return () => {
          document.removeEventListener("mousedown", handleClickOutside)
        }
      }, [])
      
      if (!isLoading) {
        if (user) {
          return (
            <div className={styles.NavbarUser} ref={dropdownRef}>
              <button onClick={() => {setIsDropdownOpen(!isDropdownOpen)}}>
                {user.username}
                <FontAwesomeIcon icon={faAngleDown}/>
              </button>
              {isDropdownOpen && (
                <ul>
                  <li><a href="/">mypage</a></li>
                  <li>
                    <a href="/" onClick={async (event) => {
                      event.preventDefault();
                      await userSignout();
                    }}>
                    signout</a>
                  </li>
                </ul>
              )}
            </div>
          );
        } else {
          return (
            <ul className={styles.NavbarEnd}>
              <li><a href="/signup">Sign Up</a></li>
              <li><a href="/signin">Sign In</a></li>
            </ul>
          );
        }
      } else {
        return <></>
      }
    };

    return (
      <nav className={styles.NavbarContainer}>
        <div className={styles.NavbarContent}>
          <div className={styles.NavbarStart}>
            <button className={styles.MenuButton} onClick={toggleSidebar}>
              <FontAwesomeIcon icon={faBars}/>
            </button>
            <span className={styles.Logo}>
              <a href="/">Global Lectures</a>
            </span>
          </div>
  
          <ul className={styles.NavbarMiddle}>
            <li><a href="/">Service</a></li>
            <li><a href="/">Pricing</a></li>
            <li><a href="/">Contact</a></li>
          </ul>

          <UserMenu />
        </div>
      </nav>
    );
};

export default Navbar;