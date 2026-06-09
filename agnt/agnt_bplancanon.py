
import math

books_data = [
    ("Genesis", 50),
    ("Exodus", 40),
    ("Leviticus", 27),
    ("Numbers", 36),
    ("Deuteronomy", 34),
    ("Joshua", 24),
    ("Judges", 21),
    ("Ruth", 4),
    ("1 Samuel", 31),
    ("2 Samuel", 24),
    ("1 Kings", 22),
    ("2 Kings", 25),
    ("1 Chronicles", 29),
    ("2 Chronicles", 36),
    ("Ezra", 10),
    ("Nehemiah", 13),
    ("Esther", 10),
    ("Job", 42),
    ("Psalms", 150),
    ("Proverbs", 31),
    ("Ecclesiastes", 12),
    ("Song of Solomon", 8),
    ("Isaiah", 66),
    ("Jeremiah", 52),
    ("Lamentations", 5),
    ("Ezekiel", 48),
    ("Daniel", 12),
    ("Hosea", 14),
    ("Joel", 3),
    ("Amos", 9),
    ("Obadiah", 1),
    ("Jonah", 4),
    ("Micah", 7),
    ("Nahum", 3),
    ("Habakkuk", 3),
    ("Zephaniah", 3),
    ("Haggai", 2),
    ("Zechariah", 14),
    ("Malachi", 4),
    ("Matthew", 28),
    ("Mark", 16),
    ("Luke", 24),
    ("John", 21),
    ("Acts", 28),
    ("Romans", 16),
    ("1 Corinthians", 16),
    ("2 Corinthians", 13),
    ("Galatians", 6),
    ("Ephesians", 6),
    ("Philippians", 4),
    ("Colossians", 4),
    ("1 Thessalonians", 5),
    ("2 Thessalonians", 3),
    ("1 Timothy", 6),
    ("2 Timothy", 4),
    ("Titus", 3),
    ("Philemon", 1),
    ("Hebrews", 13),
    ("James", 5),
    ("1 Peter", 5),
    ("2 Peter", 3),
    ("1 John", 5),
    ("2 John", 1),
    ("3 John", 1),
    ("Jude", 1),
    ("Revelation", 22),
]

months = [
    ("January", 31),
    ("February", 28),
    ("March", 31),
    ("April", 30),
    ("May", 31),
    ("June", 30),
    ("July", 31),
    ("August", 31),
    ("September", 30),
    ("October", 31),
    ("November", 30),
    ("December", 31),
]

all_chapters = []
first_five_books = set([b[0] for b in books_data[:5]])
short_books = set([b[0] for b in books_data if b[1] <= 4])

for book, count in books_data:
    for ch in range(1, count + 1):
        all_chapters.append((book, ch))

total_chapters = len(all_chapters)
current_chapter_idx = 0
day_of_year = 1
reading_plan = []

while current_chapter_idx < total_chapters and day_of_year <= 365:
    book, ch = all_chapters[current_chapter_idx]
    
    if book in first_five_books:
        count = 3
        end_idx = min(current_chapter_idx + count, total_chapters)
        day_chapters = all_chapters[current_chapter_idx:end_idx]
        current_chapter_idx = end_idx
    elif book == "Psalms" and ch == 119:
        day_chapters = [(book, ch)]
        current_chapter_idx += 1
    elif book in short_books:
        book_chapters = []
        while current_chapter_idx < total_chapters and all_chapters[current_chapter_idx][0] == book:
            book_chapters.append(all_chapters[current_chapter_idx])
            current_chapter_idx += 1
        day_chapters = book_chapters
    else:
        remaining_chapters = total_chapters - current_chapter_idx
        remaining_days = 365 - day_of_year + 1
        
        # Evenly distribute: 4 if we are ahead of 3/day
        count = 4 if (remaining_chapters / remaining_days) > 3.0 else 3
        
        # On the very last day, we MUST finish.
        if remaining_days == 1:
            count = remaining_chapters
            
        end_idx = min(current_chapter_idx + count, total_chapters)
        
        for i in range(current_chapter_idx, end_idx):
            b, c = all_chapters[i]
            if b in short_books and b != all_chapters[current_chapter_idx][0]:
                end_idx = i
                break
            if b == "Psalms" and c == 119:
                end_idx = i
                break
        
        day_chapters = all_chapters[current_chapter_idx:end_idx]
        current_chapter_idx = end_idx

    reading_plan.append((day_of_year, day_chapters))
    day_of_year += 1

# Generate monthly files...
current_day_in_year = 1
for month_name, days_in_month in months:
    month_filename = f"{month_name.lower()}.md"
    content = f"# {month_name} Reading Plan\n\n"
    content += "| Day | Reading |\n| :--- | :--- |\n"
    for day in range(1, days_in_month + 1):
        day_idx = current_day_in_year
        day_reading = next((chapters for d, chapters in reading_plan if d == day_idx), [])
        if not day_reading:
            reading_str = "No reading"
        else:
            grouped = {}
            for b, c in day_reading:
                if b not in grouped:
                    grouped[b] = []
                grouped[b].append(c)
            reading_parts = []
            for b in grouped:
                chaps = grouped[b]
                if len(chaps) == 1:
                    reading_parts.append(f"{b} {chaps[0]}")
                elif chaps[0] == min(chaps) and chaps[-1] == max(chaps) and len(chaps) == (max(chaps)-min(chaps)+1):
                    reading_parts.append(f"{b} {chaps[0]}-{chaps[-1]}")
                else:
                    reading_parts.append(f"{b} {', '.join(map(str, chaps))}")
            reading_str = ", ".join(reading_parts)
        content += f"| {day} | {reading_str} |\n"
        current_day_in_year += 1
    with open(month_filename, "w") as f:
        f.write(content)
