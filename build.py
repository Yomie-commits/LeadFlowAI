#!/usr/bin/env python3
"""
LeadFlow AI static site generator (a product by Naomi Mwangi).

Run after changing page copy, header or footer:   python3 build.py
Email, WhatsApp, booking link and analytics live in assets/js/config.js (no rebuild needed).
"""
import json, os, re, datetime

SITE_URL = "https://yomie-commits.github.io/LeadFlowAI"
PARENT_URL = "https://yomie-commits.github.io/Yomie-Verse/"
WHATSAPP = "254792002230"
WHATSAPP_DISPLAY = "+254 792 002 230"
LINKEDIN = "https://www.linkedin.com/in/naomi-njeri-m/"
ASSET_VERSION = "1"
OUT = os.path.dirname(os.path.abspath(__file__))

ICONS = {
  "arrow": '<path d="M5 12h14M13 6l6 6-6 6"/>',
  "check": '<path d="M5 12.5l4.5 4.5L19 7.5"/>',
  "mail": '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 7l9 6 9-6"/>',
  "bot": '<rect x="4" y="8" width="16" height="12" rx="3"/><path d="M12 8V4M8 4h8"/><circle cx="9" cy="14" r="1.2"/><circle cx="15" cy="14" r="1.2"/>',
  "users": '<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87M16 3.13a4 4 0 0 1 0 7.75"/>',
  "cog": '<circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.7 1.7 0 0 0 .3 1.8l.1.1a2 2 0 1 1-2.8 2.8l-.1-.1a1.7 1.7 0 0 0-1.8-.3 1.7 1.7 0 0 0-1 1.5V21a2 2 0 1 1-4 0v-.1a1.7 1.7 0 0 0-1.1-1.5 1.7 1.7 0 0 0-1.8.3l-.1.1a2 2 0 1 1-2.8-2.8l.1-.1a1.7 1.7 0 0 0 .3-1.8 1.7 1.7 0 0 0-1.5-1H3a2 2 0 1 1 0-4h.1a1.7 1.7 0 0 0 1.5-1.1 1.7 1.7 0 0 0-.3-1.8l-.1-.1a2 2 0 1 1 2.8-2.8l.1.1a1.7 1.7 0 0 0 1.8.3H9a1.7 1.7 0 0 0 1-1.5V3a2 2 0 1 1 4 0v.1a1.7 1.7 0 0 0 1 1.5 1.7 1.7 0 0 0 1.8-.3l.1-.1a2 2 0 1 1 2.8 2.8l-.1.1a1.7 1.7 0 0 0-.3 1.8V9a1.7 1.7 0 0 0 1.5 1H21a2 2 0 1 1 0 4h-.1a1.7 1.7 0 0 0-1.5 1z"/>',
  "cal": '<rect x="3" y="4" width="18" height="18" rx="2"/><path d="M16 2v4M8 2v4M3 10h18"/>',
  "puzzle": '<path d="M19.4 13.5a2.5 2.5 0 1 0 0-3H18V7a1 1 0 0 0-1-1h-3.5V4.6a2.5 2.5 0 1 0-3 0V6H7a1 1 0 0 0-1 1v3.5h1.4a2.5 2.5 0 1 1 0 3H6V17a1 1 0 0 0 1 1h3.5v-1.4a2.5 2.5 0 1 1 3 0V18H17a1 1 0 0 0 1-1v-3.5z"/>',
  "sheet": '<rect x="3" y="3" width="18" height="18" rx="2"/><path d="M3 9h18M3 15h18M9 3v18"/>',
  "zap": '<path d="M13 2L3 14h9l-1 8 10-12h-9z"/>',
  "brain": '<path d="M9.5 2A2.5 2.5 0 0 0 7 4.5v.3A3 3 0 0 0 4.5 8a3 3 0 0 0-.5 5.4A3 3 0 0 0 7 18a2.5 2.5 0 0 0 5 .5V4.5A2.5 2.5 0 0 0 9.5 2zM14.5 2A2.5 2.5 0 0 1 17 4.5v.3A3 3 0 0 1 19.5 8a3 3 0 0 1 .5 5.4A3 3 0 0 1 17 18a2.5 2.5 0 0 1-5 .5"/>',
  "hand": '<path d="M18 11V6a2 2 0 0 0-4 0v5M14 10V4a2 2 0 0 0-4 0v6M10 10.5V6a2 2 0 0 0-4 0v8"/><path d="M18 8a2 2 0 1 1 4 0v6a8 8 0 0 1-8 8h-2c-2.8 0-4.5-.9-6-2.4l-3.6-3.6a2 2 0 0 1 2.8-2.8L7 15"/>',
  "clock": '<circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/>',
  "shield": '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="M9 12l2 2 4-4"/>',
  "eye": '<path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8S1 12 1 12z"/><circle cx="12" cy="12" r="3"/>',
  "trend": '<path d="M23 6l-9.5 9.5-5-5L1 18"/><path d="M17 6h6v6"/>',
  "repeat": '<path d="M17 1l4 4-4 4"/><path d="M3 11V9a4 4 0 0 1 4-4h14M7 23l-4-4 4-4"/><path d="M21 13v2a4 4 0 0 1-4 4H3"/>',
  "inbox": '<path d="M22 12h-6l-2 3h-4l-2-3H2"/><path d="M5.45 5.11L2 12v6a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2v-6l-3.45-6.89A2 2 0 0 0 16.76 4H7.24a2 2 0 0 0-1.79 1.11z"/>',
  "list": '<path d="M8 6h13M8 12h13M8 18h13M3 6h.01M3 12h.01M3 18h.01"/>',
  "flag": '<path d="M4 22V4m0 0h13l-2 4 2 4H4"/>',
  "pen": '<path d="M12 20h9"/><path d="M16.5 3.5a2.1 2.1 0 0 1 3 3L7 19l-4 1 1-4z"/>',
  "bell": '<path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"/><path d="M13.7 21a2 2 0 0 1-3.4 0"/>',
  "sun": '<circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/>',
  "alert": '<circle cx="12" cy="12" r="10"/><path d="M12 8v4M12 16h.01"/>',
  "spark": '<path d="M12 3l1.9 5.8L20 10l-6.1 1.2L12 17l-1.9-5.8L4 10l6.1-1.2z"/><path d="M19 17l.7 2.3L22 20l-2.3.7L19 23l-.7-2.3L16 20l2.3-.7z"/>',
  "layers": '<path d="M12 2l10 5-10 5L2 7z"/><path d="M2 17l10 5 10-5M2 12l10 5 10-5"/>',
  "briefcase": '<rect x="2" y="7" width="20" height="14" rx="2"/><path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"/>',
  "megaphone": '<path d="M3 11l18-8v18L3 13z"/><path d="M11.6 16.8a3 3 0 1 1-5.8-1.6"/>',
  "home": '<path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><path d="M9 22V12h6v10"/>',
  "scale": '<path d="M12 3v18M5 21h14M3 7h18M6 7l-3 7a3 3 0 0 0 6 0zM18 7l-3 7a3 3 0 0 0 6 0z"/>',
  "heart": '<path d="M20.8 4.6a5.5 5.5 0 0 0-7.8 0L12 5.7l-1-1.1a5.5 5.5 0 0 0-7.8 7.8l1 1.1L12 21l7.8-7.5 1-1.1a5.5 5.5 0 0 0 0-7.8z"/>',
  "book": '<path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20V2H6.5A2.5 2.5 0 0 0 4 4.5z"/><path d="M4 19.5A2.5 2.5 0 0 0 6.5 22H20v-5"/>',
  "globe": '<circle cx="12" cy="12" r="10"/><path d="M2 12h20M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/>',
  "cart": '<circle cx="9" cy="21" r="1"/><circle cx="20" cy="21" r="1"/><path d="M1 1h4l2.7 13.4a2 2 0 0 0 2 1.6h9.7a2 2 0 0 0 2-1.6L23 6H6"/>',
  "search": '<circle cx="11" cy="11" r="8"/><path d="M21 21l-4.3-4.3"/>',
  "tool": '<path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.8-3.8a6 6 0 0 1-7.9 7.9l-6.9 6.9a2.1 2.1 0 0 1-3-3l6.9-6.9a6 6 0 0 1 7.9-7.9z"/>',
  "plug": '<path d="M12 22v-5M9 8V2M15 8V2M18 8v5a6 6 0 0 1-12 0V8z"/>',
  "test": '<path d="M9 2v6L4 18a2 2 0 0 0 1.8 3h12.4A2 2 0 0 0 20 18l-5-10V2M8 2h8M7 14h10"/>',
  "grad": '<path d="M22 10L12 5 2 10l10 5z"/><path d="M6 12v5c3 2 9 2 12 0v-5"/>',
  "life": '<circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="4"/><path d="M4.9 4.9l4.3 4.3M14.8 14.8l4.3 4.3M14.8 9.2l4.3-4.3M4.9 19.1l4.3-4.3"/>',
  "map": '<path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/>',
  "linkedin": '<path d="M16 8a6 6 0 0 1 6 6v7h-4v-7a2 2 0 0 0-4 0v7h-4v-7a6 6 0 0 1 6-6z"/><rect x="2" y="9" width="4" height="12"/><circle cx="4" cy="4" r="2"/>',
  "play": '<circle cx="12" cy="12" r="10"/><path d="M10 8l6 4-6 4z"/>',
  "menu": '<path d="M3 6h18M3 12h18M3 18h18"/>',
  "lang": '<path d="M5 8l6 6M4 14l6-6 2-3M2 5h12M7 2h1M22 22l-5-10-5 10M14 18h6"/>',
  "target": '<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="1"/>',
  "tag": '<path d="M20.6 13.4l-7.2 7.2a2 2 0 0 1-2.8 0L2 12V2h10l8.6 8.6a2 2 0 0 1 0 2.8z"/><circle cx="7" cy="7" r="1.5"/>',
  "chev": '<path d="M6 9l6 6 6-6"/>',
  "share": '<circle cx="18" cy="5" r="3"/><circle cx="6" cy="12" r="3"/><circle cx="18" cy="19" r="3"/><path d="M8.6 13.5l6.8 4M15.4 6.5l-6.8 4"/>',
  "funnel": '<path d="M3 4h18l-7 8v6l-4 2v-8z"/>',
  "inboxes": '<path d="M22 12h-6l-2 3h-4l-2-3H2"/><path d="M5.45 5.11L2 12v6a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2v-6l-3.45-6.89A2 2 0 0 0 16.76 4H7.24a2 2 0 0 0-1.79 1.11z"/>',
  "chart": '<path d="M3 3v18h18"/><path d="M7 15l4-4 3 3 5-6"/>',
  "school": '<path d="M22 10L12 5 2 10l10 5z"/><path d="M6 12v5c3 2 9 2 12 0v-5"/>',
  "rocket": '<path d="M4.5 16.5c-1.5 1.3-2 5-2 5s3.7-.5 5-2c.7-.8.7-2.1-.1-2.9a2.2 2.2 0 0 0-2.9-.1z"/><path d="M12 15l-3-3a22 22 0 0 1 2-3.9A12.9 12.9 0 0 1 22 2c0 2.7-.8 7.5-6 11a22.4 22.4 0 0 1-4 2z"/><path d="M9 12H4s.6-3 2-4c1.6-1.1 5 0 5 0M12 15v5s3-.6 4-2c1.1-1.6 0-5 0-5"/>',
  "user-check": '<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M16 11l2 2 4-4"/>',
  "x-circle": '<circle cx="12" cy="12" r="10"/><path d="M15 9l-6 6M9 9l6 6"/>',
  "ext": '<path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6M15 3h6v6M10 14L21 3"/>',
  "phone": '<path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.9.4 1.8.7 2.7a2 2 0 0 1-.5 2.1L8 9.8a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.7.7a2 2 0 0 1 1.7 2z"/>',
  "info": '<circle cx="12" cy="12" r="10"/><path d="M12 16v-4M12 8h.01"/>',
  "eye-sample": '<rect x="3" y="4" width="18" height="14" rx="2"/><path d="M7 21h10M9 9h6M9 13h3"/>',
}

WA_SVG = '<svg viewBox="0 0 32 32" fill="currentColor" aria-hidden="true"><path d="M16 3C9 3 3.4 8.6 3.4 15.6c0 2.2.6 4.4 1.7 6.3L3.3 29l7.3-1.9c1.8 1 3.9 1.5 6 1.5h.1C23.6 28.6 29.3 23 29.3 16 29.3 9 23.1 3 16 3zm0 23.3c-1.9 0-3.7-.5-5.3-1.4l-.4-.2-4.3 1.1 1.2-4.2-.3-.4c-1-1.6-1.5-3.5-1.5-5.4C5.4 10 10.2 5.3 16 5.3c2.8 0 5.5 1.1 7.5 3.1s3.1 4.7 3.1 7.5c0 5.8-4.8 10.4-10.6 10.4zm5.8-7.8c-.3-.2-1.9-.9-2.2-1-.3-.1-.5-.2-.7.2-.2.3-.8 1-1 1.2-.2.2-.4.2-.7.1-.3-.2-1.3-.5-2.5-1.6-.9-.8-1.6-1.8-1.7-2.1-.2-.3 0-.5.1-.7l.5-.6c.2-.2.2-.3.3-.5.1-.2.1-.4 0-.6l-1-2.4c-.3-.6-.5-.5-.7-.5h-.6c-.2 0-.6.1-.9.4-.3.3-1.2 1.2-1.2 2.9s1.2 3.3 1.4 3.6c.2.2 2.4 3.7 5.8 5.1 2.9 1.1 3.4.9 4.1.9.6-.1 1.9-.8 2.2-1.6.3-.8.3-1.4.2-1.6-.1-.2-.3-.3-.6-.4z"/></svg>'


def ic(name):
    return f'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICONS[name]}</svg>'


def wa(msg=None):
    from urllib.parse import quote
    return f"https://wa.me/{WHATSAPP}?text={quote(msg or P['wa_msg'])}"


YV_MARK = '<svg viewBox="0 0 40 40" aria-hidden="true"><defs><linearGradient id="yvg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#7c5cff"/><stop offset="1" stop-color="#2dd4bf"/></linearGradient></defs><rect width="40" height="40" rx="11" fill="url(#yvg)"/><path d="M9.5 28V12.5l9 15V12.5" fill="none" stroke="#fff" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/><path d="M22.5 28V12.5l4.75 8 4.75-8V28" fill="none" stroke="#fff" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/></svg>'
EMAIL_LINK = '<a href="#contact" data-email data-email-show>Email us</a>'
CONTACT = "#contact"
NAV = [("#features", "Features"), ("#how-it-works", "How it works"), ("#demo", "Demo"), ("#pricing", "Pricing"), ("#faq", "FAQ")]


def logo(home="index.html"):
    return f'<a class="logo" href="{home}" aria-label="{P["name"]} home">{P["logo_svg"]}<span class="lt"><span>{P["name_a"]}<b>{P["name_b"]}</b></span><small>by Naomi Mwangi</small></span></a>'


def parent_bar():
    sib = "".join(f'<a href="{u}">{n}</a>' for n, u in P["siblings"])
    return f'''<div class="parent-bar"><div class="container">
  <a href="{PARENT_URL}" data-track="parent_brand">{YV_MARK}<span>A <strong>Naomi Mwangi</strong> product</span></a>
  <nav class="sib" aria-label="Other products by Naomi Mwangi">{sib}</nav>
</div></div>'''


def header(index=True):
    pre = "" if index else "index.html"
    links = "".join(f'<li><a href="{pre}{h}">{t}</a></li>' for h, t in NAV)
    return f'''<a class="skip-link" href="#main">Skip to content</a>
{parent_bar()}
<header class="site-header">
  <nav class="container nav" aria-label="{P['name']}">
    {logo()}
    <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="menu" aria-label="Open menu">{ic("menu")}</button>
    <ul class="menu" id="menu">{links}<li class="menu-cta"><a href="{pre}#contact" data-track="cta_request_demo">{P["nav_cta"]}</a></li></ul>
  </nav>
</header>'''


def footer(index=True):
    pre = "" if index else "index.html"
    year = datetime.date.today().year
    prod = "".join(f'<li><a href="{pre}{h}">{t}</a></li>' for h, t in NAV)
    fam = "".join(f'<li><a href="{u}">{n}</a></li>' for n, u in P["siblings"])
    return f'''<footer class="site-footer">
  <div class="container">
    <div class="foot-grid">
      <div>
        {logo()}
        <p class="mt-1">{P["footer_blurb"]}</p>
        <a class="part-of mt-1" href="{PARENT_URL}">{YV_MARK} A Naomi Mwangi product</a>
      </div>
      <div><h3>{P["name"]}</h3><ul>{prod}<li><a href="{pre}#contact">{P["nav_cta"]}</a></li></ul></div>
      <div><h3>Naomi Mwangi</h3><ul>
        <li><a href="{PARENT_URL}">Naomi Mwangi home</a></li>{fam}
        <li><a href="{PARENT_URL}services.html">Custom automation</a></li>
        <li><a href="{PARENT_URL}about.html">About</a></li></ul></div>
      <div><h3>Contact</h3><ul>
        <li>{EMAIL_LINK.replace('href="#contact"', f'href="{pre}#contact"')}</li>
        <li><a href="{wa()}" target="_blank" rel="noopener" data-track="whatsapp_click">WhatsApp {WHATSAPP_DISPLAY}</a></li>
        <li><a href="{LINKEDIN}" target="_blank" rel="noopener">LinkedIn</a></li>
        <li>Nairobi, Kenya</li></ul></div>
    </div>
    <div class="foot-bottom"><span>&copy; <span data-year>{year}</span> Naomi Mwangi. {P["name"]} is a product by Naomi Mwangi.</span><span><a href="privacy.html">Privacy</a> · <a href="sitemap.xml">Sitemap</a></span></div>
  </div>
</footer>
<a class="wa-float" href="{wa()}" target="_blank" rel="noopener" aria-label="Chat about {P['name']} on WhatsApp" data-track="whatsapp_click">{WA_SVG}</a>'''


def page(fn, title, desc, body, ld=None, noindex=False):
    url = SITE_URL + "/" + ("" if fn == "index.html" else fn)
    index = fn == "index.html"
    lds = "".join('<script type="application/ld+json">' + json.dumps(x, ensure_ascii=False) + "</script>" for x in (ld or []))
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="robots" content="{"noindex, follow" if noindex else "index, follow"}">
<link rel="canonical" href="{url}">
<meta name="theme-color" content="{P["theme_color"]}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{P["name"]}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE_URL}/assets/img/og-image.png">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="assets/img/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&amp;display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/css/site.css?v={ASSET_VERSION}">
<script>document.documentElement.classList.add("js");setTimeout(function(){{if(!window.__yv)document.documentElement.classList.remove("js")}},2500);</script>
{lds}
</head>
<body>
{header(index)}
<main id="main">
{body}
</main>
{footer(index)}
<script src="assets/js/config.js?v={ASSET_VERSION}"></script>
<script src="assets/js/main.js?v={ASSET_VERSION}"></script>
</body>
</html>
'''
    open(os.path.join(OUT, fn), "w", encoding="utf-8").write(html)


def faq(items):
    return '<div class="faq">' + "".join(f'<details class="reveal"><summary>{q}</summary><div><p>{a}</p></div></details>' for q, a in items) + "</div>"


def faq_ld(items):
    strip = lambda s: re.sub(r"<[^>]+>", "", s)
    return {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": strip(q), "acceptedAnswer": {"@type": "Answer", "text": strip(a)}} for q, a in items]}


def sample_label(dark=False):
    style = ' style="color:#9aa7c9"' if dark else ""
    return f'<p class="sample-label"{style}>{ic("info")}Illustration with sample data, not a real client account</p>'


def grid(items):
    return '<div class="grid g3">' + "".join(f'<div class="card reveal"><span class="ico">{ic(i)}</span><h3>{t}</h3><p>{d}</p></div>' for i, t, d in items) + "</div>"


def flow_html(nodes):
    return '<div class="flow">' + "".join(f'<div class="flow-node reveal"><span class="ico">{ic(i)}</span><h4>{t}</h4><p>{d}</p></div>' for i, t, d in nodes) + "</div>"


def chips(items):
    return '<div class="chips">' + "".join(f'<span class="chip">{ic(i)}{t}</span>' for i, t in items) + "</div>"


def cta_block(title, text):
    return f'''<section class="section"><div class="container"><div class="cta reveal">
  <div><h2>{title}</h2><p>{text}</p></div>
  <div class="btn-row"><a class="btn btn--primary" href="#contact" data-track="cta_request_demo">{P["nav_cta"]} {ic("arrow")}</a>
  <a class="btn btn--wa" href="{wa()}" target="_blank" rel="noopener" data-track="whatsapp_click">{WA_SVG} WhatsApp us</a></div>
</div></div></section>'''


def contact_section():
    types = [("demo", "Request a demo", True), ("consultation", "Book a consultation", False), ("general", "Ask a question", False)]
    type_html = "".join(f'<label><input type="radio" name="Request type" value="{t}" data-key="{k}"{" checked" if c else ""}> {t}</label>' for k, t, c in types)
    methods = "".join(f'<label><input type="radio" name="Preferred contact method" value="{m}" required data-msg="Please choose how you&#39;d like us to contact you."> {m}</label>' for m in ["Email", "WhatsApp", "Phone call"])
    return f'''
<section class="section section--soft" id="contact">
  <div class="container split split--top split--contact">
    <div class="form-card" id="enquiry">
      <form id="enquiry-form" action="thank-you.html" method="POST" novalidate>
        <span class="eyebrow">Get started</span>
        <h2 style="font-size:1.7rem">{P["form_title"]}</h2>
        <p class="muted small">{P["form_intro"]} Fields marked <span style="color:var(--brand-700)">*</span> are required.</p>
        <noscript><p class="form-msg form-msg--err">This form needs JavaScript. Please contact us on WhatsApp ({WHATSAPP_DISPLAY}) instead.</p></noscript>
        <input type="hidden" name="Product" value="{P["name"]}">
        <input type="hidden" name="_next" value="{SITE_URL}/thank-you.html">
        <input type="hidden" name="_captcha" value="false">
        <input type="hidden" name="_template" value="table">
        <div class="hp" aria-hidden="true"><label>Leave this field empty<input type="text" name="_honey" tabindex="-1" autocomplete="off"></label></div>
        <div class="form-grid">
          <fieldset class="field full"><legend>What would you like to do?</legend><div class="seg">{type_html}</div></fieldset>
          <div class="field"><label for="f-name">Full name <span class="req">*</span></label><input id="f-name" name="Full name" autocomplete="name" required maxlength="100" data-msg="Please enter your full name."><p class="err" id="e-name"></p></div>
          <div class="field"><label for="f-biz">Business name <span class="opt">(optional)</span></label><input id="f-biz" name="Business name" autocomplete="organization" maxlength="120"><p class="err" id="e-biz"></p></div>
          <div class="field"><label for="f-email">Email address <span class="req">*</span></label><input id="f-email" type="email" name="email" autocomplete="email" required maxlength="160" data-msg="Please enter your email address."><p class="err" id="e-email"></p></div>
          <div class="field"><label for="f-phone">Phone number <span class="opt">(optional)</span></label><input id="f-phone" type="tel" name="Phone" autocomplete="tel" maxlength="20" placeholder="+254 7XX XXX XXX"><p class="err" id="e-phone"></p></div>
          <div class="field full"><label for="f-msg">{P["challenge_label"]} <span class="req">*</span></label><textarea id="f-msg" name="Challenge" required minlength="20" maxlength="3000" data-msg="Please tell us a little about what you need." placeholder="{P["challenge_ph"]}"></textarea><p class="hint">A few sentences is plenty.</p><p class="err" id="e-msg"></p></div>
          <fieldset class="field full"><legend>Preferred contact method <span class="req">*</span></legend><div class="seg">{methods}</div><p class="err" id="e-method"></p></fieldset>
          <div class="field full"><label class="consent"><input type="checkbox" name="Consent" value="Yes" required data-msg="Please confirm so we can reply to you."> I agree that Naomi Mwangi may use these details to respond to my enquiry, as described in the <a href="privacy.html">privacy notice</a>.</label><p class="err" id="e-consent"></p></div>
          <div class="full"><button class="btn btn--primary btn--block" type="submit">Send enquiry {ic("arrow")}</button></div>
        </div>
        <div id="form-msg" class="form-msg" hidden></div>
      </form>
      <div id="form-done" class="form-success" hidden tabindex="-1">
        <div class="tick">{ic("check")}</div>
        <h2 style="font-size:1.6rem">Thank you<span id="done-name"></span>. Your enquiry has been sent.</h2>
        <p class="muted">Here's what happens next:</p>
        <ol><li>We read your enquiry and look at what you described.</li><li>We contact you by <strong id="done-how">email</strong>, usually within one working day.</li><li>If it's a good fit, we arrange a demo or a short consultation.</li></ol>
        <div class="btn-row" style="justify-content:center"><a class="btn btn--outline" href="{PARENT_URL}">Visit Naomi Mwangi&#39;s site</a><a class="btn btn--wa" href="{wa("Hello, I've just sent a " + P["name"] + " enquiry on your website.")}" target="_blank" rel="noopener" data-track="whatsapp_click">{WA_SVG} Message us on WhatsApp</a></div>
      </div>
    </div>
    <aside>
      <div class="card card--flat">
        <h3>Prefer to chat?</h3>
        <p class="muted">For quick questions, WhatsApp is the fastest way to reach us.</p>
        <a class="btn btn--wa btn--block" href="{wa()}" target="_blank" rel="noopener" data-track="whatsapp_click">{WA_SVG} Chat on WhatsApp</a>
        <a class="btn btn--outline btn--block mt-1" href="#contact" data-booking hidden target="_blank" rel="noopener" data-track="cta_booking_page">{ic("cal")} Pick a time online</a>
        <ul class="contact-list mt-2">
          <li><span class="ico">{ic("mail")}</span><div><b>Email</b>{EMAIL_LINK}</div></li>
          <li><span class="ico" style="background:#dcfce7;color:#15803d">{ic("phone")}</span><div><b>WhatsApp</b><a href="{wa()}" target="_blank" rel="noopener">{WHATSAPP_DISPLAY}</a></div></li>
          <li><span class="ico">{ic("map")}</span><div><b>Location</b><span>Nairobi, Kenya · serving clients locally and remotely (EAT, UTC+3)</span></div></li>
        </ul>
      </div>
      <div class="notice mt-1">{ic("shield")}<p class="small">Please don't include passwords or confidential client data in this form.</p></div>
    </aside>
  </div>
</section>'''


def build_misc():
    page("thank-you.html", f"Thank You | {P['name']}", f"Thank you for contacting {P['name']}.", f'''
<section class="page-hero" style="text-align:center"><div class="container">
  <span class="eyebrow">Enquiry received</span><h1 style="margin-inline:auto">Thank you, we've received your enquiry</h1>
  <p style="margin-inline:auto">We'll reply using your preferred contact method, usually within one working day. For anything urgent, message us on WhatsApp.</p>
  <div class="btn-row mt-2" style="justify-content:center"><a class="btn btn--wa" href="{wa()}" target="_blank" rel="noopener">{WA_SVG} WhatsApp</a><a class="btn btn--ghost" href="index.html">Back to {P["name"]}</a><a class="btn btn--ghost" href="{PARENT_URL}">Visit Naomi Mwangi&#39;s site</a></div>
</div></section>''', noindex=True)
    page("404.html", f"Page Not Found | {P['name']}", "Page not found.", f'''
<section class="page-hero" style="text-align:center"><div class="container">
  <span class="eyebrow">Error 404</span><h1 style="margin-inline:auto">We couldn't find that page</h1>
  <p style="margin-inline:auto">The link may be out of date. Try one of these instead.</p>
  <div class="btn-row mt-2" style="justify-content:center"><a class="btn btn--primary" href="index.html">{P["name"]} home</a><a class="btn btn--ghost" href="index.html#contact">Contact</a><a class="btn btn--ghost" href="{PARENT_URL}">Naomi Mwangi</a></div>
</div></section>''', noindex=True)
    page("privacy.html", f"Privacy Notice | {P['name']}", f"How {P['name']} and Naomi Mwangi handle the information you share through this website.", f'''
<section class="page-hero"><div class="container"><span class="eyebrow">Privacy</span><h1>Privacy notice</h1><p>How we handle the information you share with us through this website.</p></div></section>
<section class="section"><div class="container narrow">
  <p class="small muted">Last updated: <span class="placeholder">[add date]</span></p>
  <h2 style="font-size:1.4rem">Who we are</h2><p>{P["name"]} is a product by Naomi Mwangi, based in Nairobi, Kenya. You can contact us by <a href="index.html#contact" data-email>email</a> or on WhatsApp ({WHATSAPP_DISPLAY}).</p>
  <h2 style="font-size:1.4rem">What we collect</h2><p>When you send an enquiry, we receive the details you enter: your name, business name, email address, phone number, your message and your preferred contact method.</p>
  <h2 style="font-size:1.4rem">How we use it</h2><p>Only to respond to your enquiry, arrange demos or consultations, and prepare proposals. We don't sell your information or use it for unrelated marketing.</p>
  <h2 style="font-size:1.4rem">How it is delivered and stored</h2><p>Form submissions are delivered to our email inbox through FormSubmit (formsubmit.co). We keep enquiries only as long as needed to respond and for reasonable business records.</p>
  <h2 style="font-size:1.4rem">Analytics</h2><p>If website analytics are switched on, we use aggregated statistics to understand which pages are useful.</p>
  <h2 style="font-size:1.4rem">Your rights</h2><p>Under Kenya's Data Protection Act, 2019, you can ask to access, correct or delete your personal data at any time by contacting us.</p>
</div></section>''')


def build_seo():
    today = datetime.date.today().isoformat()
    urls = "".join(f"  <url><loc>{SITE_URL}/{p}</loc><lastmod>{today}</lastmod><priority>{pr}</priority></url>\n" for p, pr in [("", "1.0"), ("privacy.html", "0.3")])
    open(os.path.join(OUT, "sitemap.xml"), "w").write(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}</urlset>\n')
    open(os.path.join(OUT, "robots.txt"), "w").write(f"User-agent: *\nAllow: /\nDisallow: /thank-you.html\n\nSitemap: {SITE_URL}/sitemap.xml\n")
    open(os.path.join(OUT, "assets/img/favicon.svg"), "w").write(P["logo_svg"].replace(' aria-hidden="true"', ' xmlns="http://www.w3.org/2000/svg"'))


# ============================================================== PRODUCT CONTENT
P = {
    "name": "LeadFlow AI", "name_a": "Lead", "name_b": "Flow AI",
    "theme_color": "#071433",
    "logo_svg": '<svg viewBox="0 0 40 40" aria-hidden="true"><defs><linearGradient id="lfg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#3b6ff5"/><stop offset="1" stop-color="#06b6d4"/></linearGradient></defs><rect width="40" height="40" rx="11" fill="url(#lfg)"/><path d="M10 12h20l-7.5 9v6.5L17.5 30v-9z" fill="none" stroke="#fff" stroke-width="3" stroke-linejoin="round"/><circle cx="29" cy="28" r="3" fill="#fff"/></svg>',
    "siblings": [("SocialFlow AI", "https://yomie-commits.github.io/SocialFlowAI/"), ("ExecutiveFlow AI", "https://yomie-commits.github.io/ExecutiveFlowAI/")],
    "nav_cta": "Request a demo",
    "wa_msg": "Hello, I'm interested in LeadFlow AI and would like to know more.",
    "footer_blurb": "An intelligent lead management system that captures every enquiry, qualifies it with AI, reminds you to follow up and shows where every lead stands.",
    "form_title": "Request a LeadFlow AI demo or quote",
    "form_intro": "Tell us where your enquiries come from and how you follow up today.",
    "challenge_label": "Where do your enquiries come from?",
    "challenge_ph": "For example: website form, email, WhatsApp; roughly how many a week; how you track them now (spreadsheet, CRM, memory…).",
}

CAPS = [("globe", "Website enquiry capture", "Enquiries from your website forms and business inbox are collected automatically, in one place."),
        ("tag", "Organisation and categorisation", "Each lead is labelled by service, source and urgency, so you see what's coming in at a glance."),
        ("spark", "AI-assisted qualification", "AI reads the enquiry and notes the need, budget signals and timeline to help you prioritise. You make the final call."),
        ("sheet", "CRM and spreadsheet integration", "Leads are logged to Google Sheets or a CRM you already use, with no copy-pasting."),
        ("bell", "Follow-up reminders", "Every lead gets a follow-up date, and you're reminded before anyone goes cold."),
        ("mail", "Lead notifications", "New and high-priority enquiries alert you by email straight away."),
        ("chart", "Sales pipeline reporting", "A simple weekly view of new, contacted, qualified and won leads."),
        ("pen", "First-response drafts", "A suggested first reply can be prepared for each lead, ready for you to review and send."),
        ("shield", "Your accounts, your data", "Leads stay in tools you own, with only the access each workflow needs.")]

WALK = [("globe", "1 · Enquiry arrives", "A visitor fills in your website form asking for an office cleaning quote for next month.", "Website form · 09:42"),
        ("spark", "2 · AI notes the essentials", "Need: office cleaning, 3 floors. Timeline: next month. Priority: high. Suggested next step: send a quote.", "AI qualification"),
        ("sheet", "3 · Logged to your tracker", "A new row appears in your lead tracker with the details, source and status “New”.", "Google Sheets"),
        ("bell", "4 · You're reminded to follow up", "You get an alert now, and a reminder in two days if the lead is still waiting.", "Email alert · reminder set")]

FAQ = [("Where do the leads come from?", "Usually your website forms and your business inbox. Other sources, such as Google Forms or other form tools, can often be added; we confirm this during the consultation."),
       ("Do I need a CRM?", "No. Many clients start with a Google Sheets lead tracker, which is free and easy to use. If you already use a CRM, we check whether it can be connected."),
       ("Does the AI reply to leads by itself?", "Not by default. LeadFlow AI can prepare a first-response draft, but you review and send it. Automatic replies can be considered for simple acknowledgements if you want them."),
       ("Is there a live demo?", "LeadFlow AI is set up around your own forms and tools, so demos are guided: we walk you through a working example on a call or over WhatsApp. Request one with the form below."),
       ("What does it cost?", "LeadFlow AI is quoted after a consultation, because it depends on your lead sources, how many leads you receive and the tools you use. You get a written quote before any work starts."),
       ("What other costs should I expect?", "Tools such as Make.com charge based on how much the automation runs, and AI features have usage costs. We estimate these with you before building."),
       ("Do you work with clients outside Kenya?", "Yes. We work remotely and can quote in KES or an equivalent amount in your currency.")]


def build_index():
    pipe = '''<div class="pipe">
      <div class="pipe-col"><h5>New <span>3</span></h5><div class="pipe-card">Office cleaning quote<small>Website form · today</small></div><div class="pipe-card">Apartment viewing<small>Email · today</small></div><div class="pipe-card">Monthly bookkeeping<small>Website form</small></div></div>
      <div class="pipe-col"><h5>Contacted <span>2</span></h5><div class="pipe-card">Event photography<small>Follow-up Thu</small></div><div class="pipe-card">Logo redesign<small>Follow-up Fri</small></div></div>
      <div class="pipe-col"><h5>Qualified <span>2</span></h5><div class="pipe-card">Staff training day<small>Proposal sent</small></div><div class="pipe-card">Website refresh<small>Call booked</small></div></div>
      <div class="pipe-col"><h5>Won <span>1</span></h5><div class="pipe-card">Quarterly reports<small>This week</small></div></div>
    </div>'''
    walk = "".join(f'<div class="card reveal"><span class="ico">{ic(i)}</span><h3>{t}</h3><p>{d}</p><p class="small muted mb-0">{m}</p></div>' for i, t, d, m in WALK)
    factors = ["How many places enquiries come from", "Roughly how many leads you receive", "Google Sheets or an existing CRM", "Follow-up rules and reminders", "Reporting you'd like to see"]
    included = ["Workflow design around your process", "Setup in accounts you own", "Testing with realistic enquiries", "Handover documentation and training"]
    body = f'''
<section class="hero">
  <div class="container hero-grid">
    <div>
      <span class="status">Available as a custom setup</span>
      <h1 style="margin-top:1rem">Capture every enquiry. <span class="grad">Follow up on time.</span></h1>
      <p class="hero-copy">LeadFlow AI is an intelligent lead management system. It collects enquiries from your website and inbox, organises and qualifies them with AI, reminds you to follow up and shows you where every lead stands.</p>
      <div class="btn-row">
        <a class="btn btn--primary" href="#contact" data-track="cta_request_demo">Request a demo {ic("arrow")}</a>
        <a class="btn btn--ghost" href="#demo" data-track="cta_see_walkthrough">See how it works</a>
      </div>
      <ul class="hero-notes">
        <li>{ic("globe")} Website &amp; email enquiries</li>
        <li>{ic("sheet")} Google Sheets or your CRM</li>
        <li>{ic("hand")} You decide who to contact</li>
      </ul>
    </div>
    <div><div class="frame"><div class="frame-bar"><i></i><i></i><i></i><span>LeadFlow AI · Pipeline</span></div><div class="frame-body">{pipe}</div></div>{sample_label(dark=True)}</div>
  </div>
</section>

<section class="section">
  <div class="container split split--top">
    <div class="reveal"><span class="eyebrow">The problem</span><h2>Enquiries slip through the cracks</h2>
      <p class="lead">Leads arrive by website form, email and WhatsApp. Without a system some are missed, replies are slow, and follow-ups depend on someone remembering.</p>
      <p>Every missed or late reply is a potential client who may choose someone else. LeadFlow AI gives every enquiry a place, a priority and a next step.</p></div>
    <div class="card card--flat reveal"><h3>What changes</h3><ul class="checks mb-0">
      <li>Every enquiry is captured and logged automatically</li><li>You see which leads need attention first</li>
      <li>Follow-ups happen on time, not when someone remembers</li><li>A clear weekly view of your pipeline</li></ul></div>
  </div>
</section>

<section class="section section--soft" id="features">
  <div class="container">
    <div class="head reveal"><span class="eyebrow">Features</span><h2>What LeadFlow AI does for you</h2><p class="lead">From the moment an enquiry arrives to the moment you win the work.</p></div>
    {grid(CAPS)}
  </div>
</section>

<section class="section section--dark" id="how-it-works">
  <div class="container">
    <div class="head reveal"><span class="eyebrow">How it works</span><h2>From enquiry to follow-up, automatically</h2><p class="lead">Built with tools you can own and understand: your forms, Make.com, AI and Google Sheets or your CRM.</p></div>
    {flow_html([("globe", "Enquiry arrives", "From a website form or email"), ("zap", "Make.com", "Picks it up and moves the data"), ("spark", "AI qualification", "Notes the need, urgency and next step"), ("sheet", "Lead tracker", "Logged to Google Sheets or your CRM"), ("bell", "You follow up", "Alerts, reminders and a weekly report")])}
    <div class="steps mt-3">{"".join(f'<div class="step reveal"><span class="n">{n}</span><h3>{t}</h3><p>{d}</p></div>' for n, (t, d) in enumerate([("Consultation", "We map where your leads come from and how you follow up."), ("Design", "We agree categories, priorities, reminders and reports."), ("Setup", "Built in your own accounts and tools."), ("Testing", "Tested with realistic enquiries before going live."), ("Handover", "Documentation, training and optional support.")], 1))}</div>
  </div>
</section>

<section class="section" id="demo">
  <div class="container">
    <div class="head reveal"><span class="eyebrow">Demo</span><h2>Follow one enquiry through LeadFlow AI</h2><p class="lead">A sample walkthrough of what happens when a new lead arrives.</p></div>
    <div class="grid g4">{walk}</div>
    <p class="center mt-1">{sample_label()}</p>
    <div class="cta mt-2 reveal" style="margin-top:1.5rem">
      <div><h2>Want to see it with your own enquiries?</h2><p>We'll walk you through a working example on a call or over WhatsApp, using the kind of leads your business receives.</p></div>
      <div class="btn-row"><a class="btn btn--primary" href="?type=demo#contact" data-track="cta_request_demo">Request a guided demo {ic("arrow")}</a></div>
    </div>
  </div>
</section>

<section class="section section--soft">
  <div class="container split split--top">
    <div class="reveal"><span class="eyebrow">Who it's for</span><h2>Built for businesses that run on enquiries</h2>
      {chips([("briefcase", "Service businesses"), ("home", "Real estate companies"), ("user-check", "Consultants"), ("megaphone", "Agencies"), ("users", "Sales teams")])}
      <p class="mt-2">If you receive enquiries every week and want a reliable way to respond and follow up, LeadFlow AI is built for you.</p></div>
    <div class="reveal"><span class="eyebrow">Your data</span><h2>You stay in control</h2>
      <ul class="checks"><li>Leads are stored in tools you own</li><li>AI suggests priorities; you decide who to contact</li><li>No messages are sent to leads without your approval</li><li>Plain-language documentation of how it works</li></ul></div>
  </div>
</section>

<section class="section" id="pricing">
  <div class="container">
    <div class="head reveal"><span class="eyebrow">Pricing</span><h2>Quoted for your business</h2><p class="lead">Every LeadFlow AI setup is shaped by your lead sources and tools, so it's quoted after a short consultation. You get a written quote before any work starts.</p></div>
    <div class="grid g3">
      <div class="card reveal"><span class="ico">{ic("list")}</span><h3>What affects the price</h3><ul class="checks mb-0">{"".join(f"<li>{x}</li>" for x in factors)}</ul></div>
      <div class="card reveal"><span class="ico">{ic("check")}</span><h3>Included in every setup</h3><ul class="checks mb-0">{"".join(f"<li>{x}</li>" for x in included)}</ul></div>
      <div class="card reveal"><span class="ico">{ic("tool")}</span><h3>Optional extras</h3><p>Monthly maintenance, new lead sources and extra reports can be added later.</p><p class="small muted mb-0">Third-party tool costs (for example Make.com, which charges by usage) are separate and paid directly by you.</p></div>
    </div>
    <p class="center mt-2 reveal"><a class="btn btn--primary" href="?type=consultation#contact" data-track="pricing_quote">Request a quote {ic("arrow")}</a></p>
  </div>
</section>

<section class="section section--soft" id="faq">
  <div class="container"><div class="head reveal"><span class="eyebrow">FAQ</span><h2>Questions about LeadFlow AI</h2></div>{faq(FAQ)}</div>
</section>
{contact_section()}
'''
    svc = {"@context": "https://schema.org", "@type": "Service", "name": "LeadFlow AI", "serviceType": "Lead management and follow-up automation",
           "description": P["footer_blurb"], "url": SITE_URL + "/", "areaServed": ["Kenya", "Worldwide"],
           "brand": {"@type": "Brand", "name": "LeadFlow AI"},
           "provider": {"@type": "Person", "name": "Naomi Mwangi", "url": PARENT_URL}}
    page("index.html", "LeadFlow AI | Lead Capture, Qualification &amp; Follow-up Automation",
         "LeadFlow AI captures website and email enquiries, qualifies leads with AI, logs them to your tracker or CRM, reminds you to follow up and reports on your pipeline. A product by Naomi Mwangi.",
         body, ld=[svc, faq_ld(FAQ)])


if __name__ == "__main__":
    build_index(); build_misc(); build_seo()
    print("Built LeadFlow AI site in", OUT)
