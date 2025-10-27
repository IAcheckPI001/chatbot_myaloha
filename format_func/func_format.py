
import json
import re
from typing import Dict
from functools import lru_cache

# Đường dẫn path file từ viết tắt
file_format_json = "sync_format.json"

@lru_cache(maxsize=1) # Lưu dữ liệu vào cache trong lần duyệt đầu
def load_abbreviations(path: str = "sync_format.json") -> Dict[str, str]:
    """Đọc file JSON và chuẩn hóa key (lowercase + bỏ khoảng trắng thừa)"""
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    mapping = {re.sub(r'\s+', ' ', k.strip().lower()): v.strip() for k, v in data.items()}
    return mapping

# mapping = load_abbreviations(file_format_json)
# print(mapping)

def build_abbr_pattern(mapping: Dict[str, str]) -> re.Pattern:
    """Tạo regex pattern tối ưu từ danh sách viết tắt"""
    # Sắp xếp key dài trước để tránh match sai (vd: "uv" vs "uv btv")
    sorted_keys = sorted(mapping.keys(), key=len, reverse=True)
    escaped = [re.escape(k).replace(r'\ ', r'\s+') for k in sorted_keys]
    pattern = r'(?i)(?<!\w)(' + '|'.join(escaped) + r')(?!\w)'
    return re.compile(pattern, flags=re.UNICODE)

# patten = build_abbr_pattern(mapping)
# print(patten)

def expand_abbreviations(text: str, mapping: Dict[str, str], pattern: re.Pattern) -> str:
    """Thay thế từ viết tắt bằng từ đầy đủ"""
    def repl(m: re.Match):
        key = re.sub(r'\s+', ' ', m.group(0).lower().strip())
        return mapping.get(key, m.group(0))
    return pattern.sub(repl, text)


def func_create(text: str):
    mapping = load_abbreviations(file_format_json)
    pattern = build_abbr_pattern(mapping)

    return expand_abbreviations(text, mapping, pattern)

# Test func

# tests = [
#     "ct ubnd là ai?",
#     "PBT phường hiện nay là ai?",
#     "uv btv phường đang làm gì?",
#     "pct ubnd và bt đảng ủy là ai?"
# ]

# for t in tests:
#     print("IN: ", t)
#     print("OUT:", func_create(t))
#     print("---")