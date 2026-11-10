"""Idegen (főleg angol) szavak és betűszavak kiejtése magyar szövegben ("hunglish").

A magyar szakszöveg keveri a nyelveket: CPU, RAM, cache, bootolás, commitolni, Joule, Faraday. A magyar
TTS-modell ezeket magyar betűkként olvasná ("cpu", "kacse"), ezért a modellnek a magyar helyesírású
kiejtést adjuk ("cépéú", "kes"). A modellnek nem kell angolul tudnia: a magyar betűket jól ejti.

- Betűszó (2-6 nagybetű): magyar betűnevekkel ("CPU" -> "cépéú"), kivéve a szóként ejtetteket
  (NATO, RAM, BIOS, POSIX). Magyar toldalék kötőjellel: "CPU-t" -> "cépéút".
- Angol szakszavak és nevek: kézi kiejtési szótár, toldalékkal együtt ("bootolás" -> "bútolás").
- Mássalhangzó-torlódásos parancsnevek (fsck, pwd): betűnként.
- Ismeretlen, angolnak látszó szó: figyelmeztetés, hogy a kiejtési szótárba fel lehessen venni.

A felhasználói kiejtési szótár ez előtt fut, így bármelyik alak felülírható.
"""

from __future__ import annotations

import re

# magyar betűnevek betűszóban (a "W" itt "vé": WWW -> vévévé)
LETTERS = {
    "A": "á", "B": "bé", "C": "cé", "D": "dé", "E": "é", "F": "ef", "G": "gé", "H": "há", "I": "í", "J": "jé",
    "K": "ká", "L": "el", "M": "em", "N": "en", "O": "ó", "P": "pé", "Q": "kú", "R": "er", "S": "es", "T": "té",
    "U": "ú", "V": "vé", "W": "vé", "X": "iksz", "Y": "ipszilon", "Z": "zé",
    "Á": "á", "É": "é", "Í": "í", "Ó": "ó", "Ö": "ö", "Ő": "ő", "Ú": "ú", "Ü": "ü", "Ű": "ű",
}
# magyar kettős betűk (angol betűszóban nem fordulnak elő; a CS és NY igen: CSS, NYSE)
DIGRAPHS = {"SZ": "esz", "ZS": "zsé", "GY": "gyé", "TY": "tyé", "LY": "elipszilon"}

# szóként ejtett betűszavak
ACRONYM_WORDS: dict[str, str] = {
    "NATO": "nátó", "NASA": "nászá", "CERN": "cern", "RAM": "ram", "ROM": "rom", "BIOS": "bájosz",
    "UEFI": "uefi", "ASCII": "eszki", "ANSI": "anszi", "POSIX": "pozix", "UNIX": "júniksz", "XENIX": "zeniksz",
    "IRIX": "íriksz", "MINIX": "miniksz", "GNU": "gnú", "GNOME": "gnóm", "GRUB": "grab", "LILO": "lilo",
    "SCSI": "szkazi", "RISC": "riszk", "CISC": "sziszk", "POST": "poszt", "SUN": "szan", "WINS": "vinsz",
    "GECOS": "gékosz", "FAT": "fat", "BASH": "bes", "JSON": "dzséjszon", "YAML": "jemel", "LAN": "lan",
    "WAN": "van", "LED": "led", "PIN": "pin", "SIM": "szim", "GIF": "gif", "JPEG": "dzséjpeg", "JPG": "dzséjpeg",
    "MIDI": "midi", "RAID": "rejd", "DOS": "dosz", "ISO": "ízó", "ARM": "arm", "SHA": "sá", "CRUD": "krad",
    "REST": "reszt", "SOAP": "szóp", "CAPTCHA": "kepcsa", "CUDA": "kuda", "MATE": "máté", "LABEL": "lébel",
    "WIFI": "vájfáj", "SAAS": "szász", "NAN": "nen", "TOML": "tomel", "MAC": "mek", "SWAP": "szvop",
    "IEEE": "í három é", "LINUX": "linux",
    # magyar betűszavak, amelyeket szóként mondunk
    "MÁV": "máv", "ÁFA": "áfa", "ELTE": "elte", "MOL": "mol", "NAV": "nav", "KRESZ": "kresz",
    "SOTE": "szote", "ÁNTSZ": "ántsz",
}

# kisbetűvel is gyakran írt betűszavak (csak ezek, hogy a magyar szavakat ne bántsuk)
LOWER_ACRONYMS = {"cpu", "gpu", "ram", "usb", "url", "pdf", "api", "html", "css", "sql", "json", "http", "https",
                  "tcp", "udp", "dns", "ssd", "hdd", "wifi", "ssh", "ftp", "xml", "csv", "jpg", "png", "gif"}

# Angol szakszavak, nevek -> magyar helyesírású kiejtés. Kulcs: kisbetűs írott alak (szóköz is lehet benne).
# A toldalékos alak a tőből jön ("boot" -> "bootolás", "cache-ben").
ENGLISH: dict[str, str] = {
    # rendszer, hardver
    "boot": "bút", "reboot": "ribút", "bootloader": "bútlóder", "bootstrap": "bútsztrep", "root": "rút",
    "chroot": "csérút", "mount": "maunt", "umount": "júmaunt", "unmount": "anmaunt", "shutdown": "satdaun",
    "kernel": "körnel", "firmware": "förmver", "hardware": "hárdver", "software": "szoftver", "driver": "drájver",
    "shell": "sell", "login": "login", "logout": "logaut", "logon": "logon", "user": "júzer", "username": "júzernév",
    "password": "pászvörd", "passwd": "pászvörd", "account": "akaunt", "group": "grúp", "groupadd": "grúp ed",
    "groupdel": "grúp del", "useradd": "júzer ed", "userdel": "júzer del", "sudo": "szúdú", "daemon": "dímon",
    "journal": "dzsörnöl", "filesystem": "fájlszisztem", "filesystems": "fájlszisztemz", "file": "fájl",
    "directory": "dájrektori", "path": "pász", "home": "hóm", "swap": "szvop", "mkswap": "em ká szvop",
    "respawn": "riszpón", "floppy": "floppi", "power": "pauer", "powerpc": "pauer pécé", "desktop": "desztop",
    "laptop": "leptop", "keyboard": "kíbord", "mouse": "maus", "screen": "szkrín", "screenshot": "szkrínsot",
    "cache": "kes", "buffer": "baffer", "thread": "szred", "multithread": "maltiszred", "scheduler": "skedzsúler",
    "stack": "sztek", "heap": "híp", "queue": "kjú", "pointer": "pojnter", "overflow": "óverfló",
    "hash": "hes", "async": "éjszink", "sync": "szink", "exec": "egzek", "noexec": "nó egzek", "nouser": "nó júzer",
    "hushlogin": "has login", "unix": "júniksz", "xfree": "iksz frí", "fastboot": "fasztbút",
    "nfslock": "en ef es lok", "shadow": "sedó", "showmount": "sómaunt", "smbpasswd": "es em bé pászvörd",
    "spool": "szpúl", "squash": "szkvos", "tree": "trí", "who": "hú", "whoami": "hú em áj", "write": "rájt",
    "writable": "rájtabl", "read": "ríd", "readonly": "ríd ónli", "winchester": "vincseszter",
    "webszerver": "vebszerver", "weboldal": "veboldal", "chmod": "csé mod", "chown": "csé ón", "grep": "grep",
    "awk": "ók", "sed": "szed", "cat": "ket", "mkdir": "em ká dír", "rmdir": "er em dír", "touch": "tacs",
    "kill": "kil", "man": "men", "emacs": "ímeksz", "gzip": "gé zip", "cron": "kron", "crontab": "krontab",
    "systemd": "szisztem dé", "fstab": "ef es tab", "inode": "ájnód", "symlink": "szimlink",
    "hardlink": "hárdlink", "process": "proszesz", "pipe": "pájp", "backup": "bekap", "restore": "risztór", "update": "apdét", "upgrade": "apgréd",
    "download": "daunlód", "upload": "aplód", "install": "insztol", "setup": "szetap", "patch": "pecs",
    "release": "rilíz", "copy": "kopi", "paste": "pészt", "default": "difolt", "free": "frí", "open source": "ópen szorsz",
    "source": "szorsz", "anonymous": "anonimusz", "author": "ószor", "real": "ríl", "day": "déj", "found": "faund",
    "foundation": "faundésön", "public": "pablik", "private": "prájvet", "static": "sztetik", "void": "vojd",
    "null": "nal", "float": "flót", "double": "dabl", "boolean": "búlien", "string": "sztring", "array": "eréj",
    "class": "klassz", "method": "meszod", "override": "óverrájd", "library": "lájbreri", "runtime": "rántájm",
    "compiler": "kompájler", "debug": "dibag", "debugger": "dibager", "bug": "bag", "feature": "fícsör",
    "framework": "frémvörk", "frontend": "frontend", "backend": "bekend", "full stack": "ful sztek",
    "layout": "lejaut", "interface": "interfész", "deploy": "diploj", "deployment": "diplojment",
    "commit": "komit", "merge": "mördzs", "branch": "brencs", "push": "pus", "pull": "pul",
    "pull request": "pul rikveszt", "repository": "repozitori", "repo": "repó", "fork": "fork",
    "pipeline": "pájplájn", "workflow": "vörkfló", "container": "kontéjner", "docker": "doker",
    "kubernetes": "kubernetesz", "cluster": "klaszter", "cloud": "klaud", "server": "szörver", "client": "klájent",
    "host": "hoszt", "localhost": "lokálhoszt", "proxy": "proxi", "firewall": "fájervól", "router": "ráuter",
    "switch": "szvics", "socket": "szoket", "packet": "peket", "ethernet": "ítörnet", "wireless": "vájerlesz",
    "bluetooth": "blútúsz", "wifi": "vájfáj", "wi-fi": "vájfáj", "browser": "bráuzer", "web": "veb", "website": "vebszájt", "online": "onlájn",
    "offline": "oflájn", "email": "ímél", "e-mail": "ímél", "spam": "szpem", "malware": "málver", "cookie": "kuki",
    "session": "szesön", "token": "tóken", "timeout": "tájmaut", "request": "rikveszt", "response": "riszpansz",
    "header": "heder", "payload": "pélód", "endpoint": "endpojnt", "query": "kvéri", "select": "szelekt",
    "insert": "inszert", "delete": "dilít", "join": "dzsojn", "machine learning": "mesín lörning",
    "deep learning": "díp lörning", "dataset": "déteszet", "benchmark": "bencsmark", "performance": "pörformansz",
    "feedback": "fídbek", "deadline": "dedlájn", "meeting": "míting", "startup": "sztartap", "smart": "szmárt",
    "smartphone": "szmártfón", "touchscreen": "tacsszkrín", "hacker": "heker", "game": "gém", "gamer": "gémer",
    # termékek, nyelvek
    "windows": "vindóz", "microsoft": "májkroszoft", "apple": "eppl", "iphone": "ájfón", "ios": "ájoesz",
    "macos": "mekoesz", "google": "gúgl", "chrome": "króm", "firefox": "fájerfox", "youtube": "jútúb",
    "facebook": "fészbuk", "github": "githab", "gitlab": "gitleb", "java": "dzsáva", "javascript": "dzsávaszkript",
    "typescript": "tájpszkript", "python": "pájton", "ruby": "rúbi", "perl": "pörl", "swift": "szvift",
    "rust": "raszt", "node": "nód", "react": "riekt", "freebsd": "frí bé es dé", "openbsd": "ópen bé es dé",
    "netbsd": "net bé es dé", "darwin": "darvin", "nextstep": "nekszt sztep", "distrowatch": "disztró vocs",
    "gobolinux": "gobó linux", "hewlett": "hjúlet", "packard": "pekard", "berkeley": "börkli",
    "microsystems": "májkroszisztemz", "intel": "intel", "nvidia": "envidia", "amd": "áemdé", "ibm": "íbéem",
    # fizikusok, matematikusok, mértékegység-nevek
    "coulomb": "kulomb", "joule": "dzsúl", "watt": "vatt", "weber": "véber", "newton": "nyúton",
    "faraday": "faradéj", "maxwell": "makszvel", "poynting": "pojnting", "zeeman": "zéman", "henry": "henri",
    "ampère": "ampér", "ampere": "ampér", "ohm": "óm", "gauss": "gausz", "hertz": "herc", "kirchhoff": "kirhof",
    "lenz": "lenc", "lorentz": "lorenc", "biot": "bió", "savart": "szavár", "pascal": "paszkál",
    "fourier": "furié", "laplace": "laplász", "euler": "ojler", "boltzmann": "bolcman", "planck": "plank",
    "schrödinger": "sródinger", "heisenberg": "hájzenberg", "einstein": "ájnstájn", "bohr": "bór",
    "dirac": "dirak", "hamilton": "hemilton", "bernoulli": "bernulli", "thevenin": "tevenen", "norton": "norton",
    "matthew": "meszjú", "turing": "tyúring", "neumann": "nojmann", "shannon": "senon", "dijkstra": "dejkszta",
}

# a tő után álló magyar toldalék kezdete (kötőjel nélkül csak ezekkel illesztünk, hogy pl. a "bugyi" ne
# "bag"+"yi" legyen); kötőjel után bármi jöhet
_SUFFIX = (r"(?:ol|el|öl|al|ok|ek|ök|ot|et|öt|at|os|es|ös|ja|je|ba|be|ban|ben|ból|ből|ra|re|ról|ről|hoz|hez|"
           r"höz|nak|nek|val|vel|tól|től|ig|kor|ként|on|en|ön|t|k|s)[a-záéíóöőúüű]*")
HU = "a-záéíóöőúüű"
_SHORT_SUFFIX = re.compile(r"(?:ot|et|öt|ok|ek|ök|ja|je|ban|ben|ba|be|ból|ből|ra|re|hoz|hez|nak|nek|val|vel|"
                           r"os|es|ös|t|k|ol|olni|olja|olt|olás)")
_ACR = re.compile(r"(?<![\w-])([A-ZÁÉÍÓÖŐÚÜŰ]{2,6})(\d{1,3})?(?:-([" + HU + r"]+))?(?![\w])")
_LOWER_ACR = re.compile(r"(?<![\w-])(" + "|".join(sorted(LOWER_ACRONYMS, key=len, reverse=True))
                        + r")(?:-([" + HU + r"]+))?(?![\w])")
_NO_VOWEL = re.compile(r"(?<![\w-])([bcdfghjklmnpqrstvwxz]{2,5})(?![\w-])")
_ROMAN = re.compile(r"M{0,3}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})")
# angolra utaló betűkapcsolatok (a "th" és az "ea" kimarad: magyar szóhatáron gyakori: "mintha", "leadott")
_FOREIGN_HINT = re.compile(r"w|q|oo|ee|ou|ck|[^gylnt]y$")


def spell(acronym: str) -> str:
    """Betűszó magyar betűnevekkel, a magyar kettős betűket egyben ("SZTK" -> "eszték á")."""
    out, i = [], 0
    while i < len(acronym):
        two = acronym[i:i + 2]
        if two in DIGRAPHS:
            out.append(DIGRAPHS[two])
            i += 2
        else:
            out.append(LETTERS.get(acronym[i], acronym[i].lower()))
            i += 1
    return "".join(out)


def _english_re() -> re.Pattern:
    keys = sorted(ENGLISH, key=len, reverse=True)
    alt = "|".join(re.escape(k).replace(r"\ ", r"\s+") for k in keys)
    return re.compile(r"(?<![\w])(" + alt + r")(?:(-[" + HU + r"]+)|(" + _SUFFIX + r"))?(?![\w])", re.IGNORECASE)


_EN = _english_re()


def _shouting(text: str) -> bool:
    """Csupa nagybetűs cím: a hosszú nagybetűs szavak nem betűszavak, ilyenkor csak az ismerteket bontjuk."""
    return any(len(w) >= 7 and w not in ACRONYM_WORDS for w in re.findall(r"\b[A-ZÁÉÍÓÖŐÚÜŰ]{7,}\b", text))


def apply(text: str, protect, units: dict[str, str] | None = None) -> str:
    """Idegen szavak cseréje; a `protect` a kimondott alakot helyőrzővel védi a későbbi lépésektől.

    A szám nélkül álló mértékegység-jel (km/óra) a `units` szerinti nevet kapja, nem betűzést.
    """
    units = units or {}
    shouting = _shouting(text)

    def acr(m: re.Match) -> str:
        word, digits, suf = m.group(1), m.group(2), m.group(3) or ""
        if word in ACRONYM_WORDS:
            spoken = ACRONYM_WORDS[word]
        elif word.lower() in ENGLISH:
            spoken = ENGLISH[word.lower()]
        elif shouting:
            return m.group(0)
        elif _ROMAN.fullmatch(word) and text[m.end():m.end() + 1] == ".":
            return m.group(0)  # római szám ponttal: a sorszám-lépés kezeli
        else:
            spoken = spell(word)
        return protect(spoken + suf) + (f" {digits}" if digits else "")

    def lower_acr(m: re.Match) -> str:
        w = m.group(1)
        return protect(ACRONYM_WORDS.get(w.upper(), spell(w.upper())) + (m.group(2) or ""))

    def english(m: re.Match) -> str:
        key = re.sub(r"\s+", " ", m.group(1).lower())
        suf = (m.group(2) or "")[1:] or (m.group(3) or "")
        if m.group(3) and len(key) < 4 and not _SHORT_SUFFIX.fullmatch(m.group(3)):
            return m.group(0)  # rövid tő kötőjel nélkül: "catalog" ne legyen "ket"+"alog"
        if suf.lower() in ENGLISH:  # kötőjeles angol összetétel: Hewlett-Packard
            suf = " " + ENGLISH[suf.lower()]
        spoken = ENGLISH[key]
        if m.group(1)[:1].isupper():
            spoken = spoken[:1].upper() + spoken[1:]
        return protect(spoken + suf)

    text = _EN.sub(english, text)
    text = _ACR.sub(acr, text)
    text = _LOWER_ACR.sub(lower_acr, text)
    # magánhangzó nélküli kisbetűs "szó": parancsnév vagy rövidítés (fsck, pwd), betűnként
    text = _NO_VOWEL.sub(lambda m: protect(units.get(m.group(1)) or spell(m.group(1).upper())), text)
    return text


def foreign_warnings(text: str) -> list[str]:
    """Angolnak látszó, a szótárban nem szereplő szavak (a kiejtési szótárba érdemes felvenni)."""
    seen: dict[str, None] = {}
    for w in re.findall(r"(?<![\w-])[^\W\d_]{3,}(?![\w-])", text):
        lw = w.lower()
        if not w.isascii() or not re.search(r"[aeiouy]", lw):
            continue  # a magánhangzó nélkülieket (fsck, pwd) az apply betűzi
        if lw in ENGLISH or w.upper() in ACRONYM_WORDS or w.isupper():
            continue
        if _FOREIGN_HINT.search(lw):
            seen.setdefault(w, None)
    return list(seen)
