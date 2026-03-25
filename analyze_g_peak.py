"""
Raman G-peak before/after 차이 분석 및 시각화 스크립트
사용법: python analyze_g_peak.py [파일경로]
       (파일경로 생략 시 sample_data.csv 사용)
"""

import sys
import os
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import numpy as np

# ── 한글 폰트 설정 (macOS) ──────────────────────────────────────────────────
def set_korean_font():
    candidates = [
        "AppleGothic",
        "Apple SD Gothic Neo",
        "NanumGothic",
        "Malgun Gothic",
    ]
    available = {f.name for f in fm.fontManager.ttflist}
    for name in candidates:
        if name in available:
            matplotlib.rc("font", family=name)
            print(f"한글 폰트 설정: {name}")
            return
    # 폰트 못 찾으면 유니코드 fallback
    matplotlib.rc("axes", unicode_minus=False)
    print("경고: 한글 폰트를 찾지 못했습니다. 텍스트가 깨질 수 있습니다.")

set_korean_font()
matplotlib.rc("axes", unicode_minus=False)

# ── 파일 읽기 ────────────────────────────────────────────────────────────────
BASE_DIR = "/Users/jeong-uchang/HADD SCIENCE/raman_g_peak_diff"

if len(sys.argv) > 1:
    filepath = sys.argv[1]
else:
    filepath = os.path.join(BASE_DIR, "sample_data.csv")

ext = os.path.splitext(filepath)[1].lower()
if ext == ".xlsx":
    df = pd.read_excel(filepath)
    print(f"XLSX 파일 읽기 완료: {filepath}")
else:
    df = pd.read_csv(filepath)
    print(f"CSV 파일 읽기 완료: {filepath}")

print(f"총 샘플 수: {len(df)}")

# ── diff 계산 ────────────────────────────────────────────────────────────────
df["diff"] = df["g_peak_before"] - df["g_peak_after"]

print("\ndiff 기술 통계:")
print(df["diff"].describe().round(3))

# ── 구간 분류 ────────────────────────────────────────────────────────────────
def classify_diff(v):
    if v < 0:
        return "음수 (< 0)"
    elif v < 0.5:
        return "0 ~ 0.5"
    elif v < 1:
        return "0.5 ~ 1"
    elif v < 1.5:
        return "1 ~ 1.5"
    elif v < 2:
        return "1.5 ~ 2"
    elif v < 2.5:
        return "2 ~ 2.5"
    elif v < 3:
        return "2.5 ~ 3"
    else:
        return "3 이상"

CATEGORY_ORDER = [
    "음수 (< 0)", "0 ~ 0.5", "0.5 ~ 1",
    "1 ~ 1.5", "1.5 ~ 2", "2 ~ 2.5", "2.5 ~ 3", "3 이상"
]
COLORS = {
    "음수 (< 0)": "#4C72B0",
    "0 ~ 0.5":    "#90CAF9",
    "0.5 ~ 1":    "#64B5F6",
    "1 ~ 1.5":    "#FFB74D",
    "1.5 ~ 2":    "#FF8A65",
    "2 ~ 2.5":    "#EF5350",
    "2.5 ~ 3":    "#E53935",
    "3 이상":     "#B71C1C",
}

df["category"] = df["diff"].apply(classify_diff)
counts = df["category"].value_counts()
# 실제 존재하는 카테고리만 순서대로
present = [c for c in CATEGORY_ORDER if c in counts.index]
counts = counts[present]

print("\n구간별 분포:")
for cat in present:
    print(f"  {cat}: {counts[cat]}개 ({counts[cat]/len(df)*100:.1f}%)")

# ── 시각화 ───────────────────────────────────────────────────────────────────
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 6))
fig.suptitle("Raman G-peak 차이 분포 분석\n(before - after)", fontsize=14, fontweight="bold", y=1.01)

# ── 서브플롯 1: 파이차트 ─────────────────────────────────────────────────────
pie_colors = [COLORS[c] for c in present]

# 1 이상인 구간은 explode
explode = []
for c in present:
    if c in ("1 ~ 1.5", "1.5 ~ 2", "2 ~ 2.5", "2.5 ~ 3", "3 이상"):
        explode.append(0.07)
    else:
        explode.append(0)

def autopct_fmt(pct, allvals):
    absolute = int(round(pct / 100.0 * sum(allvals)))
    return f"{absolute}개\n({pct:.1f}%)"

wedges, texts, autotexts = ax1.pie(
    counts,
    labels=present,
    colors=pie_colors,
    explode=explode,
    autopct=lambda pct: autopct_fmt(pct, counts),
    startangle=140,
    pctdistance=0.7,
    wedgeprops={"edgecolor": "white", "linewidth": 1.5},
    textprops={"fontsize": 10},
)

for at in autotexts:
    at.set_fontsize(9)

ax1.set_title("구간별 샘플 비율", fontsize=12, fontweight="bold", pad=12)

# 범례 (1이상 강조 표시)
legend_labels = []
for c in present:
    if c in ("1 ~ 1.5", "1.5 ~ 2", "2 ~ 2.5", "2.5 ~ 3", "3 이상"):
        legend_labels.append(f"{c}  ← 유의 구간")
    else:
        legend_labels.append(c)

ax1.legend(
    wedges,
    legend_labels,
    loc="lower center",
    bbox_to_anchor=(0.5, -0.18),
    fontsize=9,
    framealpha=0.8,
)

# ── 서브플롯 2: 히스토그램 ───────────────────────────────────────────────────
diff_vals = df["diff"].values
all_min = diff_vals.min()
all_max = diff_vals.max()

# 구간 경계 결정
boundaries = [0, 0.5, 1, 1.5, 2, 2.5, 3]
bin_start = min(all_min - 0.3, -1.3)
bin_end   = max(all_max + 0.3,  3.3)
bin_edges = np.arange(bin_start, bin_end + 0.25, 0.25)

# 색상: 음수=파랑, 0~1=연파랑, 1이상=주황/빨강
def bar_color(left, right):
    mid = (left + right) / 2
    if mid < 0:
        return COLORS["음수 (< 0)"]
    elif mid < 0.5:
        return COLORS["0 ~ 0.5"]
    elif mid < 1:
        return COLORS["0.5 ~ 1"]
    elif mid < 1.5:
        return COLORS["1 ~ 1.5"]
    elif mid < 2:
        return COLORS["1.5 ~ 2"]
    elif mid < 2.5:
        return COLORS["2 ~ 2.5"]
    elif mid < 3:
        return COLORS["2.5 ~ 3"]
    else:
        return COLORS["3 이상"]

counts_hist, edges = np.histogram(diff_vals, bins=bin_edges)
for i in range(len(counts_hist)):
    ax2.bar(
        edges[i],
        counts_hist[i],
        width=(edges[i + 1] - edges[i]),
        color=bar_color(edges[i], edges[i + 1]),
        edgecolor="white",
        linewidth=0.8,
        align="edge",
    )

# 구간 경계 수직 점선
for b in boundaries:
    ax2.axvline(x=b, color="gray", linestyle="--", linewidth=1.2, alpha=0.7)
    ax2.text(b + 0.04, ax2.get_ylim()[1] if ax2.get_ylim()[1] > 0 else 1,
             str(b), color="gray", fontsize=8, va="top")

# 0 기준선 강조
ax2.axvline(x=0, color="#333333", linestyle="-", linewidth=1.5, alpha=0.5)

ax2.set_xlabel("G-peak 차이 (cm-1)\nbefore - after", fontsize=11)
ax2.set_ylabel("빈도", fontsize=11)
ax2.set_title("G-peak 차이 히스토그램", fontsize=12, fontweight="bold")
ax2.set_xlim(bin_start, bin_end)
ax2.yaxis.set_major_locator(matplotlib.ticker.MaxNLocator(integer=True))

# 색상 범례
from matplotlib.patches import Patch
legend_elements = [
    Patch(facecolor=COLORS["음수 (< 0)"], edgecolor="white", label="음수 (< 0)"),
    Patch(facecolor=COLORS["0 ~ 0.5"],    edgecolor="white", label="0 ~ 0.5"),
    Patch(facecolor=COLORS["0.5 ~ 1"],    edgecolor="white", label="0.5 ~ 1"),
    Patch(facecolor=COLORS["1 ~ 1.5"],    edgecolor="white", label="1 ~ 1.5  ★"),
    Patch(facecolor=COLORS["1.5 ~ 2"],    edgecolor="white", label="1.5 ~ 2  ★"),
    Patch(facecolor=COLORS["2 ~ 2.5"],    edgecolor="white", label="2 ~ 2.5  ★"),
    Patch(facecolor=COLORS["2.5 ~ 3"],    edgecolor="white", label="2.5 ~ 3  ★"),
]
if "3 이상" in present:
    legend_elements.append(
        Patch(facecolor=COLORS["3 이상"], edgecolor="white", label="3 이상  ★")
    )
ax2.legend(handles=legend_elements, fontsize=9, loc="upper right", framealpha=0.85)

# 통계 텍스트 박스
stats_text = (
    f"n = {len(df)}\n"
    f"평균: {df['diff'].mean():.2f} cm⁻¹\n"
    f"중앙값: {df['diff'].median():.2f} cm⁻¹\n"
    f"표준편차: {df['diff'].std():.2f} cm⁻¹"
)
ax2.text(
    0.03, 0.97, stats_text,
    transform=ax2.transAxes,
    fontsize=8.5,
    verticalalignment="top",
    bbox=dict(boxstyle="round,pad=0.4", facecolor="lightyellow", alpha=0.85, edgecolor="gray"),
)

plt.tight_layout()

# ── 저장 ────────────────────────────────────────────────────────────────────
out_path = os.path.join(BASE_DIR, "g_peak_analysis.png")
plt.savefig(out_path, dpi=300, bbox_inches="tight")
print(f"\n결과 이미지 저장 완료: {out_path}")
plt.close()
