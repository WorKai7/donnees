def end_file(file: str):
    with open(f"../../rss/{file}", "a", encoding="utf-8") as rss:
        rss.write('\n    </channel>\n')
        rss.write('</rss>\n')