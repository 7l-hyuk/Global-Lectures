import { useState } from 'react';
import { useAuth } from "../context/AuthContext"
import NavbarStyles from "../css/Navbar.module.css"
import DropdownStyles from "../css/Dropdown.module.css"


function Dropdown() {
  const [isOpen, setIsOpen] = useState(false);
  const { user, logout } = useAuth();

  const toggleDropdown = () => {
    setIsOpen(prev => !prev);
  };

  return (
    <div className={NavbarStyles.navbarLinks}>
      <div
        className={DropdownStyles.userDropdown}
        onClick={toggleDropdown}
      >
        {user?.username}
      </div>

      {isOpen && (
        <div className={DropdownStyles.dropdwonContainer}>
          <div className={DropdownStyles.dropdownItem}>
            <span className={DropdownStyles.item}>mypage</span>
          </div>
          <div className={DropdownStyles.dropdownItem}>
            <span onClick={(e) => {
                e.preventDefault();
                logout();
            }}
                className={DropdownStyles.item}
            >logout</span>
          </div>
        </div>
      )}
    </div>
  );
}




export {Dropdown};
