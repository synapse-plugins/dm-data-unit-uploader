# dm-data-unit-uploader

외부 스토리지의 파일을 커스텀 변환 없이 Synapse 데이터 유닛으로 업로드하는 **기본형 범용 업로더**. 이미지·비디오·텍스트·PCD·오디오 등 다양한 데이터 타입을 지원합니다.

---

## 1. 플러그인 식별 정보

| 항목 | 값 |
| --- | --- |
| 폴더명 / GitHub 저장소 | `dm-data-unit-uploader` |
| 코드명 (`config.yaml` → `code`) | `dm-data-unit-uploader` |
| 플러그인 이름 (`config.yaml` → `name`) | `dm-data-unit-uploader` |
| 패키지명 (`pyproject.toml` → `name`) | `dm-data-unit-uploader-v2` |
| 버전 | `2.1.1` |
| 카테고리 | `upload` |
| 지원 데이터 타입 | `image`, `video`, `text`, `pcd`, `audio` |
| upload 진입점 | `plugin.upload.UploadAction` |

---

## 2. 개요

이 플러그인은 SDK의 `DefaultUploadAction`을 **거의 그대로** 사용하는 표준 업로더입니다. 포맷 변환·분할 같은 커스텀 단계를 삽입하지 않고, 기본 8단계만으로 파일을 조직화·검증·업로드합니다. 다른 변환형 플러그인(avi/tiff/pdf/video/coco)의 **기준(baseline)** 이 되는 형태입니다.

`setup_steps`를 재정의하지 않으므로 기본 단계가 그대로 실행되며, 커스터마이징이 필요하면 이 메서드를 오버라이드해 커스텀 단계를 등록할 수 있습니다.

---

## 3. 전체 업로드 워크플로우 (기본 8단계)

```mermaid
flowchart TD
    A["1 initialize<br/><i>스토리지·경로 초기화</i>"] --> B["2 process_metadata<br/><i>엑셀 메타데이터(선택)</i>"]
    B --> C["3 analyze_collection<br/><i>파일 스펙 로드</i>"]
    C --> D["4 organize_files<br/><i>파일명(stem) 기준 그룹화</i>"]
    D --> E["5 validate_files<br/><i>스펙 대비 검증</i>"]
    E --> F["6 upload_files<br/><i>스토리지 업로드</i>"]
    F --> G["7 generate_data_units<br/><i>데이터 유닛 생성</i>"]
    G --> H["8 cleanup<br/><i>임시 리소스 정리</i>"]
```

---

## 4. 경로 모드 (단일 / 다중)

```mermaid
flowchart TD
    Q{"use_single_path?"}
    Q -->|True · 기본| S["단일 경로 모드<br/>모든 스펙이 하나의 path 공유"]
    Q -->|False| M["다중 경로 모드<br/>스펙마다 assets[name].path 지정<br/>is_recursive 개별 설정"]
```

### 단일 경로 모드 (`use_single_path=True`, 기본값)

```json
{
  "name": "Standard Upload",
  "path": "/data/experiment_1",
  "storage": 1,
  "data_collection": 5
}
```

### 다중 경로 모드 (`use_single_path=False`)

```json
{
  "name": "Multi-Source Upload",
  "use_single_path": false,
  "assets": {
    "image_1": {"path": "/sensors/camera", "is_recursive": true},
    "pcd_1":   {"path": "/sensors/lidar",  "is_recursive": false}
  },
  "storage": 1,
  "data_collection": 5
}
```

---

## 5. 허용 확장자 (`get_allowed_extensions`)

타입별 허용 확장자를 명시적으로 제한하며, 특히 **비디오는 `.mp4`만** 허용합니다.

| 타입 | 허용 확장자 |
| --- | --- |
| image | `.jpg`, `.jpeg`, `.png` |
| video | `.mp4` |
| audio | `.mp3`, `.wav` |
| text | `.txt`, `.html` |
| pcd | `.pcd` |
| data | `.bin`, `.json`, `.fbx`, `.xml`, `.csv` |

---

## 6. 실행 진입점 (`_synapse_entrypoint.py`)

Ray Jobs API에서 액션을 구동하기 위한 자동 생성 진입점 스크립트입니다.

```mermaid
sequenceDiagram
    participant Ray as Ray Job
    participant EP as _synapse_entrypoint.py
    participant SDK as synapse_sdk
    Ray->>EP: 환경변수 주입<br/>(PARAMS · ENTRYPOINT · JOB_ID)
    EP->>EP: params JSON 로드
    EP->>EP: entrypoint 모듈/클래스 import
    EP->>SDK: backend client 생성
    EP->>SDK: RuntimeContext(logger·env·client) 구성
    EP->>SDK: action_cls.dispatch(params, ctx)
    SDK-->>EP: result
    EP->>Ray: __SYNAPSE_RESULT_START__ … END 마커로 출력
```

- `SYNAPSE_JOB_ID`(우선) 또는 `RAY_JOB_ID`로 `JobLogger`를 쓰고, client/job_id가 없으면 `ConsoleLogger`로 폴백.

---

## 7. 파라미터

별도 UI 스키마 없이 SDK 기본 업로드 파라미터를 사용합니다: `name`, `path` 또는 `assets`, `storage`, `data_collection`, `use_single_path` 등.

---

## 8. 의존성

- `synapse-sdk`

---

## 9. 설치 / 실행 / 배포

```bash
uv sync
synapse run upload
synapse plugin publish
```
