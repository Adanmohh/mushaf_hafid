"""
Add sample data for Al-Fatiha (Chapter 1) to the database
"""

import sqlite3

def add_sample_data():
    """Add sample data for Al-Fatiha"""
    
    conn = sqlite3.connect("app/database/quran.db")
    cursor = conn.cursor()
    
    # Add a sample mushaf layout
    cursor.execute("""
        INSERT OR REPLACE INTO mushaf_layouts 
        (id, name, total_pages, lines_per_page, font_name)
        VALUES (1, 'Uthmani Standard', 604, 15, 'KFGQPC Uthmanic Script HAFS')
    """)
    
    # Add page 1
    cursor.execute("""
        INSERT OR REPLACE INTO pages 
        (id, mushaf_layout_id, page_number, image_url)
        VALUES (1, 1, 1, '/static/images/page_001.png')
    """)
    
    # Add lines for page 1
    for line_num in range(1, 8):
        cursor.execute("""
            INSERT OR REPLACE INTO lines 
            (id, page_id, line_number)
            VALUES (?, 1, ?)
        """, (line_num, line_num))
    
    # Al-Fatiha words with sample data
    fatiha_words = [
        # Line 1: Bismillah
        (1, 1, 1, 1, 1, "بِسْمِ", "In the name", "Bismi"),
        (2, 1, 2, 1, 1, "ٱللَّهِ", "of Allah", "Allahi"),
        (3, 1, 3, 1, 1, "ٱلرَّحْمَٰنِ", "the Most Gracious", "Ar-Rahmani"),
        (4, 1, 4, 1, 1, "ٱلرَّحِيمِ", "the Most Merciful", "Ar-Raheem"),
        
        # Line 2: Verse 2
        (5, 2, 1, 1, 2, "ٱلْحَمْدُ", "All praise", "Al-hamdu"),
        (6, 2, 2, 1, 2, "لِلَّهِ", "is for Allah", "lillahi"),
        (7, 2, 3, 1, 2, "رَبِّ", "Lord", "Rabbi"),
        (8, 2, 4, 1, 2, "ٱلْعَٰلَمِينَ", "of all the worlds", "Al-alameen"),
        
        # Line 3: Verse 3
        (9, 3, 1, 1, 3, "ٱلرَّحْمَٰنِ", "The Most Gracious", "Ar-Rahmani"),
        (10, 3, 2, 1, 3, "ٱلرَّحِيمِ", "the Most Merciful", "Ar-Raheem"),
        
        # Line 4: Verse 4
        (11, 4, 1, 1, 4, "مَٰلِكِ", "Master", "Maliki"),
        (12, 4, 2, 1, 4, "يَوْمِ", "of the Day", "yawmi"),
        (13, 4, 3, 1, 4, "ٱلدِّينِ", "of Judgment", "Ad-deen"),
        
        # Line 5: Verse 5
        (14, 5, 1, 1, 5, "إِيَّاكَ", "You alone", "Iyyaka"),
        (15, 5, 2, 1, 5, "نَعْبُدُ", "we worship", "na'budu"),
        (16, 5, 3, 1, 5, "وَإِيَّاكَ", "and You alone", "wa iyyaka"),
        (17, 5, 4, 1, 5, "نَسْتَعِينُ", "we ask for help", "nasta'een"),
        
        # Line 6: Verse 6
        (18, 6, 1, 1, 6, "ٱهْدِنَا", "Guide us", "Ihdina"),
        (19, 6, 2, 1, 6, "ٱلصِّرَٰطَ", "to the path", "As-sirata"),
        (20, 6, 3, 1, 6, "ٱلْمُسْتَقِيمَ", "that is straight", "Al-mustaqeem"),
        
        # Line 7: Verse 7
        (21, 7, 1, 1, 7, "صِرَٰطَ", "The path", "Sirata"),
        (22, 7, 2, 1, 7, "ٱلَّذِينَ", "of those", "allatheena"),
        (23, 7, 3, 1, 7, "أَنْعَمْتَ", "You have blessed", "an'amta"),
        (24, 7, 4, 1, 7, "عَلَيْهِمْ", "upon them", "alayhim"),
        (25, 7, 5, 1, 7, "غَيْرِ", "not", "ghayri"),
        (26, 7, 6, 1, 7, "ٱلْمَغْضُوبِ", "of those who earned Your anger", "Al-maghdoobi"),
        (27, 7, 7, 1, 7, "عَلَيْهِمْ", "upon them", "alayhim"),
        (28, 7, 8, 1, 7, "وَلَا", "and not", "wa la"),
        (29, 7, 9, 1, 7, "ٱلضَّآلِّينَ", "of those who went astray", "Ad-dalleen")
    ]
    
    # Insert words
    for word_data in fatiha_words:
        cursor.execute("""
            INSERT OR REPLACE INTO words 
            (id, line_id, word_position, surah_number, ayah_number, 
             word_text_uthmani, translation_en, transliteration_en)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, word_data)
    
    # QUL-style word positions - clean layout with proper spacing
    # Centered RTL layout with authentic line spacing
    word_positions = [
        # Line 1: بِسْمِ ٱللَّهِ ٱلرَّحْمَٰنِ ٱلرَّحِيمِ (Bismillah - centered)
        (1, 1, 1, 1, 1, 500, 60, 70, 40),   # بِسْمِ
        (2, 2, 1, 1, 1, 420, 60, 75, 40),   # ٱللَّهِ
        (3, 3, 1, 1, 1, 310, 60, 105, 40),  # ٱلرَّحْمَٰنِ
        (4, 4, 1, 1, 1, 220, 60, 85, 40),   # ٱلرَّحِيمِ
        
        # Line 2: ٱلْحَمْدُ لِلَّهِ رَبِّ ٱلْعَٰلَمِينَ (Verse 2)
        (5, 5, 1, 1, 2, 520, 120, 85, 40),  # ٱلْحَمْدُ
        (6, 6, 1, 1, 2, 450, 120, 65, 40),  # لِلَّهِ
        (7, 7, 1, 1, 2, 400, 120, 45, 40),  # رَبِّ
        (8, 8, 1, 1, 2, 280, 120, 115, 40), # ٱلْعَٰلَمِينَ
        
        # Line 3: ٱلرَّحْمَٰنِ ٱلرَّحِيمِ (Verse 3 - shorter, centered)
        (9, 9, 1, 1, 3, 430, 180, 105, 40), # ٱلرَّحْمَٰنِ
        (10, 10, 1, 1, 3, 315, 180, 85, 40), # ٱلرَّحِيمِ
        
        # Line 4: مَٰلِكِ يَوْمِ ٱلدِّينِ (Verse 4)
        (11, 11, 1, 1, 4, 460, 240, 75, 40), # مَٰلِكِ
        (12, 12, 1, 1, 4, 395, 240, 60, 40), # يَوْمِ
        (13, 13, 1, 1, 4, 305, 240, 85, 40), # ٱلدِّينِ
        
        # Line 5: إِيَّاكَ نَعْبُدُ وَإِيَّاكَ نَسْتَعِينُ (Verse 5)
        (14, 14, 1, 1, 5, 580, 300, 75, 40), # إِيَّاكَ
        (15, 15, 1, 1, 5, 500, 300, 75, 40), # نَعْبُدُ
        (16, 16, 1, 1, 5, 400, 300, 95, 40), # وَإِيَّاكَ
        (17, 17, 1, 1, 5, 280, 300, 115, 40), # نَسْتَعِينُ
        
        # Line 6: ٱهْدِنَا ٱلصِّرَٰطَ ٱلْمُسْتَقِيمَ (Verse 6)
        (18, 18, 1, 1, 6, 530, 360, 75, 40), # ٱهْدِنَا
        (19, 19, 1, 1, 6, 435, 360, 90, 40), # ٱلصِّرَٰطَ
        (20, 20, 1, 1, 6, 300, 360, 130, 40), # ٱلْمُسْتَقِيمَ
        
        # Line 7: صِرَٰطَ ٱلَّذِينَ أَنْعَمْتَ عَلَيْهِمْ (First part of Verse 7)
        (21, 21, 1, 1, 7, 580, 420, 80, 40), # صِرَٰطَ
        (22, 22, 1, 1, 7, 490, 420, 85, 40), # ٱلَّذِينَ
        (23, 23, 1, 1, 7, 390, 420, 95, 40), # أَنْعَمْتَ
        (24, 24, 1, 1, 7, 300, 420, 85, 40), # عَلَيْهِمْ
        
        # Line 8: غَيْرِ ٱلْمَغْضُوبِ عَلَيْهِمْ وَلَا ٱلضَّآلِّينَ (Rest of Verse 7)
        (25, 25, 1, 1, 7, 580, 480, 60, 40), # غَيْرِ
        (26, 26, 1, 1, 7, 460, 480, 115, 40), # ٱلْمَغْضُوبِ
        (27, 27, 1, 1, 7, 375, 480, 80, 40), # عَلَيْهِمْ
        (28, 28, 1, 1, 7, 320, 480, 50, 40), # وَلَا
        (29, 29, 1, 1, 7, 180, 480, 135, 40) # ٱلضَّآلِّينَ
    ]
    
    # Insert word positions
    for pos_data in word_positions:
        cursor.execute("""
            INSERT OR REPLACE INTO word_positions 
            (id, word_id, mushaf_layout_id, page_number, line_number, 
             x_coordinate, y_coordinate, width, height)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, pos_data)
    
    # Add sample recitation
    cursor.execute("""
        INSERT OR REPLACE INTO recitations 
        (id, reciter_name, style)
        VALUES (1, 'Abdul Basit Abdul Samad', 'Mujawwad')
    """)
    
    # Add sample audio timing data (simplified)
    audio_timings = []
    start_time = 0
    for word_id in range(1, 30):
        duration = 500 + (word_id * 100)  # Variable duration
        audio_timings.append((
            word_id, 1, start_time, start_time + duration, 
            f"/static/audio/001_{word_id:03d}_abdul_basit.mp3"
        ))
        start_time += duration + 200  # 200ms gap between words
    
    # Insert audio timings
    for timing_data in audio_timings:
        cursor.execute("""
            INSERT OR REPLACE INTO audio_timings 
            (word_id, recitation_id, start_time, end_time, audio_file_url)
            VALUES (?, ?, ?, ?, ?)
        """, timing_data)
    
    conn.commit()
    conn.close()
    
    print("Sample data for Al-Fatiha added successfully!")

if __name__ == "__main__":
    add_sample_data()