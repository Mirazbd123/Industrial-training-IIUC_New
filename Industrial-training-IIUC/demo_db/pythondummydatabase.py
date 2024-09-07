# -*- coding: utf-8 -*-

import sqlite3

# Connect to the database (or create it if it doesn't exist)
conn = sqlite3.connect('news_db.db')

# Create a cursor object to execute SQL commands
cursor = conn.cursor()

# Create a table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS news (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        category TEXT,
        title TEXT,
        time_author TEXT,
        paragraph TEXT,
        image_link TEXT,
        summary TEXT
    )
''')

# Insert the specified dummy data
dummy_data = [
    (
        'আইন ও বিচার', 
        'হত্যা মামলায় সালমান-আনিসুল-জিয়াউল ১০ দিনের রিমান্ডে', 
        'নয়া দিগন্ত অনলাইন\n২৪ আগস্ট ২০২৪, ২০:৪৮, আপডেট: ২৪ আগস্ট ২০২৪, ২১:১৬', 
        '''হত্যার পৃথক দুই মামলায় সাবেক প্রধানমন্ত্রী শেখ হাসিনার বেসরকারি শিল্প ও বিনিয়োগ বিষয়ক উপদেষ্টা সালমান এফ রহমান, সাবেক আইনমন্ত্রী আনিসুল হক ও সেনা কর্মকর্তা জিয়াউল আহসানের ৫ দিন করে ১০ দিনের রিমান্ড মঞ্জুর করেছেন আদালত।
        শনিবার (২৪ আগস্ট) সন্ধ্যা সাড়ে ৭টায় তাদেরকে আদালতে হাজির করে পুলিশ। এদিন মামলার সুষ্ঠু তদন্তের স্বার্থে তাকে ১০ দিনের রিমান্ডে নিতে আবেদন করেন তদন্ত কর্মকর্তা লালবাগ থানার সাব-ইন্সপেক্টর আক্কাস মিয়া। শুনানি শেষে ঢাকার মেট্রোপলিটন ম্যাজিস্ট্রেট মো: জসিমের আদালত তার এ রিমান্ড মঞ্জুর করেন।
        আদালত সূত্র জানায়, লালবাগ থানায় দায়ের করা আইডিয়াল কলেজ শিক্ষার্থী খালেদ সাইফুল্লাহ হত্যা মামলায় পাঁচ দিন এবং নিউ মার্কেট থানায় ঢাকা কলেজ শিক্ষার্থী সবুল আলী হত্যা মামলায় পাঁচ দিন রিমান্ড মঞ্জুর করেন আদালত।
        গত ১৩ আগস্ট গোপন তথ্যের ভিত্তিতে নৌপথে পলায়নরত অবস্থায় রাজধানীর সদরঘাট এলাকা থেকে সালমান এফ রহমান ও সাবেক আইনমন্ত্রী আনিসুল হককে গ্রেফতার করে পুলিশ। পরদিন নিউমার্কেট থানার হত্যা মামলায় তাদের ১০ দিনের রিমান্ড মঞ্জুর করেন আদালত। আর ১৫ আগস্ট গভীর রাতে ঢাকার খিলক্ষেত এলাকা থেকে জিয়াউল আহসানকে গ্রেফতার করা হয়। পরদিন তার আট দিনের রিমান্ড মঞ্জুর করেন আদালত।
        মামলার অভিযোগ থেকে জানা যায়, বৈষম্যবিরোধী ছাত্র আন্দোলনে গত ১৮ জুলাই লালবাগের আজিমপুর সরকারি আবাসিক এলাকায় আইডিয়াল কলেজের প্রথম বর্ষের ছাত্র খালিদ হাসান সাইফুল্লাহ গুলিবিদ্ধ হয়ে মারা যান। এ ঘটনায় তার বাবা কামরুল হাসান ১৯ আগস্ট লালবাগ থানায় একটি হত্যা মামলা দায়ের করেন।''',
        'https://www.dailynayadiganta.com/resources/img/article/202408/858166_155.jpg',
        None
    )
]

# Insert data into the table
cursor.executemany('''
    INSERT INTO news (category, title, time_author, paragraph, image_link, summary)
    VALUES (?, ?, ?, ?, ?, ?)
''', dummy_data)

# Commit the changes and close the connection
conn.commit()
conn.close()

print("Data inserted successfully!")
