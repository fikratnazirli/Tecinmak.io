# -*- coding: utf-8 -*-
"""
Bu betik tecinmak.com sitesindeki gorsel ve PDF dosyalarini indirip
"tecinmak_assets" adinda yerel bir klasore kaydeder.

KULLANIM:
1. Bu dosyayi (download_tecinmak_images.py) ve yanindaki
   tecinmak_urls.txt dosyasini AYNI klasore koyun
   (subpage.html / katalog.html ile ayni klasor olmasi onerilir,
    orn: C:\.vscode\tecinmak\).
2. Bilgisayarda Python kurulu olmali (python.org/downloads).
3. Komut satirinda (cmd/terminal) bu klasore girip su komutu calistirin:
       python download_tecinmak_images.py
4. Islem bitince "tecinmak_assets" adinda bir klasor olusacak,
   icinde 129 dosya (resim + pdf) olacak.
5. Ardindan Claude'a "indirdim, tecinmak_assets klasoru hazir" deyin --
   Claude butun http://tecinmak.com linklerini otomatik olarak
   "./tecinmak_assets/dosyaadi" seklinde degistirecek.
"""

import os
import urllib.request
import urllib.error
import time

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
URLS_FILE = os.path.join(SCRIPT_DIR, "tecinmak_urls.txt")
OUT_DIR = os.path.join(SCRIPT_DIR, "tecinmak_assets")

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/120.0 Safari/537.36",
    "Referer": "http://tecinmak.com/",
}


def main():
    if not os.path.isfile(URLS_FILE):
        print(f"HATA: {URLS_FILE} bulunamadi. Bu dosyayi ayni klasore koyun.")
        return

    os.makedirs(OUT_DIR, exist_ok=True)

    with open(URLS_FILE, "r", encoding="utf-8") as f:
        urls = [line.strip() for line in f if line.strip()]

    print(f"Toplam {len(urls)} dosya indirilecek...\n")

    ok, failed = 0, []
    for i, url in enumerate(urls, 1):
        filename = url.split("/")[-1]
        dest = os.path.join(OUT_DIR, filename)

        if os.path.isfile(dest):
            print(f"[{i}/{len(urls)}] Zaten var, atlaniyor: {filename}")
            ok += 1
            continue

        try:
            req = urllib.request.Request(url, headers=HEADERS)
            with urllib.request.urlopen(req, timeout=15) as resp:
                data = resp.read()
            with open(dest, "wb") as out:
                out.write(data)
            print(f"[{i}/{len(urls)}] OK: {filename} ({len(data)} bayt)")
            ok += 1
        except Exception as e:
            print(f"[{i}/{len(urls)}] HATA: {filename} -> {e}")
            failed.append(url)

        time.sleep(0.15)  # sunucuyu yormamak icin kucuk bekleme

    print(f"\nBitti. Basarili: {ok}/{len(urls)}")
    if failed:
        print(f"Basarisiz olan {len(failed)} dosya:")
        for u in failed:
            print("  -", u)
        with open(os.path.join(SCRIPT_DIR, "failed_downloads.txt"), "w", encoding="utf-8") as f:
            f.write("\n".join(failed))
        print("\nBu liste 'failed_downloads.txt' dosyasina da kaydedildi.")


if __name__ == "__main__":
    main()
