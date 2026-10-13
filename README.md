<!---
Copyright 2024 tony9402. All rights reserved.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
-->

# Huggingface NAS

<!-- repository-guide:start -->
## 저장소 안내

Hugging Face 모델·데이터셋과 로컬 모델 파일을 Synology NAS에 업로드하고, NAS에 저장된 자료를 다시 불러오는 Python 패키지입니다.

| 경로 | 내용 |
| --- | --- |
| [src/huggingface_nas/hf_to_nas.py](src/huggingface_nas/hf_to_nas.py) | Hugging Face 모델·데이터셋 업로드 |
| [src/huggingface_nas/local_to_nas.py](src/huggingface_nas/local_to_nas.py) | 로컬 모델 업로드 |
| [src/huggingface_nas/load.py](src/huggingface_nas/load.py) | NAS 모델·데이터셋 다운로드 |
| [src/huggingface_nas/webapi.py](src/huggingface_nas/webapi.py) | NAS Web API 연동 |
| [setup.py](setup.py) | 패키지 버전, Python 요구 사항과 의존성 |
| [LICENSE](LICENSE) | Apache 2.0 라이선스 |

이 저장소의 코드를 로컬에서 사용하려면 Python 3.8 이상에서 `python -m pip install -e .`로 설치합니다. NAS의 공유 폴더 경로와 접속 정보, 접근 제한이 있는 Hugging Face 자료의 토큰은 아래 예제의 자리표시자를 자신의 환경에 맞게 채워 전달합니다.

목적과 구현 범위, 구성 분석은 [Explain.md](Explain.md)를 참고하세요.

<!-- repository-guide:end -->

## Installation

```bash
pip3 install huggingface_nas
```

## How to use

### Huggingface to Synology NAS (Model)

```python
from huggingface_nas import upload_model

upload_model(
    name="<huggingface model ex. meta-llama/Llama-3.3-70B-Instruct>",
    base_folder="<synology folder>",
    token="<huggingface token>",
    ip_address="<synology ip>",
    port="<synology port>",
    username="<synology username>",
    password="<synology password>"
)
```

### Huggingface to Synology NAS (Dataset)

```python
from huggingface_nas import upload_dataset

upload_dataset(
    name="<huggingface dataset ex. meta-llama/Llama-3.3-70B-Instruct-evals>",
    base_folder="<synology folder>",
    token="<huggingface token>",
    ip_address="<synology ip>",
    port="<synology port>",
    username="<synology username>",
    password="<synology password>"
)
```

### Load dataset from Synology NAS

```python
from huggingface_nas import load_dataset_nas

data = load_dataset_nas(
    path="<model path such as meta-llama/Llama-3.3-70B-Instruct-evals>",
    base_path="<share folder in synology NAS>",
    ip_address="<synology ip>",
    port="<synology port>",
    username="<synology username>",
    password="<synology password>"
)
```

### Load Model from Synology NAS

```python
from transformers import AutoModel
from huggingface_nas import prepare_model_from_nas

model_download_path = prepare_model_from_nas(
    path="<model path such as meta-llama/Llama-3.3-70B-Instruct>",
    base_path="<share folder in synology NAS>",
    ip_address="<synology ip>",
    port="<synology port>",
    username="<synology username>",
    password="<synology password>"
)
AutoModel.from_pretrained(model_download_path)
```
