"""
Smart Library Assistant - Comprehensive Seed Data Script
Seeds 105+ books across Fantasy, Dystopian, Mystery, Romance, Classics,
Self-Help, Habits, Productivity, Psychology, Philosophy, Finance, and Programming.
"""

from database import get_connection, init_db

def seed_database():
    init_db()
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("DELETE FROM book_relationships")
    cur.execute("DELETE FROM borrow_history")
    cur.execute("DELETE FROM users")
    cur.execute("DELETE FROM books")

    # Complete catalog of 105+ curated books
    books_data = [
        # --- 1-8: Fantasy Classics (Tolkien & Rowling) ---
        (1, "The Hobbit", "J.R.R. Tolkien", "Fantasy", 1937, "Bilbo Baggins embarks on an unexpected journey to reclaim the lost Dwarf Kingdom of Erebor from Smaug."),
        (2, "The Fellowship of the Ring", "J.R.R. Tolkien", "Fantasy", 1954, "Frodo Baggins inherits the One Ring and begins the peril-fraught pilgrimage to Mount Doom."),
        (3, "The Two Towers", "J.R.R. Tolkien", "Fantasy", 1954, "The fellowship is broken as war engulfs Rohan and Frodo guided by Gollum nears Mordor."),
        (4, "The Return of the King", "J.R.R. Tolkien", "Fantasy", 1955, "Aragorn embraces his royal destiny while the final battle for Middle-earth rages."),
        (5, "Harry Potter and the Philosopher's Stone", "J.K. Rowling", "Fantasy", 1997, "A young orphan discovers he is a wizard and attends Hogwarts School of Witchcraft and Wizardry."),
        (6, "Harry Potter and the Chamber of Secrets", "J.K. Rowling", "Fantasy", 1998, "Harry returns to Hogwarts facing mysterious attacks that leave students petrified."),
        (7, "Harry Potter and the Prisoner of Azkaban", "J.K. Rowling", "Fantasy", 1999, "An escaped convict hunts Harry as dark Dementors guard the school grounds."),
        (8, "Harry Potter and the Goblet of Fire", "J.K. Rowling", "Fantasy", 2000, "Harry is mysteriously entered into the deadly Triwizard Tournament."),

        # --- 9-13: Dystopian & Political Fiction ---
        (9, "The Hunger Games", "Suzanne Collins", "Dystopian", 2008, "Katniss Everdeen volunteers to take her sister's place in the Capitol's televised death tournament."),
        (10, "Catching Fire", "Suzanne Collins", "Dystopian", 2009, "Katniss and Peeta become targets of the Capitol as a rebellion sparks across the districts."),
        (11, "Mockingjay", "Suzanne Collins", "Dystopian", 2010, "Katniss becomes the symbol of revolution in the all-out war against President Snow."),
        (12, "1984", "George Orwell", "Dystopian", 1949, "Winston Smith rebels against totalitarian surveillance and omnipresent Big Brother in Oceania."),
        (13, "Animal Farm", "George Orwell", "Political Fiction", 1945, "Farm animals overthrow their human master only to slide into an equally oppressive totalitarian regime."),

        # --- 14-18: Romance & Classics ---
        (14, "Pride and Prejudice", "Jane Austen", "Romance", 1813, "Elizabeth Bennet navigates manners, upbringing, and pride alongside the aristocratic Mr. Darcy."),
        (15, "Sense and Sensibility", "Jane Austen", "Romance", 1811, "The Dashwood sisters experience love and heartbreak in early 19th-century England."),
        (16, "Emma", "Jane Austen", "Romance", 1815, "The clever and self-satisfied Emma Woodhouse meddles in the romantic affairs of her neighbors."),
        (17, "The Great Gatsby", "F. Scott Fitzgerald", "Classic", 1925, "Jay Gatsby pursues his obsessive love for Daisy Buchanan amidst the roaring Jazz Age excess."),
        (18, "To Kill a Mockingbird", "Harper Lee", "Classic", 1960, "Scout Finch watches her father Atticus defend an innocent black man accused of a terrible crime."),

        # --- 19-24: Fiction, Historical & Contemporary Romance ---
        (19, "The Alchemist", "Paulo Coelho", "Fiction", 1988, "Andalusian shepherd boy Santiago journeys across Egyptian deserts in search of his Personal Legend."),
        (20, "The Kite Runner", "Khaled Hosseini", "Historical Fiction", 2003, "Amir seeks redemption for betraying his childhood friend amidst Kabul's turbulent history."),
        (21, "A Thousand Splendid Suns", "Khaled Hosseini", "Historical Fiction", 2007, "Two Afghan women from different generations forge a bond of survival across three decades of war."),
        (22, "The Book Thief", "Markus Zusak", "Historical Fiction", 2005, "Narrated by Death, a young girl in Nazi Germany shares stolen books with her foster family and a hidden Jew."),
        (23, "The Fault in Our Stars", "John Green", "Romance", 2012, "Two teenage cancer patients meet at a support group and embark on a poignant journey to Amsterdam."),
        (24, "Looking for Alaska", "John Green", "Romance", 2005, "Miles Halter heads to boarding school in search of the Great Perhaps and meets the enigmatic Alaska Young."),

        # --- 25-30: Mystery & Thriller ---
        (25, "The Da Vinci Code", "Dan Brown", "Mystery", 2003, "Symbologist Robert Langdon unravels codes hidden in Leonardo da Vinci paintings to solve a Louvre murder."),
        (26, "Angels & Demons", "Dan Brown", "Mystery", 2000, "Robert Langdon races across Rome to prevent an ancient brotherhood from detonating an antimatter bomb."),
        (27, "Inferno", "Dan Brown", "Mystery", 2013, "Robert Langdon awakens in Florence with amnesia, racing to stop a plague inspired by Dante's Inferno."),
        (28, "Sherlock Holmes: A Study in Scarlet", "Arthur Conan Doyle", "Mystery", 1887, "Dr. John Watson first meets the brilliant consulting detective Sherlock Holmes."),
        (29, "The Adventures of Sherlock Holmes", "Arthur Conan Doyle", "Mystery", 1892, "Twelve classic detective cases featuring Holmes and Watson in Victorian London."),
        (30, "The Picture of Dorian Gray", "Oscar Wilde", "Classic", 1890, "A handsome young aristocrat trades his soul to keep his youth while his portrait ages in his place."),

        # --- 31-42: Self-Help, Habits, Productivity & Mindfulness ---
        (31, "Ikigai: The Japanese Secret to a Long and Happy Life", "Héctor García & Francesc Miralles", "Self-Help", 2016, "Exploring the intersection of passion, mission, vocation, and profession practiced in Okinawa."),
        (32, "Atomic Habits", "James Clear", "Habits", 2018, "An actionable framework for improving every day through tiny 1% daily habits and habit stacking."),
        (33, "The Power of Habit", "Charles Duhigg", "Habits", 2012, "The science behind habit loops—cue, routine, reward—and how individuals and businesses transform them."),
        (34, "Deep Work", "Cal Newport", "Productivity", 2016, "Rules for focused success in a distracted world to master hard tasks and produce peak value."),
        (35, "Digital Minimalism", "Cal Newport", "Productivity", 2019, "A philosophy for choosing a focused life in an increasingly noisy, technology-addicted world."),
        (36, "The 7 Habits of Highly Effective People", "Stephen R. Covey", "Self-Help", 1989, "A principle-centered approach for solving personal and professional challenges."),
        (37, "Think and Grow Rich", "Napoleon Hill", "Personal Development", 1937, "Thirteen principles of personal achievement distilled from studying over 500 self-made tycoons."),
        (38, "The Power of Now", "Eckhart Tolle", "Mindfulness", 1997, "A guide to spiritual enlightenment that emphasizes living fully in the present moment."),
        (39, "The Alchemist: Illustrated Edition", "Paulo Coelho", "Personal Growth", 1993, "The inspiring philosophical fable on listening to one's heart and following destiny."),
        (40, "The Monk Who Sold His Ferrari", "Robin Sharma", "Self-Help", 1997, "A high-powered attorney undergoes a spiritual crisis and journeys into the Himalayas for wisdom."),
        (41, "Who Will Cry When You Die?", "Robin Sharma", "Personal Development", 1999, "101 life lessons on finding balance, meaning, and leaving a lasting legacy."),
        (42, "The 5 AM Club", "Robin Sharma", "Productivity", 2018, "Own your morning, elevate your life through a transformative early-morning routine."),

        # --- 43-47: Finance & Philosophy ---
        (43, "The Psychology of Money", "Morgan Housel", "Finance", 2020, "Timeless lessons on wealth, greed, and happiness exploring how human psychology dictates financial behavior."),
        (44, "Rich Dad Poor Dad", "Robert T. Kiyosaki", "Finance", 1997, "Contrasting two mindsets about money, investing, building assets, and financial literacy."),
        (45, "Man's Search for Meaning", "Viktor E. Frankl", "Philosophy", 1946, "Psychiatrist Viktor Frankl's account of surviving Nazi concentration camps and founding logotherapy."),
        (46, "The Subtle Art of Not Giving a F*ck", "Mark Manson", "Self-Help", 2016, "A counterintuitive approach to living a good life by choosing the struggles worth caring about."),
        (47, "Everything Is F*cked", "Mark Manson", "Philosophy", 2019, "A book about hope, examining religion, politics, money, and our modern existential anxieties."),

        # --- 48-52: Psychology & Human Nature ---
        (48, "Mindset: The New Psychology of Success", "Carol S. Dweck", "Psychology", 2006, "How our beliefs about our abilities—growth mindset vs fixed mindset—shape achievement."),
        (49, "Grit: The Power of Passion and Perseverance", "Angela Duckworth", "Psychology", 2016, "Why passion and long-term perseverance count more than raw talent in reaching excellence."),
        (50, "The Mountain Is You", "Brianna Wiest", "Personal Growth", 2020, "Transforming self-sabotage into self-mastery by addressing emotional triggers."),
        (51, "The 48 Laws of Power", "Robert Greene", "Psychology", 1998, "A pragmatic synthesis of 3,000 years of power dynamics drawn from Machiavelli, Sun Tzu, and history."),
        (52, "The Laws of Human Nature", "Robert Greene", "Psychology", 2018, "Decoding human drives, emotional biases, shadow impulses, and social dynamics."),

        # --- 53-60: Mindset & Productivity Classics ---
        (53, "Think Like a Monk", "Jay Shetty", "Self-Help", 2020, "Train your mind for peace and purpose every day through timeless Vedic monastic wisdom."),
        (54, "The Compound Effect", "Darren Hardy", "Personal Development", 2010, "Jumpstarting your income, your life, and your success through small consistent daily actions."),
        (55, "Make Your Bed", "William H. McRaven", "Self-Help", 2017, "Little things that can change your life and maybe the world, from Navy SEAL training."),
        (56, "Essentialism: The Disciplined Pursuit of Less", "Greg McKeown", "Productivity", 2014, "Focusing only on what is essential to make the highest possible contribution."),
        (57, "Eat That Frog!", "Brian Tracy", "Productivity", 2001, "21 great ways to stop procrastinating and get more done in less time."),
        (58, "The One Thing", "Gary Keller & Jay Papasan", "Productivity", 2013, "The surprisingly simple truth behind extraordinary results through focused prioritization."),
        (59, "Limitless", "Jim Kwik", "Personal Development", 2020, "Upgrade your brain, learn anything faster, and unlock your exceptional life."),
        (60, "The Courage to Be Disliked", "Ichiro Kishimi & Fumitake Koga", "Psychology", 2013, "The Japanese phenomenon showing you how to free yourself, change your life, and achieve real happiness."),

        # --- 61-75: Mindset, Motivation & Stoicism ---
        (61, "The Let Them Theory", "Mel Robbins", "Self-Help", 2024, "A life-changing framework for releasing control over others and reclaiming inner peace."),
        (62, "The 10X Rule", "Grant Cardone", "Personal Development", 2011, "The only difference between success and failure is taking 10 times more massive action."),
        (63, "Can't Hurt Me", "David Goggins", "Mindset", 2018, "Master your mind and defy the odds: the raw autobiography of Navy SEAL David Goggins."),
        (64, "Never Finished", "David Goggins", "Mindset", 2022, "Unshackle your mind and win the war within: advanced mental conditioning."),
        (65, "The Magic of Thinking Big", "David J. Schwartz", "Self-Help", 1959, "Achieve financial security and power by thinking beyond small limitations."),
        (66, "As a Man Thinketh", "James Allen", "Philosophy", 1903, "Classic essay demonstrating how thoughts shape character, health, circumstances, and destiny."),
        (67, "The Secret", "Rhonda Byrne", "Mindfulness", 2006, "The law of attraction: how focused visualization and thought attract prosperity and health."),
        (68, "The Power of Your Subconscious Mind", "Joseph Murphy", "Mindset", 1963, "Unlock the limitless spiritual and psychological power residing in your subconscious mind."),
        (69, "You Are a Badass", "Jen Sincero", "Personal Growth", 2013, "How to stop doubting your greatness and start living an awesome, self-directed life."),
        (70, "You Are a Badass at Making Money", "Jen Sincero", "Finance", 2017, "Overcome money blocks, master the mindset of wealth, and build financial freedom."),
        (71, "101 Essays That Will Change the Way You Think", "Brianna Wiest", "Personal Growth", 2016, "Reflections on emotional intelligence, self-awareness, and cognitive restructuring."),
        (72, "The Things You Can See Only When You Slow Down", "Haemin Sunim", "Mindfulness", 2012, "Zen Buddhist teachings on being calm in a busy, frantic world."),
        (73, "Good Vibes, Good Life", "Vex King", "Self-Help", 2018, "How self-love is the key to unlocking your greatness and cultivating high vibrations."),
        (74, "The Art of Happiness", "Dalai Lama & Howard C. Cutler", "Mindfulness", 1998, "A handbook for living combining Buddhist spiritual practice with Western psychiatry."),
        (75, "The Four Agreements", "Don Miguel Ruiz", "Philosophy", 1997, "Toltec wisdom guide to personal freedom: be impeccable with your word, take nothing personally."),

        # --- 76-88: Stoicism, Timeless Strategy & Influence ---
        (76, "The Untethered Soul", "Michael A. Singer", "Mindfulness", 2007, "The journey beyond yourself: freeing consciousness from habitual thought patterns."),
        (77, "The Daily Stoic", "Ryan Holiday & Stephen Hanselman", "Philosophy", 2016, "366 meditations on wisdom, perseverance, and the art of living from Marcus Aurelius and Seneca."),
        (78, "Ego Is the Enemy", "Ryan Holiday", "Philosophy", 2016, "The fight to master our greatest internal opponent on the path to success and mastery."),
        (79, "Stillness Is the Key", "Ryan Holiday", "Philosophy", 2019, "Drawing on Stoicism and Buddhism to find inner tranquility in an overwhelming world."),
        (80, "The Obstacle Is the Way", "Ryan Holiday", "Philosophy", 2014, "The timeless art of turning adversity into triumph drawn from Marcus Aurelius."),
        (81, "Meditations", "Marcus Aurelius", "Philosophy", 180, "The intimate private journal of the Roman Emperor on duty, mortality, and Stoic virtue."),
        (82, "The Art of War", "Sun Tzu", "Philosophy", -500, "Ancient Chinese military treatise on strategic advantage, patience, and victory."),
        (83, "How to Win Friends and Influence People", "Dale Carnegie", "Self-Help", 1936, "Timeless advice on interpersonal relationships, leadership, and winning people to your way."),
        (84, "How to Stop Worrying and Start Living", "Dale Carnegie", "Self-Help", 1948, "Practical techniques to conquer worry, fatigue, and stress in everyday life."),
        (85, "The 5 Second Rule", "Mel Robbins", "Productivity", 2017, "Transform your life, work, and confidence with everyday courage by counting down 5-4-3-2-1."),
        (86, "The High 5 Habit", "Mel Robbins", "Self-Help", 2021, "Take control of your life with one simple habit of positive self-affirmation."),
        (87, "Feel the Fear and Do It Anyway", "Susan Jeffers", "Self-Help", 1987, "Dynamic techniques for turning fear, indecision, and anger into power and action."),
        (88, "The Gifts of Imperfection", "Brené Brown", "Personal Growth", 2010, "Let go of who you think you're supposed to be and embrace who you are."),

        # --- 89-100: Productivity, Creativity & Focus ---
        (89, "Daring Greatly", "Brené Brown", "Personal Growth", 2012, "How the courage to be vulnerable transforms the way we live, love, parent, and lead."),
        (90, "The Happiness Advantage", "Shawn Achor", "Psychology", 2010, "Seven principles of positive psychology that fuel success and performance at work."),
        (91, "Drive: The Surprising Truth About What Motivates Us", "Daniel H. Pink", "Productivity", 2009, "Why autonomy, mastery, and purpose drive human motivation rather than rewards."),
        (92, "The Willpower Instinct", "Kelly McGonigal", "Psychology", 2011, "How self-control works, why it matters, and what you can do to get more of it."),
        (93, "The Productivity Project", "Chris Bailey", "Productivity", 2016, "Accomplishing more by managing your time, attention, and energy."),
        (94, "Getting Things Done", "David Allen", "Productivity", 2001, "The art of stress-free productivity: a complete organization and workflow system."),
        (95, "The Now Habit", "Neil Fiore", "Productivity", 1989, "A strategic program for overcoming procrastination and enjoying guilt-free play."),
        (96, "The 80/20 Principle", "Richard Koch", "Productivity", 1997, "Achieving more with less by focusing on the 20% of efforts generating 80% of results."),
        (97, "Do the Work", "Steven Pressfield", "Productivity", 2011, "Overcoming resistance and getting out of your own way to produce creative projects."),
        (98, "The War of Art", "Steven Pressfield", "Productivity", 2002, "Break through blocks and win inner creative battles against procrastination."),
        (99, "Show Your Work!", "Austin Kleon", "Creativity", 2014, "10 ways to share your creativity and get discovered in the digital age."),
        (100, "Steal Like an Artist", "Austin Kleon", "Creativity", 2012, "10 things nobody told you about being creative and finding your artistic voice."),

        # --- 101-105: Sci-Fi, History, Tech & Fantasy Favorites ---
        (101, "Dune", "Frank Herbert", "Sci-Fi", 1965, "Paul Atreides leads desert warriors on the harsh planet Arrakis fighting for spice."),
        (102, "Foundation", "Isaac Asimov", "Sci-Fi", 1951, "Mathematician Hari Seldon creates psychohistory to preserve galactic knowledge."),
        (103, "Sapiens: A Brief History of Humankind", "Yuval Noah Harari", "History", 2011, "A survey of human history from the stone age cognitive revolution to the modern era."),
        (104, "Clean Code", "Robert C. Martin", "Programming", 2008, "A handbook of agile software craftsmanship for writing readable, maintainable software."),
        (105, "Percy Jackson & The Lightning Thief", "Rick Riordan", "Fantasy", 2005, "A teenager discovers he is a demigod son of Poseidon and embarks on a mythological quest.")
    ]

    cur.executemany("INSERT INTO books (id, title, author, category, year, description) VALUES (?, ?, ?, ?, ?, ?)", books_data)

    # 50 Simulated Readers
    users = [(i, f"Reader {i}") for i in range(1, 51)]
    cur.executemany("INSERT INTO users (id, name) VALUES (?, ?)", users)

    # Realistic Borrowing Records to create natural co-borrowing clusters
    borrows = []
    
    # Cluster 1: Fantasy / Tolkien & Harry Potter readers (Users 1-15)
    for u in range(1, 10):
        borrows.extend([(u, 1), (u, 2), (u, 3), (u, 4)]) # Tolkien books
    for u in range(3, 12):
        borrows.extend([(u, 5), (u, 6), (u, 7), (u, 8)]) # Harry Potter books
    for u in range(5, 14):
        borrows.extend([(u, 1), (u, 5), (u, 105)])       # The Hobbit + HP 1 + Percy Jackson

    # Cluster 2: Dystopian readers (Users 10-18)
    for u in range(10, 18):
        borrows.extend([(u, 9), (u, 10), (u, 11), (u, 12), (u, 13)]) # Hunger Games + 1984 + Animal Farm

    # Cluster 3: Classics & Romance (Users 15-22)
    for u in range(15, 23):
        borrows.extend([(u, 14), (u, 15), (u, 16), (u, 17), (u, 18), (u, 30)]) # Austen, Gatsby, Mockingbird

    # Cluster 4: Mystery & Thriller (Users 20-28)
    for u in range(20, 28):
        borrows.extend([(u, 25), (u, 26), (u, 27), (u, 28), (u, 29)]) # Dan Brown & Sherlock Holmes

    # Cluster 5: Habits & Productivity (Users 25-38)
    for u in range(25, 36):
        borrows.extend([(u, 32), (u, 33), (u, 34), (u, 35), (u, 56), (u, 58)]) # Atomic Habits, Duhigg, Newport, Essentialism
    for u in range(28, 40):
        borrows.extend([(u, 36), (u, 37), (u, 40), (u, 42), (u, 54)])          # 7 Habits, Think & Grow Rich, Sharma

    # Cluster 6: Stoicism & Philosophy (Users 35-46)
    for u in range(35, 47):
        borrows.extend([(u, 77), (u, 78), (u, 79), (u, 80), (u, 81), (u, 82)]) # Ryan Holiday, Marcus Aurelius, Sun Tzu

    # Cluster 7: Mindset, Motivation & Psychology (Users 38-50)
    for u in range(38, 49):
        borrows.extend([(u, 48), (u, 49), (u, 51), (u, 52), (u, 60)])          # Mindset, Grit, 48 Laws, Courage to be Disliked
    for u in range(40, 50):
        borrows.extend([(u, 63), (u, 64), (u, 83), (u, 85), (u, 86)])          # Goggins, Dale Carnegie, Mel Robbins

    # Cluster 8: Finance (Users 42-50)
    for u in range(42, 50):
        borrows.extend([(u, 43), (u, 44), (u, 70)])                             # Psychology of Money, Rich Dad, Jen Sincero

    borrow_tuples = [(u, b, "2026-02-15") for u, b in borrows]
    cur.executemany("INSERT INTO borrow_history (user_id, book_id, borrowed_at) VALUES (?, ?, ?)", borrow_tuples)

    # Build Graph Relationships
    # 1. Same Author (strength = 5.0)
    cur.execute("""
        INSERT OR IGNORE INTO book_relationships (book_id_1, book_id_2, relationship_type, strength)
        SELECT b1.id, b2.id, 'same_author', 5.0
        FROM books b1
        JOIN books b2 ON b1.author = b2.author AND b1.id != b2.id
    """)

    # 2. Same Category (strength = 3.0)
    cur.execute("""
        INSERT OR IGNORE INTO book_relationships (book_id_1, book_id_2, relationship_type, strength)
        SELECT b1.id, b2.id, 'same_category', 3.0
        FROM books b1
        JOIN books b2 ON b1.category = b2.category AND b1.id != b2.id
    """)

    # 3. Borrowed Together (strength = co_borrow_count * 1.5)
    cur.execute("""
        SELECT r1.book_id AS b1, r2.book_id AS b2, COUNT(DISTINCT r1.user_id) AS co_count
        FROM borrow_history r1
        JOIN borrow_history r2 ON r1.user_id = r2.user_id AND r1.book_id < r2.book_id
        GROUP BY r1.book_id, r2.book_id
        HAVING co_count >= 2
    """)
    co_borrows = cur.fetchall()

    for row in co_borrows:
        b1, b2, count = row["b1"], row["b2"], row["co_count"]
        strength = round(count * 1.5, 1)
        cur.execute("""
            INSERT OR REPLACE INTO book_relationships (book_id_1, book_id_2, relationship_type, strength)
            VALUES (?, ?, 'borrowed_together', ?)
        """, (b1, b2, strength))
        cur.execute("""
            INSERT OR REPLACE INTO book_relationships (book_id_1, book_id_2, relationship_type, strength)
            VALUES (?, ?, 'borrowed_together', ?)
        """, (b2, b1, strength))

    conn.commit()
    conn.close()
    print("Database seeded with 105+ curated books, borrowing transactions, and graph connections.")

if __name__ == "__main__":
    seed_database()
