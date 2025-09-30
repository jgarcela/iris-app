#!/usr/bin/env python3
import os
import sys
import time
import json
from datetime import datetime, timezone

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database.db import DB_AI_CACHE
from utils.challenge_ai import CHALLENGE_TEXTS, simulate_ai_analysis

def main():
    count = 0
    for text in CHALLENGE_TEXTS:
        text_id = text['id']
        existing = DB_AI_CACHE.find_one({'text_id': text_id})
        if existing:
            print(f"[CACHE] Exists for text_id={text_id}, skipping")
            continue
        ai_analysis = simulate_ai_analysis(text, manual_annotations=[])
        doc = {
            'text_id': text_id,
            'text_title': text['title'],
            'ai_analysis': ai_analysis,
            'source': 'precompute',
            'created_at': datetime.now(timezone.utc),
            'updated_at': datetime.now(timezone.utc)
        }
        DB_AI_CACHE.insert_one(doc)
        count += 1
        print(f"[CACHE] Stored AI analysis for text_id={text_id}")
        time.sleep(0.2)
    print(f"Done. New cached analyses: {count}")

if __name__ == '__main__':
    main()


