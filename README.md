## Global Lectures: AI Lecture Dubbing Service


## Contribution

> [!NOTE]
> 해당 프로젝트에 기여하기 위해서 `git`과 `uv`가 필요합니다. 
> 
> [git 다운로드](https://git-scm.com/downloads)
>
> [uv 다운로드](https://docs.astral.sh/uv/getting-started/installation/)


* 아래 명령어를 통해 Github Repository를 clone 해 주세요.

```bash
git clone https://github.com/7l-hyuk/Global-Lectures.git
```

* clone 된 디렉터터리에서 backend 디렉터리로 이동 및 브랜치 생성

```bash
cd Global_Lectures/backend
git checkout -b feat/analysis-router
```

* 의존성 설치

```bash
uv sync
```

* 작업 디렉터리로 이동
  
```bsah
cd src/routes
```

이제 해당 analysis.py 스크립트에 있는 라우터를 개발해 주시면 됩니다.

개발이 끝나면 아래 과정을 통해 PR을 보내주세요

```bash
git add .
git commit -m "FEAT(router): analysis router"
git push -u origin feat/analysis-router

# 이후 dev 브랜치에 PR
```

