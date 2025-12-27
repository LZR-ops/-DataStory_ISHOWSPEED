import json
from pathlib import Path
import matplotlib.pyplot as plt


def load_sentiments(path):
    with open(path, encoding='utf-8') as f:
        data = json.load(f)
    counts = {'positive': 0, 'neutral': 0, 'negative': 0}
    for item in data:
        s = item.get('sentiment', {})
        compound = s.get('compound', 0.0)
        if compound > 0.05:
            counts['positive'] += 1
        elif compound < -0.05:
            counts['negative'] += 1
        else:
            counts['neutral'] += 1
    return counts


def plot_counts(counts, outpath, title):
    labels = ['Negative', 'Neutral', 'Positive']
    vals = [counts['negative'], counts['neutral'], counts['positive']]
    colors = ['#d9534f', '#5bc0de', '#5cb85c']

    fig, ax = plt.subplots(figsize=(6,4))
    bars = ax.bar(labels, vals, color=colors)
    ax.set_title(title)
    ax.set_ylabel('Count')

    # annotate counts above bars
    for bar, v in zip(bars, vals):
        ax.text(bar.get_x() + bar.get_width()/2, v + max(vals)*0.01 + 1, str(v),
                ha='center', va='bottom', fontsize=10)

    plt.tight_layout()
    outpath.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(outpath, dpi=150)
    plt.close()


def main():
    root = Path(__file__).resolve().parents[1]
    sh_path = root / 'data' / 'sentiment_comments.json'
    cq_path = root / 'data2' / 'sentiment_comments.json'
    out_dir = root / 'presetation'

    if sh_path.exists():
        sh_counts = load_sentiments(sh_path)
        plot_counts(sh_counts, out_dir / 'sentiment_dist_shanghai.png', 'Sentiment distribution — Shanghai')
        print('Wrote', out_dir / 'sentiment_dist_shanghai.png')
    else:
        print('Missing', sh_path)

    if cq_path.exists():
        cq_counts = load_sentiments(cq_path)
        plot_counts(cq_counts, out_dir / 'sentiment_dist_chongqing.png', 'Sentiment distribution — Chongqing')
        print('Wrote', out_dir / 'sentiment_dist_chongqing.png')
    else:
        print('Missing', cq_path)


if __name__ == '__main__':
    main()
