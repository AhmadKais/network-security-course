<div dir="rtl" align="right">

# חלק ⁦1⁩ · פרק ⁦8⁩ – שורת הפקודה ואבחון תקלות

_~⁦6⁩ שעות · כלי עבודה – לפתוח לצד כל פרק אחר_

> 📘 **איך לקרוא את הפרק הזה**
>
> הפרק הזה שונה מהאחרים: הוא לא נושא, הוא **ארגז כלים**. החצי הראשון מסביר את שורת הפקודה של ⁦Cisco⁩ – המצבים, הפקודות שמופיעות בכל קונפיגורציה, ומה קורה כשמכבים מכשיר. החצי השני מלמד **שיטה** לאבחון תקלות – כי בבחינה המעשית של הפרויקט הבוחן **יקלקל** משהו ברשת ויבקש מכם למצוא. מי שמנחש – נכשל. מי שיש לו שיטה – מוצא. הסעיף האחרון הוא בנק של ⁦20⁩ תקלות: תסמין → פקודה → סיבה. תלמדו אותו כמו מילים.

## ⁦8.1⁩ מצבי ה-⁦IOS⁩ – לדעת איפה אתם לפי הסימן

מערכת ההפעלה של ציוד ⁦Cisco⁩ נקראת **⁦IOS**.⁩ יש לה **מצבים**, וכל מצב מרשה פקודות אחרות. **הסימן בסוף השורה אומר לכם בדיוק איפה אתם:**

<div dir="ltr" align="left">

```
Switch>                    USER EXEC        - look only. ping, show (some).
   |  enable
   v
Switch#                    PRIVILEGED EXEC  - all show commands, debug, copy, reload.
   |  configure terminal
   v
Switch(config)#            GLOBAL CONFIG    - hostname, vlan, ip route, router ospf...
   |  interface Fa0/1          |  line vty 0 15        |  router ospf 1
   v                           v                       v
Switch(config-if)#         Switch(config-line)#    Switch(config-router)#
   INTERFACE                   LINE                    ROUTER
   ip address, shutdown...     password, login...      network, router-id...

   exit   = one level up          end (or Ctrl+Z) = straight back to  #
```

</div>

| סימן | מצב | מה מותר |
|---|---|---|
| `>` | ⁦User EXEC⁩ | להסתכל. `⁦ping⁩`, חלק מ-`⁦show⁩`. |
| `#` | ⁦Privileged EXEC⁩ | כל ה-`⁦show⁩`, `⁦debug⁩`, `⁦copy⁩`, `⁦reload⁩`. |
| `(⁦config)⁩#` | ⁦Global⁩ | הגדרות כלליות |
| `(⁦config-if)⁩#` | ⁦Interface⁩ | הגדרות של ממשק אחד |
| `(⁦config-line)⁩#` | ⁦Line⁩ | קווי גישה (⁦console, vty)⁩ |
| `(⁦config-router)⁩#` | ⁦Router⁩ | פרוטוקול ניתוב |

> 💡 **שלושה קיצורים שחוסכים שעות**
>
> - **⁦Tab⁩** – משלים פקודה. `⁦sh⁩` + ⁦Tab⁩ = `⁦show⁩`.
> - **?** – מציג מה אפשר להקליד עכשיו. `⁦show ip⁩ ?` – כל האפשרויות אחרי `⁦show ip⁩`.
> - **קיצורים** – `⁦sh run⁩` = `⁦show running-config⁩`, `⁦conf t⁩` = `⁦configure terminal⁩`, `⁦int fa0/1⁩` = `⁦interface FastEthernet0/1⁩`. ⁦IOS⁩ מבין כל קיצור שהוא **חד-משמעי**.
> - **`⁦do⁩`** – להריץ פקודת `⁦show⁩` מתוך מצב ⁦config⁩ בלי לצאת: `(⁦config)# do show ip route⁩`.

## ⁦8.2 running-config⁩ לעומת ⁦startup-config⁩ – למה ⁦write memory⁩ מציל שעות

זו הטעות שקורית למישהו בכל כיתה, פעם אחת, ואז לא שוב.

| | ⁦running-config | startup-config⁩ |
|---|---|---|
| **איפה** | ⁦RAM | NVRAM⁩ |
| **מה זה** | **ההגדרות הפעילות עכשיו** | ההגדרות שנטענות בהפעלה |
| **שורד כיבוי?** | **לא** | כן |
| **משתנה על ידי** | **כל פקודה, מיד** | רק `⁦write memory⁩` / `⁦copy run start⁩` |

<div dir="ltr" align="left">

```
   You type a command  --->  running-config changes INSTANTLY  --->  device behaves differently NOW
                                        |
                                        |  write memory   (or: copy running-config startup-config)
                                        v
                               startup-config  --->  survives reload / power off

   No write memory  +  reload  =  EVERYTHING you typed is GONE.
```

</div>

> ⚠️ **⁦40⁩ דקות של עבודה נעלמות**
>
> תלמיד מגדיר מתג במשך ⁦40⁩ דקות, מכבה ומדליק "לבדוק", ומגלה מתג ריק. **כל** פקודה פועלת מיד **ונעלמת בכיבוי** עד ששומרים. ההרגל: `⁦write memory⁩` **אחרי כל שינוי שעובד**, לא בסוף השיעור.
>
> ויש לזה גם **צד שימושי**: ניסוי שהשתבש? **אל תשמרו.** `⁦reload⁩` מחזיר את ההגדרה הטובה האחרונה תוך שניות – הרבה יותר מהר מלפרק את הנזק ביד.

פקודות קשורות: `⁦show running-config⁩` (מה רץ), `⁦show startup-config⁩` (מה שמור), `⁦erase startup-config⁩` + `⁦reload⁩` (איפוס למפעל – **בזהירות**).

## ⁦8.3⁩ שש הפקודות שבכל קונפיגורציה – ולמה

הן מופיעות בכל מכשיר בפרויקט, ורוב התלמידים מדביקים אותן בלי להבין. כל אחת שווה ⁦30⁩ שניות:

| פקודה | למה היא שם |
|---|---|
| `⁦no ip domain-lookup⁩` | פקודה עם שגיאת הקלדה → ⁦IOS⁩ חושב שזה שם מחשב → מנסה לפתור ב-⁦DNS⁩ → **המסך קופא ⁦30⁩ שניות**. השורה הזאת מבטלת את זה. הכי מוערכת בקובץ. |
| `⁦logging synchronous⁩` | (על `⁦line console⁩`) הודעות לוג מופיעות באמצע מה שאתם מקלידים ומבלבלות. עם זה – ⁦IOS⁩ מדפיס מחדש את השורה שלכם אחרי כל הודעה. |
| `⁦exec-timeout 15 0⁩` | ניתוק אחרי ⁦15⁩ דקות של חוסר פעילות. `⁦0 0⁩` = לעולם לא – נוח במעבדה, **ליקוי בכל ביקורת אבטחה**. |
| `⁦enable secret⁩` | סיסמת מצב מנהל, **מגובבת** (⁦MD5).⁩ תמיד `⁦secret⁩`, אף פעם לא `⁦password⁩`. |
| `⁦service password-encryption⁩` | מסתיר סיסמאות גלויות ב-`⁦show run⁩`. **⁦Type 7⁩ – הפיך תוך שנייה.** נגד הצצה, לא נגד תוקף. |
| `⁦username X privilege 15 secret Y⁩` | חשבון מקומי. **⁦Privilege 15⁩** = מצב מנהל מלא (`#`) ישר בכניסה. ⁦Privilege 1⁩ = `>`. |
| `⁦banner motd⁩` | הודעה לפני הכניסה. **"גישה מורשית בלבד"** – גם דרישה משפטית וגם דרישת הפרויקט (⁦22.2).⁩ |

## ⁦8.4⁩ כבלים, ⁦Auto-MDIX⁩ ושמות ממשקים

**הכלל הישן:** מכשירים **דומים** (מתג-מתג, נתב-נתב, מחשב-מחשב) – כבל **מוצלב (⁦Crossover)**.⁩ מכשירים **שונים** (מתג-מחשב, מתג-נתב) – כבל **ישר (⁦Straight-through)**.⁩ נשאל בבחינות.

**המציאות היום:** **⁦Auto-MDIX⁩** – המתג מזהה כבל "לא נכון" ומחליף את הזוגות בעצמו. לכן בפרויקט כל הכבלים ישרים, גם מתג-מתג, וזה עובד. ב-⁦Packet Tracer⁩ יש כבל "אוטומטי" שבוחר לבד.

<div dir="ltr" align="left">

```
FastEthernet0/1        Fa0/1      100 Mbps
GigabitEthernet0/1     Gi0/1        1 Gbps
                       ---+-- -+-
                          |    +---- port number on that module
                          +--------- slot/module number (0 = built in)

Router interfaces:  Gi0/0, Gi0/1  (slot 0, ports 0-1)
Subinterface:       Gi0/0.11      (logical, for VLAN 11)
Virtual:            Vlan11, Loopback0, Port-channel1
```

</div>

**המהירות היא חלק מהשם** – וזה חשוב ל-⁦STP: Gi⁩ = עלות ⁦4, Fa⁩ = עלות ⁦19⁩, לפני שמישהו הגדיר כלום.

## ⁦8.5 CDP⁩ – שימושי, ומסוכן

**⁦CDP (Cisco Discovery Protocol)⁩** – כל מכשיר ⁦Cisco⁩ מודיע לשכניו הישירים, כל ⁦60⁩ שניות: מי אני, איזה דגם, איזו גרסה, מאיזה פורט. `⁦show cdp neighbors detail⁩` ממפה רשת לא מוכרת מהר מכל פקודה אחרת. וזה מה שמייצר את `%⁦CDP-4-NATIVE_VLAN_MISMATCH⁩` מפרק ⁦3.⁩

אבל: **בלי אימות, לכל מי שמחובר.** תוקף על פורט ⁦Access⁩ מקבל דגם + גרסת תוכנה – בדיוק מה שצריך כדי לבחור ⁦exploit.⁩ לכן:

```
interface range FastEthernet0/1-21
 no cdp enable              ! off on user-facing ports
! left ON for trunks and uplinks, where it is genuinely useful
```

**סלקטיבי, לא גלובלי** – מראה שקלתם תועלת מול סיכון. זו התשובה שמקבלת ניקוד.

## ⁦8.6 err-disabled⁩ – איך פורט מגיע לשם ואיך מחזירים

ארבעה מנגנונים בפרויקט יכולים לכבות פורט אוטומטית: **⁦BPDU Guard**, **Port Security⁩** (במצב ⁦shutdown), **Storm Control⁩**, ואי-התאמת ⁦Duplex.⁩ הפורט עובר למצב **⁦err-disabled⁩** – **כבוי מנהלתית ולא מתאושש לבד.** להוציא את המכשיר הבעייתי לא עוזר.

<div dir="ltr" align="left">

```
! 1. confirm, and see WHICH mechanism did it
Switch# show interfaces status err-disabled
Switch# show errdisable recovery

! 2. fix the cause, then bounce the port -- BOTH commands, in this order
Switch(config)# interface FastEthernet0/3
Switch(config-if)# shutdown
Switch(config-if)# no shutdown

! 3. or let the switch reopen it by itself after 5 minutes
Switch(config)# errdisable recovery cause bpduguard
Switch(config)# errdisable recovery cause psecure-violation
Switch(config)# errdisable recovery interval 300
```

</div>

> ⚠️ **`⁦no shutdown⁩` לבד לא עושה כלום**
>
> הפורט לא במצב ⁦shutdown⁩ – הוא במצב ⁦err-disabled.⁩ חייבים **קודם** `⁦shutdown⁩` ואז `⁦no shutdown⁩`. זו התשובה השגויה הנפוצה ביותר, ושווה לתת לתלמיד לנסות ולראות שזה לא עובד לפני שמראים את הזוג.

## ⁦8.7⁩ שיטת האבחון – איך לא לנחש

בבחינה המעשית: **"מחלקת הכספים לא מגיעה למדפסת. מצא למה."** יש שתי דרכים לגשת:

**ניחוש:** לפתוח קונפיגורציות ולחפש משהו "מוזר". לוקח שעה, מוצא במקרה.

**שיטה:** לעבור על השכבות **בסדר**, עם פקודה אחת לכל שכבה, ולעצור בראשונה שנכשלת. הבעיה תמיד בשכבה הראשונה שנכשלה או ממש מתחתיה.

<div dir="ltr" align="left">

```
BOTTOM-UP  (start physical, go up)          Use when: "nothing works at all"

  L1  Is the link up?                 show ip interface brief    -> up/up ?
  L2  Is it in the right VLAN?        show vlan brief            -> port in VLAN 11 ?
      Is the trunk carrying it?       show interfaces trunk      -> VLAN 11 allowed ?
      Is STP blocking it?             show spanning-tree vlan 11 -> FWD or BLK ?
      Did the switch learn the MAC?   show mac address-table     -> address on the port ?
  L3  Does the host have an IP?       ipconfig /all              -> 169.254 = DHCP failed
      Can it reach its gateway?       ping <gateway>             -> ARP works? SVI up?
      Does the router know the route? show ip route              -> route exists ?
      Does NAT translate?             show ip nat translations   -> entry appears ?
  L7  Does the name resolve?          nslookup / ping by name    -> DNS ?


TOP-DOWN  (start from what the user sees)   Use when: "only X does not work"

  L7  ping by name fails, ping by IP works        -> DNS
  L3  ping by IP fails, ping gateway works        -> routing / NAT / ACL
  L3  ping gateway fails, same-VLAN ping works    -> gateway / HSRP / SVI
  L2  same-VLAN ping fails                         -> VLAN / trunk / STP / cable
```

</div>

**הכלל:** כל בדיקה תלויה רק בבדיקות שמעליה בטבלה. הבדיקה הראשונה שנכשלת **מאתרת** את הבעיה. אחרי שמצאתם את השכבה – רק אז פותחים קונפיגורציה, ורק של המכשיר הרלוונטי.

## ⁦8.8⁩ הפקודות – מה כל אחת מוכיחה

### ממחשב

| פקודה | מוכיחה |
|---|---|
| `⁦ipconfig /all⁩` | כתובת, מסכה, שער, ⁦DNS, MAC. **169.254.x.x = DHCP⁩ נכשל.** |
| `⁦ping⁩ <IP>` | הגעה בשכבה ⁦3.⁩ עובד = ניתוב תקין לשם ובחזרה. |
| `⁦ping⁩ <gateway>` | השער חי וה-⁦ARP⁩ עובד. **הבדיקה השנייה תמיד.** |
| `⁦ping⁩ <name>` | ⁦DNS⁩ + הכול. אם ⁦IP⁩ עובד ושם לא → ⁦DNS.⁩ |
| `⁦tracert⁩ <IP>` | **באיזה נתב** החבילה נתקעת. הקפיצה האחרונה שענתה = הנתב שלפני הבעיה. |
| `⁦arp -a⁩` | מטמון ⁦ARP.⁩ אם השער לא בו אחרי פינג – ה-⁦ARP⁩ לא נענה. |
| `⁦nslookup⁩ <name>` | שואל ⁦DNS⁩ ישירות, מראה מי ענה ומה. |

### ממתג / נתב

| פקודה | מוכיחה |
|---|---|
| `⁦show ip interface brief⁩` | **הפקודה הראשונה תמיד.** כל ממשק: כתובת, ⁦up/down.⁩ |
| `⁦show interfaces status⁩` | (מתג) ⁦VLAN⁩, מהירות, ⁦duplex, **err-disabled**.⁩ |
| `⁦show vlan brief⁩` | איזה פורט באיזה ⁦VLAN. Trunk⁩-ים לא מופיעים – נכון. |
| `⁦show interfaces trunk⁩` | מה ⁦Trunk, Native, allowed⁩, ומה **בפועל מועבר**. |
| `⁦show mac address-table⁩` | מה המתג למד ואיפה. ריק לפורט = לא הגיעה מסגרת ממנו. |
| `⁦show spanning-tree vlan N⁩` | מי השורש, ⁦FWD/BLK.⁩ |
| `⁦show ip route⁩` | טבלת הניתוב. `⁦C⁩` = מחובר, `⁦S⁩` = סטטי, `⁦O⁩` = ⁦OSPF⁩, `⁦D⁩` = ⁦EIGRP⁩, `⁦B⁩` = ⁦BGP.⁩ **כמעט ריק במתג ⁦3560⁩ = `⁦ip routing⁩` חסר.** |
| `⁦show arp⁩` | ⁦ARP⁩ של הנתב. |
| `⁦show ip dhcp binding⁩` | מי קיבל מה. |
| `⁦show standby brief⁩` | ⁦HSRP⁩ – ⁦Active/Standby⁩, עמודת ⁦P.⁩ |
| `⁦show ip ospf neighbor⁩` / `⁦show ip eigrp neighbors⁩` | שכנים. אין שכנים = טיימרים/אזור/⁦AS/⁩אימות. |
| `⁦show ip nat translations⁩` | תרגומים. ריק = ⁦inside/outside⁩ חסר. |
| `⁦show logging⁩` | **הלוג.** המתג לרוב כבר כתב מה הבעיה. |
| `⁦show running-config⁩ \| ⁦section X⁩` | רק החלק הרלוונטי. `\| ⁦include⁩`, `\| ⁦begin⁩` – מסננים. |

### ⁦up/down⁩ – ארבעת המצבים

<div dir="ltr" align="left">

```
show ip interface brief   ->   Status  /  Protocol

  up      / up        OK.
  up      / down      Physical link fine, Layer 2 not - wrong encapsulation, clock, or (SVI) no active port in the VLAN.
  down    / down      No link. Cable, far end is off, or speed/duplex mismatch.
  admin.. / down      YOU turned it off. "no shutdown".
```

</div>

## ⁦8.9⁩ סימולציה ב-⁦Packet Tracer⁩ – לראות את החבילה

⁦Packet Tracer⁩ יכול **לעצור את הזמן** ולהראות כל מסגרת בנפרד. זה כלי הלימוד החזק ביותר בתוכנה, ורוב התלמידים לא משתמשים בו.

⁦1.⁩ למטה מימין: **⁦Simulation**.⁩
⁦2. **Edit Filters⁩** → לבטל הכול → לסמן רק את הפרוטוקול שרוצים (⁦ARP, ICMP, DHCP...).⁩ בלי סינון המסך בלתי קריא תוך שניות.
⁦3.⁩ לייצר תעבורה (פינג, חידוש ⁦DHCP).⁩
⁦4. **Capture / Forward⁩** – צעד אחד. ללחוץ על מעטפה → לראות כל שדה בכותרת.

| מה להראות | פילטר | מה רואים |
|---|---|---|
| ⁦ARP⁩ – פרק ⁦1 | ARP⁩ | שידור "למי יש", תשובה מאחד |
| מסגרת נבנית מחדש – פרק ⁦1 | ICMP⁩ | ה-⁦MAC⁩ משתנה בנתב, ה-⁦IP⁩ לא |
| סערת שידורים – פרק ⁦4 | ARP⁩ | (אחרי `⁦no spanning-tree⁩`) המעטפה מתרבה |
| ⁦DORA⁩ – פרק ⁦5 | DHCP⁩ | ארבע הודעות |
| ⁦helper-address⁩ – פרק ⁦5 | DHCP⁩ | שידור נכנס לנתב, ⁦unicast⁩ יוצא |
| ה-⁦MAC⁩ הווירטואלי – פרק ⁦5 | ARP⁩ | המחשב מקבל ⁦0000.0C9F.F00B⁩ מ"מכשיר" שלא קיים |
| ⁦NAT⁩ – פרק ⁦7 | ICMP⁩ | כתובת המקור מתחלפת בנתב הקצה |
| סיסמת ⁦Telnet⁩ גלויה – חלק ⁦2 | Telnet⁩ | הסיסמה **בטקסט פתוח** בחבילה. הטיעון ל-⁦SSH⁩ במסך אחד. |

## ⁦8.10⁩ בנק תקלות – ⁦20⁩ תסמינים

למדו את זה כמו מילים. בבחינה המעשית, הבוחן יזריק **אחת** מאלה.

| # | תסמין | פקודה לבדוק | סיבה סבירה |
|---|---|---|---|
| ⁦1⁩ | מחשב קיבל ⁦169.254.x.x⁩ | `⁦ipconfig /all⁩`, `⁦show ip dhcp binding⁩` | ⁦DHCP⁩ לא מגיע: מאגר חסר, ⁦helper⁩ חסר/בצד הלא נכון, פורט לא ב-⁦VLAN, snooping⁩ בלי ⁦trust⁩ |
| ⁦2⁩ | פינג לשער נכשל, לשכן באותו ⁦VLAN⁩ עובד | `⁦show ip interface brief⁩` בנתב | ⁦SVI down⁩ (אין פורט פעיל), ⁦HSRP⁩ לא מוגדר, כתובת שער שגויה ב-⁦DHCP⁩ |
| ⁦3⁩ | פינג בין ⁦VLAN⁩-ים נכשל, לשער עובד | `⁦show ip route⁩` | `⁦ip routing⁩` חסר (טבלה כמעט ריקה) |
| ⁦4⁩ | מחשב ב-⁦VLAN 11⁩ לא מגיע למחשב ב-⁦VLAN 11⁩ במתג אחר | `⁦show interfaces trunk⁩` | ⁦VLAN 11⁩ לא ב-⁦allowed⁩ באחד ה-⁦Trunk⁩-ים, או הפורט לא ⁦Trunk⁩ |
| ⁦5⁩ | לוג: `⁦NATIVE_VLAN_MISMATCH⁩` | `⁦show interfaces trunk⁩` | ⁦Native VLAN⁩ שונה בשני צדי הקו |
| ⁦6⁩ | לקוח ⁦VTP⁩ עם ⁦5 VLAN⁩-ים בלבד | `⁦show vtp status⁩` | דומיין / סיסמה / גרסה שונים – כשל שקט |
| ⁦7⁩ | כל ה-⁦VLAN⁩-ים נעלמו בבניין | `⁦show vtp status⁩` בכולם | מתג עם ⁦Revision⁩ גבוה הצטרף ודרס |
| ⁦8⁩ | `⁦Po1(SD)⁩` או `⁦Fa0/24(I)⁩` | `⁦show etherchannel summary⁩` | חברים לא זהים; או ⁦passive-passive⁩ |
| ⁦9⁩ | מחשב "לא מקבל ⁦DHCP"⁩ ואז כן, אחרי ⁦30⁩ שנ' | `⁦show spanning-tree interface⁩` | אין ⁦PortFast⁩ – זה ⁦STP⁩, לא ⁦DHCP⁩ |
| ⁦10⁩ | הרשת איטית מאוד, תעבורה במסלול מוזר | `⁦show spanning-tree vlan N⁩` | מתג גישה הפך לשורש (עדיפות לא הוגדרה או עדיפות ⁦0⁩ הוזרקה) |
| ⁦11⁩ | פורט `⁦err-disabled⁩` | `⁦show interfaces status err-disabled⁩` | ⁦BPDU Guard / Port Security / Storm.⁩ `⁦shutdown⁩` → `⁦no shutdown⁩` |
| ⁦12⁩ | מחשב שהועבר לפורט אחר לא עובד | `⁦show port-security address⁩` | ⁦Sticky MAC⁩ נעול לפורט הישן |
| ⁦13 | HSRP⁩: שני המתגים ⁦Active⁩ | `⁦show standby brief⁩` בשניהם | מספר קבוצה שונה, או גרסה ⁦1⁩ מול ⁦2⁩ |
| ⁦14 | HSRP⁩: התפקידים הפוכים מהתכנון | `⁦show standby brief⁩` – עמודת ⁦P⁩ | `⁦preempt⁩` חסר |
| ⁦15 | uplink⁩ נפל, אין ⁦failover⁩, אין תקשורת | `⁦show standby Vlan11⁩` – ⁦Track⁩ | `⁦track⁩` חסר, או הפחתה קטנה מדי |
| ⁦16⁩ | אין שכני ⁦OSPF⁩ | `⁦show ip ospf interface⁩` | טיימרים / אזור / אימות / ⁦Router-ID⁩ כפול |
| ⁦17⁩ | אזור ⁦OSPF⁩ שלם לא מופיע בטבלאות | `⁦show ip ospf virtual-links⁩` | אזור לא נוגע ב-⁦0⁩ ואין ⁦Virtual Link⁩, או ה-⁦RID⁩ ב-⁦Virtual Link⁩ שגוי |
| ⁦18⁩ | אין שכני ⁦EIGRP⁩ | `⁦show ip eigrp neighbors⁩` | מספר ⁦AS⁩ שונה, ⁦K-values⁩, אימות |
| ⁦19 | NAT⁩: `⁦show ip nat translations⁩` ריק | `⁦show ip nat statistics⁩` | `⁦ip nat inside/outside⁩` חסר על הממשקים |
| ⁦20⁩ | פינג ל-⁦IP⁩ עובד, לשם לא | `⁦nslookup⁩`, `⁦ipconfig /all⁩` | ⁦DNS⁩: שרת שגוי ב-⁦DHCP⁩, שרת לא נגיש, רשומה חסרה |

> 💡 **איך להשתמש בבנק**
>
> לא לשנן את העמודה הימנית. לשנן את **הפקודה** – העמודה השלישית. בבחינה, התסמין נתון. הפקודה הנכונה מובילה לסיבה תוך דקה. הסיבה בלי הפקודה היא ניחוש.

## ⁦8.11⁩ סיכום

⁦1.⁩ הסימן אומר את המצב: `>` `#` `(⁦config)⁩#` `(⁦config-if)⁩#`. ⁦Tab⁩, `?`, `⁦do⁩`.
⁦2. **running = RAM⁩ = עכשיו = נעלם בכיבוי. `⁦write memory⁩` אחרי כל שינוי.** ולהפך: ניסוי שהשתבש – `⁦reload⁩` בלי לשמור.
⁦3.⁩ `⁦no ip domain-lookup⁩`, `⁦logging synchronous⁩`, `⁦exec-timeout⁩`, `⁦enable secret⁩` (לא ⁦password)⁩, `⁦service password-encryption⁩` (⁦Type 7⁩, לא הגנה אמיתית), `⁦privilege 15⁩`.
⁦4. Auto-MDIX⁩ = כבל ישר לכולם. ⁦Fa = 100M⁩ = עלות ⁦19, Gi = 1G⁩ = עלות ⁦4.⁩
⁦5. CDP⁩: שימושי על ⁦uplinks⁩, מסוכן על פורטי משתמשים – `⁦no cdp enable⁩` סלקטיבי.
⁦6. err-disabled⁩: `⁦shutdown⁩` ואז `⁦no shutdown⁩`. `⁦no shutdown⁩` לבד לא עוזר.
⁦7.⁩ **שיטה:** שכבה-שכבה, פקודה לשכבה, הראשונה שנכשלת מאתרת. `⁦show ip interface brief⁩` ראשונה, `⁦ping⁩ <gateway>` שנייה.
⁦8. Simulation Mode⁩ – לראות את מה שלמדתם.
⁦9.⁩ בנק ⁦20⁩ התקלות – לשנן את הפקודות.

---

## ✏️ תרגילים

**תרגיל ⁦1.⁩** תלמיד נמצא ב-`⁦Switch(config-if)⁩#` ורוצה להריץ `⁦show ip route⁩`. שלוש דרכים.

<details><summary>פתרון</summary>

(⁦1)⁩ `⁦end⁩` (או ⁦Ctrl+Z)⁩ ואז `⁦show ip route⁩` מ-`#`. (⁦2)⁩ `⁦exit⁩` פעמיים. (⁦3)⁩ **`⁦do show ip route⁩`** – בלי לצאת. השלישית הכי מהירה.

</details>

**תרגיל ⁦2.⁩** מחשב לא מגיע לאינטרנט. `⁦ipconfig⁩` מציג כתובת תקינה. `⁦ping 10.1.16.1⁩` (השער) עובד. `⁦ping 8.8.8.8⁩` נכשל. `⁦ping google.com⁩` נכשל. איפה הבעיה, ואיזו בדיקה הבאה?

<details><summary>פתרון</summary>

השער עובד → שכבה ⁦2⁩ ושער תקינים. ⁦IP⁩ חיצוני נכשל → הבעיה **בניתוב או ב-⁦NAT⁩** מהנתב והלאה (⁦DNS⁩ לא רלוונטי עדיין – גם ⁦IP⁩ נכשל). הבאה: `⁦tracert 8.8.8.8⁩` לראות **איפה** נתקע, ואז בנתב הקצה `⁦show ip route⁩` (יש ברירת מחדל?) ו-`⁦show ip nat translations⁩` (יש תרגום?).

</details>

**תרגיל ⁦3.⁩** `⁦show ip interface brief⁩` מציג `⁦Vlan110  10.1.20.2  up  down⁩`. תקלה?

<details><summary>פתרון</summary>

**לא בהכרח.** ⁦up/down⁩ על ⁦SVI⁩ = ה-⁦VLAN⁩ קיים אבל **אין בו פורט פעיל**. ⁦VLAN 110⁩ הוא ⁦WiFi⁩ עובדים – אם עדיין לא חוברה נקודת גישה, זה המצב הנכון. יעלה כשיחובר מכשיר ל-⁦VLAN 110.⁩ `⁦show vlan brief⁩` יאשר שאין פורטים.

</details>

**תרגיל ⁦4.⁩** מנהל מגדיר `⁦exec-timeout 0 0⁩` על כל הקווים "כדי שלא ינתק אותי". מה הסיכון?

<details><summary>פתרון</summary>

⁦Session⁩ פתוח לנצח. מסך שנשאר פתוח ונטוש = גישת מנהל למי שעובר ליד. ליקוי בכל ביקורת אבטחה. הנכון: ערך סביר (⁦10⁩–⁦15⁩ דקות). במעבדה אפשר יותר, אבל לא ⁦0.⁩

</details>

**תרגיל ⁦5.⁩** פורט ⁦Fa0/5⁩ ב-⁦err-disabled.⁩ התלמיד מקליד `⁦no shutdown⁩`. הפורט עדיין למטה. למה, ומה נכון?

<details><summary>פתרון</summary>

הפורט לא במצב ⁦shutdown⁩ – הוא ב-⁦err-disabled⁩, מצב אחר. `⁦no shutdown⁩` על פורט שלא ב-⁦shutdown⁩ לא משנה כלום. הנכון: **`⁦shutdown⁩`** ואז **`⁦no shutdown⁩`** – ה-⁦shutdown⁩ מנקה את מצב ה-⁦err-disabled.⁩ ולפני כן – לתקן את הסיבה (`⁦show interfaces status err-disabled⁩` אומר מה), אחרת הפורט ייסגר שוב.

</details>

**תרגיל ⁦6.⁩** `⁦tracert 10.2.10.5⁩` מתל אביב מציג: ⁦10.1.16.1, 10.1.4.2, 10.1.4.10⁩, ואז `* * *` לנצח. מה למדתם?

<details><summary>פתרון</summary>

החבילה עברה שלושה נתבים (השער, הליבה, עוד אחד) והנתב **הרביעי** לא ענה – או שה-⁦10.1.4.10⁩ לא יודע לאן להעביר הלאה (אין נתיב ל-⁦10.2.x)⁩, או שהקפיצה הבאה מתה. הבדיקה: להתחבר ל-⁦10.1.4.10⁩ ו-`⁦show ip route⁩` – יש נתיב ל-⁦10.2.0.0⁩? הקפיצה האחרונה שענתה = הנתב שלפני הבעיה.

</details>

---

## ❓ חידון

**⁦1.⁩** הסימן `(⁦config-if)⁩#` אומר:
- א. מצב משתמש · ב. מצב מנהל · ג. מצב הגדרת ממשק · ד. מצב ניתוב

<details><summary>תשובה</summary>**ג**</details>

**⁦2.⁩** פקודה שהוקלדה ב-⁦config⁩:
- א. פועלת רק אחרי ⁦write memory⁩ · ב. פועלת מיד ונעלמת בכיבוי אם לא נשמרה · ג. נשמרת אוטומטית · ד. פועלת אחרי ⁦reload⁩

<details><summary>תשובה</summary>**ב**</details>

**⁦3.⁩** `⁦no ip domain-lookup⁩` מונע:
- א. גלישה · ב. הקפאת מסך בטעות הקלדה · ג. ⁦DNS⁩ ברשת · ד. פינג

<details><summary>תשובה</summary>**ב**</details>

**⁦4.⁩** `⁦service password-encryption⁩` משתמש ב:
- א. ⁦MD5⁩ · ב. ⁦AES⁩ · ג. ⁦Type 7⁩ – הפיך · ד. ⁦SHA⁩

<details><summary>תשובה</summary>**ג**</details>

**⁦5.** Privilege 15⁩ =
- א. מצב משתמש · ב. מצב מנהל מלא · ג. קריאה בלבד · ד. נעול

<details><summary>תשובה</summary>**ב**</details>

**⁦6.⁩** מתג-למתג בכבל ישר עובד בגלל:
- א. ⁦VTP⁩ · ב. ⁦Auto-MDIX⁩ · ג. ⁦STP⁩ · ד. ⁦CDP⁩

<details><summary>תשובה</summary>**ב**</details>

**⁦7.⁩** פורט ב-⁦err-disabled⁩ מחזירים עם:
- א. `⁦no shutdown⁩` · ב. `⁦shutdown⁩` ואז `⁦no shutdown⁩` · ג. `⁦reload⁩` · ד. `⁦clear port⁩`

<details><summary>תשובה</summary>**ב**</details>

**⁦8.⁩** `⁦up / down⁩` על ממשק אומר:
- א. הכול תקין · ב. אין כבל · ג. קו פיזי תקין, שכבה ⁦2⁩ לא · ד. כבוי מנהלתית

<details><summary>תשובה</summary>**ג**</details>

**⁦9.⁩** פינג ל-⁦IP⁩ עובד, לשם נכשל. הבעיה ב:
- א. ניתוב · ב. ⁦NAT⁩ · ג. ⁦DNS⁩ · ד. ⁦STP⁩

<details><summary>תשובה</summary>**ג**</details>

**⁦10.⁩** הפקודה הראשונה באבחון ממתג/נתב:
- א. `⁦show running-config⁩` · ב. `⁦show ip interface brief⁩` · ג. `⁦debug all⁩` · ד. `⁦reload⁩`

<details><summary>תשובה</summary>**ב**</details>

---

## 📝 שאלות בסגנון בחינה

**שאלה ⁦1.⁩** הסבירו את ההבדל בין ⁦running-config⁩ ל-⁦startup-config.⁩ תארו תרחיש שבו אי-הבנה של ההבדל גורמת לאובדן עבודה, ותרחיש שבו מנצלים אותו בכוונה.

**שאלה ⁦2.⁩** תארו שיטה מסודרת לאבחון תקלה שבה מחשב אינו מגיע לשרת ברשת אחרת. ציינו פקודה אחת לכל שלב ומה כל תוצאה אומרת.

**שאלה ⁦3.⁩** מהו מצב ⁦err-disabled⁩? ציינו שלושה מנגנונים שמביאים פורט למצב זה, ואת הנוהל המדויק להחזרתו.

**שאלה ⁦4.⁩** הסבירו מדוע ⁦CDP⁩ מועיל למנהל רשת ומסוכן מבחינת אבטחה. מהי המדיניות הנכונה, ומדוע?

**שאלה ⁦5.⁩** מחשב מציג כתובת ⁦169.254.10.5.⁩ תארו את סדר הבדיקות המלא – מהמחשב ועד לשרת ה-⁦DHCP⁩ – עם הפקודה בכל שלב.

---

## 📖 מילון מונחים

| מונח | הסבר |
|---|---|
| **⁦IOS⁩** | מערכת ההפעלה של ציוד ⁦Cisco.⁩ |
| **⁦User / Privileged EXEC⁩** | `>` / `#`. להסתכל / לנהל. |
| **⁦Global / Interface / Line config⁩** | `(⁦config)⁩#` / `(⁦config-if)⁩#` / `(⁦config-line)⁩#`. |
| **⁦running-config⁩** | ההגדרות הפעילות, ב-⁦RAM.⁩ נעלמות בכיבוי. |
| **⁦startup-config⁩** | ההגדרות השמורות, ב-⁦NVRAM.⁩ נטענות בהפעלה. |
| **⁦write memory⁩** | שומר ⁦running⁩ → ⁦startup.⁩ |
| **⁦Type 7⁩** | ה"הצפנה" של `⁦service password-encryption⁩`. הפיכה. |
| **⁦Privilege Level** | 0⁩–⁦15. 15⁩ = מנהל מלא. |
| **⁦Auto-MDIX⁩** | זיהוי אוטומטי של סוג כבל. |
| **⁦CDP⁩** | גילוי שכני ⁦Cisco.⁩ שימושי / מסוכן. |
| **⁦err-disabled⁩** | פורט שכובה אוטומטית בגלל הפרה. `⁦shutdown⁩` → `⁦no shutdown⁩`. |
| **⁦Bottom-Up / Top-Down⁩** | אבחון משכבה ⁦1⁩ למעלה / משכבה ⁦7⁩ למטה. |
| **⁦up/up, up/down, down/down⁩** | מצבי ממשק. |
| **⁦Simulation Mode⁩** | מצב ב-⁦Packet Tracer⁩ לצפייה במסגרות בודדות. |

</div>
