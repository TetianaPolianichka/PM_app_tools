---
name: competitor-analysis
description: Competitor analysis of a mobile app from public App Store and Google Play data (ratings, rating counts, monetization, features, mechanics, ASO) with conclusions for positioning and marketing. Run this skill when the user writes "go!" or «погнали!» / «погнали» as a start command (even with no other words), and also when they ask for a competitor analysis, a comparison with competitors, "who are our competitors in the stores", a mechanics matrix, or an update to the competitors section of the one-pager.
---

# Mobile app competitor analysis

Based on modules 4.7 (store metrics) and 4.8 (competitor analysis) and the evidence standards in `wiki/audit-framework.md`.

Work as an experienced app marketing and ASO specialist: collect verifiable public data, separate facts from conclusions, and turn data into recommendations for marketing. The main question of the analysis: **how should APP_NAME be positioned among competitors in the MARKET market, and which gaps can it fill?**

## Step 0. Collect the variables

The user starts the skill with a short "go!" (or «погнали!»), so don't wait for a filled-in YAML. Collect the variables yourself in this order:

1. The user's message and the conversation so far.
2. `wiki/overview.md` and `wiki/now.md`, if they exist (facts about the product, market and audience live there). Also `wiki/competitors/`, if a previous analysis is there: use it as a candidate list and note what changed.

**Required:** APP_NAME, APP_CATEGORY, APP_DESCRIPTION (1–2 sentences: what it does and how it's different), MARKET, COUNTRY_CODE (e.g. `us`), CURRENCY.

**Optional:** APP_STORE_URL, GOOGLE_PLAY_URL, KEY_MECHANICS, TARGET_AUDIENCE, BUSINESS_MODEL, INCLUSION_CRITERIA, EXCLUSIONS, CANDIDATES, COMPETITOR_COUNT (default 6–8).

**Files:**
- OUTPUT_FILE: default `wiki/competitors/<app-name>-<country_code>.md` (lowercase Latin, hyphenated). Later exercises expect this path, so don't rename the folder.
- ONEPAGER_FILE: if `artifacts/` has a one-pager (`*.html` with onepager / one-pager in the name), offer to update it. If not, skip.

If required variables are missing, ask in **one** short message: show what you've already found (and where), and list what's missing. You may derive COUNTRY_CODE and CURRENCY from MARKET (USA → `us`, USD) and just show them for confirmation. Don't invent optional ones: continue without them and mark assumptions `[Assumption]` or `n/a`.

## Step 1. Selecting competitors

An app makes the sample only if **both**:
- it solves the same job for the same audience (taking INCLUSION_CRITERIA into account);
- it's available in the COUNTRY_CODE storefront in both the App Store and Google Play.

A similar name or store category confirms nothing: read the description. This is where mistakes happen most often, and they break the whole analysis.

Build a shortlist twice the size of COMPETITOR_COUNT (from CANDIDATES, store searches for category keywords, the "Similar apps" section and reviews on official sites). Then pick the final competitors in three groups and briefly justify each choice:

| Group | Criterion | Count |
|---|---|---|
| **A. Direct by mechanics** | Closest to APP_NAME in format and key mechanics | 2–3 |
| **B. Category leaders** | Largest in the category in MARKET by rating count | 2–3 |
| **C. Alternative solutions** | Solve the same job a different way | 1–2 |

Check candidates from CANDIDATES against the same criteria. Replace a candidate if you find a better one, and explain why. Exclude everything in EXCLUSIONS.

If APP_NAME is already in the stores, collect the same data for it and put it as the first row in the tables.

## Step 2. Data collection

For each competitor, collect data in this order: App Store, then Google Play, then the official site. The full list of fields is in `references/data-fields.md`. Read it before collecting.

Practical tips on sources:
- App Store: `https://apps.apple.com/<country_code>/app/<slug>/id<ID>`. For exact rating, rating count and latest version release date, the public Apple lookup is handy: `https://itunes.apple.com/lookup?id=<ID>&country=<country_code>`. It's an official Apple source. In section 9, cite both it and the store page.
- Google Play: `https://play.google.com/store/apps/details?id=<package>&hl=en&gl=<country_code>`. The `gl` parameter is required; without it you may see data for another region.
- If a page doesn't load or the app isn't available in the storefront, record that in section 8. If the sample is incomplete without it, replace the competitor.

## Step 3. Report

Create OUTPUT_FILE exactly per the template in `references/output-template.md`. Before writing, double-check ratings and dates: these are the numbers people quote most often later.

When the file lives in `wiki/`, follow the wiki rules from AGENTS.md:
- Below the title there must be a `Sources:` line (App Store / Google Play (COUNTRY_CODE), official sites; full list in section 9).
- Update `wiki/index.md` (a line with a link and description) and add an entry to `wiki/log.md` (source, what changed).

## Step 4. One-pager (only if ONEPAGER_FILE is set)

Follow the rules in `references/onepager-update.md`. In short: change only the competitors section. If there's no such section, ask where to add it and don't create it yourself.

## Rules

1. **Public data only:** App Store and Google Play pages in the COUNTRY_CODE storefront and official sites. Don't use third-party analytics services (Sensor Tower, AppTweak, etc.) without separate permission. Their estimates look like facts but aren't.
2. **Invent nothing.** Field unavailable? Put `n/a` and add a row to section 8 "Data gaps". An honest `n/a` is worth more than a plausible number nobody can verify later.
3. **Don't mix platforms and regions.** iOS data doesn't carry over to Android and vice versa. Data from other storefronts isn't used.
4. **Separate facts from analysis.** Sections 1–6 contain only facts from sources (evidence level [Verified]). Section 7 is analysis; mark assumptions in it `[Assumption]`.
5. **Features from the description only**, in the store or on the site. Don't attribute to an app what isn't there.
6. **Copyright.** Paraphrase descriptions and reviews. Copy verbatim only the name and subtitle or short description, since those are public metadata.
7. **Every number has a source** in section 9.

## Self-check before finishing

- [ ] Each competitor meets the inclusion criteria and is available in the COUNTRY_CODE storefront on both platforms.
- [ ] All template columns are present and no cell is empty (data or `n/a`).
- [ ] All links point to the COUNTRY_CODE storefront.
- [ ] Dates are YYYY-MM-DD, ratings have 1 decimal, prices are in CURRENCY.
- [ ] Every `n/a` has a row in section 8.
- [ ] Conclusions in section 7 rest on facts from sections 1–6.
- [ ] If the file is in the wiki: `index.md` and `log.md` are updated.
- [ ] If the one-pager was updated: only the competitors section changed, and the data matches OUTPUT_FILE.

## Chat summary

At the end, give at most 5 bullets: what was done, 2–3 key conclusions, the number of fields with `n/a`, and a link to OUTPUT_FILE (and the one-pager, if updated).
