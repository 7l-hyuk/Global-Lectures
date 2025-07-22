import React, { useRef, useState } from "react";
import { faFolderPlus, faChevronDown, faChevronRight, faSyncAlt } from "@fortawesome/free-solid-svg-icons";

import { SettingDropdownProps } from "../types/components";
import styles from "../styles/ServicePage.module.css";
import { IconButton, ButtonIcon } from "../components/Button";


const SerivcePage: React.FC = () => {
  const fileInputRef = useRef<HTMLInputElement>(null);
  const [file, setFile] = useState<File | null>(null);
  const [isSourceDropdownOpen, setIsSourceDropdownOpen] = useState(false);
  const [isTargetDropdownOpen, setIsTargetDropdownOpen] = useState(false);

  
  const handleButtonClick = () => {
    if (fileInputRef.current) {
      fileInputRef.current.click(); 
    }
  };

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      setFile(file);
    }
  };

  const FileUploadButton: React.FC = () => {
    return (
      <div>
        <IconButton 
          label="Upload File"
          icon={faFolderPlus}
          buttonType="FileSelectButton"
          onClick={handleButtonClick}
        />
        <input 
          ref={fileInputRef}
          type="file"
          accept="video/*"
          style={{display: "none"}} 
          onChange={handleFileChange}
        />
      </div>
    );
  };

  const SettingDropdown: React.FC<SettingDropdownProps> = ({label, onClick, isDropdownOpen, items}) => {
    return (
      <div className={styles.DropdownContainer}>
        <ButtonIcon
          icon={isDropdownOpen ? faChevronDown : faChevronRight}
          label={label}
          buttonType="ServiceSettingDropdown"
          onClick={onClick}
        />
        <ul className={`${styles.Dropdown} ${styles[isDropdownOpen ? "showDropdown" : "hideDropdown"]}`}>
          {items.map((item, _) => (
            <li>{item}</li>
          ))}
        </ul>
      </div>
    )
  }
  
  const FileUploadForm: React.FC = () => {
    return (
      <div className={styles.FileUploadForm}>
        <FileUploadButton />
        <span>Max file size 2GB</span>
        <span style={{fontSize: ".7rem", color: "var(--gray-font-color)"}}>
          We are working on supporting larger files
        </span>
      </div>
    );
  };

  const ServiceSettingForm: React.FC = () => {
    return (
      <div className={styles.ServiceSettingForm}>
        <SettingDropdown
          label="Source Language"
          isDropdownOpen={isSourceDropdownOpen}
          items={["Korean", "English", "Japanese", "Chinese"]}
          onClick={() => {setIsSourceDropdownOpen(!isSourceDropdownOpen)}}
        />
        <SettingDropdown
          label="Target Language"
          isDropdownOpen={isTargetDropdownOpen}
          items={["Korean", "English", "Japanese", "Chinese"]}
          onClick={() => {setIsTargetDropdownOpen(!isTargetDropdownOpen)}}
        />
      </div>
    );
  };

  const ConvertButton: React.FC = () => {
    return (
      <div className={styles.ConvertContainer}>
        <IconButton icon={faSyncAlt} label="Convert" onClick={() => {}}/>
      </div>
    );
  };

  return (
    <div className={styles.ServiceFormContainer}>
      <FileUploadForm />
      <ServiceSettingForm />
      <ConvertButton />
    </div>
  );
};


export default SerivcePage;