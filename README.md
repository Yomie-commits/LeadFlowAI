# LeadFlow AI

Lead management: lead capture, qualification, CRM organisation, follow-up automation and sales reporting.

**LeadFlow AI is a [YomieVerse](https://yomie-commits.github.io/Yomie-Verse/) product.**

Live site: https://yomie-commits.github.io/LeadFlowAI/

Sister products: [SocialFlow AI](https://yomie-commits.github.io/SocialFlowAI/) · [ExecutiveFlow AI](https://yomie-commits.github.io/ExecutiveFlowAI/) · [LeadFlow AI](https://yomie-commits.github.io/LeadFlowAI/)

## Structure

| Path | What it is |
|---|---|
| `index.html` | Product page: hero, features, how it works, demo, pricing, FAQ, enquiry form |
| `privacy.html`, `thank-you.html`, `404.html` | Supporting pages |
| `build.py` | Generates every page, the sitemap, robots.txt and the favicon. Page copy is in the `P` dictionary and `build_index()` near the bottom |
| `assets/css/site.css` | YomieVerse design system v3, themed in electric blue |
| `assets/js/config.js` | **Settings you can change without rebuilding**: email, WhatsApp, booking link, analytics |
| `assets/js/main.js` | Menu, animations and the enquiry form (shared with YomieVerse) |
| `assets/img/` | Favicon and social share image |

After editing `build.py`, run `python3 build.py` and commit the regenerated HTML.

## Notes

- **Enquiry form:** delivered by [FormSubmit](https://formsubmit.co) to the email in `config.js`. The first real submission triggers a one-time "Activate Form" email; click its link once.
- **Demo:** a labelled sample walkthrough plus a 'Request a guided demo' form. There is no self-serve demo app.
- **Hosting:** GitHub Pages, `main` branch, root folder.
- **Theme colour substitutions** applied to the YomieVerse stylesheet: #7c5cff→#2f64ec, #6a48f0→#2556de, #5534d6→#1d4ed8, #efebff→#e7eeff, #b6a6ff→#9db8ff, #c4b5ff→#b4c8ff, #8fb0ff→#67e8f9, rgb 124,92,255→47,100,236, rgb 85,52,214→29,78,216, `--violet`→`--brand`.
- **Placeholders:** the privacy notice needs a "last updated" date.
