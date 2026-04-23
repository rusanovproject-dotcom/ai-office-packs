#!/usr/bin/env python3
"""
Парсер HTML-экспорта Telegram-канала "РУСАНОВ БИОХАКИНГ"
Извлекает посты, реакции, медиа, ссылки → JSON + MD
"""

import json
import re
import html
from datetime import datetime
from collections import Counter
from bs4 import BeautifulSoup

INPUT = "/Users/macbookpro132017/Downloads/Telegram Desktop/ChatExport_2026-04-13/messages.html"
OUT_DIR = "/Users/macbookpro132017/workspace/second-brain/tg-posts"


def parse_date(title_str):
    """Parse '20.12.2023 23:50:46 UTC+07:00' → ISO string"""
    if not title_str:
        return None
    # Remove UTC+ timezone part for parsing
    m = re.match(r'(\d{2}\.\d{2}\.\d{4} \d{2}:\d{2}:\d{2})', title_str)
    if m:
        dt = datetime.strptime(m.group(1), '%d.%m.%Y %H:%M:%S')
        return dt.isoformat()
    return title_str


def extract_text(text_div):
    """Extract clean text from div.text, preserving line breaks"""
    if not text_div:
        return ""
    # Replace <br> with newlines
    for br in text_div.find_all('br'):
        br.replace_with('\n')
    text = text_div.get_text()
    # Decode HTML entities (bs4 does most, but just in case)
    text = html.unescape(text)
    # Clean up whitespace but preserve newlines
    lines = text.split('\n')
    lines = [line.strip() for line in lines]
    text = '\n'.join(lines)
    # Remove leading/trailing blank lines
    text = text.strip()
    return text


def extract_links(text_div):
    """Extract all href links from text div"""
    if not text_div:
        return []
    links = []
    for a in text_div.find_all('a'):
        href = a.get('href', '')
        if href:
            links.append(href)
    return links


def extract_reactions(msg_div):
    """Extract reactions [{emoji, count}] from span.reactions"""
    reactions = []
    reactions_span = msg_div.find('span', class_='reactions')
    if not reactions_span:
        return reactions
    for reaction in reactions_span.find_all('span', class_='reaction'):
        emoji_span = reaction.find('span', class_='emoji')
        count_span = reaction.find('span', class_='count')
        if emoji_span and count_span:
            emoji = emoji_span.get_text().strip()
            try:
                count = int(count_span.get_text().strip())
            except ValueError:
                count = 0
            reactions.append({"emoji": emoji, "count": count})
    return reactions


def detect_media(msg_div):
    """Detect media type from media_* classes"""
    media_map = {
        'media_photo': 'photo',
        'media_voice_message': 'voice_message',
        'media_video': 'video',
        'media_audio_file': 'audio_file',
        'media_sticker': 'sticker',
        'media_video_message': 'video_message',
        'media_document': 'document',
        'media_contact': 'contact',
        'media_poll': 'poll',
        'media_location': 'location',
        'media_game': 'game',
        'media_webpage': 'webpage',
    }
    media_div = msg_div.find('div', class_='media')
    if not media_div:
        return None, None
    classes = media_div.get('class', [])
    media_type = None
    for cls in classes:
        if cls in media_map:
            media_type = media_map[cls]
            break
    # Get description
    desc_div = media_div.find('div', class_='description')
    media_desc = desc_div.get_text().strip() if desc_div else None
    return media_type, media_desc


def classify_content(text, has_media, links):
    """Auto-classify content type"""
    has_text = bool(text and len(text.strip()) > 0)
    if has_media == 'voice_message':
        return 'voice'
    if has_media == 'video':
        return 'video'
    if has_media == 'sticker':
        return 'sticker'
    if has_media == 'video_message':
        return 'video_message'
    if has_media == 'audio_file':
        return 'audio_file'
    if has_media == 'photo' and has_text:
        return 'photo_with_text'
    if has_media == 'photo' and not has_text:
        return 'photo'
    if links and has_text:
        return 'link_post'
    if has_text:
        return 'text'
    return 'other'


def main():
    print("Читаю HTML...")
    with open(INPUT, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')

    # Find all non-service messages
    all_divs = soup.find_all('div', class_='message')
    posts = []

    for div in all_divs:
        classes = div.get('class', [])
        # Skip service messages
        if 'service' in classes:
            continue
        if 'default' not in classes:
            continue

        msg_id_raw = div.get('id', '')
        # Extract numeric id
        msg_id = re.sub(r'[^0-9]', '', msg_id_raw)
        msg_id = int(msg_id) if msg_id else 0

        is_joined = 'joined' in classes

        # Date
        date_div = div.find('div', class_='date')
        date_title = date_div.get('title', '') if date_div else ''
        date_iso = parse_date(date_title)

        # Text
        text_div = div.find('div', class_='text')
        text = extract_text(text_div)

        # Links
        # Re-parse text_div for links (since we modified it for text extraction)
        # Need to find it again from original div
        text_div_for_links = div.find('div', class_='text')
        links = extract_links(text_div_for_links)

        # Reactions
        reactions = extract_reactions(div)
        total_reactions = sum(r['count'] for r in reactions)

        # Media
        has_media, media_desc = detect_media(div)

        # Word count
        word_count = len(text.split()) if text else 0

        # Content type
        content_type = classify_content(text, has_media, links)

        post = {
            "id": msg_id,
            "date": date_iso,
            "date_raw": date_title,
            "text": text,
            "reactions": reactions,
            "total_reactions": total_reactions,
            "has_media": has_media,
            "media_description": media_desc,
            "links": links,
            "word_count": word_count,
            "content_type": content_type,
            "joined": is_joined,
        }
        posts.append(post)

    # Sort by id (chronological)
    posts.sort(key=lambda p: p['id'])

    print(f"Распарсено постов: {len(posts)}")

    # === File 1: all-posts.json ===
    with open(f"{OUT_DIR}/all-posts.json", 'w', encoding='utf-8') as f:
        json.dump(posts, f, ensure_ascii=False, indent=2)
    print(f"Сохранено: all-posts.json")

    # === Stats ===
    dates = [p['date'][:10] for p in posts if p['date']]
    date_from = min(dates) if dates else ""
    date_to = max(dates) if dates else ""

    by_content_type = Counter(p['content_type'] for p in posts)
    by_month = Counter()
    for p in posts:
        if p['date']:
            ym = p['date'][:7]
            by_month[ym] = by_month.get(ym, 0) + 1

    all_reactions = [p['total_reactions'] for p in posts]
    avg_reactions = round(sum(all_reactions) / len(all_reactions), 1) if all_reactions else 0

    text_posts = [p for p in posts if p['word_count'] > 0]
    word_counts = [p['word_count'] for p in text_posts]
    avg_word_count = round(sum(word_counts) / len(word_counts), 1) if word_counts else 0

    top_by_reactions = sorted(posts, key=lambda p: p['total_reactions'], reverse=True)[:20]
    top_posts_summary = []
    for p in top_by_reactions:
        top_posts_summary.append({
            "id": p['id'],
            "date": p['date'],
            "total_reactions": p['total_reactions'],
            "reactions": p['reactions'],
            "content_type": p['content_type'],
            "text_preview": (p['text'][:150] + "...") if len(p['text']) > 150 else p['text'],
        })

    stats = {
        "total_posts": len(posts),
        "date_range": {"from": date_from, "to": date_to},
        "by_content_type": dict(sorted(by_content_type.items(), key=lambda x: -x[1])),
        "by_month": dict(sorted(by_month.items())),
        "top_posts_by_reactions": top_posts_summary,
        "avg_reactions": avg_reactions,
        "avg_word_count": avg_word_count,
        "total_with_text": len(text_posts),
        "total_without_text": len(posts) - len(text_posts),
    }

    with open(f"{OUT_DIR}/stats.json", 'w', encoding='utf-8') as f:
        json.dump(stats, f, ensure_ascii=False, indent=2)
    print(f"Сохранено: stats.json")

    # === File 3: posts-text-only.md ===
    lines = []
    for p in posts:
        if not p['text']:
            continue
        date_str = p['date'][:10] if p['date'] else "N/A"
        # Format reactions
        reaction_strs = [f"{r['emoji']}{r['count']}" for r in p['reactions']]
        reactions_display = " ".join(reaction_strs) if reaction_strs else "—"

        lines.append("---")
        lines.append(f"## {date_str} | ID: {p['id']} | Реакции: {reactions_display} | Тип: {p['content_type']}")
        lines.append("")
        lines.append(p['text'])
        lines.append("")

    with open(f"{OUT_DIR}/posts-text-only.md", 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    print(f"Сохранено: posts-text-only.md ({len(text_posts)} постов с текстом)")

    # === Print summary ===
    print("\n=== ИТОГОВАЯ СТАТИСТИКА ===")
    print(f"Всего постов: {len(posts)}")
    print(f"Диапазон дат: {date_from} — {date_to}")
    print(f"С текстом: {len(text_posts)}, без текста: {len(posts) - len(text_posts)}")
    print(f"Joined (продолжения): {sum(1 for p in posts if p['joined'])}")
    print(f"Среднее реакций: {avg_reactions}")
    print(f"Среднее слов (в текстовых): {avg_word_count}")
    print(f"\nПо типу контента:")
    for ct, count in sorted(by_content_type.items(), key=lambda x: -x[1]):
        print(f"  {ct}: {count}")
    print(f"\nТоп-5 постов по реакциям:")
    for p in top_by_reactions[:5]:
        preview = p['text'][:80].replace('\n', ' ') if p['text'] else '[no text]'
        print(f"  ID {p['id']} ({p['total_reactions']} реакций): {preview}...")


if __name__ == '__main__':
    main()
