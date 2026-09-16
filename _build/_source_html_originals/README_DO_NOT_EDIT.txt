מקורות HTML מקוריים – אינם מקור האמת!
=====================================
הקבצים כאן הם הטיוטה המקורית שממנה נוצרו קובצי ה-LaTeX פעם אחת (bootstrap).

מקור האמת לחומר העיון הוא קובצי ה-LaTeX:
    Chapter_XX/study_material.tex   ← ערוך את אלה

עריכת ה-HTML כאן לא משפיעה על שום דבר, אלא אם מריצים במפורש:
    python3 _build/make.py convert --force
פקודה זו תדרוס את קובצי ה-LaTeX שלך מה-HTML – אל תשתמש בה אלא אם אתה
רוצה לאפס הכול חזרה לטיוטה המקורית.

לבנייה רגילה (הידור ה-LaTeX ל-PDF, בלי לגעת ב-.tex):
    python3 _build/make.py latex
    python3 _build/make.py book
