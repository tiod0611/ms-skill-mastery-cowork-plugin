# MS Skill Mastery — Copilot Cowork 플러그인

> **MS Skill Mastery**는 사용자가 배우고 싶은 기술/스킬(예: "React", "Azure Kubernetes Service")을 말하면, **Microsoft Learn MCP 서버**로 실제 문서를 조사(research)하여 단계별 학습 로드맵을 만들고, 이를 항상 동일한 디자인의 **HTML 페이지**로 시각화해 주는 Copilot Cowork 플러그인입니다.

이 저장소 자체가 하나의 Cowork 플러그인 패키지입니다 — [PaoloPia/CopilotDevCamp-for-cowork](https://github.com/PaoloPia/CopilotDevCamp-for-cowork) 컨벤션을 따라 `manifest.json`을 비롯한 모든 플러그인 파일을 저장소 최상위에 배치했으며, 플러그인 사용에 꼭 필요한 파일만 남겨 최소 구성으로 유지합니다.

## 개요 (Overview)

이 플러그인은 두 개의 스킬(Skill)과 한 개의 원격 MCP 커넥터(Connector)로 구성됩니다.

```
사용자: "React 마스터하고 싶어, 로드맵 만들어줘"
   └─▶ ms-learn-research 스킬이 Microsoft Learn MCP로 조사 → 구조화된 로드맵(JSON) 생성

사용자: "이걸 HTML 로드맵 페이지로 만들어줘"
   └─▶ roadmap-html-builder 스킬이 template.html에 내용을 채워 완성된 HTML 파일 생성
```

두 스킬을 분리한 이유는 **리서치(콘텐츠 생성)**와 **렌더링(시각화)**의 관심사를 분리하기 위함입니다. 덕분에 어떤 기술을 조사하든 항상 **동일한 디자인 템플릿**으로 결과물이 나와서, 여러 번 생성해도 일관된 품질과 룩앤필(look & feel)을 유지할 수 있습니다.

## 폴더 구조

```
ms-skill-mastery-cowork-plugin/         (저장소 루트 = 플러그인 루트)
├── manifest.json                 # Teams/Cowork 앱 매니페스트
├── color.png                     # 192x192 컬러 아이콘
├── outline.png                   # 32x32 아웃라인 아이콘
├── .gitignore
├── README.md                     # 이 문서
└── skills/
    ├── ms-learn-research/
    │   └── SKILL.md              # 기술 리서치 → 구조화된 로드맵 생성
    └── roadmap-html-builder/
        ├── SKILL.md              # 로드맵 → HTML 렌더링
        └── template.html         # 재사용 가능한 HTML 템플릿 (디자인 일관성의 핵심)
```

## 스킬(Skill) 소개 & 예시 트리거 문장

### 1. `ms-learn-research`
Microsoft Learn MCP 서버를 통해 기술 문서를 검색·수집하고, **Beginner → Intermediate → Advanced** 단계별 로드맵(주제, 설명, MS Learn 링크, 예상 소요 시간 포함)을 구조화된 형태(JSON + 마크다운)로 만듭니다.

예시 트리거 프롬프트:
- "I want to master React, give me a roadmap"
- "Azure Kubernetes Service 로드맵 만들어줘"
- "Python을 처음부터 마스터하려면 뭘 배워야 해?"

### 2. `roadmap-html-builder`
`ms-learn-research`가 만든 구조화된 로드맵 콘텐츠를 받아, 같은 스킬 폴더에 번들된 `template.html`의 플레이스홀더(`{{SKILL_NAME}}`, `{{STAGE_TITLE}}` 등)를 채워서 **독립 실행 가능한(self-contained)** HTML 파일 하나를 완성합니다.

예시 트리거 프롬프트:
- "turn this into an HTML roadmap page"
- "이 로드맵을 HTML 페이지로 만들어줘"
- "render this as a webpage"

> 💡 두 스킬은 순서대로(리서치 → 렌더링) 함께 사용하도록 설계되었습니다. 같은 대화에서 첫 스킬의 결과를 그대로 두 번째 스킬에 넘기면 됩니다.

## 예시 프롬프트 모음 (사용자에게 안내할 때)

Cowork 관리 센터의 앱 설명(`manifest.json`의 `description.full`)과 두 스킬의 `description`에도 아래와 같은 트리거 문구가 포함되어 있어, 사용자가 이런 식으로 말하면 자연스럽게 인식됩니다.

**단계별로 나눠 요청하기**
1. "React 마스터하고 싶어, 로드맵 만들어줘" → `ms-learn-research` 트리거
2. "이걸 HTML 로드맵 페이지로 만들어줘" → `roadmap-html-builder` 트리거

**한 번에 요청하기** (두 스킬이 같은 턴에서 순차적으로 실행됨)
- "Copilot Cowork 스킬을 마스터 하고 싶어. 자료 조사해서, 학습 로드맵으로 그려줘."
- "Azure Kubernetes Service를 배우고 싶어. 조사해서 로드맵 페이지로 만들어줘."
- "Python 학습 로드맵을 HTML로 바로 만들어줘."

## 사용하는 MCP 커넥터

| 커넥터 ID | 표시 이름 | 엔드포인트 | 인증 |
|---|---|---|---|
| `microsoft-learn-mcp` | Microsoft Learn MCP Server | `https://learn.microsoft.com/api/mcp` | `None` (익명/공개 접근) |

이 커넥터는 `ms-learn-research` 스킬이 실제 Microsoft Learn 문서를 검색(search)·조회(fetch)하는 데 사용됩니다. 로드맵의 모든 리소스 링크는 이 MCP 서버가 반환한 실제 문서 URL이어야 합니다(임의로 지어낸 링크 금지).

## 사전 준비 사항 (Prerequisites)

- 압축 프로그램(Windows 탐색기 내장 압축, macOS Finder, 또는 `zip`/`Compress-Archive` 명령) 사용 가능 환경
- Copilot Cowork 플러그인을 업로드할 수 있는 Microsoft 365 관리자 권한 (조직 배포 시)

## 패키징 (Build)

이 저장소는 별도의 빌드 도구 없이, 아래 파일/폴더만 압축하면 바로 업로드용 `.zip`이 됩니다:

```
manifest.json, color.png, outline.png, skills/
```

**GitHub에서 바로 ZIP 다운로드하는 방법(권장)**: 저장소 페이지에서 **Code → Download ZIP**으로 전체 저장소를 내려받은 뒤, 압축을 풀고 그 안에서 위 4개 항목(`manifest.json`, `color.png`, `outline.png`, `skills/`)만 다시 선택해 압축하면 됩니다. 모든 플러그인 파일이 저장소 최상위에 있어 하위 폴더를 찾아 들어갈 필요가 없습니다.

**직접 압축하는 방법**:

```powershell
# Windows (PowerShell)
Compress-Archive -Path manifest.json, color.png, outline.png, skills -DestinationPath ms-skill-mastery.zip -Force
```

```bash
# macOS / Linux
zip -r ms-skill-mastery.zip manifest.json color.png outline.png skills/
```

## Copilot Cowork에 업로드/설치하는 방법

1. 위 방법으로 `ms-skill-mastery.zip`을 준비합니다.
2. **Microsoft 365 관리 센터**(admin.microsoft.com)에 관리자로 로그인합니다.
3. **Copilot** (또는 **Agents**) 섹션으로 이동합니다.
4. **Upload Agent**(에이전트 업로드) 옵션을 선택하고, 생성한 zip 파일을 업로드합니다.
5. 배포 범위(전체 조직 / 특정 그룹 / 특정 사용자)를 설정하고 게시합니다.
6. 사용자는 Copilot Cowork에서 플러그인을 활성화한 뒤, 위 예시 트리거 문장으로 대화를 시작할 수 있습니다.

## 배포 후 스킬 검증 방법 (Validation)

1. `manifest.json`이 올바른 JSON인지 확인:
   ```powershell
   Get-Content manifest.json | ConvertFrom-Json | Out-Null
   ```
   또는
   ```bash
   python -m json.tool manifest.json > /dev/null
   ```
2. 각 `SKILL.md`의 YAML 프런트매터(`name:`)가 폴더명과 정확히 일치하는지 확인합니다 (`ms-learn-research`, `roadmap-html-builder`).
3. Cowork에서 플러그인을 활성화한 뒤:
   - "I want to master <기술명>, give me a roadmap" 이라고 요청 → `ms-learn-research`가 트리거되어 Microsoft Learn MCP 검색 결과와 함께 구조화된 로드맵(JSON + 마크다운)을 반환하는지 확인합니다.
   - 이어서 "turn this into an HTML roadmap page"라고 요청 → `roadmap-html-builder`가 트리거되어 `template.html` 디자인을 그대로 유지한 완성된 HTML이 반환되는지 확인합니다.
   - 서로 다른 기술(예: React, AKS, Python)로 반복 생성해도 **HTML 디자인이 항상 동일하게 유지되는지** 확인합니다 — 이것이 템플릿 재사용 방식의 핵심 가치입니다.

## 참고 자료

- Cowork 플러그인 모델 설명 (한국어): https://chichoi1991.github.io/Agent_Blog/chapters/cowork-dc2-plugins/
- 참고한 예제 플러그인 저장소: https://github.com/PaoloPia/CopilotDevCamp-for-cowork
- Microsoft Learn MCP Server: https://learn.microsoft.com/api/mcp

---

실제 프로덕션 배포 전에는 조직의 거버넌스·보안 정책에 맞게 검토해야 합니다.
