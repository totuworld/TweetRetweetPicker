# TweetRetweetPicker

이 프로젝트는 트위터(현재 X)에서 특정 트윗을 리트윗한 사용자들의 데이터를 수집하고, 그 목록에서 무작위로 당첨자를 추첨하는 파이썬 스크립트들로 구성되어 있습니다.

## 코드 제작과정
[![Video Label](https://i.ytimg.com/vi/fnw0Nd8TTmU/0.jpg)](https://www.youtube.com/watch?v=fnw0Nd8TTmU)

## 프로젝트 파일 구성

이 프로젝트는 크게 세 가지 파이썬 스크립트로 구성됩니다.

*   **`00_twitter_login.py` 또는 `twitter_login.py`:** 트위터에 로그인하는 과정을 처리하고, 세션 정보를 `session.json` 파일에 저장합니다.
*   **`01_get_id.py` 또는 `get_id.py`:** `session.json` 파일을 사용하여 트위터에 로그인한 상태를 유지하고, 특정 트윗의 리트윗 사용자 목록 페이지로 이동하여 사용자 ID와 닉네임을 수집합니다. 수집한 결과는 `retweet.csv` 파일에 저장됩니다.
*   **`02_winner.py` 또는 `winner.py`:** `retweet.csv` 파일을 읽어와서, 파일 내의 사용자 목록에서 지정된 수만큼의 당첨자를 무작위로 추첨합니다. 당첨자를 발표할 때 "두구두구두구" 효과와 "짠!" 효과를 사용하여 시각적인 재미를 더합니다.

**참고:** `00_twitter_login.py`와 `twitter_login.py`, `01_get_id.py`와 `get_id.py`, `02_winner.py`와 `winner.py`는 각각 동일한 기능을 하는 파일이며, 파일명만 다를 뿐입니다.

## 파일별 역할 및 수정 지점

### `00_twitter_login.py` 또는 `twitter_login.py`

*   **역할:**
    *   눈에 보이는 브라우저 창을 통해 트위터에 로그인합니다.
    *   `session.json` 파일이 이미 존재한다면, 기존 세션을 사용하려고 시도합니다.
    *   `session.json` 파일이 존재하지 않으면, 브라우저 창에서 직접 로그인하도록 요청합니다.
    *   로그인 후, 세션 정보(쿠키, 로컬 스토리지)를 `session.json` 파일에 저장합니다.
*   **사용 방법:**
    1.  스크립트를 실행합니다: `python 00_twitter_login.py` 또는 `python twitter_login.py`
    2.  안내 메시지가 표시되면, 열린 브라우저 창에서 직접 트위터 계정 정보를 입력하여 로그인합니다.
    3.  로그인이 완료되면, 세션 정보가 `session.json` 파일에 저장됩니다.
*   **수정 지점:**
    *   이 파일은 트위터 로그인 프로세스가 변경되지 않는 한 수정할 필요가 없습니다.
    *   만약 트위터에서 로그인 과정이나 페이지 구조를 변경한다면, 로그인 폼과 버튼을 찾아 상호작용하는 데 사용되는 CSS 선택자를 수정해야 합니다.

### `01_get_id.py` 또는 `get_id.py`

*   **역할:**
    *   `session.json` 파일을 읽어와서, 트위터 로그인 상태를 유지합니다.
    *   지정된 트윗 URL( `/retweets`가 없는 URL)로 이동합니다.
    *   트윗 페이지 로드 후 5초 동안 대기합니다.
    *   해당 트윗의 `/retweets` 페이지로 이동합니다.
    *   리트윗 페이지 로드 후 5초 동안 대기합니다.
    *   페이지를 여러 번 부분적으로 스크롤하여, 리트윗 정보를 모두 로드합니다.
    *   각 리트윗 사용자 요소에서 사용자 ID와 닉네임을 추출합니다.
    *   중복된 사용자 ID는 제거합니다.
    *   수집된 데이터(사용자 ID, 닉네임)를 `retweet.csv` 파일에 저장합니다.
*   **사용 방법:**
    1.  `session.json` 파일이 있는지 확인합니다. (`00_twitter_login.py` 또는 `twitter_login.py`를 실행하여 생성 가능)
    2.  스크립트를 실행합니다: `python 01_get_id.py` 또는 `python get_id.py`
    3.  추출된 데이터가 `retweet.csv` 파일에 저장됩니다.
*   **수정 지점:**
    *   **`tweet_url`:** `get_retweeters()` 함수 내의 `tweet_url` 변수 값을 변경하여, 다른 트윗을 대상으로 할 수 있습니다.
    *   **`max_scroll`:** `max_scroll` 변수를 변경하여, 스크롤 횟수를 늘리거나 줄일 수 있습니다. 스크롤 횟수가 많을수록 더 많은 데이터를 수집하지만, 시간이 더 오래 걸립니다. 테스트를 위해서는 적게, 많은 데이터를 위해서는 많이 설정하는 것이 좋습니다.
    *   **`scroll_delay`:** `scroll_delay` 변수를 변경하여, 스크롤 후 대기 시간을 조절할 수 있습니다. 데이터가 누락되는 현상이 발생하면 대기 시간을 늘리는 것이 좋습니다.
    *   **CSS 선택자:** 만약 트위터에서 HTML 구조를 변경하게 되면, 사용자 정보(ID, 닉네임)를 찾기 위해 사용되는 CSS 선택자를 수정해야 합니다.

### `02_winner.py` 또는 `winner.py`

*   **역할:**
    *   `retweet.csv` 파일을 읽어옵니다.
    *   `retweet.csv` 파일 내의 사용자 목록에서 지정된 수만큼의 당첨자를 무작위로 추첨합니다.
    *   각 당첨자 발표 전에 "두구두구두구" 효과를 표시합니다.
    *   각 당첨자를 "🎉 짠!" 효과와 함께 발표합니다.
    *   마지막에 모든 당첨자의 목록을 출력합니다.
*   **사용 방법:**
    1.  `retweet.csv` 파일이 있는지 확인합니다. (`01_get_id.py` 또는 `get_id.py`를 실행하여 생성 가능)
    2.  스크립트를 실행합니다: `python 02_winner.py` 또는 `python winner.py`
    3.  터미널에 당첨자 정보가 시각적인 효과와 함께 출력됩니다.
*   **수정 지점:**
    *   **`csv_file`:** `main()` 함수 내의 `csv_file` 변수 값을 변경하여, 다른 CSV 파일을 사용할 수 있습니다.
    *   **`num_winners`:** `main()` 함수 내의 `num_winners` 변수 값을 변경하여, 당첨자 수를 조절할 수 있습니다.
    *   **"두구두구두구" 및 "짠!" 효과:** "두구" 와 "짠!" 의 횟수와 문구는 해당 부분을 수정해서 변경할 수 있습니다.

## 설치 요구 사항

1.  **파이썬:**
    *   시스템에 파이썬 3.1 이상이 설치되어 있어야 합니다.
    *   터미널을 열고 `python --version` 또는 `python3 --version` 명령어를 실행하여 파이썬 버전을 확인할 수 있습니다.
    *   파이썬이 설치되어 있지 않다면, 공식 파이썬 웹사이트에서 다운로드하여 설치할 수 있습니다: [https://www.python.org/downloads/](https://www.python.org/downloads/)

2.  **Playwright 및 기타 라이브러리:**
    *   **Playwright 설치:**
        ```bash
        pip install playwright
        playwright install
        ```
    *   이 명령어를 실행하면, Playwright 브라우저 바이너리(Chromium, Firefox, WebKit)가 함께 설치됩니다.
    *   **기타 필수 라이브러리**:  `csv`, `random`, `time`, `os`
    *   위 라이브러리들은 파이썬 내장 모듈이므로, 별도의 설치가 필요하지 않습니다.

## 사용 방법

1.  **트위터 로그인 및 세션 저장:**
    ```bash
    python 00_twitter_login.py
    # 또는
    python twitter_login.py
    ```
2.  **리트윗 사용자 ID 수집:**
    ```bash
    python 01_get_id.py
    # 또는
    python get_id.py
    ```
3.  **당첨자 추첨:**
    ```bash
    python 02_winner.py
    # 또는
    python winner.py
    ```

## 저자 정보
이런 업무 자동화 방법에 관한 저서가 있습니다. 많은 관심 부탁드려요.

아울러 오픈 채팅방을 통해 도움을 받으실 수 있습니다.

[**정말 쉽네? 챗GPT 구글 업무 자동화**](https://search.shopping.naver.com/book/catalog/53074830698?cat_id=50010702&frm=PBOKPRO&query=%EC%86%A1%EC%9A%94%EC%B0%BD&NaPm=ct%3Dm7u5rfsg%7Cci%3D8f5ca1839645e9f84c834e3ed37501b72cfb1638%7Ctr%3Dboknx%7Csn%3D95694%7Chk%3D20ea94c2725d723f05610deb8468f5cc05a4066b)

## 면책 조항

* 이 스크립트를 트위터의 서비스 약관을 존중하며, 윤리적으로 책임감 있게 사용해 주시기 바랍니다.
* 웹사이트의 구조는 변경될 수 있으며, 이로 인해 스크립트가 작동을 멈출 수 있습니다. 이런 경우, 코드 내의 CSS 선택자나 로직을 수정해야 합니다.
* 2단계 인증이 설정되어 있을 경우, 코드가 동작하지 않을 수 있습니다.

