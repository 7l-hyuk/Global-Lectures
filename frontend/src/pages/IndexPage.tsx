import React, { useState } from "react";
import { faChevronRight, faDatabase, faGlobe, faMicrophoneLines, faRotate } from "@fortawesome/free-solid-svg-icons";

import styles from "../styles/IndexPage.module.css";
import { ButtonIcon, CountryButton } from "../components/Button";
import LecturePlayer from "../components/Video";
import { ServiceIntroProps } from "../types/components";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";


const ServiceIntro: React.FC<ServiceIntroProps> = ({ title, description, icon, iconColor }) => {
  return (
    <div className={styles.ServiceIntroContainer}>
      <h1 style={{color: iconColor}}>
        <FontAwesomeIcon icon={icon} />
        {title}
      </h1>
      <p>{description}</p>
    </div>
  );
};


const IndexPage: React.FC = () => {
  type LangKey = 'Korean' | 'English' | 'Japanese' | 'Chinese';
  const [activatedLang, setActivatedLang] = useState<LangKey>("Korean");
  const Languages: LangKey[] = ["Korean", "English", "Japanese", "Chinese"];

  const LangCodeMap = {
    Korean: "ko",
    English: "en",
    Japanese: "ja",
    Chinese: "zh"
  };
  return (
    <div className={styles.IndexContentContainer}>
      <h1>Dub Any Lecture, In Any Language</h1>
      <p>Multilingual lecture translation and dubbing service</p>
      <div className={styles.ButtonContainer}>
        <ButtonIcon
          icon={faChevronRight}
          label="Get Started"
          buttonType="IndexPageBotton"
          color="red"
          onClick={() => {}}
        />
        <ButtonIcon
          icon={faChevronRight}
          label="Watch Preview"
          buttonType="IndexPageBotton"
          color="gray"
          onClick={() => {}}
        />
      </div>
      <div className={styles.IndexContent}>
        <ul className={styles.ServiceIntroTable}>
          <li>
            <ServiceIntro
              title="Global Service"
              icon={faGlobe}
              iconColor="#b53836"
              description=" Global Lectures offers multilingual dubbing, so you can enjoy great lectures without language barriers—no need to re-record in every language.."
            />
          </li>
          <li>
            <ServiceIntro
              title="Dubbing Lectures"
              icon={faMicrophoneLines}
              iconColor="#27b08b"
              description="Dubbed lectures offer a more immersive experience than subtitles, and Global Lectures includes both for greater translation accuracy."
            />
          </li>
          <li>
            <ServiceIntro
              title="Lecture Database"
              icon={faDatabase}
              iconColor="#ffca16"
              description="Sign up to store your videos and subtitles online—no local storage needed. Add translations anytime, with secure Amazon S3 storage."
            />
          </li>
        </ul>
      </div>
      <div className={styles.IndexContent}>
        <div className={styles.UseCaseContent}>
          <span>
            <FontAwesomeIcon icon={faRotate} />
            Lectuer Translation
          </span>
          <h1>Use Cases of Sample Lectures</h1>
          <p>Here are sample use cases of an English lecture translated into Korean, Japanese, and Chinese. Feel free to switch languages and watch comfortably.</p>
        </div>
      </div>
      <div className={styles.IndexContent}>
        <div className={styles.LangButtonContainer}>
          <CountryButton
            country="KR"
            label={Languages[0]}
            buttonType={activatedLang == Languages[0] ? "ActivatedLangBotton" : "LangBotton"}
            color="transparent"
            onClick={() => { setActivatedLang(Languages[0]) }}
          />
          <CountryButton
            country="US"
            label={Languages[1]}
            buttonType={activatedLang == Languages[1] ? "ActivatedLangBotton" : "LangBotton"}
            color="transparent"
            onClick={() => { setActivatedLang(Languages[1]) }}
          />
          <CountryButton
            country="JP"
            label={Languages[2]}
            buttonType={activatedLang == Languages[2] ? "ActivatedLangBotton" : "LangBotton"}
            color="transparent"
            onClick={() => { setActivatedLang(Languages[2]) }}
          />
          <CountryButton
            country="CN"
            label={Languages[3]}
            buttonType={activatedLang == Languages[3] ? "ActivatedLangBotton" : "LangBotton"}
            color="transparent"
            onClick={() => { setActivatedLang(Languages[3]) }}
          />
        </div>
      </div>
      <div className={styles.IndexContent}>
        <LecturePlayer 
          videoPath="/sample.mp4"
          audioPath={`/${LangCodeMap[activatedLang]}.wav`}
          scriptPath={`/${LangCodeMap[activatedLang]}.json`}
        />
      </div>
    </div>
  );
};


export default IndexPage;