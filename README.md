# AEMA Skills

AI 숏드라마 제작을 위한 AEMA 전용 Codex 스킬 6종입니다. 9:16 세로 영상, 캐릭터·배경·소품 레퍼런스의 일관성, 제작 이력 보존을 중심으로 설계했습니다.

이미지·영상 생성, 업로드, Higgsfield Elements 등록처럼 비용이나 외부 변경이 발생하는 작업은 기본적으로 실행하지 않습니다. 먼저 dry-run 계획을 검토한 뒤 사용자가 정확한 범위를 승인해야 실행합니다.

## 빠른 시작

1. Codex에서 이 GitHub 저장소의 아래 6개 폴더를 모두 설치해 달라고 요청합니다.
2. 새 대화에서 `$aema-drama-pipeline`을 호출하고 작품 아이디어를 설명합니다.
3. 대본과 레퍼런스를 검토·승인합니다.
4. 이미지 또는 영상 생성 계획에 비용과 작업 범위가 표시되면, 원하는 항목만 명시적으로 승인합니다.

예시:

```text
$skill-installer로 비공개 GitHub 저장소 aemastudio/aema-skills의
aema-scriptwriter, aema-asset-builder, aema-seedance25-video,
aema-drama-pipeline, aema-korean-srt, aema-blender를 모두 설치해줘.
```

설치 후에는 새 대화에서 다음처럼 시작할 수 있습니다.

```text
$aema-drama-pipeline
60초짜리 9:16 로맨틱 코미디 숏드라마를 만들고 싶어.
먼저 대본과 제작 계획까지만 dry-run으로 만들어줘.
```

## 포함된 스킬

| 스킬 | 역할 |
|---|---|
| `aema-scriptwriter` | 아이디어, 시놉시스, 회차 구성, 시나리오와 대본 작성 |
| `aema-asset-builder` | 대본에서 캐릭터·배경·소품을 추출하고 일관된 이미지 레퍼런스 계획 작성 |
| `aema-seedance25-video` | 승인된 씬과 레퍼런스를 Seedance 2.5용 9:16 컷과 생성 계획으로 변환 |
| `aema-drama-pipeline` | 전체 제작 단계, 승인 지점, archive 상태를 관리하는 통합 오케스트레이터 |
| `aema-korean-srt` | 로컬 Whisper 우선 방식으로 한국어 SRT와 QC 자료 생성 |
| `aema-blender` | Blender 씬, 카메라, 조명, 재질, 애니메이션과 렌더 자동화 계획 작성 |

여섯 폴더는 공통 archive 규약을 공유하므로 함께 설치하는 것을 권장합니다.

전체 설치법, 단계별 호출 예시, archive 구조와 문제 해결은 [한국어 사용 매뉴얼](USAGE-KO.md)을 참고하세요.
