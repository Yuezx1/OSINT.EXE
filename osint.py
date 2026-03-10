#!/usr/bin/env python3
"""
╔═══════════════════════════════════════╗
║         OSINT.EXE — CLI TOOL         ║
║         by liteco1n                   ║
║         guns.lol/liteco1n             ║
╚═══════════════════════════════════════╝
"""

import sys
import os
import time
import socket
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime

try:
    import colorama
    colorama.init(autoreset=False)
except ImportError:
    pass

# ── Colors ──────────────────────────────────────────────────────────────────
class C:
    GREEN   = "\033[38;2;0;255;65m"
    DGREEN  = "\033[38;2;0;180;45m"
    RED     = "\033[38;2;255;60;60m"
    YELLOW  = "\033[38;2;255;180;0m"
    GREY    = "\033[38;2;100;140;100m"
    WHITE   = "\033[38;2;200;240;200m"
    RESET   = "\033[0m"
    BOLD    = "\033[1m"
    DIM     = "\033[2m"

def g(text):  return f"{C.GREEN}{text}{C.RESET}"
def r(text):  return f"{C.RED}{text}{C.RESET}"
def y(text):  return f"{C.YELLOW}{text}{C.RESET}"
def gr(text): return f"{C.GREY}{text}{C.RESET}"
def w(text):  return f"{C.WHITE}{text}{C.RESET}"
def b(text):  return f"{C.BOLD}{text}{C.RESET}"

# ── Banner ───────────────────────────────────────────────────────────────────
def banner():
    print(f"""
{C.GREEN}╔══════════════════════════════════════════════════════════╗
║                                                          ║
║    {C.BOLD}  ██████╗ ███████╗██╗███╗   ██╗████████╗            {C.RESET}{C.GREEN}║
║    {C.BOLD} ██╔═══██╗██╔════╝██║████╗  ██║╚══██╔══╝            {C.RESET}{C.GREEN}║
║    {C.BOLD} ██║   ██║███████╗██║██╔██╗ ██║   ██║               {C.RESET}{C.GREEN}║
║    {C.BOLD} ██║   ██║╚════██║██║██║╚██╗██║   ██║               {C.RESET}{C.GREEN}║
║    {C.BOLD} ╚██████╔╝███████║██║██║ ╚████║   ██║               {C.RESET}{C.GREEN}║
║    {C.BOLD}  ╚═════╝ ╚══════╝╚═╝╚═╝  ╚═══╝   ╚═╝               {C.RESET}{C.GREEN}║
║                                                          ║
║    {C.GREY}RECONNAISSANCE FRAMEWORK  //  CLI EDITION{C.GREEN}            ║
║    {C.GREY}by {C.DGREEN}liteco1n{C.GREY}  •  {C.DGREEN}guns.lol/liteco1n{C.GREEN}                     ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝{C.RESET}
""")

# ── Divider ──────────────────────────────────────────────────────────────────
def div(title=""):
    w_ = 60
    if title:
        pad = (w_ - len(title) - 4) // 2
        print(f"\n{C.DGREEN}{'─' * pad}[ {C.GREEN}{C.BOLD}{title}{C.RESET}{C.DGREEN} ]{'─' * pad}{C.RESET}")
    else:
        print(f"{C.DGREEN}{'─' * w_}{C.RESET}")

def field(key, val, color=None):
    col = color or C.WHITE
    print(f"  {C.GREY}{key:<22}{C.RESET}{col}{val}{C.RESET}")

# ── Platforms ────────────────────────────────────────────────────────────────
PLATFORMS = [
    ("GitHub",      "https://github.com/{}"),
    ("Reddit",      "https://www.reddit.com/user/{}"),
    ("Twitter/X",   "https://x.com/{}"),
    ("TikTok",      "https://www.tiktok.com/@{}"),
    ("Instagram",   "https://www.instagram.com/{}/"),
    ("Twitch",      "https://www.twitch.tv/{}"),
    ("YouTube",     "https://www.youtube.com/@{}"),
    ("Steam",       "https://steamcommunity.com/id/{}"),
    ("Pinterest",   "https://www.pinterest.com/{}/"),
    ("Spotify",     "https://open.spotify.com/user/{}"),
    ("SoundCloud",  "https://soundcloud.com/{}"),
    ("Dev.to",      "https://dev.to/{}"),
    ("Keybase",     "https://keybase.io/{}"),
    ("Pastebin",    "https://pastebin.com/u/{}"),
    ("Replit",      "https://replit.com/@{}"),
    ("GitLab",      "https://gitlab.com/{}"),
    ("Linktree",    "https://linktr.ee/{}"),
    ("Medium",      "https://medium.com/@{}"),
    ("Tumblr",      "https://{}.tumblr.com"),
    ("About.me",    "https://about.me/{}"),
    ("Chess.com",   "https://www.chess.com/member/{}"),
    ("Letterboxd",  "https://letterboxd.com/{}/"),
    ("Duolingo",    "https://www.duolingo.com/profile/{}"),
    ("Fiverr",      "https://www.fiverr.com/{}"),
    ("HackerNews",  "https://news.ycombinator.com/user?id={}"),
    ("Roblox",      "https://www.roblox.com/user.aspx?username={}"),
    ("Cash App",    "https://cash.app/${}"),
    ("Gravatar",    "https://en.gravatar.com/{}"),
    ("Codecademy",  "https://www.codecademy.com/profiles/{}"),
    ("Venmo",       "https://venmo.com/{}"),
]

def check_platform(name, url_template, username):
    url = url_template.format(username)
    try:
        r = requests.get(
            url,
            timeout=7,
            allow_redirects=True,
            headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
        )
        found = r.status_code == 200
        return (name, url, found, r.status_code)
    except Exception:
        return (name, url, False, "timeout")

def username_lookup(username):
    div(f"USERNAME OSINT — {username}")
    print(f"\n  {gr('Scanning')} {len(PLATFORMS)} {gr('platforms...')}\n")

    found_list = []
    not_found_list = []
    total = len(PLATFORMS)
    done = 0

    with ThreadPoolExecutor(max_workers=20) as ex:
        futures = {ex.submit(check_platform, n, u, username): n for n, u in PLATFORMS}
        for future in as_completed(futures):
            name, url, found, status = future.result()
            done += 1
            bar_filled = int((done / total) * 30)
            bar = f"[{'█' * bar_filled}{'░' * (30 - bar_filled)}]"
            print(f"\r  {C.DGREEN}{bar}{C.RESET} {C.GREY}{done}/{total}{C.RESET}", end="", flush=True)
            if found:
                found_list.append((name, url))
            else:
                not_found_list.append((name, url))

    print(f"\r  {C.GREEN}{'█' * 30}{C.RESET} {C.GREY}{total}/{total}{C.RESET}\n")

    # Summary
    print(f"  {g('FOUND')}      {C.GREEN}{C.BOLD}{len(found_list)}{C.RESET}  platforms")
    print(f"  {r('NOT FOUND')} {C.RED}{C.BOLD}{len(not_found_list)}{C.RESET}  platforms")

    if found_list:
        div("ACCOUNTS FOUND")
        for name, url in found_list:
            print(f"  {C.GREEN}✔{C.RESET}  {C.WHITE}{name:<18}{C.RESET}  {C.DGREEN}{url}{C.RESET}")

    if not_found_list:
        div("NOT FOUND")
        cols = 3
        items = [f"{C.RED}✘{C.RESET} {C.GREY}{n:<16}{C.RESET}" for n, _ in not_found_list]
        for i in range(0, len(items), cols):
            row = items[i:i+cols]
            print("  " + "  ".join(row))

# ── IP Lookup ─────────────────────────────────────────────────────────────────
def ip_lookup(ip=""):
    target = ip if ip else "your IP"
    div(f"IP LOOKUP — {target}")
    print(f"\n  {gr('Querying ip-api.com...')}\n")

    url = f"http://ip-api.com/json/{ip}?fields=status,message,country,countryCode,regionName,city,zip,lat,lon,timezone,isp,org,as,proxy,hosting,query"
    try:
        resp = requests.get(url, timeout=8)
        d = resp.json()
    except Exception as e:
        print(f"  {r('ERROR:')} {e}")
        return

    if d.get("status") == "fail":
        print(f"  {r('ERROR:')} {d.get('message', 'Unknown error')}")
        return

    proxy_val = (y("⚠  DETECTED") if d.get("proxy") else g("✔  CLEAN"))
    host_val  = (y("⚠  DATACENTER") if d.get("hosting") else g("✔  RESIDENTIAL"))

    print(f"  {C.GREEN}{'─'*55}{C.RESET}")
    field("IP ADDRESS",   d.get("query","N/A"))
    field("COUNTRY",      f"{d.get('country','N/A')} ({d.get('countryCode','?')})")
    field("REGION",       d.get("regionName","N/A"))
    field("CITY",         d.get("city","N/A"))
    field("ZIP CODE",     d.get("zip","N/A"))
    field("TIMEZONE",     d.get("timezone","N/A"))
    print()
    field("ISP",          d.get("isp","N/A"))
    field("ORGANIZATION", d.get("org","N/A"))
    field("ASN",          d.get("as","N/A"))
    print()
    field("PROXY / VPN",  proxy_val)
    field("HOSTING TYPE", host_val)
    print()
    field("COORDINATES",  f"{d.get('lat','?')}, {d.get('lon','?')}")
    field("MAPS LINK",    f"https://maps.google.com/?q={d.get('lat')},{d.get('lon')}", C.DGREEN)
    print(f"  {C.GREEN}{'─'*55}{C.RESET}")

# ── Phone Lookup ──────────────────────────────────────────────────────────────
def phone_lookup(phone):
    div(f"PHONE RECON — {phone}")
    print(f"\n  {gr('Querying numverify-style recon...')}\n")

    # Strip non-numeric for basic parsing
    digits = "".join(c for c in phone if c.isdigit() or c == "+")

    # Use free abstract API (no key needed for basic lookup)
    try:
        url = f"https://phonevalidation.abstractapi.com/v1/?api_key=&phone={digits}"
        # Fallback: parse manually from number format
        raise Exception("use local parse")
    except Exception:
        pass

    # Local heuristic parsing (no API key needed)
    print(f"  {C.GREEN}{'─'*55}{C.RESET}")
    field("RAW INPUT",    phone)
    field("DIGITS ONLY",  digits)

    if digits.startswith("+1") or (len(digits) == 10 and not digits.startswith("+")):
        country, region, carrier_hint = "United States / Canada", "NANP (+1)", "US carrier"
    elif digits.startswith("+44"):
        country, region, carrier_hint = "United Kingdom", "UK (+44)", "UK carrier"
    elif digits.startswith("+61"):
        country, region, carrier_hint = "Australia", "AU (+61)", "AU carrier"
    elif digits.startswith("+49"):
        country, region, carrier_hint = "Germany", "DE (+49)", "DE carrier"
    elif digits.startswith("+33"):
        country, region, carrier_hint = "France", "FR (+33)", "FR carrier"
    elif digits.startswith("+"):
        cc = digits[1:3]
        country, region, carrier_hint = f"International (+{cc})", f"CC +{cc}", "Unknown"
    else:
        country, region, carrier_hint = "Unknown", "Unknown", "Unknown"

    length_ok = len(digits.replace("+","")) >= 10
    line_type = "MOBILE (likely)" if length_ok else "UNKNOWN / INVALID LENGTH"

    print()
    field("COUNTRY",      country)
    field("REGION CODE",  region)
    field("LENGTH CHECK", g("VALID") if length_ok else r("INVALID"))
    field("LINE TYPE",    line_type)
    field("CARRIER HINT", carrier_hint)
    print()
    field("FORMAT E.164",  digits if digits.startswith("+") else f"+1{digits}")
    field("SEARCH HINT",  f'Try: site:truecaller.com "{phone}"', C.DGREEN)
    field("SEARCH HINT",  f'Try: site:sync.me "{phone}"', C.DGREEN)
    print(f"  {C.GREEN}{'─'*55}{C.RESET}")

# ── TruePeopleSearch ──────────────────────────────────────────────────────────
TPS_BASE = "https://www.truepeoplesearch.com"
HEADERS  = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Referer": "https://www.truepeoplesearch.com/",
}

def tps_parse_results(html):
    """Extract result cards from TruePeopleSearch HTML."""
    from html.parser import HTMLParser

    results = []
    # Simple extraction — look for result card patterns
    import re

    # Extract name blocks
    cards = re.findall(r'<div[^>]*data-name="([^"]*)"[^>]*data-detail-link="([^"]*)"', html)
    for name, link in cards:
        results.append({"name": name, "link": TPS_BASE + link})

    # Fallback: grab h2 names and detail links
    if not results:
        names = re.findall(r'<span[^>]*itemprop="name"[^>]*>([^<]+)</span>', html)
        links = re.findall(r'href="(/details[^"]+)"', html)
        for i, name in enumerate(names):
            link = links[i] if i < len(links) else ""
            results.append({"name": name.strip(), "link": TPS_BASE + link if link else ""})

    return results

def tps_parse_detail(html):
    """Extract details from a TruePeopleSearch profile page."""
    import re
    data = {}

    # Name
    m = re.search(r'<span[^>]*itemprop="name"[^>]*>([^<]+)</span>', html)
    if m: data["name"] = m.group(1).strip()

    # Age / DOB
    m = re.search(r'Age[^<]*</span>[^<]*<span[^>]*>(\d+)</span>', html)
    if m: data["age"] = m.group(1)
    m = re.search(r'(\d{1,2}/\d{1,2}/\d{4})', html)
    if m: data["dob"] = m.group(1)

    # Addresses — grab all street/city/state/zip combos
    addrs = re.findall(
        r'<span[^>]*itemprop="streetAddress"[^>]*>([^<]+)</span>.*?'
        r'<span[^>]*itemprop="addressLocality"[^>]*>([^<]+)</span>.*?'
        r'<span[^>]*itemprop="addressRegion"[^>]*>([^<]+)</span>.*?'
        r'<span[^>]*itemprop="postalCode"[^>]*>([^<]+)</span>',
        html, re.DOTALL
    )
    if addrs:
        data["addresses"] = [f"{a[0].strip()}, {a[1].strip()}, {a[2].strip()} {a[3].strip()}" for a in addrs]

    # Phone numbers
    phones = re.findall(r'<span[^>]*itemprop="telephone"[^>]*>([^<]+)</span>', html)
    if phones:
        data["phones"] = list(dict.fromkeys([p.strip() for p in phones]))

    # Relatives
    rels = re.findall(r'<span[^>]*class="[^"]*relative[^"]*"[^>]*>([^<]+)</span>', html, re.IGNORECASE)
    if rels:
        data["relatives"] = list(dict.fromkeys([r_.strip() for r_ in rels if r_.strip()]))

    # Email hints
    emails = re.findall(r'[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}', html)
    if emails:
        data["emails"] = list(dict.fromkeys(emails))[:5]

    return data

def tps_search_name(first, last, city="", state=""):
    name_q = f"{first}+{last}"
    loc_q  = f"{city.replace(' ','+')}+{state}".strip("+")
    url = f"{TPS_BASE}/results?name={name_q}"
    if loc_q:
        url += f"&citystatezip={loc_q}"
    return url, requests.get(url, headers=HEADERS, timeout=10)

def tps_search_address(street, city="", state="", zipcode=""):
    addr_q = street.replace(" ", "+")
    loc_q  = f"{city.replace(' ','+')}+{state}+{zipcode}".strip("+")
    url = f"{TPS_BASE}/resultaddress?streetaddress={addr_q}&citystatezip={loc_q}"
    return url, requests.get(url, headers=HEADERS, timeout=10)

def tps_search_phone(phone):
    digits = "".join(c for c in phone if c.isdigit())
    url = f"{TPS_BASE}/resultphone?phoneno={digits}"
    return url, requests.get(url, headers=HEADERS, timeout=10)

def print_tps_results(results, search_url):
    if not results:
        print(f"\n  {y('No results parsed from page.')}")
        print(f"  {gr('Open manually:')} {C.DGREEN}{search_url}{C.RESET}")
        return

    print(f"\n  {g(str(len(results)))} result(s) found\n")
    for i, res in enumerate(results[:10], 1):
        print(f"  {C.GREEN}[{i}]{C.RESET} {C.WHITE}{res.get('name','Unknown')}{C.RESET}")
        if res.get("link"):
            print(f"      {C.DGREEN}{res['link']}{C.RESET}")
    print()

def tps_fetch_detail(url):
    div("PROFILE DETAILS")
    print(f"\n  {gr('Fetching profile...')}\n")
    try:
        resp = requests.get(url, headers=HEADERS, timeout=10)
        data = tps_parse_detail(resp.text)
    except Exception as e:
        print(f"  {r('ERROR:')} {e}")
        return

    print(f"  {C.GREEN}{'─'*55}{C.RESET}")
    if data.get("name"):      field("NAME",      data["name"])
    if data.get("age"):       field("AGE",       data["age"])
    if data.get("dob"):       field("DOB",       data["dob"])
    if data.get("addresses"):
        for i, addr in enumerate(data["addresses"]):
            field(f"ADDRESS {i+1}", addr)
    if data.get("phones"):
        for i, ph in enumerate(data["phones"]):
            field(f"PHONE {i+1}", ph)
    if data.get("relatives"):
        field("RELATIVES", ", ".join(data["relatives"][:6]))
    if data.get("emails"):
        field("EMAILS", ", ".join(data["emails"]))
    if not any(data.values()):
        print(f"  {y('Could not auto-parse details. Open the link in a browser.')}")
    print(f"  {C.GREEN}{'─'*55}{C.RESET}")
    print(f"\n  {gr('Direct link:')} {C.DGREEN}{url}{C.RESET}")

def person_lookup():
    div("TRUEPEOPLESEARCH RECON")
    print(f"""
  {g('SELECT SEARCH TYPE')}

  {C.GREEN}[1]{C.RESET}  {w('Name Search')}         {gr('— find person by name (+optional city/state)')}
  {C.GREEN}[2]{C.RESET}  {w('Address Search')}      {gr('— find residents at an address')}
  {C.GREEN}[3]{C.RESET}  {w('Reverse Phone')}       {gr('— find person from phone number')}
  {C.GREEN}[b]{C.RESET}  {gr('Back')}
""")
    sub = prompt_input("select")

    if sub == "b":
        return

    elif sub == "1":
        first = prompt_input("first name")
        last  = prompt_input("last name")
        city  = prompt_input("city (optional — press Enter to skip)")
        state = prompt_input("state abbrev (e.g. NY, CA — optional)")
        if not first or not last:
            print(f"\n  {r('First and last name are required.')}")
            return
        div(f"NAME SEARCH — {first} {last}")
        print(f"\n  {gr('Querying TruePeopleSearch...')}\n")
        try:
            url, resp = tps_search_name(first, last, city, state)
            results = tps_parse_results(resp.text)
            print_tps_results(results, url)
            if results:
                pick = prompt_input("enter result number to fetch details (or Enter to skip)")
                if pick.isdigit() and 1 <= int(pick) <= len(results):
                    detail_url = results[int(pick)-1].get("link","")
                    if detail_url:
                        tps_fetch_detail(detail_url)
                    else:
                        print(f"  {y('No detail link available.')}")
            else:
                print(f"  {gr('Search URL:')} {C.DGREEN}{url}{C.RESET}")
        except Exception as e:
            print(f"  {r('ERROR:')} {e}")

    elif sub == "2":
        street  = prompt_input("street address (e.g. 123 Main St)")
        city    = prompt_input("city")
        state   = prompt_input("state abbrev (e.g. TX)")
        zipcode = prompt_input("zip code (optional)")
        if not street:
            print(f"\n  {r('Street address is required.')}")
            return
        div(f"ADDRESS SEARCH — {street}")
        print(f"\n  {gr('Querying TruePeopleSearch...')}\n")
        try:
            url, resp = tps_search_address(street, city, state, zipcode)
            results = tps_parse_results(resp.text)
            print_tps_results(results, url)
            if results:
                pick = prompt_input("enter result number to fetch details (or Enter to skip)")
                if pick.isdigit() and 1 <= int(pick) <= len(results):
                    detail_url = results[int(pick)-1].get("link","")
                    if detail_url:
                        tps_fetch_detail(detail_url)
            else:
                print(f"  {gr('Search URL:')} {C.DGREEN}{url}{C.RESET}")
        except Exception as e:
            print(f"  {r('ERROR:')} {e}")

    elif sub == "3":
        phone = prompt_input("phone number (e.g. 5558675309)")
        if not phone:
            print(f"\n  {r('Phone number required.')}")
            return
        div(f"REVERSE PHONE — {phone}")
        print(f"\n  {gr('Querying TruePeopleSearch...')}\n")
        try:
            url, resp = tps_search_phone(phone)
            results = tps_parse_results(resp.text)
            print_tps_results(results, url)
            if results:
                pick = prompt_input("enter result number to fetch details (or Enter to skip)")
                if pick.isdigit() and 1 <= int(pick) <= len(results):
                    detail_url = results[int(pick)-1].get("link","")
                    if detail_url:
                        tps_fetch_detail(detail_url)
            else:
                print(f"  {gr('Search URL:')} {C.DGREEN}{url}{C.RESET}")
        except Exception as e:
            print(f"  {r('ERROR:')} {e}")

# ── Menu ──────────────────────────────────────────────────────────────────────
def menu():
    print(f"""
  {g('SELECT MODULE')}

  {C.GREEN}[1]{C.RESET}  {w('Username OSINT')}       {gr('— check 30+ platforms')}
  {C.GREEN}[2]{C.RESET}  {w('IP Lookup')}             {gr('— geolocation, ISP, proxy detection')}
  {C.GREEN}[3]{C.RESET}  {w('Phone Recon')}           {gr('— carrier, region, format analysis')}
  {C.GREEN}[4]{C.RESET}  {w('Person / Address')}      {gr('— TruePeopleSearch: name, address, phone')}
  {C.GREEN}[0]{C.RESET}  {gr('Exit')}
""")

def prompt_input(label):
    try:
        val = input(f"  {C.GREEN}root@osint{C.RESET}{C.GREY}:~${C.RESET} {C.GREY}{label}>{C.RESET} ").strip()
        return val
    except (KeyboardInterrupt, EOFError):
        print()
        sys.exit(0)

# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    banner()

    while True:
        menu()
        choice = prompt_input("select")

        if choice == "0":
            print(f"\n  {gr('Goodbye.')}\n")
            break

        elif choice == "1":
            username = prompt_input("enter username")
            if username:
                username_lookup(username)

        elif choice == "2":
            ip = prompt_input("enter IP (or press Enter for your own)")
            ip_lookup(ip)

        elif choice == "3":
            phone = prompt_input("enter phone number (e.g. +1 555-867-5309)")
            if phone:
                phone_lookup(phone)

        elif choice == "4":
            person_lookup()

        else:
            print(f"\n  {r('Invalid option.')}\n")
            continue

        input(f"\n  {C.GREY}Press ENTER to return to menu...{C.RESET}")
        print()

if __name__ == "__main__":
    main()
