# AI기반 소프트웨어 결함 예측 모델 개발 및 시각화 대시보드

NASA MDP (JM1 + CM1) 코드 메트릭 데이터를 활용하여 소프트웨어 모듈의 결함 위험도를 예측하고, QA(품질보증) 부서에서 실시간으로 검사 및 리포트를 다운로드할 수 있는 Streamlit 웹 대시보드 시스템입니다.

---

## 배포 사이트
🔗 [Streamlit 앱 바로가기](https://defect-prediction-app-ergntpi64o9gc6pnluud7g.streamlit.app/)
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


