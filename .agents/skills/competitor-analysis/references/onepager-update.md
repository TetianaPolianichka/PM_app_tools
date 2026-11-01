# Updating the competitors section in the one-pager

Other people see the one-pager, and someone tuned its layout by hand. So changes must be surgical.

1. Find the competitors section (e.g. `<section id="competitors">` or a heading containing "Competitors" or "Конкуренти").
   - If the section isn't found, don't create it. Ask the user where to add it.
2. Update only the content of this section. Don't change other sections, `<head>`, styles or scripts.
3. Use the page's existing CSS classes and structure. Don't add new inline styles.
4. Section content:
   - a compact top-5 table (Name, Rating iOS, Rating Android, Model, key difference)
   - 3 key conclusions for APP_NAME
   - caption: "Data as of YYYY-MM-DD, sources: App Store (COUNTRY_CODE), Google Play (COUNTRY_CODE), official sites"
5. Check that the HTML is valid (tags closed) and the data matches OUTPUT_FILE.
