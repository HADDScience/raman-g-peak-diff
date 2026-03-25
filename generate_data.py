"""
예시 데이터 생성 스크립트
Raman G-peak before/after 데이터를 CSV와 XLSX로 저장
"""

import pandas as pd
import numpy as np

np.random.seed(42)

# 샘플 정의: (sample_id, condition, concentration, replicate)
samples = [
    ("Sample_01", "Ref_1M",     "1M",    93),
    ("Sample_02", "Fmn1_1M",   "1M",    92),
    ("Sample_03", "Ref_100mM", "100mM", 88),
    ("Sample_04", "Fmn1_100mM","100mM", 87),
    ("Sample_05", "Ref_100mM", "100mM", 85),
    ("Sample_06", "Fmn1_100mM","100mM", 84),
    ("Sample_07", "Ref_10mM",  "10mM",  76),
    ("Sample_08", "Fmn1_10mM", "10mM",  75),
    ("Sample_09", "Ref_10mM",  "10mM",  73),
    ("Sample_10", "Fmn1_10mM", "10mM",  72),
    ("Sample_11", "Ref_1mM",   "1mM",   68),
    ("Sample_12", "Fmn1_1mM",  "1mM",   67),
    ("Sample_13", "Ref_1mM",   "1mM",   65),
    ("Sample_14", "Fmn1_1mM",  "1mM",   64),
    ("Sample_15", "Ref_1M",    "1M",    91),
    ("Sample_16", "Fmn1_1M",   "1M",    90),
    ("Sample_17", "Ref_100mM", "100mM", 83),
    ("Sample_18", "Fmn1_100mM","100mM", 82),
    ("Sample_19", "Ref_10mM",  "10mM",  71),
    ("Sample_20", "Fmn1_10mM", "10mM",  70),
]

# 목표 diff 분포: 음수, 0~1, 1~2, 2~3 에 골고루
# diff = before - after
target_diffs = [
    -0.8,   # 음수
     0.3,   # 0~1
    -0.5,   # 음수
     0.7,   # 0~1
     1.1,   # 1~2
     0.9,   # 0~1
     2.2,   # 2~3
     1.5,   # 1~2
    -0.2,   # 음수
     0.4,   # 0~1
     2.8,   # 2~3
     1.8,   # 1~2
     0.6,   # 0~1
    -1.0,   # 음수
     1.3,   # 1~2
     0.2,   # 0~1
     2.5,   # 2~3
     0.8,   # 0~1
     1.6,   # 1~2
    -0.3,   # 음수
]

rows = []
for i, (sid, cond, conc, rep) in enumerate(samples):
    diff = target_diffs[i]
    # before: 1586~1593 범위
    before = round(1589.0 + np.random.uniform(-1.5, 1.5), 1)
    # after = before - diff (+ 작은 노이즈)
    after = round(before - diff + np.random.uniform(-0.05, 0.05), 1)
    rows.append({
        "sample_id": sid,
        "condition": cond,
        "concentration": conc,
        "replicate": rep,
        "g_peak_before": before,
        "g_peak_after": after,
    })

df = pd.DataFrame(rows)

# CSV 저장
csv_path = "/Users/jeong-uchang/HADD SCIENCE/raman_g_peak_diff/sample_data.csv"
df.to_csv(csv_path, index=False)
print(f"CSV saved: {csv_path}")

# XLSX 저장
xlsx_path = "/Users/jeong-uchang/HADD SCIENCE/raman_g_peak_diff/sample_data.xlsx"
df.to_excel(xlsx_path, index=False)
print(f"XLSX saved: {xlsx_path}")

print("\n생성된 데이터 미리보기:")
print(df.to_string(index=False))
