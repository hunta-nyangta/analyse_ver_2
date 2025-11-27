import pandas as pd
import numpy as np
from sklearn.impute import SimpleImputer, KNNImputer
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer
from sklearn.preprocessing import StandardScaler
import time

print("=" * 80)
print("UCI-SECOM 결측치 처리 방법 비교")
print("=" * 80)

# 데이터 로드
df = pd.read_csv('uci-secom.csv')
print(f"\n원본 데이터 형태: {df.shape}")
print(f"전체 결측치 비율: {(df.isnull().sum().sum() / (df.shape[0] * df.shape[1]) * 100):.2f}%")

# Time 컬럼이 있다면 분리
time_col = None
if 'Time' in df.columns:
    time_col = df['Time']
    df = df.drop('Time', axis=1)
    print("\nTime 컬럼 분리 완료")

# Pass/Fail 컬럼(타겟) 분리
target_col = None
if 'Pass/Fail' in df.columns:
    target_col = df['Pass/Fail']
    df = df.drop('Pass/Fail', axis=1)
    print("Pass/Fail 타겟 컬럼 분리 완료")

print(f"처리할 특징 데이터 형태: {df.shape}")

# ============================================================================
# 방법 1: 높은 결측치 컬럼 제거 (>70%)
# ============================================================================
print("\n" + "=" * 80)
print("방법 1: 높은 결측치 컬럼 제거 (>70%)")
print("=" * 80)

missing_ratio = df.isnull().sum() / len(df)
cols_to_keep = missing_ratio[missing_ratio <= 0.7].index
df_method1 = df[cols_to_keep].copy()

print(f"제거 전 컬럼 수: {df.shape[1]}")
print(f"제거 후 컬럼 수: {df_method1.shape[1]}")
print(f"제거된 컬럼 수: {df.shape[1] - df_method1.shape[1]}")

# ============================================================================
# 방법 2: 단순 대체 - 평균값
# ============================================================================
print("\n" + "=" * 80)
print("방법 2: 단순 대체 - 평균값 (Mean Imputation)")
print("=" * 80)

start_time = time.time()
imputer_mean = SimpleImputer(strategy='mean')
df_method2 = pd.DataFrame(
    imputer_mean.fit_transform(df_method1),
    columns=df_method1.columns
)
elapsed = time.time() - start_time

print(f"처리 시간: {elapsed:.2f}초")
print(f"결측치 개수: {df_method2.isnull().sum().sum()}")
print(f"✓ 완료")

# ============================================================================
# 방법 3: 단순 대체 - 중앙값
# ============================================================================
print("\n" + "=" * 80)
print("방법 3: 단순 대체 - 중앙값 (Median Imputation)")
print("=" * 80)

start_time = time.time()
imputer_median = SimpleImputer(strategy='median')
df_method3 = pd.DataFrame(
    imputer_median.fit_transform(df_method1),
    columns=df_method1.columns
)
elapsed = time.time() - start_time

print(f"처리 시간: {elapsed:.2f}초")
print(f"결측치 개수: {df_method3.isnull().sum().sum()}")
print(f"✓ 완료")

# ============================================================================
# 방법 4: 순방향/역방향 채우기 (Forward/Backward Fill)
# ============================================================================
print("\n" + "=" * 80)
print("방법 4: 순방향 채우기 후 역방향 채우기 (FFill + BFill)")
print("=" * 80)

start_time = time.time()
df_method4 = df_method1.copy()
# 순방향 채우기
df_method4 = df_method4.fillna(method='ffill')
# 역방향 채우기 (순방향에서 못 채운 것 처리)
df_method4 = df_method4.fillna(method='bfill')
# 그래도 남은 결측치는 평균으로
df_method4 = df_method4.fillna(df_method4.mean())
elapsed = time.time() - start_time

print(f"처리 시간: {elapsed:.2f}초")
print(f"결측치 개수: {df_method4.isnull().sum().sum()}")
print(f"✓ 완료")
print("  (시계열 특성이 있는 센서 데이터에 적합)")

# ============================================================================
# 방법 5: KNN Imputer
# ============================================================================
print("\n" + "=" * 80)
print("방법 5: KNN Imputer (k=5)")
print("=" * 80)
print("  (가장 가까운 5개 샘플의 값을 사용하여 대체)")

# 컬럼 수가 많아 시간이 오래 걸리므로 샘플링 또는 최적화
# 여기서는 전체 데이터에 적용
start_time = time.time()
imputer_knn = KNNImputer(n_neighbors=5, weights='distance')
df_method5 = pd.DataFrame(
    imputer_knn.fit_transform(df_method1),
    columns=df_method1.columns
)
elapsed = time.time() - start_time

print(f"처리 시간: {elapsed:.2f}초")
print(f"결측치 개수: {df_method5.isnull().sum().sum()}")
print(f"✓ 완료")

# ============================================================================
# 방법 6: Iterative Imputer (MICE)
# ============================================================================
print("\n" + "=" * 80)
print("방법 6: Iterative Imputer (MICE - Multiple Imputation)")
print("=" * 80)
print("  (다른 특징들을 사용하여 결측치를 반복적으로 예측)")

start_time = time.time()
imputer_iter = IterativeImputer(max_iter=10, random_state=42)
df_method6 = pd.DataFrame(
    imputer_iter.fit_transform(df_method1),
    columns=df_method1.columns
)
elapsed = time.time() - start_time

print(f"처리 시간: {elapsed:.2f}초")
print(f"결측치 개수: {df_method6.isnull().sum().sum()}")
print(f"✓ 완료")

# ============================================================================
# 방법 7: 하이브리드 접근법 (권장)
# ============================================================================
print("\n" + "=" * 80)
print("방법 7: 하이브리드 접근법 (권장)")
print("=" * 80)
print("  • 70% 이상 결측치 컬럼 제거")
print("  • 10% 이하 결측치: Forward/Backward Fill")
print("  • 10% 초과 결측치: KNN Imputer")

start_time = time.time()

# 1단계: 70% 이상 결측치 컬럼 제거 (이미 df_method1에 적용됨)
df_hybrid = df_method1.copy()

# 2단계: 결측치 비율 계산
missing_ratio_filtered = df_hybrid.isnull().sum() / len(df_hybrid)

# 3단계: 10% 이하 결측치 컬럼 - Forward/Backward Fill
low_missing_cols = missing_ratio_filtered[missing_ratio_filtered <= 0.1].index
if len(low_missing_cols) > 0:
    df_hybrid[low_missing_cols] = df_hybrid[low_missing_cols].fillna(method='ffill').fillna(method='bfill')
    print(f"  - Forward/Backward Fill 적용: {len(low_missing_cols)}개 컬럼")

# 4단계: 10% 초과 결측치 컬럼 - KNN Imputer
high_missing_cols = missing_ratio_filtered[missing_ratio_filtered > 0.1].index
if len(high_missing_cols) > 0:
    imputer_hybrid = KNNImputer(n_neighbors=5, weights='distance')
    df_hybrid[high_missing_cols] = imputer_hybrid.fit_transform(df_hybrid[high_missing_cols])
    print(f"  - KNN Imputer 적용: {len(high_missing_cols)}개 컬럼")

# 5단계: 남은 결측치 처리 (있을 경우)
if df_hybrid.isnull().sum().sum() > 0:
    df_hybrid = df_hybrid.fillna(df_hybrid.mean())
    print(f"  - 남은 결측치 평균으로 대체")

elapsed = time.time() - start_time

print(f"\n처리 시간: {elapsed:.2f}초")
print(f"결측치 개수: {df_hybrid.isnull().sum().sum()}")
print(f"✓ 완료")

# ============================================================================
# 결과 저장
# ============================================================================
print("\n" + "=" * 80)
print("처리된 데이터 저장")
print("=" * 80)

# 각 방법별로 저장
methods = {
    'method1_drop_high_missing': df_method1,  # 컬럼 제거만
    'method2_mean': df_method2,
    'method3_median': df_method3,
    'method4_ffill_bfill': df_method4,
    'method5_knn': df_method5,
    'method6_mice': df_method6,
    'method7_hybrid': df_hybrid
}

for method_name, df_result in methods.items():
    # Time과 Pass/Fail 컬럼 다시 추가
    df_save = df_result.copy()
    if time_col is not None:
        df_save.insert(0, 'Time', time_col.values)
    if target_col is not None:
        df_save['Pass/Fail'] = target_col.values
    
    filename = f'uci-secom_{method_name}.csv'
    df_save.to_csv(filename, index=False)
    print(f"✓ {filename} 저장 완료")

# ============================================================================
# 요약 및 권장사항
# ============================================================================
print("\n" + "=" * 80)
print("결측치 처리 방법 요약 및 권장사항")
print("=" * 80)

print("\n각 방법의 특징:")
print("\n1. 컬럼 제거 (70% 이상)")
print("   - 장점: 신뢰도 낮은 센서 제거, 빠른 처리")
print("   - 단점: 정보 손실")
print("   - 적합: 초기 탐색, 빠른 프로토타입")

print("\n2. 평균값 대체")
print("   - 장점: 빠르고 단순")
print("   - 단점: 분산 감소, 관계성 무시")
print("   - 적합: 결측치가 적고 정규분포를 따를 때")

print("\n3. 중앙값 대체")
print("   - 장점: 이상치에 강건함")
print("   - 단점: 분산 감소, 관계성 무시")
print("   - 적합: 이상치가 많은 센서 데이터")

print("\n4. Forward/Backward Fill")
print("   - 장점: 시계열 특성 보존")
print("   - 단점: 순서 의존적")
print("   - 적합: 시계열 센서 데이터 (✓ 추천)")

print("\n5. KNN Imputer")
print("   - 장점: 다변량 관계 고려")
print("   - 단점: 계산 비용 높음")
print("   - 적합: 센서 간 상관관계가 높을 때 (✓ 추천)")

print("\n6. MICE (Iterative Imputer)")
print("   - 장점: 가장 정교한 대체")
print("   - 단점: 매우 느림")
print("   - 적합: 정확도가 중요한 최종 모델")

print("\n7. 하이브리드 방법 (★ 최고 권장)")
print("   - 장점: 각 방법의 장점 결합, 균형잡힌 접근")
print("   - 단점: 중간 복잡도")
print("   - 적합: 대부분의 실전 상황")

print("\n" + "=" * 80)
print("반도체 제조 데이터 특성 고려사항:")
print("=" * 80)
print("• 센서 고장이나 측정 불가 상황으로 인한 결측치가 많음")
print("• 시계열 특성이 있으므로 Forward Fill이 의미 있음")
print("• 센서 간 상관관계를 고려한 KNN/MICE가 효과적")
print("• 하이브리드 방법(방법 7)을 우선 추천")
print("• 모델링 후 성능 비교를 통해 최적 방법 선택")

print("\n다음 단계:")
print("1. 처리된 데이터로 탐색적 데이터 분석(EDA)")
print("2. 여러 방법으로 처리된 데이터로 모델 학습 및 비교")
print("3. 검증 성능이 가장 좋은 방법 선택")
