import React, { useState, useRef, useEffect } from "react";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faBars, faAngleDown } from "@fortawesome/free-solid-svg-icons";
import {faGithub, faYoutube} from '@fortawesome/free-brands-svg-icons'
import { useNavigate } from "react-router-dom";

import { NavbarProps } from "../../types/components";
import { BasicButton, ButtonIcon, IconButton } from "../Button";
import { useAuth } from "../../viewmodels/AuthContext";
import styles from "../../styles/Navbar.module.css";


const Navbar: React.FC<NavbarProps> = ({toggleSidebar}) => {
    const [isDropdownOpen, setIsDropdownOpen] = useState(false);
    const dropdownRef = useRef<HTMLDivElement>(null);
    const {user, userSignout, isLoading} = useAuth();
    const navigate = useNavigate();

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
              <ButtonIcon 
                label={user.username}
                color="transparent"
                buttonType="UserButton"
                icon={faAngleDown}
                onClick={() => setIsDropdownOpen(!isDropdownOpen)}
              />
              {isDropdownOpen && (
                <ul>
                  <li><a href="/">mypage</a></li>
                  <li>
                    <a href="/" onClick={async (event) => {
                      event.preventDefault();
                      await userSignout();
                      setIsDropdownOpen(false);
                    }}>
                      signout
                    </a>
                  </li>
                </ul>
              )}
            </div>
          );
        } else {
          return (
            <ul className={styles.NavbarEnd}>
              <IconButton 
                label="GitHub"
                color="transparent"
                buttonType="LinkButton"
                icon={faGithub}
                onClick={() => {window.open('https://github.com/7l-hyuk/Global-Lectures', '_blank')}}
              />
              <IconButton 
                label="Youtube"
                color="transparent"
                buttonType="LinkButton"
                icon={faYoutube}
                onClick={() => {window.open('https://www.youtube.com/@global-lectures-korea', '_blank')}}
              />
              <li><BasicButton label="Sign In" onClick={()=>{navigate("/signin")}}/></li>
              <li><BasicButton label="Sign Up" color="red" onClick={()=>{navigate("/signup")}}/></li>
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
            <li><a href="/service">Service</a></li>
            <li><a href="/">Pricing</a></li>
            <li><a href="/">Contact</a></li>
          </ul>

          <UserMenu />
        </div>
      </nav>
    );
};

export default Navbar;