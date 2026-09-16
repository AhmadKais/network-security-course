# אבטחת מידע – חומרי הוראה (מגמת תקשוב)

חבילת הוראה מלאה בעברית ל-9 פרקי תכנית הלימודים, מבוססת על התכנית הרשמית ועל מבנה שאלון הבגרות 735001.
**ספר הקורס המלא:** `Full_Course.pdf` – כל 9 הפרקים ב-PDF אחד עם תוכן עניינים וסימניות (78 עמ').

**הכי פשוט:** פתח את `index.html` בדפדפן – תפריט לכל הפרקים (חומר עיון + מצגת).

## מבנה – תיקייה לכל פרק

כל פרק בתיקייה משלו, ובה שני חלקים:

```
Chapter_01_Network_Threats/
├── study_material.tex   ← מקור LaTeX (עריך)
├── study_material.pdf   ← חומר העיון שאתה קורא ולומד ממנו
└── presentation.html    ← המצגת שאתה מקרין לתלמידים (עצמאית, עובדת בלי אינטרנט)
```

| תיקייה | פרק |
|--------|-----|
| `Chapter_00_Overview` | סקירה, תכנון שנתי, פתרון שאלון הבגרות לדוגמה (ללא מצגת) |
| `Chapter_01_Network_Threats` | מבוא לאיומי רשת |
| `Chapter_02_Device_Security` | אבטחת אביזרי רשת |
| `Chapter_03_AAA` | מודל ה-AAA |
| `Chapter_04_Firewalls` | חומות אש ו-ACL |
| `Chapter_05_IDS_IPS` | IDS / IPS |
| `Chapter_06_LAN_Security` | אבטחת הרשת המקומית |
| `Chapter_07_Cryptography` | הצפנה וקריפטולוגיה |
| `Chapter_08_VPN` | מערכות VPN |
| `Chapter_09_Security_Management` | ניהול אבטחה מתקדם |

## חומר העיון (LaTeX → PDF)
כל פרק כולל: חומר עיוני מלא, מדריך פקודות CLI, סיפורים מהחיים,
תיבות "שאלת תלמיד", "טעות נפוצה", "טיפ להוראה", תרגילים עם פתרונות,
ושאלות בסגנון בגרות עם תשובות.

המקור הוא **LaTeX** (`study_material.tex`). לעריכה, שנה את ה-tex והדר מחדש:
```
cd Chapter_03_AAA
lualatex study_material.tex     # פעמיים, לעדכון מספרי עמודים
```
דורש: LuaLaTeX (TeX Live) + הגופנים Noto Sans Hebrew ו-DejaVu (מותקנים במערכת).

## המצגות
פתח `presentation.html` של הפרק בדפדפן. מקשים:

| מקש | פעולה |
|-----|-------|
| `→` / רווח | הבא (התוכן מתגלה בהדרגה) |
| `←` | אחורה |
| `N` | הערות למורה (מה להגיד, איזו שאלה לשאול) |
| `F` | מסך מלא |
| `Home` / `End` | ראשון / אחרון |

בשקפי "שאלה" התשובה מוסתרת עד ללחיצה, כדי לתת לכיתה לנסות קודם.

## עריכה ובנייה מחדש

**מקור האמת:**
- חומר עיון = קובץ ה-LaTeX `Chapter_XX/study_material.tex` — **ערוך את זה**.
- מצגות = ה-HTML בתיקייה `_build/slides_src/`.

לאחר עריכה, בנה מחדש (מריצים מתוך `Course_Materials/`):
```
python3 _build/make.py latex    # מהדר כל study_material.tex ל-PDF (לא נוגע ב-.tex)
python3 _build/make.py book     # מרכיב את Full_Course.pdf מקובצי ה-.tex
python3 _build/make.py slides   # בונה מחדש את המצגות מ-_build/slides_src
python3 _build/make.py all      # מצגות + latex + ספר
```
דורש: LuaLaTeX (TeX Live) + הגופנים Noto Sans Hebrew ו-DejaVu.

> **חשוב:** `make.py latex` **רק מהדר** את ה-.tex ל-PDF — הוא לעולם לא דורס את העריכות שלך.
> הספר (`book`) מורכב ישירות מקובצי ה-.tex, כך שכל עריכה שלך מופיעה גם בו.

תוכן תיקיית `_build/`:
- `slides_src/`              – מקור המצגות (HTML + CSS + JS) = מקור האמת למצגות
- `html2tex.py`, `make.py`   – סקריפטים לבנייה
- `_source_html_originals/`  – טיוטות ה-HTML המקוריות ש**מהן נוצר ה-LaTeX פעם אחת**. אינן מקור
  האמת ואין לערוך אותן. הן משמשות רק לפקודת האיפוס:
  ```
  python3 _build/make.py convert --force   # מאפס את קובצי ה-.tex חזרה לטיוטה (דורס עריכות!)
  ```
  בלי `--force` הפקודה מדלגת על כל .tex קיים ולא דורסת דבר.
