import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from PIL import Image
import matplotlib.font_manager as fm
import os

# 한글 폰트 설정
font_path = 'C:/Windows/Fonts/NanumGothic.ttf'
if os.path.exists(font_path):
    fm.fontManager.addfont(font_path)
    font_name = fm.FontProperties(fname=font_path).get_name()
    plt.rcParams['font.family'] = [font_name]
else:
    plt.rcParams['font.family'] = 'Malgun Gothic'

plt.rcParams['axes.unicode_minus'] = False

# PDF 생성
pdf_path = 'secom_defect_analysis_report.pdf'

with PdfPages(pdf_path) as pdf:
    # ========== 페이지 1: 표지 및 개요 ==========
    fig = plt.figure(figsize=(8.27, 11.69))  # A4 size
    fig.patch.set_facecolor('white')
    
    # 제목
    fig.text(0.5, 0.85, 'UCI-SECOM', 
             ha='center', fontsize=20, color='#2c3e50')
    fig.text(0.5, 0.80, '반도체 수율 분석 보고서', 
             ha='center', fontsize=28, fontweight='bold')
    fig.text(0.5, 0.75, '시계열 불량률 패턴 분석 및 개선 방안',
             ha='center', fontsize=14, color='#555')
    
    # 구분선
    line1 = plt.Line2D([0.15, 0.85], [0.72, 0.72], transform=fig.transFigure, 
                       color='#2c3e50', linewidth=1.5)
    fig.add_artist(line1)
    
    # 분석 개요
    fig.text(0.15, 0.65, '분석 개요', fontsize=18, fontweight='bold', color='#2c3e50')
    
    overview_items = [
        ('데이터셋', 'UCI-SECOM (반도체 제조 공정 데이터)'),
        ('총 샘플 수', '1,567개'),
        ('전체 불량률', '6.64%'),
        ('분석 기간', '2008년 1월 ~ 12월'),
        ('분석 방법', '시간대별, 요일별, 월별 불량률 패턴 분석')
    ]
    
    y_pos = 0.60
    for label, value in overview_items:
        fig.text(0.18, y_pos, f'{label}:', fontsize=12, fontweight='bold')
        fig.text(0.40, y_pos, value, fontsize=12)
        y_pos -= 0.05
    
    # 주요 발견사항
    fig.text(0.15, 0.30, '주요 발견사항', fontsize=18, fontweight='bold', color='#2c3e50')
    
    findings = [
        '시간대별: 15시에 최고 불량률 11.11%, 10시에 최저 1.89%',
        '요일별: 수요일에 최고 불량률 10.16%, 목요일에 최저 3.59%',
        '월별: 7월에 최고 불량률 14.04%, 여름철 불량률 급증',
        '특이사항: 수요일 새벽 4시에 66.67% 불량률 기록'
    ]
    
    y_pos = 0.24
    for finding in findings:
        fig.text(0.18, y_pos, f'- {finding}', fontsize=11)
        y_pos -= 0.04
    
    # 날짜
    fig.text(0.5, 0.05, '2008년 반도체 제조 공정 분석',
             ha='center', fontsize=10, color='#888')
    
    pdf.savefig(fig, bbox_inches='tight')
    plt.close()
    
    # ========== 페이지 2: 시간대별 분석 ==========
    fig = plt.figure(figsize=(8.27, 11.69))
    fig.patch.set_facecolor('white')
    
    fig.text(0.5, 0.95, '시간대별 불량률 분석', 
             ha='center', fontsize=20, fontweight='bold')
    
    if os.path.exists('hourly_defect_analysis.png'):
        img = Image.open('hourly_defect_analysis.png')
        ax = fig.add_axes([0.1, 0.45, 0.8, 0.45])
        ax.imshow(img)
        ax.axis('off')
    
    # 분석 내용
    fig.text(0.15, 0.40, '분석 결과', fontsize=14, fontweight='bold')
    analysis_text = """
    오후 시간대 (15시)에 불량률이 최고치를 기록하며,
    오전 시간대 (10시)에 가장 낮은 불량률을 보입니다.
    
    15시 이후 저녁 시간대까지 불량률이 높게 유지되는 경향이 있으며,
    이는 장비 가동 시간 누적에 따른 열화 현상과 관련이 있을 것으로 판단됩니다.
    """
    fig.text(0.18, 0.35, analysis_text, fontsize=11, verticalalignment='top')
    
    fig.text(0.15, 0.20, '개선 방안', fontsize=14, fontweight='bold')
    recommendations_text = """
    1. 오후 시간대 장비 상태 집중 점검 실시
    2. 15시 전후 공정 파라미터 모니터링 강화
    3. 10시 시간대의 공정 조건을 벤치마크로 활용
    4. 장비 냉각 시스템 점검 및 유지보수 스케줄 조정
    """
    fig.text(0.18, 0.15, recommendations_text, fontsize=11, verticalalignment='top')
    
    pdf.savefig(fig, bbox_inches='tight')
    plt.close()
    
    # ========== 페이지 3: 요일별 분석 ==========
    fig = plt.figure(figsize=(8.27, 11.69))
    fig.patch.set_facecolor('white')
    
    fig.text(0.5, 0.95, '요일별 불량률 분석', 
             ha='center', fontsize=20, fontweight='bold')
    
    if os.path.exists('daily_defect_analysis.png'):
        img = Image.open('daily_defect_analysis.png')
        ax = fig.add_axes([0.1, 0.45, 0.8, 0.45])
        ax.imshow(img)
        ax.axis('off')
    
    fig.text(0.15, 0.40, '분석 결과', fontsize=14, fontweight='bold')
    analysis_text = """
    수요일에 불량률이 가장 높고 목요일에 가장 낮은 패턴을 보입니다.
    주중과 주말의 불량률 차이는 미미하여 운영 인력보다는
    장비 및 공정 요인의 영향이 더 큰 것으로 분석됩니다.
    """
    fig.text(0.18, 0.35, analysis_text, fontsize=11, verticalalignment='top')
    
    fig.text(0.15, 0.22, '개선 방안', fontsize=14, fontweight='bold')
    recommendations_text = """
    1. 수요일 특별 점검 체크리스트 운영
    2. 주간 피로도 누적 요인 분석 및 대응
    3. 목요일의 우수 운영 사례 표준화
    4. 교대 근무 인수인계 절차 개선
    """
    fig.text(0.18, 0.17, recommendations_text, fontsize=11, verticalalignment='top')
    
    pdf.savefig(fig, bbox_inches='tight')
    plt.close()
    
    # ========== 페이지 4: 월별 분석 ==========
    fig = plt.figure(figsize=(8.27, 11.69))
    fig.patch.set_facecolor('white')
    
    fig.text(0.5, 0.95, '월별 불량률 분석', 
             ha='center', fontsize=20, fontweight='bold')
    
    if os.path.exists('monthly_defect_analysis.png'):
        img = Image.open('monthly_defect_analysis.png')
        ax = fig.add_axes([0.1, 0.45, 0.8, 0.45])
        ax.imshow(img)
        ax.axis('off')
    
    fig.text(0.15, 0.40, '분석 결과', fontsize=14, fontweight='bold')
    analysis_text = """
    7월에 불량률이 14.04%로 급증하며, 8월에도 높은 수준을 유지합니다.
    여름철 높은 온습도 환경이 반도체 공정에 부정적 영향을 미치는 것으로
    판단되며, 환경 제어 시스템의 성능 점검이 필요합니다.
    """
    fig.text(0.18, 0.35, analysis_text, fontsize=11, verticalalignment='top')
    
    fig.text(0.15, 0.22, '개선 방안', fontsize=14, fontweight='bold')
    recommendations_text = """
    1. 여름철 이전 냉각 설비 사전 점검 실시
    2. 클린룸 온습도 제어 시스템 성능 향상
    3. 7월 이전 장비 정밀 캘리브레이션 수행
    4. 계절별 공정 파라미터 최적화 방안 수립
    """
    fig.text(0.18, 0.17, recommendations_text, fontsize=11, verticalalignment='top')
    
    pdf.savefig(fig, bbox_inches='tight')
    plt.close()
    
    # ========== 페이지 5: 히트맵 및 종합 결론 ==========
    fig = plt.figure(figsize=(8.27, 11.69))
    fig.patch.set_facecolor('white')
    
    fig.text(0.5, 0.95, '시간대×요일 불량률 히트맵', 
             ha='center', fontsize=20, fontweight='bold')
    
    if os.path.exists('hour_day_heatmap.png'):
        img = Image.open('hour_day_heatmap.png')
        ax = fig.add_axes([0.1, 0.50, 0.8, 0.40])
        ax.imshow(img)
        ax.axis('off')
    
    fig.text(0.15, 0.45, '종합 결론', fontsize=14, fontweight='bold')
    conclusion_text = """
    수요일 새벽 4시에 66.67%의 최고 불량률을 기록하였으며,
    시간대와 요일이 복합적으로 작용하는 패턴이 확인되었습니다.
    
    전반적으로 오후 시간대, 주중, 여름철에 불량률이 높아지는 경향이 있으며,
    이는 장비 열화, 인력 피로도, 환경 조건이 복합적으로 작용한 결과입니다.
    """
    fig.text(0.18, 0.40, conclusion_text, fontsize=11, verticalalignment='top')
    
    fig.text(0.15, 0.25, '최종 권장사항', fontsize=14, fontweight='bold')
    final_recommendations = """
    1. 실시간 SPC 시스템 도입으로 이상 징후 조기 감지
    2. 예측 모델 구축을 통한 사전 예방 관리 체계 확립
    3. 센서 데이터 기반 머신러닝 분석으로 불량 원인 규명
    4. 시간대별, 계절별 맞춤형 공정 관리 프로토콜 수립
    5. 불량률 제로 달성 사례 분석 및 표준화
    """
    fig.text(0.18, 0.20, final_recommendations, fontsize=11, verticalalignment='top')
    
    pdf.savefig(fig, bbox_inches='tight')
    plt.close()

print(f"보고서가 생성되었습니다: {pdf_path}")
print("총 5페이지로 구성되었습니다.")
