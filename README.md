# UCI-SECOM 반도체 수율 분석 프로젝트

## 프로젝트 개요

UCI-SECOM 데이터셋을 활용한 반도체 제조 공정의 시계열 불량률 패턴 분석 프로젝트입니다. 시간대별, 요일별, 월별 불량률 변화를 분석하여 제조 공정 개선을 위한 인사이트를 도출합니다.

## 데이터셋 정보

- **데이터셋**: UCI-SECOM (Semiconductor Manufacturing Process Data)
- **총 샘플 수**: 1,567개
- **특성 수**: 592개
- **전체 불량률**: 6.64%
- **분석 기간**: 2008년 1월 ~ 12월

## 주요 분석 결과

### 시간대별 분석
- **최고 불량률**: 15시 (11.11%)
- **최저 불량률**: 10시 (1.89%)
- 오후 시간대(15-21시)에 불량률이 증가하는 경향

### 요일별 분석
- **최고 불량률**: 수요일 (10.16%)
- **최저 불량률**: 목요일 (3.59%)
- 주중/주말 불량률 차이는 미미 (6.68% vs 6.62%)

### 월별 분석
- **최고 불량률**: 7월 (14.04%)
- **최저 불량률**: 12월 (0.00%)
- 여름철(7-8월)에 불량률이 급증

### 특이사항
- 수요일 새벽 4시에 최고 불량률 66.67% 기록
- 시간대와 요일이 복합적으로 작용하는 패턴 확인

## 파일 구조

```
analyse_ver_2/
│
├── csv/                                      # 결측치 처리된 데이터셋
│   ├── uci-secom.csv                        # 원본 데이터
│   ├── uci-secom_method1_drop_high_missing.csv
│   ├── uci-secom_method2_mean.csv
│   ├── uci-secom_method3_median.csv
│   ├── uci-secom_method5_knn.csv
│   ├── uci-secom_method6_mice.csv
│   └── uci-secom_method7_hybrid.csv
│
├── uci-secom_method4_ffill_bfill.csv        # 분석에 사용된 데이터 (Forward/Backward Fill)
├── secom_yield_temporal_analysis.ipynb      # 주 분석 노트북
├── generate_report.py                        # PDF 보고서 생성 스크립트
├── secom_defect_analysis_report.pdf         # 최종 분석 보고서 (5페이지)
│
├── analyze_missing_values.py                # 결측치 분석 스크립트
├── impute_missing_values.py                 # 결측치 처리 스크립트
│
├── hourly_defect_analysis.png               # 시간대별 분석 그래프
├── daily_defect_analysis.png                # 요일별 분석 그래프
├── monthly_defect_analysis.png              # 월별 분석 그래프
├── date_defect_analysis.png                 # 날짜별 분석 그래프
├── hour_day_heatmap.png                     # 시간×요일 히트맵
│
└── README.md                                 # 프로젝트 문서 (본 파일)
```

## 환경 설정

### 필수 라이브러리

```bash
pip install pandas numpy matplotlib seaborn scikit-learn pillow
```

### Python 버전
- Python 3.11.9

### 설치된 패키지 버전
- pandas 2.3.3
- numpy 2.3.5
- matplotlib 3.10.7
- seaborn 0.13.2
- scikit-learn 1.7.2
- Pillow (최신 버전)

## 사용 방법

### 1. 결측치 분석
```bash
python analyze_missing_values.py
```

### 2. 결측치 처리 (7가지 방법)
```bash
python impute_missing_values.py
```

### 3. 시계열 분석 (Jupyter Notebook)
```bash
jupyter notebook secom_yield_temporal_analysis.ipynb
```

### 4. PDF 보고서 생성
```bash
python generate_report.py
```

## 분석 방법론

### 1. 데이터 전처리
- Forward Fill과 Backward Fill을 조합한 결측치 처리
- 시계열 특성 추출 (Hour, DayOfWeek, Month, Date)

### 2. 시계열 패턴 분석
- 시간대별 불량률 계산 및 시각화
- 요일별 불량률 비교 (주중/주말 포함)
- 월별 불량률 추세 분석
- 특정 날짜 불량률 분석

### 3. 복합 패턴 분석
- 시간×요일 히트맵을 통한 교차 패턴 발견
- 고위험 시간대 및 날짜 식별

## 주요 인사이트

### 장비 및 공정 관련
- 오후 시간대 장비 가동 누적으로 인한 열화 현상
- 여름철 온습도 환경이 반도체 공정에 부정적 영향

### 운영 관리 관련
- 주중 피로도 누적 (수요일 불량률 상승)
- 교대 근무 인수인계 시점 관리 필요

### 환경 요인
- 계절별 환경 조건 변화에 따른 불량률 변동
- 클린룸 환경 제어 시스템 성능 점검 필요

## 개선 권장사항

1. **시간대별 관리**
   - 15시 전후 장비 점검 및 공정 파라미터 모니터링 강화
   - 10시 시간대의 우수 공정 조건을 벤치마크로 활용

2. **요일별 관리**
   - 수요일 특별 점검 체크리스트 운영
   - 주간 피로도 누적 요인 분석 및 대응

3. **계절별 관리**
   - 여름철 이전 냉각 설비 사전 점검
   - 클린룸 온습도 제어 시스템 성능 향상

4. **실시간 모니터링**
   - SPC (Statistical Process Control) 시스템 도입
   - 이상 징후 조기 감지 시스템 구축

5. **예측 분석**
   - 머신러닝 기반 불량 예측 모델 개발
   - 센서 데이터 기반 사전 예방 관리 체계 확립

## 시각화 결과

프로젝트는 다음 5가지 시각화를 생성합니다:

1. **hourly_defect_analysis.png**: 시간대별 불량률 추이 및 샘플 수 분포
2. **daily_defect_analysis.png**: 요일별 불량률 비교 및 주중/주말 분석
3. **monthly_defect_analysis.png**: 월별 불량률 추세 및 샘플 수
4. **date_defect_analysis.png**: 날짜별 불량률 타임라인 및 Top 10 고위험 날짜
5. **hour_day_heatmap.png**: 시간×요일 불량률 히트맵 (24시간 × 7일)

## 보고서

최종 분석 결과는 `secom_defect_analysis_report.pdf` 파일로 제공됩니다.

**보고서 구성** (5페이지):
- 페이지 1: 표지 및 분석 개요
- 페이지 2: 시간대별 분석 및 개선 방안
- 페이지 3: 요일별 분석 및 개선 방안
- 페이지 4: 월별 분석 및 개선 방안
- 페이지 5: 히트맵 및 종합 결론

## 기술 스택

- **데이터 분석**: pandas, numpy
- **시각화**: matplotlib, seaborn
- **머신러닝**: scikit-learn
- **보고서 생성**: matplotlib PdfPages, Pillow
- **개발 환경**: Jupyter Notebook, Python 3.11

## 한글 폰트 설정

프로젝트는 한글 폰트 렌더링을 위해 NanumGothic을 사용합니다.

```python
import matplotlib.font_manager as fm
font_path = 'C:/Windows/Fonts/NanumGothic.ttf'
fm.fontManager.addfont(font_path)
font_name = fm.FontProperties(fname=font_path).get_name()
plt.rcParams['font.family'] = [font_name]
plt.rcParams['axes.unicode_minus'] = False
```

## 라이선스

이 프로젝트는 UCI-SECOM 공개 데이터셋을 사용합니다.

## 참고 자료

- UCI Machine Learning Repository: SECOM Dataset
- 반도체 제조 공정 품질 관리 문헌
- 통계적 공정 관리 (SPC) 이론

## 작성자

반도체 수율 분석 프로젝트 팀

## 업데이트 이력

- 2008년: 데이터 수집 기간
- 2025년 11월: 시계열 분석 및 보고서 작성
