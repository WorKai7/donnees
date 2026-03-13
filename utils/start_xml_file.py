def start_file(file: str, title: str, link: str, desc: str):
    with open(f"../../rss/{file}", "w", encoding="utf-8") as rss:
        rss.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        rss.write('<rss version="2.0">\n')
        rss.write('    <channel>\n')
        rss.write(f'        <title>{title}</title>\n')
        rss.write(f'        <link>{link}</link>\n')
        rss.write(f'        <description>{desc}</description>\n')