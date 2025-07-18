import React, { useState } from "react";
import { faChevronRight, faEarthOceania } from "@fortawesome/free-solid-svg-icons";

import styles from "../styles/IndexPage.module.css";
import { ButtonIcon, CountryButton } from "../components/Button";
import LecturePlayer from "../components/Video";
import { ServiceIntroProps } from "../types/components";


const ServiceIntro: React.FC<ServiceIntroProps> = ({title, description}) => {
    return (
        <div className={styles.ServiceIntroContainer}>
            <h1>{title}</h1>
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
                    <li><ServiceIntro title="test" description="dsadsaadsad" /></li>
                    <li><ServiceIntro title="test" description="dsadsaadsad" /></li>
                    <li><ServiceIntro title="test" description="dsadsaadsad" /></li>
                </ul>
            </div>
            <div className={styles.IndexContent}>
                <div className={styles.LangButtonContainer}>
                    <CountryButton
                        country="KR"
                        label={Languages[0]}
                        buttonType={activatedLang == Languages[0] ? "ActivatedLangBotton" : "LangBotton"}
                        color="transparent"
                        onClick={() => {setActivatedLang(Languages[0])}}
                    />
                    <CountryButton
                        country="US"
                        label={Languages[1]}
                        buttonType={activatedLang == Languages[1] ? "ActivatedLangBotton" : "LangBotton"}
                        color="transparent"
                        onClick={() => {setActivatedLang(Languages[1])}}
                    />
                    <CountryButton
                        country="JP"
                        label={Languages[2]}
                        buttonType={activatedLang == Languages[2] ? "ActivatedLangBotton" : "LangBotton"}
                        color="transparent"
                        onClick={() => {setActivatedLang(Languages[2])}}
                    />
                    <CountryButton
                        country="CN"
                        label={Languages[3]}
                        buttonType={activatedLang == Languages[3] ? "ActivatedLangBotton" : "LangBotton"}
                        color="transparent"
                        onClick={() => {setActivatedLang(Languages[3])}}
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