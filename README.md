<div dir="rtl" align="right">

# 🌐🔐 רשתות תקשורת ואבטחת מידע — קורס מלא (מגמת תקשוב)

קורס משולב: **לומדים איך הרשת עובדת, ומיד אחר כך איך תוקפים ומגנים על אותו רכיב.** כל נושא ברשתות מוסבר מאפס, ואז בא הנושא באבטחה שנשען עליו – כך שהתלמיד מבין *למה* ההגנה עובדת, ולא רק *איך*.

הקורס בנוי ללמידה ישירה מ-⁦GitHub⁩: כל פרק הוא קובץ ⁦Markdown⁩ אחד עם הסבר למתחילים, ציורים, דוגמאות מהעולם האמיתי, תרגילים, חידון ושאלות בגרות – **כולם עם תשובות**.

> 💡 **הרעיון המרכזי:** כמעט כל התקפה אינה "שוברת" דבר – היא **מנצלת מנגנון תקין** של הרשת. אי אפשר להבין למה ⁦DHCP Snooping⁩ עובד בלי להבין ⁦DHCP⁩; אי אפשר להבין ⁦VLAN Hopping⁩ בלי להבין תיוג ⁦802.1Q.⁩ לכן בכל מודול: **קודם הרשת (🌐), ואז האבטחה (🔐) שנשענת עליה.**

---

## 🧭 מסלול הקורס — לפי מודולים

לכל מודול: פרקי הרשת שמסבירים את המנגנון, ואז פרקי האבטחה שמגנים עליו. זה הסדר המומלץ ללמידה.

### מודול ⁦1⁩ · יסודות: איך רשת עובדת ומהו איום

| | פרק | נושאים | מצגת |
|---|---|---|:---:|
| 🌐 | [רשת — איך היא עובדת](Part_1_Networking/01_How_Networks_Work/study_material.md) | שכבות · מסגרת/חבילה · מתג · ⁦ARP⁩ · ניתוב | — |
| 🌐 | [כתובות ⁦IP⁩ וחלוקה לרשתות](Part_1_Networking/02_Addressing_and_Subnetting/study_material.md) | בינארי · מסכה · ⁦Subnetting⁩ · ⁦VLSM⁩ · ⁦Wildcard⁩ | — |
| 🔐 | [מבוא לאיומי רשת](Chapter_01_Network_Threats/study_material.md) | ⁦CIA⁩ · נוזקות · ⁦DoS⁩ · הנדסה חברתית · בקרות | [📊](https://ahmadkais.github.io/network-security-course/Chapter_01_Network_Threats/presentation.html) |

> ה-🔐 כאן הוא ה"למה" של כל הקורס: אחרי שיודעים מה זו רשת, מבינים על מה בכלל מגנים ומפני מי.

### מודול ⁦2⁩ · המתג והרשת המקומית ⭐ הליבה של הקורס

| | פרק | נושאים | מצגת |
|---|---|---|:---:|
| 🌐 | [מיתוג, ⁦VLAN⁩-ים ו-⁦Trunk⁩](Part_1_Networking/03_Switching_and_VLANs/study_material.md) | ⁦VLAN⁩ · ⁦802.1Q⁩ · ⁦Native VLAN⁩ · ⁦VTP⁩ · ⁦EtherChannel⁩ | — |
| 🌐 | [⁦Spanning Tree⁩](Part_1_Networking/04_Spanning_Tree/study_material.md) | סערת שידורים · ⁦Root Bridge⁩ · ⁦PortFast⁩ | — |
| 🌐 | [ניתוב מקומי, ⁦DHCP⁩ ו-⁦HSRP⁩](Part_1_Networking/05_Routing_Inside_the_LAN/study_material.md) | ⁦Inter-VLAN⁩ · ⁦SVI⁩ · ⁦DORA⁩ · ⁦HSRP⁩ | — |
| 🔐 | [אבטחת הרשת המקומית](Chapter_06_LAN_Security/study_material.md) | ⁦MAC flooding⁩ · ⁦VLAN hopping⁩ · התקפות ⁦STP⁩ · ⁦DHCP/ARP spoofing⁩ · ⁦Port Security⁩ · ⁦DAI⁩ | [📊](https://ahmadkais.github.io/network-security-course/Chapter_06_LAN_Security/presentation.html) |

> **הצמד ההדוק ביותר בקורס:** כל התקפה בפרק האבטחה מנצלת בדיוק מנגנון שלמדתם בשלושת פרקי הרשת שלפניו. ⁦MAC flooding⁩ ↔ למידת המתג · ⁦VLAN hopping⁩ ↔ ⁦802.1Q⁩ · התקפת ⁦STP⁩ ↔ בחירת ⁦Root⁩ · ⁦rogue DHCP⁩ ↔ ⁦DORA⁩ · ⁦ARP spoofing⁩ ↔ ⁦ARP.⁩

### מודול ⁦3⁩ · ניהול ההתקן וגישה מאובטחת

| | פרק | נושאים | מצגת |
|---|---|---|:---:|
| 🌐 | [שורת הפקודה ואבחון תקלות](Part_1_Networking/08_CLI_and_Troubleshooting/study_material.md) | מצבי ⁦IOS⁩ · ⁦running/startup⁩ · שיטת אבחון · בנק תקלות | — |
| 🔐 | [אבטחת אביזרי רשת](Chapter_02_Device_Security/study_material.md) | הקשחה · ⁦SSH⁩ · סיסמאות מגובבות · ⁦Syslog⁩ · ⁦NTP⁩ | [📊](https://ahmadkais.github.io/network-security-course/Chapter_02_Device_Security/presentation.html) |
| 🔐 | [מודל ה-⁦AAA⁩](Chapter_03_AAA/study_material.md) | אימות · הרשאה · רישום · ⁦RADIUS/TACACS⁩+ · ⁦802.1X⁩ | [📊](https://ahmadkais.github.io/network-security-course/Chapter_03_AAA/presentation.html) |

> אחרי שיודעים לדבר עם נתב ולאבחן אותו (🌐), לומדים איך מקשיחים את הגישה אליו – ⁦SSH⁩ במקום ⁦Telnet⁩, סיסמאות מגובבות, וניהול מרכזי של מי נכנס לאן.

### מודול ⁦4⁩ · ניתוב, הקצה וסינון תעבורה

| | פרק | נושאים | מצגת |
|---|---|---|:---:|
| 🌐 | [פרוטוקולי ניתוב](Part_1_Networking/06_Routing_Protocols/study_material.md) | סטטי · ⁦OSPF⁩ רב-אזורי · ⁦EIGRP⁩ · סיכום | — |
| 🌐 | [החיבור לעולם: ⁦NAT, BGP, DNS⁩](Part_1_Networking/07_WAN_NAT_and_Internet/study_material.md) | ⁦NAT⁩ · ⁦BGP⁩ · ⁦ISP⁩ · ⁦DNS⁩ | — |
| 🔐 | [חומות אש ו-⁦ACL⁩](Chapter_04_Firewalls/study_material.md) | ⁦ACL⁩ סטנדרטי/מורחב · ⁦Wildcard⁩ · ⁦Stateful⁩ · ⁦ZPF⁩ · ⁦DMZ⁩ | [📊](https://ahmadkais.github.io/network-security-course/Chapter_04_Firewalls/presentation.html) |
| 🔐 | [⁦IDS / IPS⁩](Chapter_05_IDS_IPS/study_material.md) | זיהוי · חתימות · אנומליה · ⁦SPAN⁩ · ⁦Zero-Day⁩ | [📊](https://ahmadkais.github.io/network-security-course/Chapter_05_IDS_IPS/presentation.html) |

> אחרי שהחבילה יודעת לנתב החוצה (🌐 ניתוב + ⁦NAT)⁩, שמים בקצה שומר סף: ⁦ACL⁩ וחומת אש שמסננים *מי* עובר, ו-⁦IPS⁩ שבודק *מה* עובר בתוך תעבורה מותרת.

### מודול ⁦5⁩ · הצפנה ותקשורת מאובטחת

| | פרק | נושאים | מצגת |
|---|---|---|:---:|
| 🔐 | [הצפנה וקריפטולוגיה](Chapter_07_Cryptography/study_material.md) | סימטרי/א-סימטרי · גיבוב · חתימה · ⁦PKI⁩ · ⁦Diffie-Hellman⁩ | [📊](https://ahmadkais.github.io/network-security-course/Chapter_07_Cryptography/presentation.html) |
| 🔐 | [מערכות ⁦VPN⁩](Chapter_08_VPN/study_material.md) | ⁦IPsec⁩ · ⁦AH/ESP⁩ · ⁦IKE⁩ · ⁦Site-to-Site⁩ · ⁦SSL VPN⁩ | [📊](https://ahmadkais.github.io/network-security-course/Chapter_08_VPN/presentation.html) |

> נשען על ה-⁦WAN⁩ וה-⁦NAT⁩ ממודול ⁦4⁩: איך מחברים שני סניפים בבטחה מעל האינטרנט. קודם הכלים (הצפנה), אז השימוש (⁦VPN).⁩

### מודול ⁦6⁩ · ניהול אבטחה — התמונה הגדולה

| | פרק | נושאים | מצגת |
|---|---|---|:---:|
| 🔐 | [ניהול אבטחה מתקדם](Chapter_09_Security_Management/study_material.md) | ניהול סיכונים · מדיניות · ⁦pentest⁩ · תגובה לאירועים · התאוששות מאסון | [📊](https://ahmadkais.github.io/network-security-course/Chapter_09_Security_Management/presentation.html) |

> מחבר את הכול לרמה הניהולית: סיכונים, נהלים, בדיקות חדירה והמשכיות עסקית.

🧪 **מבוא לרשתות – שני שיעורים עם סיפור ומעבדות Kali** (מומלץ להתחלה, גם ללא רקע; בסופו תמצית מרוכזת לבגרות): [מבוא לרשתות](Chapter_00b_Networking_Reminder/study_material.md) · **סקירה ופתרון שאלון:** [פרק ⁦0⁩](Chapter_00_Overview/study_material.md)

---

## 📚 שני מדדים — למי שמעדיף לגלוש לפי תחום

<details><summary><b>חלק ⁦1⁩ — רשתות תקשורת (⁦8⁩ פרקים)</b></summary>

| # | פרק |
|---|---|
| ⁦1⁩ | [איך רשת עובדת](Part_1_Networking/01_How_Networks_Work/study_material.md) |
| ⁦2⁩ | [כתובות וחלוקה לרשתות](Part_1_Networking/02_Addressing_and_Subnetting/study_material.md) |
| ⁦3⁩ | [מיתוג ו-⁦VLAN⁩](Part_1_Networking/03_Switching_and_VLANs/study_material.md) |
| ⁦4 | [Spanning Tree⁩](Part_1_Networking/04_Spanning_Tree/study_material.md) |
| ⁦5⁩ | [ניתוב מקומי, ⁦DHCP, HSRP⁩](Part_1_Networking/05_Routing_Inside_the_LAN/study_material.md) |
| ⁦6⁩ | [פרוטוקולי ניתוב](Part_1_Networking/06_Routing_Protocols/study_material.md) |
| ⁦7 | [NAT, BGP, DNS⁩](Part_1_Networking/07_WAN_NAT_and_Internet/study_material.md) |
| ⁦8 | [CLI⁩ ואבחון תקלות](Part_1_Networking/08_CLI_and_Troubleshooting/study_material.md) |

[📂 אינדקס חלק ⁦1⁩](Part_1_Networking/README.md)
</details>

<details><summary><b>חלק ⁦2⁩ — אבטחת רשת (⁦9⁩ פרקים, לפי שאלון ⁦735001)⁩</b></summary>

| # | פרק |
|---|---|
| ⁦1⁩ | [מבוא לאיומי רשת](Chapter_01_Network_Threats/study_material.md) |
| ⁦2⁩ | [אבטחת אביזרי רשת](Chapter_02_Device_Security/study_material.md) |
| ⁦3⁩ | [מודל ⁦AAA⁩](Chapter_03_AAA/study_material.md) |
| ⁦4⁩ | [חומות אש ו-⁦ACL⁩](Chapter_04_Firewalls/study_material.md) |
| ⁦5 | [IDS / IPS⁩](Chapter_05_IDS_IPS/study_material.md) |
| ⁦6⁩ | [אבטחת הרשת המקומית](Chapter_06_LAN_Security/study_material.md) |
| ⁦7⁩ | [הצפנה](Chapter_07_Cryptography/study_material.md) |
| ⁦8 | [VPN⁩](Chapter_08_VPN/study_material.md) |
| ⁦9⁩ | [ניהול אבטחה](Chapter_09_Security_Management/study_material.md) |
</details>

---

## 🎓 איך משתמשים

**ללמד ולהציג:** פותחים את קובץ ה-⁦Markdown⁩ של הפרק ישירות ב-⁦GitHub⁩ ומקרינים. תיבות הפתרונות והתשובות (▶) סגורות כברירת מחדל – אפשר לתת לכיתה לנסות ואז לפתוח. לחלק מפרקי האבטחה יש גם מצגות ⁦HTML⁩ (📊) באתר הקורס: ⁦https://ahmadkais.github.io/network-security-course/⁩

**ללמוד:** לפי מסלול הקורס למעלה — מודול אחר מודול, 🌐 ואז 🔐. קוראים סעיף, עוצרים בתרגיל, פותרים על נייר, ואז פותחים את הפתרון.

**מבנה כל פרק:** הסבר למתחילים · ציורים (⁦ASCII⁩ באנגלית) · דוגמאות מהעולם האמיתי · תרגילים עם פתרונות · חידון עם תשובות · שאלות בסגנון בחינה עם תשובות · מילון מונחים.

---

## 🗂️ מבנה המאגר

```
README.md                          <- מסלול הקורס (מודולים משולבים)
Part_1_Networking/                 חלק רשתות
  0X_.../study_material.md
Chapter_0X_.../                    חלק אבטחה (+ presentation.html)
  study_material.md
_build/isolate_md.py               עוטף קטעי אנגלית לתצוגת RTL תקינה
```

**כלל כתיבה:** הקורס בעברית, מונחים ופקודות באנגלית. אחרי עריכת פרק מריצים `⁦python3 _build/isolate_md.py⁩ <file>` (בטוח להרצה חוזרת). ציורי ⁦ASCII⁩ תמיד באנגלית בלבד.

---
*נבנה עבור מגמת תקשוב · מבוסס על תכנית הלימודים ועל שאלונים ⁦735001⁩ ו-⁦735918⁩ של משרד החינוך.*

</div>
