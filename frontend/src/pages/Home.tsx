import React, { useState, useRef, useEffect } from "react";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faFolderPlus, faFile, faSyncAlt, faTimes, faGlobe, faDatabase, faHeadphonesSimple, faRotate, faChevronDown, faGear } from "@fortawesome/free-solid-svg-icons";
import { IconDefinition } from "@fortawesome/free-solid-svg-icons";

import IntroStyles from "../css/Intro.module.css";
import DropdownStyles from "../css/Dropdown.module.css";
import { BaseButton } from "../components/Form";
import { dub } from "../api/service";

const Home: React.FC = () => {
  const fileInputRef = useRef<HTMLInputElement>(null);
  const srcDropdownRef = useRef<HTMLDivElement>(null);
  const tarDropdownRef = useRef<HTMLDivElement>(null);

  const [video, setVideo] = useState<File | null>(null);
  const [srcLang, setSrcLang] = useState("...");
  const [srcIsSelected, setSrcIsSelected] = useState(false);
  const [tarLang, setTarLang] = useState("...");
  const [tarLangs, setTarLangs] = useState(["..."]);
  const [isSrcOpen, setIsSrcOpen] = useState(false);
  const [isTarOpen, setIsTarOpen] = useState(false);
  const [showAdvanced, setShowAdvanced] = useState(false);
  const [sttModel, setSttModel] = useState("basic model");
  const [translationModel, setTranslationModel] = useState("basic model");
  const [ttsModel, setTtsModel] = useState("basic model");

  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (srcDropdownRef.current && !srcDropdownRef.current.contains(event.target as Node)) {
        setIsSrcOpen(false);
      }
      if (tarDropdownRef.current && !tarDropdownRef.current.contains(event.target as Node)) {
        setIsTarOpen(false);
      }
    };

    const handleEscKey = (event: KeyboardEvent) => {
      if (event.key === "Escape") {
        setIsSrcOpen(false);
        setIsTarOpen(false);
      }
    };

    document.addEventListener("mousedown", handleClickOutside);
    document.addEventListener("keydown", handleEscKey);
    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
      document.removeEventListener("keydown", handleEscKey);
    };
  }, []);

  const srcLangs = ["Korean", "English", "Japanese", "Chinese"];
  type Language = 'Korean' | 'English' | 'Japanese' | 'Chinese';
  const tarLangList: { [key in Language]: string[] } = {
    Korean: ["English", "Japanese", "Chinese"],
    English: ["Korean", "Japanese", "Chinese"],
    Japanese: ["Korean", "English", "Chinese"],
    Chinese: ["Korean", "English", "Japanese"],
  };

  interface DescriptionProps {
    icon: IconDefinition;
    title: string;
    description: string;
  }

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      setVideo(file);
    }
  };

  const handleButtonClick = () => {
    if (fileInputRef.current) {
      fileInputRef.current.click();
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
          <div style={{ flex: "1" }}>
            <h1>Dub Your Lecture in Any Language</h1>
            <p>Global Lectures is a service that dubs your uploaded lectures into the language of your choice. To use the service, upload the lecture from your computer, select the original language and the language you want to convert it to, then click the Convert button.</p>
          </div>
          <div style={{ flex: "1", textAlign: "center", display: "flex", gap: "5px", justifyContent: "center", alignItems: "center", flexDirection: "row" }}>
            <h2>convert</h2>
            <div>
              <button className={DropdownStyles.dropdownButton} onClick={toggleSrcDropdown}>{srcLang}</button>
            </div>
            {isSrcOpen && (
              <div ref={srcDropdownRef} className={DropdownStyles.scrLangDropdwonContainer}>
                {srcLangs.map(lang => (
                  <div className={DropdownStyles.langDropdownItem} key={lang}>
                    <span
                      className={DropdownStyles.langItem}
                      onClick={(e) => {
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
                ))}
              </div>
            )}
            <h2>to</h2>
            <div>
              <button className={DropdownStyles.dropdownButton} onClick={toggleTarDropdown} disabled={!srcIsSelected}>{tarLang}</button>
            </div>
            {isTarOpen && (
              <div ref={tarDropdownRef} className={DropdownStyles.tarLangDropdwonContainer}>
                {tarLangs.map(lang => (
                  <div className={DropdownStyles.langDropdownItem} key={lang}>
                    <span
                      className={DropdownStyles.langItem}
                      onClick={(e) => {
                        e.preventDefault();
                        setTarLang(lang);
                        toggleTarDropdown();
                      }}
                    >
                      {lang}
                    </span>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>
    );
  };

  const Description: React.FC<DescriptionProps> = ({ icon, title, description }) => {
    return (
      <div className={IntroStyles.DescriptionBody}>
        <div style={{ fontSize: "5rem", flex: "0 0 33.33%", maxWidth: "33.33%", textAlign: "center", alignContent: "center" }}>
          <FontAwesomeIcon icon={icon} />
        </div>
        <div style={{ flex: "0 0 66.66%", maxWidth: "66.66%" }}>
          <h3 style={{ margin: "0", fontSize: "1.51rem", marginBottom: ".5rem" }}>{title}</h3>
          <p style={{ marginTop: "0", marginBottom: "0", fontSize: "1rem", fontWeight: "400" }}>{description}</p>
        </div>
      </div>
    );
  };

  return (
    <div>
      <Intro />
      <div className={IntroStyles.contentWrapper}>
        {video === null ? (
          <div className={IntroStyles.FileuploadButtonContainer}>
            <BaseButton label="Select Video" icon={faFolderPlus} buttonStyle={IntroStyles.BaseButton} onClick={handleButtonClick} disabled={false} />
            <input
              ref={fileInputRef}
              type="file"
              accept="video/*"
              style={{ display: "none" }}
              onChange={handleFileChange}
            />
          </div>
        ) : (
          <div>
            <div className={IntroStyles.card}>
              <div className={IntroStyles.cardContent}>
                <div style={{ width: "40%", padding: "1rem", alignSelf: "center" }}>
                  <ul style={{ listStyle: "none", paddingLeft: "0" }}>
                    <li style={{ overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}>
                      <FontAwesomeIcon icon={faFile} style={{ marginRight: "1rem", textAlign: "center", width: "1.25em" }} />
                      <span>{video.name}</span>
                    </li>
                  </ul>
                </div>
                <div style={{ width: "25%", whiteSpace: "nowrap", paddingLeft: "1rem", paddingRight: "1rem", alignSelf: "center" }}>
                  <span>
                    <FontAwesomeIcon icon={faSyncAlt} style={{ marginRight: "1rem", textAlign: "center", width: "1.25rem" }} />
                    Convert to <b>{tarLang}</b>
                  </span>
                </div>
                <div style={{ padding: "1rem", alignSelf: "center", flexGrow: "1" }}></div>
                <div style={{ padding: "1rem", alignSelf: "center" }}>
                  <a
                    href="Delete"
                    onClick={e => {
                      e.preventDefault();
                      setVideo(null);
                      if (fileInputRef.current) {
                        fileInputRef.current.value = "";
                      }
                    }}
                    style={{ backgroundColor: "transparent", color: "#b53836", textDecoration: "none" }}
                  >
                    <FontAwesomeIcon icon={faTimes} />
                  </a>
                </div>
              </div>
            </div>
            <div style={{ padding: "1rem", alignSelf: "center" }}>
              <div onClick={() => setShowAdvanced(prev => !prev)} className={IntroStyles.advancedToggle}>
                <FontAwesomeIcon icon={faGear} style={{paddingRight: "0.5rem"}}/>
                <span>Advanced Settings</span>
                <FontAwesomeIcon icon={faChevronDown} style={{ marginLeft: "0.5rem" }} />
              </div>
            </div>
            {showAdvanced && (
              <div className={IntroStyles.advancedSettingsBox}>
                <div className={IntroStyles.advancedSettingsRow}>
                  <label className={IntroStyles.advancedSettingsLabel}>STT Model</label>
                  <select className={IntroStyles.advancedSettingsSelect} value={sttModel} onChange={(e) => setSttModel(e.target.value)}>
                    <option value="basic model">Basic Model</option>
                    <option value="advanced model">Advanced Model</option>
                  </select>
                </div>

                <div className={IntroStyles.advancedSettingsRow}>
                  <label className={IntroStyles.advancedSettingsLabel}>Translation Model</label>
                  <select className={IntroStyles.advancedSettingsSelect} value={translationModel} onChange={(e) => setTranslationModel(e.target.value)}>
                    <option value="basic model">Basic Model</option>
                    <option value="advanced model">Advanced Model</option>
                  </select>
                </div>
                
                <div className={IntroStyles.advancedSettingsRow}>
                  <label className={IntroStyles.advancedSettingsLabel}>TTS Model</label>
                  <select className={IntroStyles.advancedSettingsSelect} value={ttsModel} onChange={(e) => setTtsModel(e.target.value)}>
                    <option value="basic model">Basic Model</option>
                    <option value="advanced model">Advanced Model</option>
                  </select>
                </div>
              </div>
            )}
            <div style={{ display: "flex", marginBottom: "1.5rem", marginTop: "1.5rem", flexDirection: "row", justifyContent: "end" }}>
              <BaseButton
                label="Convert"
                icon={faSyncAlt}
                buttonStyle={IntroStyles.BaseButton}
                onClick={() => {
                  const dubData = {
                    video: video,
                    sourceLang: srcLang,
                    targetLang: tarLang,
                    sttModel: sttModel,
                    ttsModel: ttsModel,
                    translationModel: translationModel
                  };
                  const res = dub(dubData);
                  console.log(res);
                }}
                disabled={tarLang === "..." && srcLang === "..."}
              />
            </div>
          </div>
        )}
      </div>
      <div className={IntroStyles.contentWrapper} style={{ display: "flex" }}>
        <div className={IntroStyles.DescriptionRow}>
          <Description
            icon={faGlobe}
            title="Global Service"
            description="
            Global Lectures supports multilingual lecture dubbing.
            Choose any language you prefer. 
            Now, you won't miss out on great lectures just because they're in a language you don't understand, 
            and there's no need to record the same lecture multiple times to offer it in different languages."
          />
          <Description
            icon={faHeadphonesSimple}
            title="Dubbing Lectures"
            description="
              Dubbed lectures offer a more immersive experience compared to subtitles. 
              Global Lectures also provides subtitles alongside dubbing to ensure even greater accuracy in lecture translation."
          />
        </div>
        <div className={IntroStyles.DescriptionRow}>
          <Description
            icon={faRotate}
            title="Fast Conversion"
            description="
              The Global Lectures paid plan delivers dubbed versions of one-hour videos in just 10 minutes.
              Quickly translate and watch the lectures you want.
            "
          />
          <Description
            icon={faDatabase}
            title="Lecture Database"
            description="
              By signing up, you can store your converted videos and subtitles directly on our website—without taking up space on your local computer. 
              You can also add translations into other languages anytime you want. All data is securely stored using Amazon S3.
            "
          />
        </div>
      </div>
    </div>
  );
};

export default Home;
