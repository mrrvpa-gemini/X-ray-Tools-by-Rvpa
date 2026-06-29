#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import warnings
warnings.filterwarnings("ignore")

import requests
import sys
import os
import time
import random
import re
import threading
from urllib.parse import urljoin
from concurrent.futures import ThreadPoolExecutor, as_completed
from colorama import init, Fore, Back, Style

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

init(autoreset=True)

# KONFIGURASI
THREADS = 150
TIMEOUT = 8
MAX_RETRIES = 2

USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 Version/17.1 Safari/605.1.15',
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/121.0',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 17_1 like Mac OS X) Version/17.1 Mobile/15E148 Safari/604.1',
    'Mozilla/5.0 (iPad; CPU OS 17_1 like Mac OS X) Version/17.1 Mobile/15E148 Safari/604.1',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/119.0.0.0 OPR/105.0.0.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0 Edg/120.0.0.0'
]

def banner():
    os.system('clear' if os.name == 'posix' else 'cls')
    print(Fore.BLACK + '''
┳┓┓┏┏┓┏┓          ┓┏┏┓┳┳┓┳┓┏┓┏┓
┣┫┃┃┃┃┣┫          ┣┫┃┃┃┃┃┃┃┫┣┫
┛┗┗┛┣┛┛┗          ┗┛┗┛┻┛┗┻┛┛┗┛┗
''' + Fore.MAGENTA + '''
┏┳┓┓┏┏┓  ┳┓┏┓┳┓┓┏┓  ┏┓┏┓┳┓┏┓┏┓
 ┃ ┣┫┣   ┃┃┣┫┣┫┃┫   ┃ ┣┫┃┃┣┫┣┫
 ┻ ┛┗┗┛  ┻┛┛┗┛┗┛┗┛  ┗┛┛┗┻┛┛┗┛┗
''' + Fore.RED + '''
┓ ┏┓┳┓┳┓          ┏┓┳┓┏┓┏┓┳┓┏┓
┃ ┃┃┣┫┃┃          ┃┃┣┫┣ ┃┃┃┃┣┫
┗┛┗┛┛┗┻┛          ┗┛┛┗┗┛┗┛┻┛┛┗
''' + Fore.CYAN + '''
╔══════════════════════════════════════════════╗
║  X-RAY WEB OVER POWER v8.0                   ║
║  MEGA 1000+ PARAMETER EDITION               ║
║  4 FILES x 1000+ PATHS = 4000+ TOTAL        ║
║  TERMINAL ONLY - NO FILES SAVED              ║
║  WARNINGS DISABLED - CLEAN OUTPUT            ║
╚══════════════════════════════════════════════╝
''' + Fore.RESET)
    print(Fore.CYAN + "="*60)
    print(Fore.YELLOW + "  X-RAY WEB OVER POWER v8.0")
    print(Fore.RED + "  MEGA 1000+ PARAMETER EDITION")
    print(Fore.GREEN + "  4000+ PAYLOADS READY")
    print(Fore.CYAN + "  RESULTS STREAMING TO TERMINAL")
    print(Fore.CYAN + "="*60 + "\n")

def get_headers():
    return {
        'User-Agent': random.choice(USER_AGENTS),
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.9,id;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'X-Forwarded-For': f'127.0.0.{random.randint(1,255)}',
        'X-Originating-IP': f'127.0.0.{random.randint(1,255)}',
        'X-Remote-IP': f'127.0.0.{random.randint(1,255)}',
        'X-Remote-Addr': f'127.0.0.{random.randint(1,255)}',
        'X-Client-IP': f'127.0.0.{random.randint(1,255)}',
        'X-Host': 'localhost',
        'X-Forwarded-Host': 'localhost',
        'Referer': random.choice(['https://google.com', 'https://bing.com']),
        'Cache-Control': 'no-cache',
        'Pragma': 'no-cache'
    }

def load_paths(filename):
    try:
        with open(filename, 'r') as f:
            return [line.strip() for line in f if line.strip()]
    except:
        return []

def check_url(base, path):
    url = urljoin(base, path)
    for _ in range(MAX_RETRIES):
        try:
            resp = requests.get(url, headers=get_headers(), timeout=TIMEOUT, verify=False, allow_redirects=True)
            status = resp.status_code
            if status in [200, 201, 301, 302, 303, 307, 308, 401, 403, 500]:
                size = len(resp.content)
                title = re.search(r'<title>(.*?)</title>', resp.text, re.I)
                title = title.group(1).strip()[:80] if title else 'No Title'
                server = resp.headers.get('Server', 'Unknown')
                return {
                    'url': url,
                    'status': status,
                    'size': size,
                    'title': title,
                    'server': server
                }
        except:
            time.sleep(0.3)
            continue
    return None

def main():
    banner()
    
    target = input(Fore.YELLOW + "[?] Enter web (contoh: https://example.com): " + Fore.RESET).strip()
    if not target:
        print(Fore.RED + "[-] URL required!" + Fore.RESET)
        sys.exit(1)
    if not target.startswith('http'):
        target = 'https://' + target
    if not target.endswith('/'):
        target += '/'
    
    print(Fore.CYAN + f"\n[+] Target: {target}")
    print(Fore.CYAN + "[+] Loading 1000+ paths per file...\n" + Fore.RESET)
    
    all_paths = []
    files = [
        'admin_paths.txt',
        'server_paths.txt',
        'auth_paths.txt',
        'api_paths.txt'
    ]
    
    total_loaded = 0
    for f in files:
        paths = load_paths(f)
        print(Fore.CYAN + f"[+] Loaded {len(paths)} paths from {f}" + Fore.RESET)
        all_paths.extend(paths)
        total_loaded += len(paths)
    
    all_paths = list(dict.fromkeys(all_paths))
    
    print(Fore.GREEN + f"\n[+] Total unique paths: {len(all_paths)}")
    print(Fore.CYAN + "[+] Threads: " + str(THREADS))
    print(Fore.CYAN + "[+] Starting scan...\n" + Fore.RESET)
    
    found = 0
    total = len(all_paths)
    
    with ThreadPoolExecutor(max_workers=THREADS) as executor:
        futures = {executor.submit(check_url, target, path): path for path in all_paths}
        done = 0
        for future in as_completed(futures):
            done += 1
            result = future.result()
            
            if done % 10 == 0 or done == total:
                sys.stdout.write(f'\r{Fore.YELLOW}[*] Progress: {done}/{total} ({done*100//total}%) | Found: {found}{Fore.RESET}')
                sys.stdout.flush()
            
            if result and result['status'] in [200, 201, 301, 302, 401, 403]:
                found += 1
                if result['status'] == 200:
                    color = Fore.GREEN
                elif result['status'] in [301, 302]:
                    color = Fore.YELLOW
                else:
                    color = Fore.RED
                
                print(f'\n{color}[+] {result["url"]} [{result["status"]}]')
                print(f'    Title: {result["title"]}')
                print(f'    Server: {result["server"]}')
                print(f'    Size: {result["size"]} bytes{Fore.RESET}')
    
    print(Fore.CYAN + f"\n\n[+] Scan completed! Total found: {found}" + Fore.RESET)
    print(Fore.GREEN + "[+] All results shown above in terminal!" + Fore.RESET)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print(Fore.RED + "\n[-] Interrupted by user!" + Fore.RESET)
        sys.exit(0)
