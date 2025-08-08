# interlinking_core.py

import os
import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urlparse
from collections import defaultdict

MAX_LINKS_PER_ARTICLE = 6


def fetch_article_html(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.text
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None


def extract_domain_path(url):
    parsed = urlparse(url)
    return parsed.path


def clean_keyword(kw):
    return kw.lower().strip()


def inject_links(html, link_injections):
    soup = BeautifulSoup(html, "html.parser")
    full_text = str(soup)
    injected = 0
    used_keywords = set()

    for keyword, target_url in link_injections:
        if injected >= MAX_LINKS_PER_ARTICLE:
            break

        if keyword in used_keywords:
            continue

        pattern = rf'(?<![>\w])({re.escape(keyword)})(?![<\w])'
        link_tag = f'<a href="{target_url}">\\1</a>'

        new_text, count = re.subn(pattern, link_tag, full_text, count=1, flags=re.IGNORECASE)
        if count > 0:
            full_text = new_text
            used_keywords.add(keyword)
            injected += 1

    return full_text, injected


def run_interlinking(input_csv, output_dir):
    df = pd.read_csv(input_csv)
    df['keywords'] = df['keywords'].fillna('').apply(lambda x: [clean_keyword(k) for k in x.split(',') if k.strip()])
    url_keywords_map = dict(zip(df['url'], df['keywords']))

    keyword_to_url = {}
    for url, keywords in url_keywords_map.items():
        for kw in keywords:
            if kw not in keyword_to_url:
                keyword_to_url[kw] = url  # Link keyword to its source url

    url_html_map = {}
    url_text_map = {}
    for url in df['url']:
        html = fetch_article_html(url)
        if html:
            url_html_map[url] = html
            soup = BeautifulSoup(html, 'html.parser')
            url_text_map[url] = soup.get_text(" ", strip=True).lower()

    results = []
    for source_url, source_text in url_text_map.items():
        html = url_html_map[source_url]
        used_keywords = set()
        link_injections = []

        for keyword, target_url in keyword_to_url.items():
            if target_url == source_url:
                continue  # Don’t link to itself
            if keyword in used_keywords:
                continue
            if keyword not in source_text:
                continue

            link_injections.append((keyword, target_url))
            used_keywords.add(keyword)
            if len(link_injections) >= MAX_LINKS_PER_ARTICLE:
                break

        updated_html, link_count = inject_links(html, link_injections)

        filename = f"linked_{os.path.basename(extract_domain_path(source_url)) or 'index.html'}"
        output_html_path = os.path.join(output_dir, filename)
        with open(output_html_path, "w", encoding="utf-8") as f:
            f.write(updated_html)

        for keyword, target_url in link_injections[:link_count]:
            snippet_index = source_text.find(keyword)
            snippet = source_text[max(0, snippet_index-30):snippet_index+30]
            results.append({
                "source_url": source_url,
                "target_keyword": keyword,
                "target_url": target_url,
                "context_snippet": snippet
            })

    output_excel_path = os.path.join(output_dir, "interlinking_output.xlsx")
    pd.DataFrame(results).to_excel(output_excel_path, index=False)
    return output_excel_path, output_dir

# Example usage
# run_interlinking("input_sample.csv", "./outputs")
