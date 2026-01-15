from nba_api.stats.endpoints import leaguedashplayerstats
import matplotlib.pyplot as plt
import pandas as pd
import requests
from PIL import Image, ImageDraw, ImageFilter
from io import BytesIO
from matplotlib.offsetbox import OffsetImage, AnnotationBbox

# ---------------------------------------------------------
# 1.  INVERTED MONOCHROME THEME – WHITE BG, BLACK BARS
# ---------------------------------------------------------
plt.rcParams.update({
    "figure.facecolor": "#ffffff",
    "axes.facecolor":   "#ffffff",
    "axes.edgecolor":   "#000000",
    "axes.labelcolor":  "#000000",
    "xtick.color":      "#000000",
    "ytick.color":      "#000000",
    "grid.color":       "#cccccc",
    "text.color":       "#000000",
    "font.weight":      "semibold"
})

# ---------------------------------------------------------
# 2.  DATA: 2025-26 season
# ---------------------------------------------------------
stats = leaguedashplayerstats.LeagueDashPlayerStats(season="2025-26")
df_25_26 = stats.get_data_frames()[0]
df_25_26["PPG"] = df_25_26["PTS"] / df_25_26["GP"]
df_25_26 = df_25_26[["PLAYER_ID", "PLAYER_NAME", "PPG"]].rename(columns={"PPG": "PPG_25_26"})

# ---------------------------------------------------------
# 3.  DATA: 2024-25 season
# ---------------------------------------------------------
stats = leaguedashplayerstats.LeagueDashPlayerStats(season="2024-25")
df_24_25 = stats.get_data_frames()[0]
df_24_25["PPG"] = df_24_25["PTS"] / df_24_25["GP"]
df_24_25 = df_24_25[["PLAYER_ID", "PLAYER_NAME", "PPG"]].rename(columns={"PPG": "PPG_24_25"})

# ---------------------------------------------------------
# 4.  MERGE & CALC DIFF
# ---------------------------------------------------------
merged = pd.merge(df_25_26, df_24_25, on="PLAYER_ID", suffixes=("_this", "_last"), how="inner")
merged["PLAYER_NAME"] = merged["PLAYER_NAME_this"]
merged["PPG_DIFF"] = (merged["PPG_25_26"] - merged["PPG_24_25"]).round(2)

# ---------------------------------------------------------
# 5.  TOP-10 IMPROVERS (ascending for plot)
# ---------------------------------------------------------
top10 = merged.sort_values("PPG_DIFF", ascending=False).head(10).sort_values("PPG_DIFF", ascending=True)

# ---------------------------------------------------------
# 6.  PLOT FRAME
# ---------------------------------------------------------
plt.figure(figsize=(12, 8))
ax = plt.gca()
bars = ax.bar(range(len(top10)), top10["PPG_DIFF"], color="#555555", width=0.65, zorder=3)
ax.yaxis.grid(True, linestyle="-", alpha=0.35, zorder=0)
ax.set_axisbelow(True)
plt.subplots_adjust(bottom=0.25, top=0.90)

# ---------------------------------------------------------
# 7.  HEAD-SHOT MASK HELPER
# ---------------------------------------------------------
def circ_mask(img: Image.Image) -> Image.Image:
    mask = Image.new("L", img.size, 0)
    draw = ImageDraw.Draw(mask)
    cx, cy = img.width // 2, img.height // 2
    r = min(cx, cy)
    draw.ellipse((cx - r, cy - r, cx + r, cy + r), fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(0.8))
    img = img.copy()
    img.putalpha(mask)
    return img

# ---------------------------------------------------------
# 8.  PLACE HEAD-SHOTS
# ---------------------------------------------------------
for idx, pid in enumerate(top10["PLAYER_ID"]):
    url = f"https://cdn.nba.com/headshots/nba/latest/260x190/{pid}.png"
    try:
        rsp = requests.get(url, timeout=6)
        rsp.raise_for_status()
        img = Image.open(BytesIO(rsp.content)).convert("RGBA")
        img = circ_mask(img)
        imagebox = OffsetImage(img, zoom=70/img.height, resample=True)
        ab = AnnotationBbox(imagebox, (idx, -0.7), frameon=False, box_alignment=(0.5, 1))
        ax.add_artist(ab)
    except Exception as e:
        print(pid, e)

# ---------------------------------------------------------
# 9.  VALUE LABELS
# ---------------------------------------------------------
for bar, value in zip(bars, top10["PPG_DIFF"]):
    ax.text(bar.get_x() + bar.get_width()/2,
            bar.get_height() + 0.15,
            f"{value:.2f}",
            ha="center", va="bottom", fontsize=10, fontweight="bold", color="#000000")

# ---------------------------------------------------------
# 10. FINAL STYLING
# ---------------------------------------------------------
plt.xticks(range(len(top10)), [""]*len(top10))
plt.title("Top 10 PPG Improvements: 2024-25 to 2025-26 @MetrixBall", fontsize=16, weight="bold", pad=12)
plt.ylabel("PPG Increase", fontsize=12)
plt.ylim(-1, top10["PPG_DIFF"].max() + 3)
plt.tight_layout()
plt.show()