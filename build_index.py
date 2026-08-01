"""Build the complete index.html from parts."""
import sys

def main():
    # Read the existing index.html to extract JS blocks
    with open('index.html', 'r', encoding='utf-8') as f:
        old = f.read()

    # Extract the 4 JS blocks from old index.html
    js_start = old.find('<script>')
    # Find all script content between <script> and </script>
    scripts = []
    pos = 0
    while True:
        s = old.find('<script>', pos)
        if s == -1:
            break
        e = old.find('</script>', s)
        if e == -1:
            break
        scripts.append(old[s+8:e])
        pos = e + 9

    print(f"Found {len(scripts)} script blocks")

    # We need the first 4 blocks (excluding the 5th which was our new payment code)
    # Actually let's find them by content:
    lunar_core = None
    star_data = None
    ziwei_core = None
    interpretations = None
    app_code = None

    for s in scripts:
        if 'var LunarCore' in s:
            lunar_core = s
        elif 'var StarData' in s:
            star_data = s
        elif 'var ZiWeiCore' in s:
            ziwei_core = s
        elif 'var Interpretations' in s:
            interpretations = s
        elif 'var App' in s:
            app_code = s

    print(f"LunarCore: {len(lunar_core) if lunar_core else 'NOT FOUND'}")
    print(f"StarData: {len(star_data) if star_data else 'NOT FOUND'}")
    print(f"ZiWeiCore: {len(ziwei_core) if ziwei_core else 'NOT FOUND'}")
    print(f"Interpretations: {len(interpretations) if interpretations else 'NOT FOUND'}")
    print(f"App: {len(app_code) if app_code else 'NOT FOUND'}")

    if not all([lunar_core, star_data, ziwei_core, interpretations, app_code]):
        print("ERROR: Missing required script blocks!")
        sys.exit(1)

    # Write the combined JS
    combined_js = (
        lunar_core + '\n' +
        star_data + '\n' +
        ziwei_core + '\n' +
        interpretations + '\n' +
        app_code
    )

    with open('_extracted_js.js', 'w', encoding='utf-8') as f:
        f.write(combined_js)
    print(f"Extracted JS written: {len(combined_js)} chars")

if __name__ == '__main__':
    main()
