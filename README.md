# OSINT.EXE
# OSINT.EXE — CLI Reconnaissance Framework

```
╔══════════════════════════════════════════════════════════╗
║                                                          ║
║      ██████╗ ███████╗██╗███╗   ██╗████████╗             ║
║     ██╔═══██╗██╔════╝██║████╗  ██║╚══██╔══╝             ║
║     ██║   ██║███████╗██║██╔██╗ ██║   ██║                ║
║     ██║   ██║╚════██║██║██║╚██╗██║   ██║                ║
║     ╚██████╔╝███████║██║██║ ╚████║   ██║                ║
║      ╚═════╝ ╚══════╝╚═╝╚═╝  ╚═══╝   ╚═╝                ║
║                                                          ║
║     RECONNAISSANCE FRAMEWORK  //  CLI EDITION            ║
║     by liteco1n  •  guns.lol/liteco1n                    ║
╚══════════════════════════════════════════════════════════╝
```

> A terminal-based OSINT toolkit for reconnaissance and information gathering.  
> Built for educational and ethical research purposes only.

---

## Features

| Module | Description |
|--------|-------------|
| `[1] Username OSINT` | Check 30+ platforms for a username simultaneously |
| `[2] IP Lookup` | Real geolocation, ISP, ASN, proxy/VPN detection via ip-api.com |
| `[3] Phone Recon` | Format analysis, carrier detection, country identification |
| `[4] Person / Address` | Name → address, address → person, reverse phone via TruePeopleSearch |

---

## Installation

**Requirements:** Python 3.8+

```bash
# Clone the repo
git clone https://github.com/liteco1n/osint.exe.git
cd osint.exe

# Install dependencies
pip install -r requirements.txt

# Run
python3 osint.py
```

**Windows users:** Use Command Prompt or Windows Terminal (not PowerShell ISE).  
Colors require `colorama` which is included in `requirements.txt`.

---

## Usage

```
python3 osint.py
```

### Username OSINT
Checks 30+ platforms including GitHub, Reddit, Twitter/X, TikTok, Instagram, Twitch, Steam, Spotify, and more. Found accounts are displayed with clickable URLs.

```
root@osint:~$ enter username> johndoe

  [████████████████████████████████] 30/30

  FOUND       8  platforms
  NOT FOUND  22  platforms

── ACCOUNTS FOUND ────────────────────────
  ✔  GitHub              https://github.com/johndoe
  ✔  Reddit              https://www.reddit.com/user/johndoe
  ...
```

### IP Lookup
Real data from `ip-api.com`. Leave blank to look up your own IP.

```
root@osint:~$ enter IP> 8.8.8.8

  IP ADDRESS            8.8.8.8
  COUNTRY               United States (US)
  CITY                  Mountain View
  ISP                   Google LLC
  PROXY / VPN           ✔  CLEAN
  COORDINATES           37.386, -122.0838
```

### Person / Address (TruePeopleSearch)

Three sub-modes:
- **Name Search** — `First Last` + optional city/state
- **Address Search** — street + city/state/zip
- **Reverse Phone** — phone number → person

Results are scraped live. Pick a result number to pull full profile details (addresses, phones, relatives).

---

## Platforms Checked (Username Module)

GitHub • Reddit • Twitter/X • TikTok • Instagram • Twitch • YouTube • Steam • Pinterest • Spotify • SoundCloud • Dev.to • Keybase • Pastebin • Replit • GitLab • Linktree • Medium • Tumblr • About.me • Chess.com • Letterboxd • Duolingo • Fiverr • HackerNews • Roblox • Cash App • Gravatar • Codecademy • Venmo

---

## Dependencies

```
requests
colorama
```

---

## Disclaimer

> This tool is intended for **educational and ethical OSINT research only**.  
> Only use it on yourself or with explicit permission.  
> The author is not responsible for any misuse of this tool.  
> All data sourced from publicly available information.

---

## Author

**liteco1n** — [guns.lol/liteco1n](https://guns.lol/liteco1n)
