#!/usr/bin/env python3
"""
Test script to generate an RTF review file with multiple articles
"""

from create_rtf_review import create_rtf_review_file

# Read all the uploaded HTML files
articles = [
    'BBC_2023-10-10_Radcliffe-Camera-in-Oxford',
    'BBC_2023-10-11_Paint-sprayed-on-Falmouth',
    'BBC_2023-10-12_Just-Stop-Oil-protesters'
]

original_articles = {}
summary_articles = {}

for article_id in articles:
    # Read original
    with open(f'/mnt/user-data/uploads/{article_id}_original.html', 'r') as f:
        original_articles[article_id] = f.read()
    
    # Read summary
    with open(f'/mnt/user-data/uploads/{article_id}_summary.html', 'r') as f:
        summary_articles[article_id] = f.read()

# Generate the RTF file with all articles
create_rtf_review_file(
    original_articles, 
    summary_articles, 
    '/mnt/user-data/outputs/article_review_multiple.rtf'
)

print(f"RTF file created with {len(articles)} articles!")
print("Article IDs included:")
for article_id in articles:
    print(f"  - {article_id}")
