"""Read the traffic-guard columns from MLIT's public works labor rate tables.

Each yearly release has one page whose last two columns are
交通誘導警備員A and 交通誘導警備員B (called 交通誘導員A/B in FY2012),
with one row per prefecture. Two independent PDF engines are supported
(PyMuPDF and pdfplumber/pdfminer) so the results can be compared.
"""
import re

PREFECTURES = [
    "北海道", "青森県", "岩手県", "宮城県", "秋田県", "山形県", "福島県", "茨城県",
    "栃木県", "群馬県", "埼玉県", "千葉県", "東京都", "神奈川県", "新潟県", "富山県",
    "石川県", "福井県", "山梨県", "長野県", "岐阜県", "静岡県", "愛知県", "三重県",
    "滋賀県", "京都府", "大阪府", "兵庫県", "奈良県", "和歌山県", "鳥取県", "島根県",
    "岡山県", "広島県", "山口県", "徳島県", "香川県", "愛媛県", "高知県", "福岡県",
    "佐賀県", "長崎県", "熊本県", "大分県", "宮崎県", "鹿児島県", "沖縄県",
]

NUM = re.compile(r"^([(（<＜]?)(\d{1,2},\d{3})([)）>＞]?)$")


def words_pymupdf(path):
    import pymupdf
    doc = pymupdf.open(path)
    for i, page in enumerate(doc):
        yield i + 1, page.get_text(), [(w[0], w[1], w[2], w[3], w[4]) for w in page.get_text("words")]


def words_pdfplumber(path):
    import pdfplumber
    with pdfplumber.open(path) as pdf:
        for i, page in enumerate(pdf.pages):
            ws = page.extract_words(keep_blank_chars=False, use_text_flow=False)
            text = page.extract_text() or ""
            yield i + 1, text, [(w["x0"], w["top"], w["x1"], w["bottom"], w["text"]) for w in ws]


def is_guard_page(text, words):
    """The main rate table page that carries the guard columns (not the
    'reference' page that adds employer costs in brackets)."""
    if "参考公表" in text or "必要経費を含" in text or "必要経費（法定福利費" in text:
        return False
    header = [w for w in words if "交通誘導" in w[4] and len(w[4]) <= 12]
    names = [w for w in words if w[4] in ("東京都", "大阪府")]
    return bool(header) and bool(names)


def read_release(path, engine="pymupdf"):
    """Return (page_number, rows). Each row: dict with pref, a, b, a_mark, b_mark."""
    reader = words_pymupdf if engine == "pymupdf" else words_pdfplumber
    for pn, text, words in reader(path):
        if not is_guard_page(text, words):
            continue
        # prefecture name tokens (rightmost one per name, to skip council labels)
        name_tok = {}
        for w in words:
            t = w[4].replace("　", "")
            if t in PREFECTURES and (t not in name_tok or w[0] > name_tok[t][0]):
                name_tok[t] = w
        if len(name_tok) < 40:
            continue
        nums = [(w, NUM.match(w[4])) for w in words]
        nums = [(w, m) for w, m in nums if m]
        # guard columns = the two right-most columns of numbers (by right edge)
        edges = sorted({round(w[2]) for w, _ in nums})
        clusters = []
        for e in edges:
            if clusters and e - clusters[-1][-1] <= 8:
                clusters[-1].append(e)
            else:
                clusters.append([e])
        cA, cB = [sum(c) / len(c) for c in clusters[-2:]]
        rows = []
        for pref in PREFECTURES:
            if pref not in name_tok:
                rows.append({"pref": pref, "a": None, "b": None, "a_mark": "", "b_mark": ""})
                continue
            y = name_tok[pref][1]
            row = {"pref": pref, "a": None, "b": None, "a_mark": "", "b_mark": ""}
            for w, m in nums:
                if abs(w[1] - y) > 4:
                    continue
                for col, cx in (("a", cA), ("b", cB)):
                    if abs(w[2] - cx) <= 10:
                        if row[col] is not None:
                            raise ValueError(f"{path} p{pn} {pref}: two values in column {col}")
                        row[col] = int(m.group(2).replace(",", ""))
                        row[col + "_mark"] = {"(": "()", "（": "()", "<": "<>", "＜": "<>"}.get(m.group(1), "")
            rows.append(row)
        return pn, rows
    raise ValueError(f"{path}: guard table page not found ({engine})")
