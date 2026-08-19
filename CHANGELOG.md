# Changelog

## [Unreleased]

### Added
### Changed
### Fixed
### Removed

## [2.4.0] - 2026-08-19

### Changed
- `synapse-sdk` 핀을 `2026.1.162` 로 올린다 (이전 릴리즈 v2.3.0 은 핀 없음).
  **플러그인 코드는 바뀌지 않았다** — 이 릴리즈가 담는 것은 전부 SDK 쪽 변화다.

  주요한 것:
  - **[SYN-7401] 업로드 워커 확장 (FR-4)** — 파일 전송·유닛 등록을 조각으로 나눠
    Ray 워커에 흩을 수 있다. 신규 파라미터 `upload_ray_workers`, **기본 1(기존 동작)**.
    N=15,000 실측에서 W=5 가 전체 2.28배, 유닛 등록 6.39배, 파일 전송 1.98배.
    올리는 결정은 별개다 — 전송이 2배에서 막히고 backend 부하가 W 배다.
  - **[SYN-7439] 보안** — executor 가 제출자 셸의 `os.environ` 전체를 Ray job
    레코드에 싣던 것을 `SYNAPSE_*`/`RAY_*` 로 좁혔다. tune trial 경로도 함께.
  - **[SYN-7435] 진행률** — 유닛 생성 중에도 진행률이 움직이고, 단계 가중치가
    실측을 따른다. 이전에는 전체의 63% 를 차지하는 구간이 바의 20% 였다.
  - **[SYN-7436] JobLog 배치** — 로그 전송 요청이 N=1,000 에서 3,046 → 35 로 줄었다.

### Note
- 2.3.1~2.3.8 은 test env `debug=True` 게시본으로, 측정용 발판이었고 릴리즈가 아니다.
  이 릴리즈는 v2.3.0 다음이다.

## [2.3.0] - 2026-08-05

### Added
- `supported_data_types` 에 `data` 추가 — 일반 데이터(data unit) 컬렉션 대상 업로드 지원 (`synapse-sdk` `DataType.DATA`).
- config entrypoint 정리: `.venv` 절대경로로 손상됐던 sample/to_task entrypoint 를 정규 클래스 경로로 복구.

## [2.1.0] - 2026-05-21

### Changed
- 본 메타 repo 에 submodule 로 등록 (category=upload). v2 라인 시작.
