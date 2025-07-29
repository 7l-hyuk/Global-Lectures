import React, { useRef, useState, useEffect } from "react";
import { faFolderPlus, faChevronDown, faChevronRight, faSyncAlt, faArrowRightArrowLeft, faFile, faTimes } from "@fortawesome/free-solid-svg-icons";

import { dubbingVideo } from "../viewmodels/dubbing";
import { SettingDropdownProps, Language, LangCode } from "../types/components";
import { IconButton, ButtonIcon } from "../components/Button";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { LanguageType } from "../types/components";
import styles from "../styles/ServicePage.module.css";


const tarLangList:  { [key in LanguageType]: LanguageType[] } = {
  Korean: ["English", "Japanese", "Chinese"],
  English: ["Korean", "Japanese", "Chinese"],
  Japanese: ["Korean", "English", "Chinese"],
  Chinese: ["Korean", "English", "Japanese"],
}

const langCodeMapping: { [key in LanguageType]: LangCode } = {
  Korean: "ko",
  English: "en",
  Japanese: "ja",
  Chinese: "zh"
};


const SerivcePage: React.FC = () => {
  const fileInputRef = useRef<HTMLInputElement>(null);
  const [file, setFile] = useState<File | null>(null);
  const [isSourceDropdownOpen, setIsSourceDropdownOpen] = useState(false);
  const [isTargetDropdownOpen, setIsTargetDropdownOpen] = useState(false);
  const [sourceLang, setSourceLang] = useState<LanguageType>("Korean")
  const [targetLang, setTargetLang] = useState<LanguageType>(tarLangList[sourceLang][0])

  

  
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

  const SettingDropdown: React.FC<SettingDropdownProps> = ({label, onClick, isDropdownOpen, items, setItem}) => {
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
            <li onClick={() => setItem(item)}>{item}</li>
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


  const UploadedFileInfo: React.FC = () => {
    return file ? (
      <div className={styles.UploadedFileInfo}>
        <div className={styles.fileName}>
          <FontAwesomeIcon icon={faFile} />
          <span>{file.name}</span>
        </div>
        <div className={styles.langInfo}>
          <FontAwesomeIcon icon={faSyncAlt} />
          <span>Convert</span>
          <span className={styles.LangTextBox}>{sourceLang}</span>
          <span>to</span>
          <span className={styles.LangTextBox}>{targetLang}</span>
        </div>
        <button onClick={() => {setFile(null)}}>
          <FontAwesomeIcon icon={faTimes} />
        </button>
      </div>
    ) : (
      <></>
    )
  }
  const ServiceSettingForm: React.FC = () => {
    return (
      <div className={styles.ServiceSettingForm}>
        <SettingDropdown
          label={sourceLang}
          isDropdownOpen={isSourceDropdownOpen}
          items={["Korean", "English", "Japanese", "Chinese"]}
          onClick={() => {setIsSourceDropdownOpen(!isSourceDropdownOpen)}}
          setItem={(item: LanguageType) => {
            setSourceLang(item);
            if (item == targetLang) {
              setTargetLang(tarLangList[item][0]);
            }
            setIsSourceDropdownOpen(false);
          }}
        />
        <button className={styles.LangChangeButton} onClick={() => {
          const src: LanguageType = sourceLang;
          const tar: LanguageType = targetLang;
          setSourceLang(tar);
          setTargetLang(src);
        }}>
          <FontAwesomeIcon icon={faArrowRightArrowLeft} />
        </button>
        <SettingDropdown
          label={targetLang}
          isDropdownOpen={isTargetDropdownOpen}
          items={tarLangList[sourceLang]}
          onClick={() => {setIsTargetDropdownOpen(!isTargetDropdownOpen)}}
          setItem={(item: Language) => {
            setTargetLang(item);
            setIsTargetDropdownOpen(false);
          }}
        />
      </div>
    );
  };

  const ConvertButton: React.FC = () => {
    return (
      <div className={styles.ConvertContainer}>
        <IconButton 
          icon={faSyncAlt}
          label="Convert"
          onClick={async () => {
            if (file) {
              const dubbingRequest = {
                video: file as File,
                source_lang: langCodeMapping[sourceLang],
                target_lang: langCodeMapping[targetLang],
                stt_model: "whisperX",
                translation_model: "NLLB-200",
                tts_model: "coqui-xtts-v2"
              };
              await dubbingVideo(dubbingRequest);
            } else {
              alert("upload file");
            }
          }}
        />
      </div>
    );
  };

  return (
    <div className={styles.ServiceFormContainer}>
      {file ? <UploadedFileInfo /> : <FileUploadForm />}
      <ServiceSettingForm />
      <ConvertButton />
    </div>
  );
};


export default SerivcePage;