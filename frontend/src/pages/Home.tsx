import React, { useState, useRef } from "react";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faFolderPlus, faFile, faSyncAlt, faTimes } from "@fortawesome/free-solid-svg-icons";

import IntroStyles from "../css/Intro.module.css";
import DropdownStyles from "../css/Dropdown.module.css";
import { BaseButton } from "../components/Form";
import { dub } from "../api/service";


const Home: React.FC = () => {
  const fileInputRef = useRef<HTMLInputElement>(null)
  const [video, setVideo] = useState<File | null>(null);
  const [srcLang, setSrcLang] = useState("...");
  const [srcIsSelected, setSrcIsSelected] = useState(false);
  const [tarLang, setTarLang] = useState("...");
  const [tarLangs, setTarLangs] = useState(["..."])
  const [isSrcOpen, setIsSrcOpen] = useState(false);
  const [isTarOpen, setIsTarOpen] = useState(false);

  const srcLangs = ["Korean", "English", "Japanese", "Chinese"];
  type Language = 'Korean' | 'English' | 'Japanese' | 'Chinese';
  const tarLangList:  { [key in Language]: string[] } = {
    Korean: ["English", "Japanese", "Chinese"],
    English: ["Korean", "Japanese", "Chinese"],
    Japanese: ["Korean", "English", "Chinese"],
    Chinese: ["Korean", "English", "Japanese"],
  }


  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
      const file = event.target.files?.[0]; // 선택된 파일
      if (file) {
        // 선택된 파일을 URL로 변환하여 상태에 저장
        setVideo(file); // 영상 URL을 상태에 저장
      }
    };

    const handleButtonClick = () => {
      if (fileInputRef.current) {
        fileInputRef.current.click(); // 파일 입력 클릭
      }
    };

    const toggleSrcDropdown = () => {
      setIsSrcOpen(prev => !prev);
    };

    const toggleTarDropdown = () => {
      setIsTarOpen(prev => !prev);
    };

  const Intro: React.FC = () => {
    return (
      <div className={IntroStyles.introContainer}>
        <div className={IntroStyles.introContent}>
          <div style={{flex: "1"}}>
            <h1>Dub Your Lecture in Any Language</h1>
            <p>Global Lectures is a service that dubs your uploaded lectures into the language of your choice. To use the service, upload the lecture from your computer, select the original language and the language you want to convert it to, then click the Convert button.</p>
          </div>
          <div style={{flex: "1", textAlign: "center", display: "flex", gap: "5px", justifyContent: "center", alignItems: "center", flexDirection: "row"}}>
              <h2>convert</h2>
              <div>
                <button className={DropdownStyles.dropdownButton} onClick={toggleSrcDropdown}>{srcLang}</button>
              </div>
              {isSrcOpen && 
              <div className={DropdownStyles.scrLangDropdwonContainer}>
              {srcLangs.map(lang => (
                  <div className={DropdownStyles.langDropdownItem}>
                    <span 
                      className={DropdownStyles.langItem}
                      onClick={(e)=>{
                        e.preventDefault();
                        setSrcLang(lang);
                        setSrcIsSelected(true);
                        const newTarLangs = tarLangList[lang as Language];
                        setTarLangs(newTarLangs);
                        setTarLang(newTarLangs[0]);
                        toggleSrcDropdown();
                      }}  
                    >
                      {lang}
                    </span>
                  </div>
              ))}</div>}
              <h2>to</h2>
              <div>
                <button className={DropdownStyles.dropdownButton} onClick={toggleTarDropdown} disabled={!srcIsSelected}>{tarLang}</button>
              </div>
              {isTarOpen && 
              <div className={DropdownStyles.tarLangDropdwonContainer}>
              {tarLangs.map(lang => (
                  <div className={DropdownStyles.langDropdownItem}>
                    <span 
                      className={DropdownStyles.langItem}
                      onClick={(e)=>{
                        e.preventDefault();
                        setTarLang(lang);
                        toggleTarDropdown();
                      }}  
                    >
                      {lang}
                    </span>
                  </div>
              ))}</div>}
          </div>
        </div>
      </div>
    );
  }

  return (
    <div>
      <Intro />
      <div className={IntroStyles.contentWrapper}>
        {video === null ? (
          <div className={IntroStyles.FileuploadButtonContainer}>
            <BaseButton label="Select Video" icon={faFolderPlus} buttonStyle={IntroStyles.BaseButton} onClick={handleButtonClick} disabled={false}/>
            <input 
              ref={fileInputRef}
              type="file"
              accept="video/*"
              style={{display: "none"}} 
              onChange={handleFileChange}
            />
          </div>
      ) : (
        <div>
          <div className={IntroStyles.card}>
            <div className={IntroStyles.cardContent}>
              <div style={{width: "40%", padding: "1rem", alignSelf: "center"}}>
                <ul style={{listStyle: "none", paddingLeft: "0"}}>
                  <li style={{overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap"}}>
                    <FontAwesomeIcon icon={faFile} style={{marginRight: "1rem", textAlign: "center", width: "1.25em"}}/>
                    <span>{video.name}</span>
                  </li>
                </ul>
              </div>
              <div style={{width: "25%", whiteSpace: "nowrap", paddingLeft: "1rem", paddingRight: "1rem", alignSelf: "center"}}>
                <span>
                  <FontAwesomeIcon icon={faSyncAlt} style={{marginRight: "1rem", textAlign: "center", width: "1.25rem"}}/>
                  Convert to <b>{tarLang}</b>
                </span>
              </div>
              <div 
                style={{padding: "1rem", alignSelf: "center", flexGrow: "1"}}
              >
              </div>
              <div style={{padding: "1rem", alignSelf: "center"}}>
                <a 
                  href="Delete" 
                  onClick={e => {e.preventDefault()}}
                  style={{backgroundColor: "transparent", color: "#b53836", textDecoration: "none"}}
                >
                  <FontAwesomeIcon icon={faTimes} />
                </a>
              </div>
            </div>
          </div>
          <div style={{display: "flex", marginBottom: "1.5rem", marginTop: "1.5rem", flexDirection: "row", justifyContent: "end"}}>
            <BaseButton label="Convert" icon={faSyncAlt} buttonStyle={IntroStyles.BaseButton} onClick={() => {
              const dubData = {
                video: video,
                sourceLang: srcLang,
                targetLang: tarLang
              }
              const res = dub(dubData);
              console.log(res);
            }} disabled={tarLang === "..." && srcLang === "..."}/>
          </div>
      </div>
      )}
      </div>
    </div>
  );
};

export default Home;
