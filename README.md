<div dir="rtl" align="right">

# 🌐🔐 רשתות תקשורת ואבטחת מידע — קורס מלא (מגמת תקשוב)

קורס בשני חלקים, בנוי כך שאפשר **ללמד ממנו ישירות מ-⁦GitHub⁩**: כל פרק הוא קובץ ⁦Markdown⁩ אחד עם הסבר מלא למתחילים, ציורים, דוגמאות, תרגילים עם פתרונות, חידון, שאלות בסגנון בחינה ומילון מונחים.

| | חלק ⁦1⁩ – רשתות תקשורת | חלק ⁦2⁩ – אבטחת רשת |
|---|---|---|
| **מה** | איך רשת עובדת – מהביט הראשון ועד ⁦BGP⁩ | איך מגנים עליה – מאיומים ועד ⁦VPN⁩ |
| **למי** | מי שמתחיל מאפס | מי שסיים את חלק ⁦1⁩ |
| **משרת את** | פרויקט הגמר ברשתות (שאלון ⁦735918)⁩ | בחינת הבגרות באבטחה (שאלון ⁦735001)⁩ |
| **מצב** | ⁦2⁩ מתוך ⁦8⁩ פרקים מלאים, השאר בכתיבה | ⁦10⁩ פרקים מלאים |

> 💡 **למה שני חלקים?** רוב התלמידים מגיעים לאבטחה בלי להבין איך רשת באמת עובדת – הם יודעים לקרוא לדברים בשם, לא להסביר מה הם עושים. אי אפשר להבין למה ⁦DHCP Snooping⁩ עובד בלי להבין איך ⁦DHCP⁩ עובד, ואי אפשר להבין ⁦VLAN Hopping⁩ בלי להבין תיוג ⁦802.1Q.⁩ לכן קודם רשתות, אחר כך אבטחה, ובכל פרק בחלק ⁦1⁩ יש תיבת 🔐 שמצביעה על החיבור לחלק ⁦2.⁩

---

## חלק ⁦1⁩ · רשתות תקשורת

📂 [**לתוכן המלא של חלק ⁦1⁩**](Part_1_Networking/README.md)

| # | פרק | מצב |
|---|---|---|
| ⁦1⁩ | [איך רשת בכלל עובדת](Part_1_Networking/01_How_Networks_Work/study_material.md) — שכבות, מסגרת/חבילה, מתג, ⁦ARP⁩, ניתוב | ✅ |
| ⁦2⁩ | [כתובות ⁦IP⁩, בינארי וחלוקה לרשתות משנה](Part_1_Networking/02_Addressing_and_Subnetting/study_material.md) — ⁦Subnetting, VLSM⁩, סיכום, ⁦Wildcard⁩ | ✅ |
| ⁦3⁩ | [מיתוג, ⁦VLAN⁩-ים ו-⁦Trunk⁩](Part_1_Networking/03_Switching_and_VLANs/study_material.md) | 🔜 |
| ⁦4 | [Spanning Tree⁩](Part_1_Networking/04_Spanning_Tree/study_material.md) | 🔜 |
| ⁦5⁩ | [ניתוב בתוך הרשת המקומית](Part_1_Networking/05_Routing_Inside_the_LAN/study_material.md) — ⁦ROAS, SVI, DHCP, HSRP⁩ | 🔜 |
| ⁦6⁩ | [פרוטוקולי ניתוב](Part_1_Networking/06_Routing_Protocols/study_material.md) — ⁦OSPF, EIGRP⁩ | 🔜 |
| ⁦7⁩ | [החיבור לעולם](Part_1_Networking/07_WAN_NAT_and_Internet/study_material.md) — ⁦NAT, BGP, DNS⁩ | 🔜 |
| ⁦8⁩ | [שורת הפקודה ואבחון תקלות](Part_1_Networking/08_CLI_and_Troubleshooting/study_material.md) | 🔜 |
| 📎 | [דף תזכורת מרוכז](Chapter_00b_Networking_Reminder/study_material.md) — כל חלק ⁦1⁩ בעמוד אחד | ✅ |

## חלק ⁦2⁩ · אבטחת רשת

מבוסס על תכנית הלימודים של משרד החינוך ועל מבנה שאלון הבגרות **⁦735001**.⁩

| # | פרק | חומר עיון | מצגת |
|---|---|---|:---:|
| ⁦0⁩ | סקירה, תכנון שנתי ופתרון שאלון | [📖](Chapter_00_Overview/study_material.md) | — |
| ⁦1⁩ | מבוא לאיומי רשת ⭐ | [📖](Chapter_01_Network_Threats/study_material.md) | [📊](https://ahmadkais.github.io/network-security-course/Chapter_01_Network_Threats/presentation.html) |
| ⁦2⁩ | אבטחת אביזרי רשת | [📖](Chapter_02_Device_Security/study_material.md) | [📊](https://ahmadkais.github.io/network-security-course/Chapter_02_Device_Security/presentation.html) |
| ⁦3⁩ | מודל ה-⁦AAA⁩ | [📖](Chapter_03_AAA/study_material.md) | [📊](https://ahmadkais.github.io/network-security-course/Chapter_03_AAA/presentation.html) |
| ⁦4⁩ | חומות אש ו-⁦ACL⁩ | [📖](Chapter_04_Firewalls/study_material.md) | [📊](https://ahmadkais.github.io/network-security-course/Chapter_04_Firewalls/presentation.html) |
| ⁦5 | IDS / IPS⁩ | [📖](Chapter_05_IDS_IPS/study_material.md) | [📊](https://ahmadkais.github.io/network-security-course/Chapter_05_IDS_IPS/presentation.html) |
| ⁦6⁩ | אבטחת הרשת המקומית | [📖](Chapter_06_LAN_Security/study_material.md) | [📊](https://ahmadkais.github.io/network-security-course/Chapter_06_LAN_Security/presentation.html) |
| ⁦7⁩ | הצפנה וקריפטולוגיה | [📖](Chapter_07_Cryptography/study_material.md) | [📊](https://ahmadkais.github.io/network-security-course/Chapter_07_Cryptography/presentation.html) |
| ⁦8⁩ | מערכות ⁦VPN⁩ | [📖](Chapter_08_VPN/study_material.md) | [📊](https://ahmadkais.github.io/network-security-course/Chapter_08_VPN/presentation.html) |
| ⁦9⁩ | ניהול אבטחה מתקדם | [📖](Chapter_09_Security_Management/study_material.md) | [📊](https://ahmadkais.github.io/network-security-course/Chapter_09_Security_Management/presentation.html) |

⭐ = פרק שעבר הרחבה מלאה. שאר פרקי חלק ⁦2⁩ יעברו התאמה לאותו מבנה של חלק ⁦1⁩ (חידון, תרגילים מורחבים) בהמשך.

---

## 🎓 איך משתמשים

**ללמד ולהציג:** פותחים את קובץ ה-⁦Markdown⁩ של הפרק ישירות ב-⁦GitHub⁩ ומקרינים. הכול נקרא בדפדפן, בלי להתקין דבר. תיבות הפתרונות והתשובות (▶ פתרון / ▶ תשובה) סגורות כברירת מחדל – אפשר לתת לכיתה לנסות ואז ללחוץ.

**ללמוד:** קוראים סעיף, עוצרים בתרגיל שאחריו, פותרים על נייר, ורק אז פותחים את הפתרון.

**מצגות (חלק ⁦2)⁩:** קיימות גם מצגות ⁦HTML⁩ לחלק מהפרקים, באתר הקורס: ⁦https://ahmadkais.github.io/network-security-course/⁩ · מקשים: `→` הבא · `←` אחורה · `⁦N⁩` הערות למורה · `⁦F⁩` מסך מלא.

---

## 🗂️ מבנה המאגר

```
├── README.md                          <- you are here
├── Part_1_Networking/                 Part 1 - networking (new)
│   ├── README.md                      Part 1 index
│   └── 0X_Chapter_Name/study_material.md
├── Chapter_00_Overview/               Part 2 - security (existing)
├── Chapter_00b_Networking_Reminder/   one-page summary of Part 1
├── Chapter_01_Network_Threats/ ...
│   ├── study_material.md              <- the chapter (primary)
│   └── presentation.html              optional slides
└── _build/
    └── isolate_md.py                  wraps English runs so RTL renders correctly
```

### כלל כתיבה אחד שחשוב לדעת

הקורס בעברית, אבל מונחים, פקודות וציורים באנגלית. כדי שהעברית והאנגלית לא "יתערבבו" בתצוגה, כל קטע אנגלי עטוף בסימני בידוד בלתי-נראים. אחרי עריכת פרק, מריצים:

```
python3 _build/isolate_md.py Part_1_Networking/01_How_Networks_Work/study_material.md
```

הסקריפט בטוח להרצה חוזרת. **ציורי ⁦ASCII⁩ תמיד באנגלית בלבד** – עברית בתוך ציור שוברת את היישור.

---
*נבנה עבור מגמת תקשוב · מבוסס על תכנית הלימודים ועל שאלונים ⁦735001⁩ ו-⁦735918⁩ של משרד החינוך.*

</div>
