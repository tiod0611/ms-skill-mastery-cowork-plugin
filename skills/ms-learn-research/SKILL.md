---
name: ms-learn-research
description: |
  Microsoft Learn MCP 서버를 사용해 기술이나 스킬(예: React, Azure Kubernetes Service, Python, Microsoft Fabric)을 조사하고, 주제·리소스 링크·예상 소요 시간이 포함된 단계별 학습 로드맵을 구조화된 형태로 만듭니다.
  사용자가 특정 기술을 배우고/마스터하고 싶다고 하거나, 스킬에 대한 학습 경로/로드맵을 요청하거나, "React를 마스터하고 싶어", "Azure Kubernetes Service 로드맵 만들어줘", "Python을 처음부터 어떻게 배우지?", "Microsoft Fabric 학습 계획 세워줘", "Kubernetes 잘하려면 뭘 배워야 해?" 같은 말을 할 때 사용하세요.
license: MIT
metadata:
  author: MS Skill Mastery Demo
  version: "1.0"
---

# MS Learn 리서치 스킬

## 이 스킬이 하는 일

기술이나 스킬 이름이 주어지면 이 스킬은 다음을 수행합니다:

1. 사용자가 마스터하고 싶은 **대상 스킬을 확인**합니다 (필요하다면 현재 수준이나 목표도 함께).
2. **Microsoft Learn MCP 서버** 커넥터(`microsoft-learn-mcp`)를 이용해 공식 문서, 학습 경로, 모듈을 검색하며 해당 주제를 **조사**합니다.
3. 조사 결과를 순서가 있는 단계별 학습 로드맵(Beginner → Intermediate → Advanced)으로 **정리**합니다.
4. 짝을 이루는 `roadmap-html-builder` 스킬에 곧바로 전달되어 완성도 높은 HTML 페이지로 렌더링될 수 있도록 **구조화된 로드맵 콘텐츠**를 출력합니다(아래 "출력 형식" 참고).

## 언제 이 스킬을 사용하나

다음의 경우 이 스킬을 활성화하세요:
- 사용자가 기술/스킬 이름을 언급하며 배우기, 마스터하기, 공부하기를 요청할 때
- 스킬에 대한 "로드맵", "학습 경로", "학습 계획", "커리큘럼"을 요청할 때
- "X를 잘하려면 뭘 배워야 해?"라고 물을 때

예시: "React 마스터하고 싶어, 로드맵 만들어줘", "Azure Kubernetes Service 로드맵 만들어줘", "Microsoft Fabric을 처음부터 고급까지 배우고 싶어".

## 워크플로

### 1단계: 대상 스킬 확인

명확하지 않다면 사용자에게 다음을 확인합니다:
- **스킬/기술 이름** (정확히, 예: "React", "Azure Kubernetes Service (AKS)")
- 관련이 있다면 **시작 지점** (완전 초보 vs. 어느 정도 경험 있음)
- 구체적인 목표 (예: "AZ-104 합격", "프로덕션 앱 만들기")

사용자가 메시지에서 이미 스킬을 명확히 밝혔다면 여기서 멈추지 말고, 합리적인 기본값(초급부터 고급까지 전체 로드맵)으로 바로 진행하세요.

### 2단계: Microsoft Learn MCP 서버로 조사

`microsoft-learn-mcp` 커넥터(`https://learn.microsoft.com/api/mcp`)를 사용해 대상 스킬에 대한 문서를 검색·조회합니다. 스킬의 전체 흐름을 다루기 위해 여러 번 검색하세요. 예:

1. 검색: "[스킬] 시작하기 소개"
2. 검색: "[스킬] 핵심 개념 기초"
3. 검색: "[스킬] 중급 패턴 모범 사례"
4. 검색: "[스킬] 고급 아키텍처 / 프로덕션 / 자격증"
5. 검색: "[스킬] learning path" (Microsoft Learn은 전용 학습 경로가 있는 경우가 많으니 가능하면 이를 직접 링크하세요)

실제 제목과 URL을 추출할 수 있도록 가장 관련성 높은 문서/모듈 페이지를 조회하세요 — 로드맵의 모든 주제는 MCP 서버가 반환한 실제 Microsoft Learn 리소스 링크를 인용해야 합니다(URL을 임의로 만들지 마세요).

### 3단계: 단계별 로드맵 구성

조사 결과를 **순서가 있는 단계**로 그룹화합니다 — 일반적으로:
- **Beginner** (기초, 설정, 핵심 개념)
- **Intermediate** (실전 패턴, 도구, 일반적인 워크플로)
- **Advanced** (아키텍처, 성능, 보안, 프로덕션/자격증)

기술 특성에 따라 단계를 더 늘리거나 줄여도 됩니다(예: "Expert / Certification" 단계 추가). 단, 항상 순서를 유지하고 명확히 표기하세요.

각 단계마다 다음을 만듭니다:
- 짧은 단계 제목
- 단계를 완료하는 데 걸리는 **예상 시간** (예: "1-2주", "10-15시간")
- **주제** 목록, 각 주제마다:
  - 주제 이름
  - 1-2문장 설명
  - MCP 조사에서 얻은 Microsoft Learn 리소스 링크(제목 + URL)

### 4단계: 구조화된 출력 생성

`roadmap-html-builder` 스킬이 바로 파싱하고 재사용할 수 있도록 로드맵을 명확히 구분된 구조화된 콘텐츠(JSON 형태)로 출력합니다. 다음 형식을 정확히 사용하세요 (키 이름은 두 스킬 간 연결을 위한 것이므로 영어 그대로 유지하고, 값의 내용만 한국어로 작성해도 됩니다):

```json
{
  "skillName": "React",
  "summary": "이 스킬을 마스터한다는 것이 무엇을 의미하는지 한두 문장으로 요약합니다.",
  "stages": [
    {
      "title": "Beginner",
      "estimatedTime": "2-3주",
      "topics": [
        {
          "name": "JSX & Components",
          "description": "JSX가 React 엘리먼트로 컴파일되는 방식과 컴포넌트를 조합하는 방법을 배웁니다.",
          "resourceTitle": "Describe UI with JSX - Microsoft Learn",
          "resourceUrl": "https://learn.microsoft.com/..."
        }
      ]
    },
    {
      "title": "Intermediate",
      "estimatedTime": "3-4주",
      "topics": [ /* ... */ ]
    },
    {
      "title": "Advanced",
      "estimatedTime": "4-6주",
      "topics": [ /* ... */ ]
    }
  ]
}
```

사용자가 채팅에서 HTML로 변환되기 전에 검토할 수 있도록, 위 JSON 블록의 바로 위나 아래에 동일한 내용을 읽기 쉬운 마크다운(단계 헤더, 링크가 포함된 불릿 목록)으로도 함께 제시하세요.

## 출력 형식

이 스킬의 최종 채팅 응답에는 다음이 포함되어야 합니다:
1. 조사 중인 스킬을 확인하는 짧은 도입 문장
2. 구조화된 JSON 로드맵 블록 (위 형식 그대로의 ```json 코드 블록)
3. 동일한 로드맵을 사람이 읽기 쉬운 마크다운으로 요약 (단계 → 주제 → 링크 → 예상 시간)

이 구조화된 출력은 `roadmap-html-builder` 스킬을 위한 인계 계약(hand-off contract)입니다 — JSON 블록을 생략하지 말고, 리소스 링크를 지어내지 마세요. 모든 `resourceUrl`은 실제 Microsoft Learn MCP 검색/조회 결과에서 나와야 합니다.

## 참고 사항

- 모든 리서치는 Microsoft Learn MCP 서버(`https://learn.microsoft.com/api/mcp`) 커넥터를 통해 이루어져야 합니다 — 리소스 링크에 일반적인 웹 지식을 대신 사용하지 마세요.
- 틈새 기술이라 MCP 검색 결과가 제한적이라면 이를 명시적으로 언급하고, 가능한 최선의 공식 Microsoft Learn 리소스나 일반 Microsoft Learn 검색/랜딩 페이지를 대체 링크로 사용하세요.
- 사용자가 더 세분화된 내용을 요청하지 않는 한, 가독성을 위해 단계 수는 3~4개로 유지하세요.
