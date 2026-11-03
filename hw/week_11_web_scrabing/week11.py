from bs4 import BeautifulSoup
from bs4.element import Tag
from IPython.core.display import HTML


#file_path = "2566.html"
def Q1(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        html = f.read()
    soup = BeautifulSoup(html, "html.parser")

    days = ["จันทร์", "อังคาร", "พุธ", "พฤหัสบดี", "ศุกร์", "เสาร์", "อาทิตย์"]
    counts = [0] * 7

    for d in soup.find_all("div", class_="bud-day"):
        text = d.find("div", class_="bud-day-col").get_text(strip=True)
        for i, name in enumerate(days):
            if text.startswith("วัน" + name + "ที่"):
                counts[i] += 1
                break

    return counts
def Q2(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        html = f.read()
    soup = BeautifulSoup(html, "html.parser")

    for d in soup.find_all("div", class_="bud-day"):
        if "วันวิสาขบูชา" in d.get_text():
            return d.find("div", class_="bud-day-col").get_text(strip=True)
exec(input().strip()) # do not delete this line (starting input line)
# eg, print(Q1("2566.html"))Z
# print(Q2("2566.html"))
