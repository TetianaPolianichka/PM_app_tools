# OUTPUT_FILE template

Follow this structure exactly. It's needed so reports for different dates and markets can be compared with each other.

````markdown
# Competitor Analysis — APP_NAME (MARKET)

Sources: App Store (COUNTRY_CODE), Google Play (COUNTRY_CODE), official sites (full list in section 9)

**Data collected:** YYYY-MM-DD · **Storefront:** COUNTRY_CODE · **Number of competitors:** N

## 1. Competitor overview

| # | Name | Site | App Store | Google Play | Rating iOS | Rating Android | Last update |
|---|------|------|-----------|-------------|------------|----------------|-------------|

*Last update: iOS / Android, if the dates differ.*

## 2. Store metrics

| # | Name | Group | Ratings iOS | Ratings Android | Downloads Android | Category position iOS | Age |
|---|------|-------|-------------|-----------------|-------------------|-----------------------|-----|

## 3. Monetization

| # | Name | Model | Prices (CURRENCY) | Trial | Ads |
|---|------|-------|-------------------|-------|-----|

## 4. Key features

| # | Name | Feature 1 | Feature 2 | Feature 3 | Feature 4 | Feature 5 | Format / approach |
|---|------|-----------|-----------|-----------|-----------|-----------|-------------------|

## 5. Mechanics matrix vs APP_NAME

| Mechanic | APP_NAME | Competitor 1 | Competitor 2 | … |
|----------|----------|--------------|--------------|---|

## 6. Competitor cards

### [Name]
- **Why it's on the list:** group and rationale
- **Positioning:** 1 sentence
- **ASO:** name / subtitle
- **Strengths:** 2–3 bullets
- **Weaknesses or vulnerabilities:** 2–3 bullets (from public data only)
- **Sources:** URL

## 7. Conclusions for APP_NAME  *(analysis, not facts)*
- **Positioning:** where APP_NAME differs from competitors
- **Market gaps:** what competitors don't do or do poorly
- **Threats:** who is closest by mechanics or audience
- **Marketing recommendations:** messages, ASO ideas, pricing (3–5 bullets with priority P0/P1/P2)

## 8. Data gaps

| Competitor | Field | Reason | How to get it |
|------------|-------|--------|---------------|

## 9. Sources
List of all URLs with access dates.
````

The `Sources:` line is needed only when the file lives in `wiki/`. Elsewhere it can be removed.

## Formatting rules
- In tables, format links as `[App Store](url)` and `[Google Play](url)`.
- Order: APP_NAME (if it's in the stores), then group A → B → C, and within a group by iOS rating count.
- Write numbers as they appear in the store ("1.2M", "4.7").
