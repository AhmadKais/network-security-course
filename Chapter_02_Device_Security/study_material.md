# פרק 2 – אבטחת אביזרי רשת

_10 שעות עיוני + 2 מעשי · שבועות 4–6_

> **מטרות:** הקשחת נתב ב-CLI · אבטחת גישה · SSH · syslog/NTP/SNMP · AutoSecure  
> **בבגרות:** line vty / login local / secret, מפתחות RSA ל-SSH, פקודת logging

> 📘 **לפני שמתחילים – איך בכלל מדברים עם נתב? (למי שאין רקע)**
>
> כל הפרק הזה עוסק ב"הקשחת נתב" – אבל איך פונים לנתב מלכתחילה? הנה הבסיס: 
> - **CLI (Command Line Interface)** – ממשק שורת פקודה. במקום עכבר וחלונות, מקלידים פקודות טקסט. כל ציוד סיסקו מנוהל כך.
> - **IOS** – מערכת ההפעלה של ציוד סיסקו (כמו Windows למחשב, רק לנתב). ה-CLI הוא הדרך לדבר איתה.
> - **מצבי עבודה (Modes)** – ל-CLI יש "רמות". הסימן שאחרי שם הנתב מראה איפה אתם:  `R1>` – מצב בסיסי (User) – רק צפייה. `R1#` – מצב מנהל (Privileged) – אחרי הקלדת `enable`. אפשר הכול. `R1(config)#` – מצב הגדרות – אחרי `configure terminal`. כאן משנים הגדרות. `R1(config-if)#` – מצב ממשק – מגדירים כרטיס רשת ספציפי.
> - **קונפיגורציה (Configuration)** – כל ההגדרות של הנתב. יש **running-config** (הפעילה כרגע בזיכרון, נמחקת בכיבוי) ו-**startup-config** (השמורה, נטענת באתחול). שומרים עם `copy running-config startup-config` או `write`.
> - **ממשק (Interface)** – כרטיס רשת/פורט פיזי בנתב, למשל `GigabitEthernet0/0` (בקיצור g0/0). **דוגמה – כניסה והגדרה ראשונה:** 
> ```
> Router> enable                 ! מעבר למצב מנהל
> Router# configure terminal     ! מעבר למצב הגדרות
> Router(config)# hostname R1    ! שינוי שם הנתב
> R1(config)# exit
> R1# write                      ! שמירת ההגדרות
> ```

## 2.1 למה הנתב הוא המטרה הראשונה

**נתב הקצה** (Edge router) הוא הנקודה שבה רשת הארגון פוגשת את האינטרנט. מי ששולט בו יכול לנתב תעבורה לאן שירצה, להאזין לה, לחסום אותה או לפתוח פתח פנימה. שלוש גישות לתכנון:

- **נתב יחיד** – הנתב הוא גם חומת האש (ACL, ZPF). מתאים לעסק קטן (SOHO).
- **הגנה לעומק (Defense in depth)** – נתב קצה מסנן גס ⇒ חומת אש ייעודית (ASA) ⇒ נתב פנימי. כל שכבה עצמאית.
- **DMZ** – אזור מפורז בין שתי חומות אש (או בין שני ממשקים של אותה חומה) ובו השרתים הציבוריים (web, mail). אם שרת ב-DMZ נפרץ, התוקף עדיין לא בפנים.

אבטחת הנתב עצמו כוללת שלושה תחומים: **אבטחה פיזית** (חדר נעול, UPS – מי שיש לו גישה פיזית לקונסול יכול לאפס סיסמה דרך password recovery), **אבטחת מערכת ההפעלה** (גרסת IOS עדכנית, זיכרון מספיק, גיבוי של ה-image והקונפיגורציה) ו**הקשחה** (hardening) – סגירת שירותים מיותרים, סיסמאות, גישה מוצפנת, ניטור. זה ליבת הפרק.

> 📖 **סיפור מהחיים: הנתבים שנשארו עם admin/admin**
>
> ב-2016 רשת Mirai הדביקה 600,000 מכשירים – מצלמות אבטחה, ראוטרים ביתיים, מקליטי DVR – בשיטה פרימיטיבית להדהים: היא ניסתה 62 צירופים של שם משתמש וסיסמה מברירת המחדל של היצרנים (admin/admin, root/12345, admin/password). זהו. בלי פגיעות מתוחכמת. עם הצבא הזה הופלו ב-DDoS של 1.2 טרה-ביט/שנייה שירות ה-DNS של Dyn, ואיתו Twitter, Netflix, Spotify ו-PayPal ליום שלם. כל מה שנלמד בפרק הזה – סיסמה חזקה, SSH במקום Telnet, כיבוי שירותים – היה מונע את ההדבקה. שאלו: כמה מכם שינו את הסיסמה של הראוטר בבית?

## 2.2 שלוש דרכי ניהול לנתב

| **ממשק** | **איך מתחברים** | **אבטחה** |
| --- | --- | --- |
| **Console** | כבל קונסול פיזי, `line console 0` | מי שמגיע פיזית – שולט. חובה סיסמה + exec-timeout. |
| **AUX** | פורט עזר למודם (ישן), `line aux 0` | לרוב מכבים: `no exec` / `transport input none` |
| **VTY** (Virtual Terminal) | Telnet/SSH דרך הרשת, `line vty 0 4` (5 קווים וירטואליים 0–4; ב-IOS חדש 0–15) | הנקודה הרגישה ביותר – חייבים SSH בלבד + אימות משתמשים. |

> 📘 **In-band מול Out-of-band (OOB)**
>
> **In-band** – ניהול דרך אותה רשת שמעבירה את תעבורת המשתמשים (SSH מהמשרד לנתב). זול, אבל אם הרשת נופלת – אין ניהול, ואם התוקף ברשת – הוא רואה את תעבורת הניהול.  
>  **Out-of-band (OOB)** – רשת ניהול נפרדת פיזית או לוגית: שרת קונסולים, VLAN ניהול ייעודי, מודם/LTE לחירום. עדיף לארגונים; לפחות VLAN ניהול נפרד.

## 2.3 סיסמאות בנתב – מה ההבדל בין כל הסוגים

```
! מדיניות מינימום
R1(config)# security passwords min-length 10
! סיסמת מצב enable – תמיד secret, לעולם לא password
R1(config)# enable secret Str0ng-P@ss
! קונסול
R1(config)# line console 0
R1(config-line)# password C0ns0le-P@ss
R1(config-line)# login
R1(config-line)# exec-timeout 5 0        ! ניתוק אחרי 5 דק' חוסר פעילות
R1(config-line)# logging synchronous      ! שהודעות לוג לא ישברו את השורה שמקלידים
! הצפנת כל הסיסמאות בטקסט גלוי בקונפיג (type 7 – חלשה, אבל עדיף מכלום)
R1(config)# service password-encryption
```

| **פקודה** | **איך נשמר בקונפיג** | **חוזק** |
| --- | --- | --- |
| `enable password X` | טקסט גלוי (type 0) | אפס. לא להשתמש. |
| `service password-encryption` | Vigenère "type 7" | חלש – מפוענח באתרים אונליין בשנייה. מגן רק מהצצה מעבר לכתף. |
| `enable secret X` | MD5 (type 5), ב-IOS חדש scrypt (type 9) | גיבוב חד-כיווני – לא ניתן לשחזר. **זה מה שמשתמשים בו.** |
| `username admin secret X` | גיבוב כמו enable secret | חזק – לחשבונות מקומיים. |
| `username admin password X` | גלוי / type 7 | חלש – לא להשתמש. |

> ❓ **שאלת תלמיד: "אם הגדרתי גם enable password וגם enable secret – מה קובע?"**
>
> ה-secret. ה-IOS מתעלם מ-enable password כשקיים enable secret (ומזהיר אם הן זהות). למען הסדר – פשוט לא מגדירים enable password.

> ❓ **שאלת תלמיד: "מה ההבדל בין login ל-login local?"**
>
> `login` – מבקש רק את הסיסמה שהוגדרה בקו עצמו (`password` בתוך line). כולם משתמשים באותה סיסמה, אין שמות, אין מעקב מי נכנס.  
>  `login local` – מבקש שם משתמש וסיסמה ומאמת מול מסד המשתמשים המקומי (`username … secret …`). **SSH דורש שם משתמש ולכן חייב login local (או AAA).** זה בדיוק מה שנשאל בבגרות שאלה 2א: התשובה הנכונה היא `username admin privilege 15 secret …` + `login local`.

## 2.4 Telnet מול SSH – והגדרת SSH צעד אחר צעד

**Telnet** (TCP 23) מעביר הכול – כולל שם משתמש וסיסמה – בטקסט גלוי. כל מי שמאזין לרשת (Wireshark) רואה אותם. **SSH** (Secure Shell, TCP 22) מצפין את כל ההפעלה ומאמת את השרת. SSH גרסה 2 בלבד (גרסה 1 פגיעה).

כדי ש-SSH יעבוד, הנתב צריך **זוג מפתחות RSA** (פרק 7 יסביר לעומק: מפתח ציבורי שנשלח ללקוח ומפתח פרטי שנשאר בנתב). כדי לייצר מפתח הנתב צריך שם מלא (FQDN) = hostname + domain-name, כי השם נכנס למפתח.

```
! 1. שם ייחודי ודומיין – חובה לפני יצירת מפתחות
Router(config)# hostname R1
R1(config)# ip domain-name school.local
! 2. יצירת זוג מפתחות RSA (2048 ביט ומעלה)
R1(config)# crypto key generate rsa general-keys modulus 2048
The name for the keys will be: R1.school.local
! 3. משתמש מקומי
R1(config)# username admin privilege 15 secret Adm1n-P@ss
! 4. פרמטרים של SSH
R1(config)# ip ssh version 2
R1(config)# ip ssh time-out 60              ! זמן לסיום ההזדהות
R1(config)# ip ssh authentication-retries 2
! 5. קווי VTY – רק SSH, אימות מקומי
R1(config)# line vty 0 4
R1(config-line)# login local
R1(config-line)# transport input ssh          ! חוסם Telnet לחלוטין
R1(config-line)# exec-timeout 5 0
! בדיקה
R1# show ip ssh
R1# show ssh                                  ! חיבורים פעילים
R1# show crypto key mypubkey rsa
! חיבור מנתב אחר / ממחשב
R2# ssh -l admin 10.0.0.1
PC> ssh -l admin 10.0.0.1
```

> ⚠️ **טעויות נפוצות בהגדרת SSH**
>
> • שכחו `ip domain-name` ⇒ הפקודה `crypto key generate rsa` נכשלת ("Please define a domain-name first").  
>  • השאירו hostname "Router" ⇒ אותה שגיאה.  
>  • הגדירו `login` במקום `login local` ⇒ SSH דוחה ("Password required, but none set" / אין אימות בשם משתמש).  
>  • מפתח קטן מ-768 ביט לא מאפשר SSHv2. משתמשים ב-1024 לפחות; מומלץ 2048.  
>  • `transport input ssh` חוסם Telnet – אם התלמיד היה מחובר ב-Telnet הוא לא יינתק, אבל חיבור הבא ייכשל. זה מכוון.

> 📝 **בבגרות (שאלה 5ב)**
>
> "מנהל רשת הפיק מפתחות RSA בנתב. מה ניתן לעשות כעת עם המפתחות?" – **ניתן להשתמש בהם לצורך חיבור SSH** (ללא צורך באיפוס). Telnet לא משתמש במפתחות כלל.

> 📖 **סיפור מהחיים: Telnet בבית חולים**
>
> בבדיקת חדירה בבית חולים (סיפור שמופיע בדוחות של חברות אבטחה רבות), הבודקים חיברו מחשב נייד לשקע רשת בחדר המתנה, הריצו Wireshark, וחיכו. תוך 40 דקות הם לכדו session של Telnet של טכנאי שהתחבר למתג הראשי – שם משתמש וסיסמה בטקסט גלוי. עם הסיסמה הזו הם קיבלו שליטה בכל המתגים בבניין. הטכנאי לא עשה שום דבר "לא נכון" – הוא פשוט השתמש בכלי שהיה זמין. ההגנה: `transport input ssh` – שורה אחת.

## 2.5 רמות הרשאה (Privilege Levels) ותצוגות תפקיד (Role-Based CLI Views)

ל-IOS יש 16 רמות הרשאה (0–15). בפועל משתמשים בשלוש:

| **רמה** | **שם** | **מה מותר** |
| --- | --- | --- |
| 0 | – | רק disable, enable, exit, help, logout |
| 1 | User EXEC (`R1>`) | פקודות show בסיסיות, ping. ברירת מחדל אחרי login. |
| 2–14 | מותאם אישית | מה שהמנהל מעביר אליהן בעזרת `privilege` |
| 15 | Privileged EXEC (`R1#`) | הכול, כולל configure terminal |

```
! רמה 5: מותר גם reload ו-show running-config
R1(config)# privilege exec level 5 reload
R1(config)# privilege exec level 5 show running-config
R1(config)# enable secret level 5 Lvl5-P@ss
R1(config)# username helpdesk privilege 5 secret Help-P@ss
! כניסה לרמה
R1> enable 5
R1# show privilege
Current privilege level is 5
```

**מגבלות של רמות:** אין שליטה "בין רמות" (רמה 5 מקבלת אוטומטית גם כל מה שמותר ב-1–4), ופקודות show מסוימות חושפות הרבה. הפתרון המדויק יותר: **Role-Based CLI Views** – "תצוגה" שמכילה רשימת פקודות מדויקת. דורש AAA מופעל.

```
R1(config)# aaa new-model
R1(config)# exit
R1# enable view                                ! נכנסים ל-root view (מבקש enable secret)
R1# configure terminal
R1(config)# parser view MONITOR
R1(config-view)# secret Mon-P@ss
R1(config-view)# commands exec include show ip interface brief
R1(config-view)# commands exec include show ip route
R1(config-view)# commands exec include ping
R1(config-view)# exit
! משתמש שמשויך לתצוגה
R1(config)# username noc view MONITOR secret Noc-P@ss
! בדיקה
R1# enable view MONITOR
R1# show parser view
Current view is 'MONITOR'
```

**Superview** – תצוגה שמאגדת כמה תצוגות (`parser view ADMIN superview` ⇒ `view MONITOR`).

## 2.6 Banner – אזהרה משפטית

```
R1(config)# banner motd #
*** UNAUTHORIZED ACCESS IS PROHIBITED ***
This system is for authorized personnel only.
All activity is monitored and logged.
#
```

> 💡 **טיפ: מה לא לכתוב בבאנר**
>
> לא "Welcome" (בית משפט בארה"ב קיבל טענה של פורץ ש"הוזמן"), לא שם החברה, לא דגם הנתב, לא שם המנהל. רק אזהרה ותו לא. ה-motd מוצג לפני ההזדהות; `banner login` מוצג אחרי motd ולפני בקשת שם משתמש; `banner exec` אחרי הכניסה.

## 2.7 Logging ו-Syslog

הנתב מייצר הודעות על אירועים (ממשק עלה/ירד, כניסה כושלת, ACL שחסם). ניתן לשלוח אותן ל: **קונסול** (ברירת מחדל), **קווי VTY** (`terminal monitor`), **חוצץ בזיכרון** (buffer – נמחק ב-reload), ו**שרת syslog** (UDP 514) – היעד הנכון לארגון, כי הלוגים נשמרים גם אם הנתב נפרץ או אופס.

### מבנה הודעה

```
*Mar  1 00:12:45.123: %LINK-3-UPDOWN: Interface FastEthernet0/1, changed state to down
 ^זמן                  ^facility ^severity ^mnemonic  ^תיאור
```

### 8 רמות חומרה (Severity) – חובה לזכור

| **רמה** | **שם** | **משמעות** |
| --- | --- | --- |
| 0 | Emergencies | המערכת אינה שמישה |
| 1 | Alerts | נדרשת פעולה מיידית |
| 2 | Critical | מצב קריטי |
| 3 | Errors | שגיאה (ממשק נפל) |
| 4 | Warnings | אזהרה |
| 5 | Notifications | אירוע רגיל אך משמעותי (ממשק עלה, config שונה) |
| 6 | Informational | מידע (ACL match) |
| 7 | Debugging | פלט debug – עצום, רק לפתרון תקלות |

מנמוניקה באנגלית: **E**very **A**wesome **C**isco **E**ngineer **W**ill **N**eed **I**ce-cream **D**aily. כשמגדירים רמה – מקבלים אותה **וכל מה שחמור ממנה** (רמה 4 = 0–4).

```
R1(config)# logging host 2.9.20.22       ! או בקיצור: logging 2.9.20.22 (זו התשובה בבגרות שאלה 2ח)
R1(config)# logging trap warnings        ! שלח לשרת רמות 0–4 (אפשר לכתוב 4)
R1(config)# logging source-interface loopback 0
R1(config)# logging buffered 16384 informational   ! חוצץ 16KB, רמות 0–6
R1(config)# service timestamps log datetime msec  ! חותמת זמן – חסר טעם בלי NTP!
R1(config)# logging on
R1# show logging
```

## 2.8 NTP – למה זמן מדויק הוא עניין של אבטחה

לוגים בלי זמן נכון חסרי ערך: אי אפשר לשחזר סדר אירועים בין נתב, חומת אש ושרת. גם תעודות דיגיטליות (פרק 7) ומפתחות IPsec (פרק 8) תלויים בזמן. **NTP** (Network Time Protocol, UDP 123) מסנכרן את כל הציוד למקור אחד. **Stratum** – מרחק ממקור הזמן (stratum 0 = שעון אטומי/GPS, stratum 1 = שרת שמחובר אליו ישירות…).

```
! נתב כלקוח NTP
R1(config)# ntp server 10.0.0.5
R1(config)# clock timezone IST 2
! אימות NTP – שלא יזייפו לנו את הזמן
R1(config)# ntp authenticate
R1(config)# ntp authentication-key 1 md5 NtpK3y
R1(config)# ntp trusted-key 1
R1(config)# ntp server 10.0.0.5 key 1
! נתב כשרת NTP לרשת הפנימית
R1(config)# ntp master 3
R1# show ntp status
R1# show ntp associations
R1# show clock
```

## 2.9 SNMP – ניטור ציוד, ולמה גרסה 3

**SNMP** (Simple Network Management Protocol, UDP 161/162) מאפשר לתחנת ניהול (NMS – PRTG, SolarWinds, Zabbix) לקרוא נתונים מהנתב (GET – תעבורה, CPU) ואף לשנות (SET). הנתב יכול גם לשלוח התראות יזומות (**trap**). הנתונים מאורגנים ב-**MIB** (עץ של משתנים, כל אחד עם מזהה OID).

| **גרסה** | **אימות** | **הצפנה** | **הערכה** |
| --- | --- | --- | --- |
| SNMPv1 | Community string בטקסט גלוי ("public"/"private") | אין | לא לשימוש |
| SNMPv2c | Community string בטקסט גלוי | אין | נפוץ, אך חלש – לפחות read-only + ACL |
| **SNMPv3** | שם משתמש + HMAC (MD5/SHA) | DES/AES | **היחיד המומלץ**. רמות: noAuthNoPriv, authNoPriv, authPriv |

```
! v2c מוגבל (אם חייבים): קריאה בלבד ורק מ-NMS
R1(config)# access-list 5 permit host 10.0.0.50
R1(config)# snmp-server community S3cr3tRO ro 5
! v3 – הדרך הנכונה
R1(config)# snmp-server group ADMINS v3 priv
R1(config)# snmp-server user monitor ADMINS v3 auth sha AuthP@ss priv aes 128 PrivP@ss
R1(config)# snmp-server host 10.0.0.50 version 3 priv monitor
R1(config)# snmp-server enable traps
R1# show snmp
```

## 2.10 שירותים שסוגרים ו-AutoSecure

ה-IOS מגיע עם שירותים שהיו נחוצים פעם והיום הם רק שטח תקיפה. רשימת הקשחה ידנית:

```
R1(config)# no cdp run                 ! CDP חושף דגם, IOS וכתובות לשכנים (השאירו על קישורים פנימיים אם צריך)
R1(config)# no ip http server          ! ממשק web – או ip http secure-server אם חייבים
R1(config)# no ip finger
R1(config)# no ip bootp server
R1(config)# no service tcp-small-servers
R1(config)# no service udp-small-servers
R1(config)# no ip source-route            ! מונע מהשולח להכתיב מסלול
R1(config)# no service pad
R1(config)# interface g0/0
R1(config-if)# no ip redirects
R1(config-if)# no ip proxy-arp
R1(config-if)# no ip unreachables
R1(config-if)# no ip directed-broadcast   ! נגד Smurf (ברירת מחדל כבר כך)
```

**AutoSecure** – פקודה אחת שעושה את רוב זה: מכבה שירותים מסוכנים, מפעילה שירותי אבטחה (logging, login block), מקשיחה ממשקים, ומציעה להגדיר SSH ו-CBAC. במצב אינטראקטיבי שואלת שאלות; במצב `no-interact` משתמשת בברירות מחדל.

```
R1# auto secure
R1# auto secure no-interact
R1# show auto secure config
```

> ❓ **שאלת תלמיד: "אז למה לא פשוט להריץ auto secure תמיד?"**
>
> כי הוא "עיוור": יכול לכבות CDP שהמתגים צריכים, להפעיל חומת אש (CBAC) שתחסום תעבורה לגיטימית, ואי אפשר לבטל אותו בפקודה אחת (`no auto secure` לא קיים – צריך לשחזר config). מומלץ להריץ אותו, לבדוק את מה שהוא שינה עם `show auto secure config`, ולכוונן.

## 2.11 שמירה על ה-IOS והקונפיג – Resilient Configuration

תוקף שהשיג גישה יכול למחוק את ה-IOS ואת ה-startup-config ולהשבית את הנתב. תכונת **IOS Resilient Configuration** שומרת עותק מוגן (bootset) שלא ניתן למחוק מה-CLI, גם לא ב-`format flash:`.

```
R1(config)# secure boot-image
R1(config)# secure boot-config
R1# show secure bootset
! שחזור: ROMMON > boot flash:<image>  ואז  R1(config)# secure boot-config restore flash:rescue-cfg
```

גיבוי שוטף: `copy running-config tftp:` / `archive` + `path` + `time-period` לגיבוי אוטומטי.

## 2.12 ביקורת חשבונות (Auditing)

לדעת *מי* עשה *מה* ומתי. הכלים בפרק זה: `login on-failure log` / `login on-success log`, `archive log config` (רישום כל פקודת config עם שם המשתמש), syslog מרכזי, ו-`show users` לראות מי מחובר עכשיו. הרחבה מלאה – Accounting של AAA בפרק 3.

```
R1(config)# archive
R1(config-archive)# log config
R1(config-archive-log-cfg)# logging enable
R1(config-archive-log-cfg)# hidekeys      ! לא לרשום סיסמאות
R1# show archive log config all
```

## 2.13 SDM / CCP – מה זה ומה אומרים לתלמידים

תכנית הלימודים מזכירה "SDM לוריפיקציה". **SDM** (Security Device Manager) היה ממשק גרפי מבוסס Java שרץ בדפדפן מול הנתב והציע אשפים (wizards) ל-SSH, חומת אש, VPN ו-"Security Audit" – סריקה שמציגה רשימת שירותים מסוכנים ומציעה לתקן בלחיצה ("One-step lockdown", המקבילה הגרפית של AutoSecure). SDM הוחלף ב-CCP (Cisco Configuration Professional) ב-2009, ו-CCP הופסק ב-2015. **הבגרות בודקת CLI בלבד.** אמרו לתלמידים: "קיימים ממשקים גרפיים; אנחנו לומדים CLI כי הוא אוניברסלי, מדויק ונשאל בבחינה".

## 2.14 מדריך פקודות מרוכז – פרק 2

| **פקודה** | **מצב** | **תפקיד** |
| --- | --- | --- |
| `enable secret X` | config | סיסמת enable מגובבת |
| `service password-encryption` | config | מסתיר סיסמאות type 7 |
| `security passwords min-length N` | config | אורך סיסמה מינימלי |
| `username U privilege 15 secret P` | config | משתמש מקומי |
| `login block-for S attempts N within T` | config | הגנה מ-brute force |
| `ip domain-name D` / `crypto key generate rsa` | config | הכנה ל-SSH |
| `ip ssh version 2` | config | SSHv2 בלבד |
| `line vty 0 4` → `login local` / `transport input ssh` | line | גישה מרחוק מאובטחת |
| `exec-timeout M S` | line | ניתוק חוסר פעילות |
| `privilege exec level N CMD` | config | העברת פקודה לרמה |
| `parser view V` | config (אחרי aaa new-model) | תצוגת תפקיד |
| `banner motd #…#` | config | אזהרה |
| `logging host IP` / `logging trap LEVEL` | config | syslog |
| `ntp server IP` / `ntp authenticate` | config | זמן |
| `snmp-server …` | config | ניטור |
| `auto secure` | exec | הקשחה אוטומטית |
| `secure boot-image` / `secure boot-config` | config | הגנה על IOS וקונפיג |
| `show ip ssh`, `show logging`, `show ntp status`, `show privilege`, `show login` | exec | וריפיקציה |

## 2.15 תרגילים לתלמידים

> ✏️ **תרגיל 1 – מצאו את 5 הבעיות בקונפיג**
>
> ```
> Router(config)# enable password cisco
> Router(config)# line vty 0 4
> Router(config-line)# password cisco
> Router(config-line)# login
> Router(config-line)# transport input telnet
> Router(config)# banner motd # Welcome to ACME Corp main router! #
> Router(config)# snmp-server community public rw
> ```
>
> **תשובה:** 1. `enable password` במקום `enable secret` (טקסט גלוי). 2. hostname נשאר Router (ובלי domain-name לא יהיה SSH). 3. סיסמה חלשה "cisco" ובלי שם משתמש (`login` במקום `login local`). 4. `transport input telnet` – לא מוצפן; צריך ssh. 5. באנר "Welcome" עם שם החברה. 6. SNMP community "public" עם הרשאת **rw** – כל אחד יכול לשנות את הקונפיג. 7. אין exec-timeout. (כל 5 מתוך 7 מתקבלים.)

> ✏️ **תרגיל 2 – סדר נכון**
>
> סדרו את הפקודות הבאות בסדר שבו חייבים להקליד אותן כדי ש-SSH יעבוד: `crypto key generate rsa` · `ip domain-name lab.local` · `transport input ssh` · `hostname R1` · `username admin secret P@ss` · `login local` · `line vty 0 4`
>
> **תשובה:** hostname R1 → ip domain-name lab.local → crypto key generate rsa → username admin secret P@ss → line vty 0 4 → login local → transport input ssh. (username יכול לבוא בכל מקום לפני login local; hostname ו-domain-name חייבים לפני crypto key.)

> ✏️ **תרגיל 3 – syslog**
>
> הנתב הגדיר `logging trap 4`. סמנו אילו מההודעות יגיעו לשרת:  
>  א. `%SYS-5-CONFIG_I: Configured from console` ב. `%LINK-3-UPDOWN` ג. `%SEC_LOGIN-4-LOGIN_FAILED` ד. `%SEC-6-IPACCESSLOGP` ה. `%OSPF-5-ADJCHG`
>
> **תשובה:** ב (3) ו-ג (4) יגיעו. א (5), ד (6), ה (5) לא – חמורים פחות מ-4. **מנמוניקה:** המספר במרכז ההודעה הוא רמת החומרה.

> ✏️ **תרגיל 4 – תכנון**
>
> אתם מנהלי הרשת של בית ספר עם 3 נתבים ו-12 מתגים. כתבו רשימת 8 צעדי הקשחה שתבצעו על כל מכשיר, לפי סדר עדיפות, ונמקו את הראשון.
>
> **תשובה:** דוגמה: 1. enable secret + username secret (בלי זה – כל השאר חסר ערך). 2. SSH בלבד, כיבוי Telnet. 3. login block-for. 4. exec-timeout. 5. syslog + NTP לשרת מרכזי. 6. כיבוי HTTP, CDP על ממשקי קצה, small servers. 7. SNMPv3 בלבד. 8. banner אזהרה. 9. גיבוי config. 10. secure boot-image/config.

## 2.16 שאלות בסגנון בגרות

> 📝 **שאלה 1**
>
> מנהל רשת הקליד: `hostname R1`, `crypto key generate rsa` – וקיבל שגיאה. מה חסר?
>
> **תשובה:** `ip domain-name`. יצירת מפתחות RSA דורשת FQDN (hostname + domain).

> 📝 **שאלה 2**
>
> מהו הסדר הנכון של רמות חומרה ב-syslog מהחמורה לקלה: Warning, Emergency, Debugging, Error?
>
> **תשובה:** Emergency (0) → Error (3) → Warning (4) → Debugging (7).

> 📝 **שאלה 3**
>
> השלימו כדי לאפשר גישה מרחוק ב-SSH בלבד עם אימות מול משתמש מקומי:  
> `R1(config)# line vty 0 4`  
> `R1(config-line)# ______`  
> `R1(config-line)# ______`
>
> **תשובה:** `login local` ו-`transport input ssh`.

> 📝 **שאלה 4**
>
> מנהל הגדיר `logging trap 3`. אילו הודעות יישלחו לשרת ה-syslog?
>
> **תשובה:** רמות 0–3: Emergencies, Alerts, Critical, Errors. הודעות Warning ומטה לא יישלחו.

> 📝 **שאלה 5**
>
> נכון / לא נכון: (א) `service password-encryption` מצפין את הסיסמאות באופן שאינו ניתן לפענוח. (ב) SNMPv3 תומך בהצפנה. (ג) NTP משתמש ב-TCP. (ד) SSH גרסה 1 מאובטחת יותר מגרסה 2.
>
> **תשובה:** (א) לא נכון – type 7, ניתן לפענוח בקלות. (ב) נכון. (ג) לא נכון – UDP 123. (ד) לא נכון.

> 📝 **שאלה 6**
>
> איזו פקודה תגרום לנתב לנתק משתמש בקונסול לאחר 3 דקות ללא פעילות?
>
> **תשובה:** `line console 0` → `exec-timeout 3 0`.

## 2.17 מעבדה (2 שעות) – הקשחת נתב ב-Packet Tracer

1. טופולוגיה: PC — Switch — R1 — Syslog/NTP server (Server-PT עם שירותי SYSLOG ו-NTP מופעלים).
2. הגדירו hostname, enable secret, min-length, service password-encryption, banner.
3. הגדירו SSH לפי 2.4. נסו Telnet – ודאו שנכשל. התחברו ב-SSH מה-PC.
4. הפעילו `login block-for 60 attempts 3 within 30`; נסו 3 סיסמאות שגויות; ראו ב-`show login` את מצב ה-quiet mode.
5. הגדירו logging לשרת ו-`logging trap informational`; כבו והדליקו ממשק; ראו את ההודעה בשרת ה-Syslog.
6. הגדירו NTP מול השרת; ודאו ב-`show ntp status` ש-synchronized.
7. צרו משתמש ברמה 5 שיכול רק `show running-config`; בדקו שאינו יכול להיכנס ל-configure terminal.

## בנק שאלות שתלמידים שואלים – ותשובות מוכנות

שאלות נפוצות בפרק הקשחת הנתב, עם תשובות מוכנות.

### סיסמאות וגישה

**ש: "אם אני שם סיסמה חזקה ל-Telnet, למה בכל זאת צריך SSH?"**  
ת: כי Telnet מעביר את **הכול** בטקסט גלוי, כולל את הסיסמה החזקה עצמה. כל מי שמאזין לרשת (Wireshark) רואה אותה. SSH מצפין את כל התקשורת. חוזק הסיסמה לא עוזר אם היא נשלחת גלויה.

**ש: "מה ההבדל בין `password` ל-`secret`?"**  
ת: `secret` נשמר כ**גיבוב חד-כיווני** (לא ניתן לשחזר). `password` נשמר גלוי, ואפילו עם `service password-encryption` הוא רק "type 7" שמפוענח באתר אונליין בשנייה. תמיד להשתמש ב-`secret`.

**ש: "אם `service password-encryption` זו הצפנה, למה היא חלשה?"**  
ת: כי זה אלגוריתם הפיך וישן (וריאציה על Vigenère). הוא מגן רק מפני מישהו שמציץ מעבר לכתף בזמן שאתם צופים בקונפיג – לא מפני תוקף אמיתי. ה"חוזק" האמיתי הוא ב-`secret` (גיבוב).

**ש: "מה קורה אם שכחתי את ה-enable secret?"**  
ת: יש הליך **password recovery** דרך גישה פיזית לקונסול: מאתחלים, נכנסים ל-ROMMON, משנים את ה-configuration register (0x2142) כדי לדלג על ה-startup-config, ומגדירים סיסמה חדשה. המסקנה החשובה: **מי שיש לו גישה פיזית לנתב – שולט בו**, ולכן אבטחה פיזית קריטית.

**ש: "מה ההבדל בין רמות הרשאה (privilege levels) לתצוגות (views)?"**  
ת: רמות הרשאה גסות – רמה נתונה מקבלת אוטומטית גם את כל מה שמתחתיה. תצוגות (parser view) מדויקות – מגדירים רשימת פקודות מדויקת לכל תפקיד, אך דורשות שה-AAA יופעל.

### SSH

**ש: "למה צריך `ip domain-name` כדי ליצור מפתחות SSH?"**  
ת: כי שם המפתח נגזר מהשם המלא של הנתב = hostname + domain-name (FQDN). בלי דומיין הנתב לא יודע איזה שם לתת למפתח, והפקודה נכשלת עם "Please define a domain-name first".

**ש: "אחרי `transport input ssh` ניתקתי בטעות את Telnet – זו טעות?"**  
ת: לא, זה בדיוק מה שרוצים – לחסום את Telnet הלא-מאובטח ולאפשר רק SSH. חיבור Telnet חדש ייכשל, וזו התנהגות רצויה.

### שירותים וניטור

**ש: "למה זמן מדויק (NTP) קשור לאבטחה בכלל?"**  
ת: כי בלי זמן מסונכרן, הלוגים מכל המכשירים לא ניתנים לשחזור – אי אפשר לדעת מה קרה לפני מה כשחוקרים אירוע. בנוסף, תעודות דיגיטליות ומפתחות VPN תלויים בזמן נכון.

**ש: "SNMPv2 באמת כל כך גרוע?"**  
ת: הבעיה שלו היא ה-community string שעובר בטקסט גלוי (ולעיתים נשאר "public"). אם חייבים v2c – לפחות read-only + הגבלה ב-ACL לכתובת תחנת הניהול. אבל הנכון הוא v3, שמוסיף אימות (HMAC) והצפנה.

**ש: "אז למה שלא נריץ תמיד `auto secure` ונגמור עם זה?"**  
ת: כי הוא "עיוור" – יכול לכבות CDP שהמתגים צריכים, להפעיל חומת אש שתחסום תעבורה לגיטימית, ואי אפשר לבטלו בפקודה אחת. מריצים אותו, בודקים מה שינה עם `show auto secure config`, ומכווננים.

**ש: "מה זה בעצם CLI, ולמה לא ללמוד ממשק גרפי?"**  
ת: CLI הוא ממשק שורת הפקודה של הנתב. אנחנו לומדים אותו כי הוא אוניברסלי (עובד על כל ציוד סיסקו וגם דרך SSH), מדויק, וניתן לאוטומציה – **והבגרות בודקת אותו בלבד**. הממשקים הגרפיים (SDM/CCP) יצאו משימוש.

## מילון מונחים – הגדרות

הגדרות תמציתיות של המונחים המרכזיים בפרק. שימושי גם כדף עזר לבחינה (מותר מילון מונחים).

| **מונח** | **הגדרה** |
| --- | --- |
| **CLI (Command Line Interface)** | ממשק שורת פקודה לניהול ציוד רשת בהקלדת פקודות טקסט. |
| **IOS** | מערכת ההפעלה של ציוד סיסקו. |
| **running-config** | ההגדרות הפעילות בזיכרון; נמחקות בכיבוי אם לא נשמרו. |
| **startup-config** | ההגדרות השמורות שנטענות באתחול הנתב. |
| **Console / VTY / AUX** | דרכי גישה לנתב: קונסול (פיזי), VTY (מרחוק ברשת), AUX (מודם ישן). |
| **In-band / OOB** | ניהול דרך רשת הנתונים (In-band) או דרך רשת ניהול נפרדת (Out-of-band). |
| **enable secret** | סיסמת מצב מנהל, נשמרת כגיבוב חד-כיווני (בטוח). |
| **service password-encryption** | מסתיר סיסמאות בקונפיג בהצפנה חלשה (type 7) – מגן רק מהצצה. |
| **SSH (Secure Shell)** | פרוטוקול ניהול מרחוק מוצפן (פורט 22); מחליף את Telnet הלא-מאובטח. |
| **Telnet** | פרוטוקול ניהול מרחוק לא מוצפן (פורט 23) – מסוכן, לא לשימוש. |
| **מפתחות RSA** | זוג מפתחות (ציבורי/פרטי) שהנתב מייצר כדי לאפשר הצפנת SSH. |
| **רמות הרשאה (Privilege levels)** | 16 רמות (0–15) הקובעות אילו פקודות מותרות; 15 = הכול. |
| **Parser View** | תצוגת תפקיד – רשימת פקודות מדויקת למשתמש; דורשת AAA. |
| **Banner** | הודעת אזהרה משפטית המוצגת בכניסה לנתב. |
| **Syslog** | מנגנון יומן אירועים; שולח הודעות לשרת מרכזי (UDP 514). |
| **Severity levels** | 8 רמות חומרה ליומן (0=Emergency החמור ביותר עד 7=Debug). |
| **NTP (Network Time Protocol)** | מסנכרן שעונים בכל הציוד (UDP 123); קריטי ללוגים ולתעודות. |
| **SNMP** | פרוטוקול לניטור ציוד (UDP 161); גרסה 3 בלבד מאובטחת. |
| **AutoSecure** | פקודה שמבצעת הקשחה אוטומטית של הנתב בצעד אחד. |
| **Hardening (הקשחה)** | סגירת שירותים מיותרים והגדרות אבטחה למזעור שטח התקיפה. |
| **err-disabled** | מצב שבו פורט מושבת אוטומטית עקב הפרת אבטחה. |
