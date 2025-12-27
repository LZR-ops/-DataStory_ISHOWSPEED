# filename: top10_keywords_with_chart.py
import json
from collections import Counter
import re
import matplotlib.pyplot as plt

# ========= CONFIGURATION =========
FILE_PATH = "clean_comments_chongqing.json"   
TOP_N = 10
# ==================================

def get_top_keywords(file_path, top_n=10):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Combine all clean_text fields
    all_text = ' '.join(item.get('clean_text', '') for item in data if item.get('clean_text'))

    # Basic cleaning
    all_text = re.sub(r'[^\w\s]', '', all_text.lower())
    words = all_text.split()

    # Simple English stopwords + very common short/generic words in this context
    stopwords = {
        'the','a','an','and','or','but','if','while','at','by','for','with','about','to','from',
        'in','out','on','off','over','up','down','it','is','are','was','were','be','been','have',
        'has','had','do','does','did','of','that','this','i','you','he','she','we','they','me',
        'him','her','us','them','not','no','yes','s','t','can','will','just','so','very','lol',
        'www','w','ww','u','im','n'
    }

    # Filter: remove stopwords & very short words
    filtered = [word for word in words if word not in stopwords and len(word) > 2]

    # Count and get top N
    counter = Counter(filtered)
    top_keywords = counter.most_common(top_n)

    return top_keywords

# ============= RUN =============
top_10 = get_top_keywords(FILE_PATH, TOP_N)

print("\n" + "="*50)
print("     TOP 10 KEYWORDS IN COMMENTS")
print("="*50)
for rank, (keyword, count) in enumerate(top_10, 1):
    print(f"{rank:2}. {keyword:<12} → {count:>4} times")
print("="*50 + "\n")

# ============= PLOT =============
keywords = [kw for kw, _ in top_10]
counts   = [cnt for _, cnt in top_10]

plt.figure(figsize=(12, 7))
bars = plt.bar(keywords, counts, color='#1f77b4', edgecolor='black', linewidth=0.8)

# Styling to match your screenshot
plt.title('Top 10 Keywords in Comments', fontsize=18, fontweight='bold', pad=20)
plt.xlabel('Keyword', fontsize=14)
plt.ylabel('Frequency', fontsize=14)
plt.xticks(rotation=15, fontsize=12)
plt.yticks(fontsize=12)

# Add value labels on top of each bar
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2., height + max(counts)*0.01,
             f'{int(height)}', ha='center', va='bottom', fontsize=11, fontweight='bold')

plt.tight_layout()

plt.savefig('Top_10_Keywords_Chart.png', dpi=300, bbox_inches='tight')
print("Chart saved as → Top_10_Keywords_Chart.png")

plt.show()