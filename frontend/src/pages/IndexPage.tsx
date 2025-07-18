import React, { useState } from "react";
import { faChevronRight, faDatabase, faGlobe, faMicrophoneLines } from "@fortawesome/free-solid-svg-icons";

import styles from "../styles/IndexPage.module.css";
import { ButtonIcon, CountryButton } from "../components/Button";
import LecturePlayer from "../components/Video";
import { ServiceIntroProps } from "../types/components";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";


const ServiceIntro: React.FC<ServiceIntroProps> = ({ title, description, icon, iconColor }) => {
  return (
    <div className={styles.ServiceIntroContainer}>
      <h1>
        <FontAwesomeIcon icon={icon} style={{color: iconColor}} />
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
      <div style={{boxShadow: " -53px -6px 87px 68px rgba(108,21,21, 0.32), 53px 13px 100px 50px rgba(98,17,17, 0.37)", width: "40%"}} />
      <div className={styles.ButtonContainer}>
        <ButtonIcon
          icon={faChevronRight}
          label="Get Started"
          buttonType="IndexPageBotton"
          color="red"
          onClick={() => { }}
        />
        <ButtonIcon
          icon={faChevronRight}
          label="Watch Preview"
          buttonType="IndexPageBotton"
          color="gray"
          onClick={() => { }}
        />
      </div>
      <div className={styles.IndexContent}>
        <ul className={styles.ServiceIntroTable}>
          <li>
            <ServiceIntro
              title="Global Service"
              icon={faGlobe}
              iconColor="#baa7ff"
              description=" Global Lectures supports multilingual lecture dubbing. Choose any language you prefer.
                          Now, you won't miss out on great lectures just because they're in a language you don't understand, 
                          and there's no need to record the same lecture multiple times to offer it in different languages."
            />
          </li>
          <li>
            <ServiceIntro
              title="Dubbing Lectures"
              icon={faMicrophoneLines}
              iconColor="#27b08b"
              description="Dubbed lectures offer a more immersive experience compared to subtitles. 
                          Global Lectures also provides subtitles alongside dubbing to ensure even greater accuracy in lecture translation."
            />
          </li>
          <li>
            <ServiceIntro
              title="Lecture Database"
              icon={faDatabase}
              iconColor="#ffca16"
              description="By signing up, you can store your converted videos and subtitles directly on our website—without taking up space on your local computer. 
                          You can also add translations into other languages anytime you want. 
                          All data is securely stored using Amazon S3."
            />
          </li>
        </ul>
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
        <LecturePlayer videoPath="/sample.mp4" audioPath={`/${LangCodeMap[activatedLang]}.wav`} />
      </div>
    </div>
  );
};


export default IndexPage;