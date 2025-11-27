import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# 데이터 로드
df = pd.read_csv('uci-secom.csv')

print("=" * 60)
print("UCI-SECOM 데이터셋 결측치 분석")
print("=" * 60)

# 기본 정보
print(f"\n데이터 형태: {df.shape}")
print(f"총 샘플 수: {df.shape[0]}")
print(f"총 특징 수: {df.shape[1]}")

# 결측치 통계
missing_stats = pd.DataFrame({
    '결측치 개수': df.isnull().sum(),
    '결측치 비율(%)': (df.isnull().sum() / len(df) * 100).round(2)
}).sort_values('결측치 비율(%)', ascending=False)

print("\n" + "=" * 60)
print("결측치 통계")
print("=" * 60)
print(f"결측치가 있는 컬럼 수: {(missing_stats['결측치 개수'] > 0).sum()}")
print(f"결측치가 없는 컬럼 수: {(missing_stats['결측치 개수'] == 0).sum()}")
print(f"\n전체 데이터의 결측치 비율: {(df.isnull().sum().sum() / (df.shape[0] * df.shape[1]) * 100):.2f}%")

# 결측치가 많은 상위 20개 컬럼
print("\n결측치가 많은 상위 20개 컬럼:")
print(missing_stats.head(20))

# 결측치 비율별 컬럼 분포
print("\n" + "=" * 60)
print("결측치 비율별 컬럼 분포")
print("=" * 60)
bins = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
labels = ['0-10%', '10-20%', '20-30%', '30-40%', '40-50%', 
          '50-60%', '60-70%', '70-80%', '80-90%', '90-100%']
missing_distribution = pd.cut(missing_stats['결측치 비율(%)'], bins=bins, labels=labels).value_counts().sort_index()
print(missing_distribution)

# 각 행의 결측치 비율
row_missing = df.isnull().sum(axis=1)
print("\n" + "=" * 60)
print("행별 결측치 통계")
print("=" * 60)
print(f"행당 평균 결측치 수: {row_missing.mean():.2f}")
print(f"행당 최대 결측치 수: {row_missing.max()}")
print(f"행당 최소 결측치 수: {row_missing.min()}")
print(f"결측치가 전혀 없는 행 수: {(row_missing == 0).sum()}")

# 시각화
fig, axes = plt.subplots(2, 2, figsize=(15, 12))

# 1. 결측치 비율 히스토그램
axes[0, 0].hist(missing_stats['결측치 비율(%)'], bins=50, edgecolor='black', alpha=0.7)
axes[0, 0].set_title('컬럼별 결측치 비율 분포', fontsize=12, fontweight='bold')
axes[0, 0].set_xlabel('결측치 비율 (%)')
axes[0, 0].set_ylabel('컬럼 수')
axes[0, 0].grid(True, alpha=0.3)

# 2. 결측치 비율 카테고리별 분포
missing_distribution.plot(kind='bar', ax=axes[0, 1], color='steelblue', edgecolor='black')
axes[0, 1].set_title('결측치 비율 구간별 컬럼 분포', fontsize=12, fontweight='bold')
axes[0, 1].set_xlabel('결측치 비율 구간')
axes[0, 1].set_ylabel('컬럼 수')
axes[0, 1].tick_params(axis='x', rotation=45)
axes[0, 1].grid(True, alpha=0.3, axis='y')

# 3. 행별 결측치 분포
axes[1, 0].hist(row_missing, bins=50, edgecolor='black', alpha=0.7, color='coral')
axes[1, 0].set_title('행별 결측치 개수 분포', fontsize=12, fontweight='bold')
axes[1, 0].set_xlabel('결측치 개수')
axes[1, 0].set_ylabel('행 수')
axes[1, 0].grid(True, alpha=0.3)

# 4. 상위 20개 결측치가 많은 컬럼
top_missing = missing_stats.head(20)
axes[1, 1].barh(range(len(top_missing)), top_missing['결측치 비율(%)'], color='indianred', edgecolor='black')
axes[1, 1].set_yticks(range(len(top_missing)))
axes[1, 1].set_yticklabels(top_missing.index, fontsize=8)
axes[1, 1].set_title('결측치가 많은 상위 20개 컬럼', fontsize=12, fontweight='bold')
axes[1, 1].set_xlabel('결측치 비율 (%)')
axes[1, 1].invert_yaxis()
axes[1, 1].grid(True, alpha=0.3, axis='x')

plt.tight_layout()
plt.savefig('missing_values_analysis.png', dpi=300, bbox_inches='tight')
print("\n시각화 저장 완료: missing_values_analysis.png")

# 결측치 처리 권장사항
print("\n" + "=" * 60)
print("결측치 처리 권장 방법")
print("=" * 60)

high_missing_cols = missing_stats[missing_stats['결측치 비율(%)'] > 50].shape[0]
medium_missing_cols = missing_stats[(missing_stats['결측치 비율(%)'] > 10) & 
                                     (missing_stats['결측치 비율(%)'] <= 50)].shape[0]
low_missing_cols = missing_stats[(missing_stats['결측치 비율(%)'] > 0) & 
                                  (missing_stats['결측치 비율(%)'] <= 10)].shape[0]

print(f"\n1. 높은 결측치(>50%): {high_missing_cols}개 컬럼")
print("   → 권장: 해당 컬럼 삭제 또는 도메인 지식 기반 특별 처리")

print(f"\n2. 중간 결측치(10-50%): {medium_missing_cols}개 컬럼")
print("   → 권장: KNN Imputer, Iterative Imputer 등 고급 대체 기법")

print(f"\n3. 낮은 결측치(0-10%): {low_missing_cols}개 컬럼")
print("   → 권장: 평균/중앙값 대체, Forward/Backward Fill")

print("\n추천 전략:")
print("• 반도체 제조 공정 데이터 특성상 센서 결측이 많을 수 있음")
print("• 시계열적 특성을 고려한 Forward/Backward Fill 적용 가능")
print("• 다변량 대체 방법 (MICE, KNN) 권장")
print("• 높은 결측치 컬럼(>70%)은 제거 고려")
print("• 도메인 전문가와 협의하여 센서별 결측 원인 파악 필요")
