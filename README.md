# Quality Intelligence | 결함 예측

코드 메트릭으로 소프트웨어 모듈의 결함 위험도를 예측하고, QA가 우선 검토할 대상을 정하는 Streamlit 대시보드입니다.

NASA MDP(JM1 + CM1)로 학습한 Random Forest 모델을 사용합니다. 모듈 메트릭이 담긴 엑셀을 올리면 결함 의심 모듈 수, 결함 비율, 위험 수준(높음 / 중간 / 낮음)을 바로 보여 줍니다. 집중 테스트 권장 목록과 권장 QA 프로세스, 세부 예측 결과를 엑셀과 PDF 보고서로 받을 수 있습니다.

🔗 [배포 사이트](https://defect-prediction-app-ergntpi64o9gc6pnluud7g.streamlit.app/)

🔗 [데이터셋 출처] https://www.kaggle.com/datasets/radowanulhaque/software-defect

---

##  주요 특징 및 해결 과제

1. **데이터 병합 및 정제**
   - JM1(약 10,885건)과 CM1(약 498건) 데이터셋을 결합하여 총 11,383건의 학습 데이터 확보.
   - 결측치 및 데이터 누수를 유발하는 `id` 컬럼 제거.

2. **다중공선성(Multicollinearity) 해결**
   - VIF 분석 및 상관관계 분석을 통해 심한 중복을 유발하는 8개 지표(`e`, `n`, `v`, `b`, `total_Op`, `total_Opnd`, `branchCount`, `lOCode`)를 선별 제거하여 모델 과적합 방지.

3. **데이터 불균형 해소 (SMOTE)**
   - Train/Test 8:2 분할 후, 학습 데이터에만 SMOTE를 적용하여 정상(0)과 결함(1) 클래스 비율을 1:1로 균형화.

4. **Streamlit 웹 대시보드 구축**
   - 엑셀(`xlsx`) 파일 업로드 시 실시간으로 Random Forest 모델 예측 수행[cite: 8].
   - 결함 위험도에 따른 QA Action 가이드 자동 부여 및 결과 리포트 엑셀 다운로드 기능 제공[cite: 8].

---

##  프로젝트 구조

```text
defect-prediction-app/
│
├── models/
│   └── rf_model.pkl           # 학습된 Random Forest 모델 파일
├── notebooks/
│   └── AI_defect_prediction.ipynb # 데이터 탐색, 전처리 및 모델 학습 노트북
├── .gitignore
├── app.py                     # Streamlit 웹 대시보드 메인 앱
├── requirements.txt           # 파이썬 필수 패키지 목록
└── README.md


