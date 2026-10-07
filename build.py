#!/usr/bin/env python3
"""Static site generator for shakshuka.org — Tunisian-American community of the DMV.

Edit the data blocks (EVENTS, TEAM, TUNISIA, BLOG…) and page copy below, then:

    python3 build.py

Output goes to docs/ (served by GitHub Pages or any static host).
"""
import os, re, json, shutil, html, datetime as dt
from pathlib import Path

ROOT = Path(__file__).parent
OUT = ROOT / "docs"
TODAY = dt.date.today()

# Set SITE/BASE for the GitHub Pages preview: BASE=/shakshuka.org SITE=https://inestanitxr.github.io/shakshuka.org python3 build.py
SITE = os.environ.get("SITE", "https://www.shakshuka.org")
BASE = os.environ.get("BASE", "")  # path prefix when served from a sub-folder
ORG = "Shakshuka.org"
TAGLINE = "Reimagining community, one table at a time."
# [CHECK] Shakshuka needs its own address: the live site only lists the web designer's gmail.
CONTACT_EMAIL = "info@shakshuka.org"
# FormSubmit endpoint (free, no backend): first submission sends an activation email to CONTACT_EMAIL.
FORM_ACTION = f"https://formsubmit.co/{CONTACT_EMAIL}"
# Where "Donate" goes until a Zeffy/Givebutter page exists. [CHECK]
DONATE_URL = "/donate/"
SOCIALS = {  # [CHECK] none found publicly; fill in when they share handles
    # "instagram": "https://www.instagram.com/…",
    # "facebook": "https://www.facebook.com/…",
}

# ---------------------------------------------------------------- data ----

TEAM = [
    dict(name="Leila Chennoufi", role="President", img="team-leila",
         bio="Born in Tunisia and based in Washington, Leila has spent two decades in sustainability and diaspora work. She founded Shakshuka to give Tunisians of the DMV, and everyone who loves Tunisia, a place to reconnect through culture rather than politics."),
    dict(name="Nour Bouzouita", role="Secretary", img="team-nour",
         bio="Born in Tunisia, Nour works in economics and policy. She keeps the organization's records, runs membership and makes sure every newcomer gets a warm welcome."),
    dict(name="Aoufa Ezzine", role="Treasurer", img="team-aoufa",
         bio="An engineer by training with a career in international development, Aoufa is also a musician. She manages the books and leads the music behind our sing-alongs."),
    dict(name="Sadok Rouai", role="Board member", img="team-sadok",
         bio="Economist and banker with years at the Central Bank of Tunisia and the International Monetary Fund. Sadok brings institutional memory and a deep love of Tunisian history."),
    dict(name="Hella Akrout", role="Board member", img="team-hella",
         bio="Hella imports extra-virgin olive oil from her family's grove in Tunisia. She leads our food programs and the Tunisian cookbook project."),
    dict(name="Radhia Jihane Guizani", role="Board member", img="team-radhia",
         bio="A Cap Bon native passionate about dance, film and cuisine. Radhia curates our film screenings and cultural evenings."),
    dict(name="Raed Gnaoui", role="Board member", img="team-raed",
         bio="Born in the United States to Tunisian parents, Raed is a father and soccer enthusiast who makes sure the second generation sees itself in what we do."),
    dict(name="Ines Said", role="Board member", img="team-ines",
         bio="Immersive artist and XR technologist from Nabeul, founder of Tanit XR. Brings heritage, technology and the next generation to the table."),
]

# Events. Past ones are history (keep them, they show what we do). Set `tickets` and
# `reserve_url` for paid events (Zeffy/Eventbrite checkout), `free=True` for RSVP-only ones.
EVENTS = [
    # ---- upcoming (examples of the two reservation flows; set draft=False to publish) ----
    dict(slug="cooking-class-5-couscous", title="Cooking Class 5: Couscous & Mloukhia",
         date="2026-11-15", time="4:00 – 6:00 PM ET", venue="Online (Google Meet)", address="Link sent after registration",
         img="ev-cooking1", kind="Cooking class", draft=True,
         tickets=[("Cooking class", 25), ("Cooking class + support Shakshuka", 40)],
         reserve_url="https://www.zeffy.com/ticketing/EXAMPLE-replace-with-real-link",
         summary="Chef Salma Sellami returns with the dish every Tunisian Friday is built on.",
         body="""<p>Couscous is the Friday dish, the wedding dish, the dish your grandmother judges you on. In this live class Chef de cuisine Salma Sellami walks you through steaming couscous the traditional way, a lamb and vegetable stew, and the deep-green mloukhia that takes patience and rewards it.</p>
<p>You'll receive a shopping list and prep notes a week before. Recordings are shared with registered participants.</p>"""),
    dict(slug="tunisian-sing-along-winter", title="Winter Tunisian Sing-Along",
         date="2026-12-12", time="3:30 – 5:30 PM", venue="Tenley-Friendship Library", address="4450 Wisconsin Ave NW, Washington, DC 20016",
         img="ev-singalong", kind="Music", draft=True, free=True,
         summary="Malouf, Saliha, Lotfi Bouchnak and Hedi Jouini, with lyrics in Arabic, transliteration and English.",
         body="""<p>Bring your voice, your kids and your parents. Local Tunisian musicians lead an afternoon of classics, and we hand out lyric sheets in Arabic, transliteration and English so everyone can sing.</p>
<p>Free to attend in a public library. Donations welcome on the day.</p>"""),

    # ---- 2026 ----
    dict(slug="film-screening-promised-sky", title="Film Screening: Promised Sky",
         date="2026-06-25", time="8:00 PM", venue="The Avalon Theatre", address="5612 Connecticut Ave NW, Washington, DC 20015",
         img="ev-promised-sky", kind="Film", tickets=[("General admission", 18), ("General admission + contribution", 28)],
         summary="Erige Sehiri's film about three Ivorian women building a life in Tunisia.",
         body="""<p>French-Tunisian director Erige Sehiri follows Marie, a pastor and former journalist, Naney and Jolie as they take in Kenza, a young shipwreck survivor. A story of sisterhood and endurance that looks squarely at the discrimination sub-Saharan migrants face in Tunisia today.</p>"""),
    dict(slug="a-love-affair-with-tunisia", title="A Love Affair with Tunisia: A Lifetime of Discovery",
         date="2026-05-31", time="10:30 AM", venue="Launch Workplaces", address="2201 Wisconsin Ave NW #200, Washington, DC 20007",
         img="hallets", kind="Talk", free=True,
         summary="Judith Dwan Hallet and Stanley Hallet on six decades of Tunisia, the Amazigh and the kitchen.",
         body="""<p>Documentary filmmaker Judith Dwan Hallet (fifty years of films, including for National Geographic) and architect-photographer Stanley Hallet shared the heartbeat of the Amazigh people through six decades of photographs, stories and recipes. The pair co-created <a href="/cookbook/">Discovering Tunisian Cuisine</a>.</p>"""),
    dict(slug="fashioning-power-fashioning-peace-2026", title="Fashioning Power, Fashioning Peace 2026",
         date="2026-05-02", time="10:00 AM – 5:00 PM", venue="Woodrow Wilson House", address="2340 S St NW, Washington, DC 20008",
         img="ev-fpfp-2026", kind="Exhibition", tickets=[("Exhibit ticket", 20)],
         summary="Third annual exhibition with the Embassy of Tunisia: garments that tell stories of power and peace.",
         body="""<p>For the third year Shakshuka partnered with the Embassy of Tunisia on this exhibition at the Woodrow Wilson House, where garments from around the world explore the intersection of fashion, diplomacy and heritage. The Tunisian piece, a hand-embroidered <em>farmla</em> worked in gold thread, was loaned by a member of our community.</p>"""),
    dict(slug="where-the-wind-comes-from", title="Free Film Screening: Where the Wind Comes From",
         date="2026-03-30", time="6:30 – 8:30 PM", venue="Embassy of France", address="4101 Reservoir Rd NW, Washington, DC 20007",
         img="ev-wind", kind="Film", free=True,
         summary="Amel Guellaty's debut: two friends on a road trip to the Tunisian south, chasing a way out.",
         body="""<p>Alyssa and Mehdi set off for southern Tunisia to enter a competition that could change everything. Director Amel Guellaty's first feature mixes road movie and daydream to show a corner of Tunisia rarely seen on screen. The screening at the Embassy of France was followed by a conversation with the filmmaker.</p>"""),
    dict(slug="iftar-2026", title="2026 Iftar Dinner and Celebration",
         date="2026-03-07", time="5:45 – 9:30 PM", venue="Phoenicia", address="2236 Gallows Rd, Vienna, VA 22182",
         img="ev-iftar-2026", kind="Dinner", tickets=[("Ramadan dinner & celebration", 78)],
         summary="Our annual Iftar: lentil soup, mezze, live music, and everyone welcome regardless of faith.",
         body="""<p>Each Ramadan we break the fast together. The 2026 Iftar brought more than a hundred guests to Phoenicia for lentil soup, mohammara and baba ghanouj, fattoush, falafel and grilled mains, followed by live music. As always, the table was open to everyone, whatever their background or belief.</p>"""),
    dict(slug="tunisian-sing-along-tenleytown", title="Tunisian Sing-Along in Tenleytown",
         date="2026-01-03", time="3:30 – 5:30 PM", venue="Tenley-Friendship Library", address="4450 Wisconsin Ave NW, Washington, DC 20016",
         img="ev-singalong", kind="Music", free=True,
         summary="Lotfi Bouchnak, Saliha, Sadok Thraya and Malouf classics, sung together with lyric sheets.",
         body="""<p>Local Tunisian artists led an afternoon of classics with lyric sheets in Arabic, transliteration and English. Free in a public library, pay-what-you-wish donations welcome.</p>"""),
    # ---- 2025 ----
    dict(slug="fashioning-power-fashioning-peace-2025", title="Fashioning Power, Fashioning Peace 2025",
         date="2025-05-08", time="May 8 – 10", venue="Woodrow Wilson House", address="2340 S St NW, Washington, DC 20008",
         img="ev-fpfp-2025", kind="Exhibition", tickets=[("Exhibit ticket", 20)],
         summary="Second annual exhibition with the Embassy of Tunisia, during EU Embassy Open House weekend.",
         body="""<p>Shakshuka sponsored the Tunisian garment in the second edition: a traditional farmla with handmade embroidery and golden threads, contributed by a member of the community. Guided tours Thursday and Friday, open house Saturday.</p>"""),
    dict(slug="aicha-dc-film-festival", title="Aicha at the DC International Film Festival",
         date="2025-05-01", time="May 1 & 2, 6:00 PM", venue="Arabian Sights Film Festival", address="701 7th St NW, Washington, DC 20001",
         img="ev-aicha", kind="Film",
         summary="Shakshuka sponsored Mehdi M. Barsaoui's Aicha and brought the director to DC for both nights.",
         body="""<p>Aya, trapped in debt and dead-end jobs in southern Tunisia, is presumed dead after an accident and seizes the chance to disappear. Shakshuka sponsored the film's two screenings at the 30th Arabian Sights Film Festival and hosted director Mehdi M. Barsaoui for post-screening conversations.</p>"""),
    dict(slug="iftar-2025", title="Iftar Dinner and Celebration 2025",
         date="2025-03-23", time="7:00 PM", venue="Láylí Mediterranean", address="3033 Wilson Blvd, Arlington, VA 22201",
         img="ev-iftar-2026", kind="Dinner", tickets=[("Dinner", 78)],
         summary="Family-style Iftar in Arlington, in the spirit of community and inclusivity.",
         body="""<p>Our first large Iftar: family-style Mediterranean dishes, Tunisian sweets, and a room full of people meeting each other for the first time.</p>"""),
    dict(slug="under-the-fig-trees", title="Film Screening: Under the Fig Trees",
         date="2025-03-06", time="7:30 PM", venue="The Avalon Theatre", address="5612 Connecticut Ave NW, Washington, DC 20015",
         img="ev-fig-trees", kind="Film", tickets=[("General admission", 18)],
         summary="Erige Sehiri's luminous day among young fig harvesters in the Tunisian north-west.",
         body="""<p>One summer day in an orchard, young women and men harvesting figs flirt, argue and dream. Selected for Cannes Directors' Fortnight, the film is a portrait of a Tunisia far from the capital.</p>"""),
    dict(slug="cooking-class-4-lablabi", title="Cooking Class 4: Lablabi",
         date="2025-01-12", time="4:30 PM ET", venue="Online (Google Meet)", address="",
         img="ev-lablabi", kind="Cooking class", tickets=[("Cooking class", 25)],
         summary="The chickpea soup that every Tunisian city claims as its own.",
         body="""<p>Chef Salma Sellami taught the fourth online class: lablabi with day-old bread, cumin, harissa, a soft egg and tuna, the way it is eaten in Tunis at dawn.</p>"""),
    # ---- 2024 ----
    dict(slug="the-man-behind-the-microphone", title="Film & Sing-Along: The Man Behind the Microphone",
         date="2024-12-07", time="6:00 – 9:00 PM", venue="Imagination Stage", address="4908 Auburn Ave, Bethesda, MD 20814",
         img="ev-hedi-jouini", kind="Film & music",
         summary="Claire Belhassine's documentary on Hedi Jouini, followed by his greatest hits sung together.",
         body="""<p>Hedi Jouini has been called the Frank Sinatra of Tunisia. The film by his granddaughter Claire Belhassine traces a life of songs that every Tunisian knows; afterwards local musicians led the room through them.</p>"""),
    dict(slug="cooking-class-3-keftagi", title="Cooking Class 3: Keftagi and Bread",
         date="2024-12-01", time="10:00 AM ET", venue="Online (Google Meet)", address="",
         img="ev-cooking3", kind="Cooking class", tickets=[("Cooking class", 25)],
         summary="Fried summer vegetables chopped with harissa and eggs, and the bread to scoop them.",
         body="""<p>Keftagi is street food from the Sahel: fried peppers, tomatoes, potatoes and squash chopped fine with eggs and harissa. Chef Salma Sellami showed the technique and a quick Tunisian bread to go with it.</p>"""),
    dict(slug="calligraphy-workshop", title="Arabic Calligraphy Workshop with Khalil Ayed",
         date="2024-11-16", time="2:30 – 4:00 PM", venue="Residence of Ambassador Hanène Tajouri Bessassi", address="Washington, DC",
         img="ev-calligraphy", kind="Workshop", tickets=[("Workshop + name art by Khalil", 45)],
         summary="Classical styles to calligraffiti, hosted by Tunisia's ambassador to the United States.",
         body="""<p>Tunisian artist and New York creative director Khalil Ayed introduced the major calligraphic styles and the modern fusion known as calligraffiti, then guided everyone through writing their own words. Each participant left with a personalised name piece signed by the artist.</p>"""),
    dict(slug="cooking-class-2-fricasse", title="Cooking Class 2: Fricassé and Hsou",
         date="2024-11-03", time="4:30 PM ET", venue="Online (Google Meet)", address="",
         img="ev-cooking2", kind="Cooking class", tickets=[("Cooking class", 25)],
         summary="The fried sandwich of every Tunisian beach, and the spicy semolina soup for the first cold day.",
         body="""<p>Fricassé, the little fried roll stuffed with tuna, potato, olives and harissa, and hsou, the thin semolina soup with capers and cumin.</p>"""),
    dict(slug="babaziz", title="Film Screening: Bab'Aziz, The Prince Who Contemplated His Soul",
         date="2024-10-17", time="7:30 – 10:00 PM", venue="The Avalon Theatre", address="5612 Connecticut Ave NW, Washington, DC 20015",
         img="ev-babaziz", kind="Film", tickets=[("General admission", 18)],
         summary="Nacer Khemir's Sufi fable of a blind dervish and his granddaughter crossing the desert.",
         body="""<p>A blind dervish, Bab'Aziz, and his spirited granddaughter Ishtar cross the desert in search of a gathering of dervishes held once every thirty years. Our first film evening at the Avalon sold out.</p>"""),
    dict(slug="cooking-class-1-shan-tounsi", title="Cooking Class 1: S'han Tounsi & Olive Bread",
         date="2024-09-29", time="10:00 AM – 12:00 PM ET", venue="Online (Google Meet)", address="",
         img="ev-cooking1", kind="Cooking class", tickets=[("Cooking class", 25)],
         summary="Our very first class: the Tunisian plate of shakshuka, mabsout bread and yoyo doughnuts.",
         body="""<p>Chef de cuisine Salma Sellami launched the series with the <em>assiette tunisienne</em>: bread mabsout, shakshuka and yoyo, plus a history of the spices that make Tunisian food taste the way it does.</p>"""),
]

BLOG = [
    dict(title="Recipes of Resilience: When Everything's Falling Apart, Except Dinner", date="2025-10-10", author="Ella Schonberger",
         img="blog-couscous", caption="Making couscous from scratch at the Kairouan Couscous Festival, 2025",
         summary="A new series of comfort recipes, starting with the classic couscous and lamb stew (2 hours, serves 6 to 8) and the story of a husband who took over the kitchen after three dinners without red sauce.",
         url="https://www.shakshuka.org/post/recipes-of-resilience-when-everything-s-falling-apart-except-dinner"),
    dict(title="Harissa Arbi from the Shakshuka Test Kitchen", date="2025-05-08", author="Ella Schonberger",
         img="harissa-sm", caption="Harissa. Photo: Jules, CC BY 3.0",
         summary="Making the reigning condiment of Tunisian cooking in an American kitchen, with guajillo, puya and árbol chilis standing in for baklouti.",
         url="https://www.shakshuka.org/post/harissa-arbi-from-the-shakshuka-test-kitchen"),
    dict(title="Spice, Memory and Migration: the History of Tunisia's Red Gold", date="2025-05-07", author="Ella Schonberger",
         img="ojja-sm", caption="Ojja. Photo: Una723, CC BY 4.0",
         summary="How baklouti peppers, garlic, olive oil and salt became harissa, and how harissa travelled with every Tunisian who left.",
         url="https://www.shakshuka.org/post/spice-memory-and-migration-the-history-of-tunisia-s-red-gold"),
    dict(title="Diplomacy and Style: Shakshuka at Fashioning Power, Fashioning Peace", date="2025-04-15", author="Mark Guenther",
         img="blog-framla", caption="The exhibition at the Woodrow Wilson House",
         summary="Why we sponsored the Tunisian farmla in the Woodrow Wilson House exhibition, and how to visit.",
         url="https://www.shakshuka.org/post/step-into-a-world-of-diplomacy-and-style-shakshuka-org-at-fashioning-power-fashioning-peace"),
    dict(title="Aicha Takes Center Stage at the Arabian Sights Film Festival", date="2025-04-15", author="Mark Guenther",
         img="ev-aicha-sm", caption="Still from Aicha (Mehdi M. Barsaoui, 2024)",
         summary="Tunisian cinema at the 30th Arabian Sights Film Festival, with the director in the room.",
         url="https://www.shakshuka.org/post/celebrating-tunisian-cinema-aicha-takes-center-stage-at-the-arabian-sights-film-festival"),
]

# Tunisian organizations and works to highlight. type: org | work | artist | placeholder
TUNISIA = [
    dict(type="org", name="Tanit XR", where="Tunisia · United States · worldwide", url="https://tanitxr.org",
         img="tanitxr-logo", logo=True,
         text="A volunteer community from Tunisia and around the world that scans endangered heritage objects in 3D with their phones, one object at a time, and brings them to life in AR and VR. Volunteers in Tunisia, the United States, Europe and Nigeria meet every Thursday; those who have never been to Tunisia learn its history while modelling lamps, pottery and plants for a free virtual museum. More than 100 models published, 85+ volunteers on four continents."),
    # ---- shops and makers (sent by Leila, Oct 2026) ----
    dict(type="work", name="Carthage.co", where="Stoneware, made in Tunisia", url="https://carthage.co/",
         img="shop-carthage-sm",
         text="Hand-finished stoneware collections named after Tunisian places, La Marsa, Zaghouan, Dadasi, for a dinner table that starts conversations."),
    dict(type="work", name="Natural OliveWood", where="New York", url="https://www.naturalolivewood.com/",
         img="shop-olivewood-sm",
         text="Olive wood cutting boards, bowls and spoons from Tunisian groves, sold retail and wholesale across the US."),
    dict(type="work", name="Soukra", where="Contemporary Tunisian design", url="https://soukra.co/",
         img="shop-soukra-sm",
         text="A platform for contemporary Tunisian design: fashion, foutas, ceramics, pantry and gifts shaped by heritage. Free US shipping over $100."),
    dict(type="work", name="OSAY", where="Handcrafted Mediterranean footwear", url="https://osaythelabel.com/",
         img="shop-osay-sm",
         text="Our Stories Are Yours: babouches and bags made by artisans, sustainable luxury with a Tunisian soul."),
    dict(type="work", name="Alyssa Bazaar", where="Washington, DC", url="https://alyssabazaar.com/",
         img="shop-alyssa-sm",
         text="A family-run DC business curating hand-painted Tunisian ceramics and olive wood for the kitchen and the table."),
    dict(type="work", name="The Fouta Spa", where="Tunisian fouta towels", url="https://thefoutaspa.com/",
         img="shop-fouta-sm",
         text="Loomed Tunisian foutas for beach, bath and home, soft, quick-drying and made to last."),
    # ---- artists (Leila, Oct 7 2026) ----
    dict(type="artist", name="Khalil Ayed", where="Calligrapher · New York", url="/events/calligraphy-workshop/",
         img="ev-calligraphy-sm",
         text="Tunisian artist and creative director working between classical Arabic calligraphy and calligraffiti. He led our 2024 workshop at the Ambassador's residence."),
    dict(type="artist", name="VAJO Cosmos", where="Jawher Soudani · visual artist, Washington, DC", url="https://www.instagram.com/vajo.cosmos/",
         img="art-vajo-sm",
         text="Born in Gabès, trained in graphic design in Tunis, now in DC. Bold geometric compositions rooted in North African culture, on walls, textiles and canvas."),
    dict(type="artist", name="Alia Ben Sliman", where="Painter and photographer", url="https://aliabenslimanart.com/",
         img="art-alia-sm",
         text="Paintings, drawings and photographs at the meeting point of East and West, with a focus on North African and Amazigh art."),
    dict(type="artist", name="Nour Harkati", where="Singer-songwriter · New York", url="https://www.instagram.com/nour.harkati/",
         img="art-nour-sm",
         text="Tunisian-born, Brooklyn-based. The guembri and Gnawa rhythms meet New York groove; his album Moulena (2024) is about migration, memory and belonging. Residency at Pioneer Works, stages at globalFEST and Celebrate Brooklyn."),
    # ---- authors and books ----
    dict(type="book", name="Who Is in Charge? Why AI Must Remain Under Human Control", where="Khaled Koubaa", url="https://www.amazon.com/Who-Charge-Remain-Under-Control/dp/B0H8N8VW98/",
         img="book-koubaa", portrait=True,
         text="The Sfax-born internet-governance expert and CEO of AT Worthy Technology argues for human oversight as AI systems take on more decisions."),
    dict(type="book", name="Tunisie, Émeutes du pain de janvier 1984", where="Sadok Rouai · 2026", url="https://www.amazon.com/Tunisie-%C3%89meutes-Janvier-Mythes-R%C3%A9alit%C3%A9s/dp/B0GVVVNM3X",
         img="book-rouai-emeutes", portrait=True,
         text="Myths and realities about the role of the IMF and the Central Bank, from a Shakshuka board member who lived it from inside both institutions. In French."),
    dict(type="book", name="La genèse de la création de la Banque centrale de Tunisie et du dinar", where="Sadok Rouai · Arcadia, Tunis, 2026", url="https://kapitalis.com/tunisie/2026/10/06/sadok-rouai-revient-sur-la-naissance-de-la-bct-et-du-dinar/",
         img=None, portrait=True,
         text="How Tunisia won its monetary sovereignty: the negotiations with France and the IMF behind the birth of the dinar and the Central Bank. In French."),
    dict(type="book", name="A Calamity of Noble Houses", where="Amira Ghenim · translated by Miled Faiza & Karen McNeil", url="https://www.europaeditions.com/book/9798889660507/a-calamity-of-noble-houses",
         img="book-calamity", portrait=True,
         text="One night in Tunis, December 1935, told by eleven voices across two families. Finalist for the International Prize for Arabic Fiction, in English from Europa Editions (2025)."),
    dict(type="book", name="The Italian", where="Shukri Mabkhout · translated by Miled Faiza & Karen McNeil", url="https://www.europaeditions.com/book/9781609457013/the-italian",
         img="book-italian", portrait=True,
         text="Winner of the International Prize for Arabic Fiction: a friendship, a newsroom and a revolution betrayed in 1980s Tunis. Europa Editions, 2021. Miled Faiza, who is Tunisian, teaches at Brown University."),
]

PHOTO_CREDITS = [
    ("sidi-bou-said-doors", "Doors of Sidi Bou Said", "SvenZ", "CC BY-SA 2.5"),
    ("sidi-bou-said-gate", "Gate with blue doors, Sidi Bou Said", "Sharon Hahn Darlin", "CC BY 2.0"),
    ("tunis-medina", "Street in the medina of Tunis", "Kritzolina", "CC BY-SA 4.0"),
    ("harissa", "Harissa in a jar", "Jules (stonesoup)", "CC BY 3.0"),
    ("ojja", "Tunisian ojja", "Una723", "CC BY 4.0"),
    ("couscous", "Tunisian couscous mhakkek", "Wajih Khalfallah", "CC BY-SA 4.0"),
    ("el-jem", "Amphitheatre of El Jem", "Diego Delso", "CC BY-SA 4.0"),
    ("kairouan", "Courtyard of the Great Mosque of Kairouan", "Keith Roper", "CC BY 2.0"),
    ("brik", "Tunisian briks", "Souad Anane Lesina", "CC BY-SA 3.0"),
    ("tunisian-meal", "Tunisian meal", "Kritzolina", "CC BY-SA 4.0"),
    ("djerba-weaving", "Weaving workshops, Houmt Souk, Djerba", "Noland architect", "CC BY-SA 4.0"),
    ("cap-bon-olives", "Olive groves, Cap Bon", "Nicholas.gosse", "CC BY-SA 4.0"),
    ("carthage", "Antonine Baths, Carthage", "Silar", "CC BY-SA 4.0"),
    ("qallaline-panel", "Qallaline ceramic panel, Bardo Museum", "Khalil Mokaddem", "CC BY-SA 4.0"),
    ("barber-wall", "Tiled wall, Mosque of the Barber, Kairouan", "Jerzystrzelecki", "CC BY 3.0"),
    ("dar-cherait", "Tiles of Dar Cherait, Tozeur", "Keith Roper", "CC BY 2.0"),
    ("nabeul-ceramist", "Ceramist painting a plate, Nabeul", "SouthAngel", "CC BY-SA 2.0"),
    ("nabeul-potteries", "Potteries in Nabeul", "SouthAngel", "CC BY-SA 2.0"),
    ("art-nour", "Nour Harkati, photo by Carlos Cruz, courtesy Pioneer Works", "Carlos Cruz", "used with attribution"),
]

# ----------------------------------------------------------------- css ----

CSS = r"""
:root{
  --red:#5e2246; --red-deep:#43203a; --saffron:#e8b83a; --saffron-soft:#f7ead0;
  --blue:#5e2246; --blue-deep:#1b1b22; --blue-tint:#f3e8ee;
  --olive:#8a6200;
  --ink:#1f1b22; --body:#4a3f48; --muted:#8c7f88; --line:#eadfd6;
  --cream:#fcf7f1; --paper:#ffffff; --sand:#f6ede4;
  --display:'Yeseva One',Georgia,serif; --sans:'Roboto',-apple-system,'Helvetica Neue',Arial,sans-serif;
  --arabic:'Aref Ruqaa',serif;
}
*{box-sizing:border-box;margin:0;padding:0}
html{scroll-behavior:smooth}
body{font-family:var(--sans);color:var(--body);background:var(--cream);line-height:1.65;font-size:17px;-webkit-font-smoothing:antialiased}
img{max-width:100%;height:auto;display:block}
a{color:var(--blue-deep)}
h1,h2,h3,h4{font-family:var(--display);font-weight:400;color:var(--ink);line-height:1.12;letter-spacing:-.01em;text-wrap:balance}
h1{font-size:clamp(2.4rem,5.4vw,4rem)} h2{font-size:clamp(1.8rem,3.4vw,2.6rem)} h3{font-size:1.35rem}
p+p{margin-top:1em}
.wrap{max-width:1140px;margin:0 auto;padding:0 22px}
.narrow{max-width:760px}
.kicker{font-size:.76rem;font-weight:700;letter-spacing:.2em;text-transform:uppercase;color:var(--olive);margin-bottom:12px;display:flex;align-items:center;gap:10px}
.center .kicker{justify-content:center}
.center{text-align:center}
.lede{font-size:1.15rem;color:var(--body);max-width:62ch}
.center .lede{margin-inline:auto}
.btn{display:inline-flex;align-items:center;gap:8px;background:var(--saffron);color:var(--ink);font-weight:700;font-size:.95rem;padding:13px 28px;border-radius:999px;text-decoration:none;border:2px solid var(--saffron);box-shadow:0 6px 18px rgba(192,138,46,.25);transition:.18s;cursor:pointer;font-family:var(--sans)}
.btn:hover{background:#d4a52a;border-color:#d4a52a;transform:translateY(-2px)}
.btn.ghost{background:transparent;color:var(--ink);border-color:var(--ink);box-shadow:none} .btn.ghost:hover{background:var(--ink);color:#fff;border-color:var(--ink)}
.btn.light{background:transparent;color:#fff;border-color:rgba(255,255,255,.75);box-shadow:none} .btn.light:hover{background:#fff;border-color:#fff;color:var(--ink)}
.btn.saffron{background:var(--saffron);border-color:var(--saffron);color:var(--ink)}
.btn.blue{background:var(--ink);border-color:var(--ink);color:#fff} .btn.blue:hover{background:#000;border-color:#000}
.btn-row{display:flex;gap:12px;flex-wrap:wrap}
.center .btn-row{justify-content:center}

/* quiet accents only */
.tile-band{height:3px;background:var(--saffron)}
.tile-bg{position:relative}
.tile-corner{position:relative}
.kicker::before{content:"";width:26px;height:2px;background:var(--saffron);flex:none}
.tile-rule{display:none}
.tile-frame{position:relative}
.tile-side{position:relative}
.tile-single{display:none}

/* header */
.site-header{position:sticky;top:0;z-index:50;background:rgba(252,247,241,.94);backdrop-filter:blur(10px);border-bottom:1px solid var(--line)}
.site-header .wrap{display:flex;align-items:center;justify-content:space-between;gap:18px;min-height:72px}
.brand{display:flex;align-items:center;gap:12px;text-decoration:none;color:var(--ink)}
.brand img{width:40px;height:40px;border-radius:50%;object-fit:cover}
.brand b{font-family:var(--display);font-weight:600;font-size:1.25rem;letter-spacing:-.01em}
.brand small{display:block;font-size:.68rem;letter-spacing:.14em;text-transform:uppercase;color:var(--muted);font-weight:800;margin-top:-2px}
nav.main{display:flex;gap:4px;align-items:center}
nav.main a{font-size:.8rem;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:var(--body);text-decoration:none;padding:8px 11px;border-radius:8px}
nav.main a:hover{background:var(--sand);color:var(--ink)}
nav.main a.on{color:var(--ink);box-shadow:inset 0 -2px 0 var(--saffron);border-radius:0}
nav.main a.cta{background:var(--saffron);color:var(--ink);margin-left:8px;padding:9px 18px;border-radius:999px}
nav.main a.cta:hover{background:#d4a52a}
.menu-btn{display:none;background:none;border:2px solid var(--line);border-radius:8px;padding:6px 10px;font:800 .8rem var(--sans);color:var(--ink);cursor:pointer}
@media(max-width:960px){
  nav.main{display:none;position:absolute;top:72px;left:0;right:0;background:var(--cream);border-bottom:1px solid var(--line);flex-direction:column;align-items:stretch;padding:12px 22px 18px;gap:2px;box-shadow:0 20px 40px rgba(35,26,22,.12)}
  nav.main.open{display:flex} nav.main a{padding:11px 8px;font-size:1rem} nav.main a.cta{margin:10px 0 0;text-align:center}
  .menu-btn{display:block}
}

/* hero */
.hero{position:relative;color:#fff;background:var(--blue-deep);overflow:hidden}
.hero .bg{position:absolute;inset:0;background-size:cover;background-position:center 40%}
.hero .bg::after{content:"";position:absolute;inset:0;background:linear-gradient(100deg,rgba(27,27,34,.9) 0%,rgba(27,27,34,.7) 50%,rgba(27,27,34,.3) 100%)}
.hero .in{position:relative;padding:110px 0 120px;max-width:720px}
.hero .ar{font-family:var(--arabic);font-size:1.9rem;color:var(--saffron);margin-bottom:10px;display:block}
.hero h1{color:#fff;margin-bottom:20px}
.hero h1 em{font-style:italic;color:var(--saffron)}
.hero p{font-size:1.15rem;color:rgba(255,255,255,.9);max-width:56ch;margin-bottom:30px}
.hero .credit{position:absolute;right:16px;bottom:10px;font-size:.68rem;color:rgba(255,255,255,.55)}
.hero .credit a{color:inherit}
.page-hero{background:var(--blue-deep);color:#fff;position:relative;overflow:hidden}
.page-hero .bg{position:absolute;inset:0;background-size:cover;background-position:center;opacity:.55}
.page-hero .bg::after{content:"";position:absolute;inset:0;background:linear-gradient(90deg,rgba(27,27,34,.8),rgba(27,27,34,.3))}
.page-hero .in{position:relative;padding:72px 0 64px}
.page-hero h1{color:#fff} .page-hero .kicker{color:var(--saffron)}
.page-hero p{color:rgba(255,255,255,.85);max-width:62ch;margin-top:14px;font-size:1.1rem}

/* sections */
section{padding:72px 0} section.tight{padding:48px 0}
.sec-head{margin-bottom:36px}
.sec-head h2{margin-bottom:10px}
.sec-head p{color:var(--muted);max-width:66ch}
.center .sec-head p{margin-inline:auto}
.band-sand{background:var(--sand)} .band-blue{background:var(--ink);color:#fff}
.band-blue h2,.band-blue h3{color:#fff} .band-blue .kicker{color:var(--saffron)} .band-blue p{color:rgba(255,255,255,.86)}
.band-red{background:var(--red-deep);color:#fff} .band-red h2{color:#fff} .band-red p{color:rgba(255,255,255,.9)}

/* grids */
.grid{display:grid;gap:26px}
.g2{grid-template-columns:repeat(2,1fr)} .g3{grid-template-columns:repeat(3,1fr)} .g4{grid-template-columns:repeat(4,1fr)}
@media(max-width:900px){.g3,.g4{grid-template-columns:repeat(2,1fr)}}
@media(max-width:600px){.g2,.g3,.g4{grid-template-columns:1fr}}
.pillar{background:var(--paper);border:1px solid var(--line);border-radius:18px;padding:30px 28px;position:relative;overflow:hidden;transition:.2s}
.pillar:hover{transform:translateY(-3px);box-shadow:0 18px 40px rgba(35,26,22,.09)}
.pillar .num{font-family:var(--display);font-size:2.4rem;color:var(--saffron);line-height:1;margin-bottom:12px}
.pillar h3{margin-bottom:10px} .pillar p{color:var(--body);font-size:.98rem}
.card{background:var(--paper);border:1px solid var(--line);border-radius:18px;overflow:hidden;display:flex;flex-direction:column;transition:.2s;text-decoration:none;color:inherit}
a.card:hover{transform:translateY(-3px);box-shadow:0 18px 40px rgba(35,26,22,.1)}
.card img{width:100%;aspect-ratio:16/10;object-fit:cover}
.card .body{padding:20px 22px 24px;display:flex;flex-direction:column;gap:8px;flex:1}
.card h3{font-size:1.2rem} .card p{font-size:.95rem;color:var(--body)}
.card .meta{font-size:.76rem;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:var(--olive);display:flex;gap:10px;flex-wrap:wrap}
.card .meta .past{color:var(--muted)}
.card .more{margin-top:auto;padding-top:8px;font-weight:700;color:var(--red);font-size:.92rem}
.tag{display:inline-block;background:var(--sand);color:var(--body);font-size:.72rem;font-weight:800;letter-spacing:.1em;text-transform:uppercase;padding:4px 10px;border-radius:999px}
.tag.red{background:var(--saffron);color:var(--ink)} .tag.gold{background:var(--saffron-soft);color:#7a5410} .tag.olive{background:var(--blue-tint);color:var(--red-deep)}

/* split */
.split{display:grid;grid-template-columns:1.1fr 1fr;gap:56px;align-items:center}
.split.rev{grid-template-columns:1fr 1.1fr} .split.rev .text{order:2} .split.rev .pic{order:1}
@media(max-width:860px){.split,.split.rev{grid-template-columns:1fr}.split.rev .text,.split.rev .pic{order:initial}.quote-grid{grid-template-columns:1fr!important}}
.pic{position:relative;margin:0}
.pic img{border-radius:18px;box-shadow:0 18px 44px rgba(35,26,22,.16);width:100%;object-fit:cover}
.pic figcaption{font-size:.74rem;color:var(--muted);margin-top:8px}
.pic.framed img{border:8px solid #fff;border-radius:18px 42px 24px 38px/34px 20px 42px 26px}
.text h2{margin-bottom:16px}
.text ul{padding-left:20px;margin:14px 0} .text li{margin:6px 0}

/* stats */
.stats{display:grid;grid-template-columns:repeat(4,1fr);gap:20px;text-align:center}
.stats b{display:block;font-family:var(--display);font-size:2.6rem;color:var(--saffron);line-height:1.05}
.stats span{font-size:.86rem;letter-spacing:.06em;text-transform:uppercase;font-weight:800;color:rgba(255,255,255,.8)}
@media(max-width:700px){.stats{grid-template-columns:repeat(2,1fr)}}

/* quote */
.quote{border-left:4px solid var(--saffron);padding:6px 0 6px 24px;font-family:var(--display);font-size:1.3rem;color:var(--ink);font-style:italic;max-width:62ch}
.quote cite{display:block;font-style:normal;font-family:var(--sans);font-size:.85rem;color:var(--muted);margin-top:10px}

/* team */
.team{display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:30px 26px}
.person{text-align:center}
.person img{width:170px;height:170px;border-radius:50%;object-fit:cover;margin:0 auto 14px;border:5px solid #fff;box-shadow:0 12px 30px rgba(35,26,22,.14)}
.person h3{font-size:1.15rem} .person .role{color:var(--olive);font-weight:800;font-size:.8rem;letter-spacing:.1em;text-transform:uppercase;margin:4px 0 10px}
.person p{font-size:.93rem;color:var(--body)}

/* events */
.ev-list{display:grid;gap:18px}
.ev-row{display:grid;grid-template-columns:120px 1fr auto;gap:22px;align-items:center;background:var(--paper);border:1px solid var(--line);border-radius:16px;padding:16px 20px;text-decoration:none;color:inherit;transition:.2s}
.ev-row:hover{transform:translateX(4px);box-shadow:0 12px 30px rgba(35,26,22,.08)}
.ev-row .date{text-align:center;border-right:1px solid var(--line);padding-right:18px}
.ev-row .date b{display:block;font-family:var(--display);font-size:2rem;color:var(--red);line-height:1}
.ev-row .date span{font-size:.74rem;font-weight:800;letter-spacing:.12em;text-transform:uppercase;color:var(--muted)}
.ev-row h3{font-size:1.15rem;margin-bottom:4px} .ev-row p{font-size:.9rem;color:var(--muted)}
.ev-row .btn{padding:9px 18px;font-size:.85rem}
@media(max-width:640px){.ev-row{grid-template-columns:90px 1fr}.ev-row .btn{display:none}}
.ev-hero{display:grid;grid-template-columns:1.2fr .8fr;gap:40px;align-items:start}
@media(max-width:860px){.ev-hero{grid-template-columns:1fr}}
.ev-hero img{border-radius:20px;width:100%;aspect-ratio:16/10;object-fit:cover;box-shadow:0 22px 50px rgba(35,26,22,.18)}
.ev-facts{background:var(--paper);border:1px solid var(--line);border-radius:20px;padding:26px;position:sticky;top:90px}
.ev-facts dl{display:grid;grid-template-columns:auto 1fr;gap:10px 16px;font-size:.95rem;margin:14px 0 22px}
.ev-facts dt{font-weight:800;color:var(--muted);font-size:.74rem;letter-spacing:.12em;text-transform:uppercase;padding-top:3px}
.ev-facts .price{font-family:var(--display);font-size:1.6rem;color:var(--ink)}
.ev-facts .tickets{border-top:1px dashed var(--line);margin-top:8px;padding-top:12px;font-size:.92rem}
.ev-facts .tickets div{display:flex;justify-content:space-between;gap:12px;padding:4px 0}
.ev-facts .note{font-size:.8rem;color:var(--muted);margin-top:12px}
.ev-facts .btn{width:100%;justify-content:center}
.past-badge{display:inline-block;background:var(--sand);color:var(--muted);font-weight:800;font-size:.76rem;letter-spacing:.1em;text-transform:uppercase;padding:8px 14px;border-radius:999px}
.draft-banner{background:var(--saffron);color:var(--ink);font-weight:700;text-align:center;padding:10px 20px;font-size:.9rem}
.prose{max-width:720px;font-size:1.05rem} .prose p{margin-bottom:1em} .prose h2,.prose h3{margin:1.6em 0 .6em}
.prose ul,.prose ol{padding-left:22px;margin-bottom:1em} .prose li{margin:.35em 0}

/* forms */
form.nice{display:grid;gap:14px}
form.nice .row{display:grid;grid-template-columns:1fr 1fr;gap:14px} @media(max-width:600px){form.nice .row{grid-template-columns:1fr}}
form.nice label{font-size:.8rem;font-weight:800;letter-spacing:.06em;text-transform:uppercase;color:var(--muted);display:block;margin-bottom:5px}
form.nice input,form.nice select,form.nice textarea{width:100%;font:inherit;padding:12px 14px;border:1.5px solid var(--line);border-radius:10px;background:#fff;color:var(--ink)}
form.nice input:focus,form.nice textarea:focus,form.nice select:focus{outline:2px solid var(--saffron);border-color:var(--saffron)}
form.nice textarea{min-height:120px;resize:vertical}
form.nice .hint{font-size:.8rem;color:var(--muted)}
.inline-form{display:flex;gap:10px;flex-wrap:wrap} .inline-form input{flex:1;min-width:220px;font:inherit;padding:13px 16px;border-radius:999px;border:1.5px solid var(--line)}

/* membership */
.plans{display:grid;grid-template-columns:repeat(2,1fr);gap:26px;max-width:860px;margin:0 auto} @media(max-width:700px){.plans{grid-template-columns:1fr}}
.plan{background:var(--paper);border:1.5px solid var(--line);border-radius:22px;padding:34px 30px;position:relative}
.plan.best{border-color:var(--saffron);box-shadow:0 20px 50px rgba(227,169,58,.22)}
.plan .best-tag{position:absolute;top:-14px;left:30px;background:var(--saffron);color:var(--ink);font-weight:700;font-size:.72rem;letter-spacing:.12em;text-transform:uppercase;padding:5px 12px;border-radius:999px}
.plan .price{font-family:var(--display);font-size:3rem;color:var(--ink);line-height:1;margin:10px 0 4px} .plan .price small{font-size:1rem;color:var(--muted);font-family:var(--sans)}
.plan ul{list-style:none;margin:20px 0 26px} .plan li{padding:7px 0 7px 28px;position:relative;font-size:.95rem;border-bottom:1px dashed var(--line)}
.plan li::before{content:"✦";position:absolute;left:4px;color:var(--saffron)}
.amounts{display:flex;gap:10px;flex-wrap:wrap} .amounts label{cursor:pointer}
.amounts input{position:absolute;opacity:0} .amounts span{display:inline-block;padding:12px 22px;border-radius:999px;border:2px solid var(--line);font-weight:800;background:#fff}
.amounts input:checked+span{background:var(--ink);color:#fff;border-color:var(--ink)}

/* tunisia directory */
.filters{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:28px}
.filters button{font:800 .8rem var(--sans);letter-spacing:.06em;text-transform:uppercase;padding:9px 16px;border-radius:999px;border:2px solid var(--line);background:#fff;color:var(--body);cursor:pointer}
.filters button.on{background:var(--ink);border-color:var(--ink);color:#fff}
.dir{display:grid;grid-template-columns:repeat(3,1fr);gap:26px} @media(max-width:900px){.dir{grid-template-columns:repeat(2,1fr)}} @media(max-width:600px){.dir{grid-template-columns:1fr}}
.dir .card.logo img{object-fit:contain;padding:28px;background:#fff}
.dir .card.portrait img{object-fit:contain;background:var(--sand);padding:18px;aspect-ratio:16/12}
.dir .cover{aspect-ratio:16/12;background:var(--blue-deep);color:#fff;display:flex;flex-direction:column;justify-content:flex-end;padding:22px;gap:6px}
.dir .cover span{font-family:var(--display);font-size:1.15rem;line-height:1.2}
.dir .cover small{font-size:.78rem;color:rgba(255,255,255,.7)}
.dir .card.hide{display:none}

/* footer */
footer{background:var(--blue-deep);color:rgba(255,255,255,.78);padding:60px 0 30px;font-size:.92rem;border-top:0}
footer .cols{display:grid;grid-template-columns:1.4fr 1fr 1fr 1fr;gap:36px;margin-bottom:40px} @media(max-width:860px){footer .cols{grid-template-columns:1fr 1fr}} @media(max-width:520px){footer .cols{grid-template-columns:1fr}}
footer h4{color:#fff;font-family:var(--sans);font-size:.78rem;letter-spacing:.16em;text-transform:uppercase;margin-bottom:14px}
footer a{color:rgba(255,255,255,.78);text-decoration:none;display:block;padding:3px 0} footer a:hover{color:var(--saffron)}
footer .brand b{color:#fff} footer .brand small{color:rgba(255,255,255,.55)}
footer .fine{border-top:1px solid rgba(255,255,255,.12);padding-top:20px;font-size:.78rem;color:rgba(255,255,255,.5);display:flex;justify-content:space-between;gap:16px;flex-wrap:wrap}
footer .fine a{display:inline;padding:0;color:rgba(255,255,255,.65)}
.photo-credit{font-size:.72rem;color:var(--muted)}
table.credits{width:100%;border-collapse:collapse;font-size:.92rem} table.credits td,table.credits th{padding:10px 8px;border-bottom:1px solid var(--line);text-align:left;vertical-align:top}
"""

JS = r"""
document.querySelector('.menu-btn')?.addEventListener('click',e=>{const n=document.querySelector('nav.main');const o=n.classList.toggle('open');e.currentTarget.setAttribute('aria-expanded',o)});
document.querySelectorAll('.filters button').forEach(b=>b.addEventListener('click',()=>{document.querySelectorAll('.filters button').forEach(x=>x.classList.remove('on'));b.classList.add('on');const t=b.dataset.t;document.querySelectorAll('.dir .card').forEach(c=>c.classList.toggle('hide',t!=='all'&&c.dataset.t!==t))}));
"""

# -------------------------------------------------------------- helpers ----

NAV = [("/", "Home"), ("/about/", "About"), ("/events/", "Events"), ("/tunisia/", "Tunisia"),
       ("/cookbook/", "Cookbook"), ("/blog/", "Blog"), ("/membership/", "Join"), ("/contact/", "Contact")]

def esc(s): return html.escape(s, quote=True)

def fmt_date(d, long=False):
    d = dt.date.fromisoformat(d)
    return d.strftime("%A, %B %-d, %Y") if long else d.strftime("%b %-d, %Y")

def is_past(ev): return dt.date.fromisoformat(ev["date"]) < TODAY

def page(path, title, body, desc="", og_img="assets/img/sidi-bou-said-doors.jpg"):
    """Write a page with clean URL path like '/events/foo/' → docs/events/foo/index.html"""
    nav = "".join(f'<a href="{h}"{" class=on" if (h==path or (h!="/" and path.startswith(h))) else ""}>{t}</a>' for h, t in NAV)
    nav += f'<a class="cta" href="{DONATE_URL}">Donate</a>'
    full_title = f"{title} | {ORG}" if title != ORG else f"{ORG} · Tunisian-American community of the DMV"
    doc = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(full_title)}</title>
<meta name="description" content="{esc(desc or TAGLINE)}">
<link rel="canonical" href="{SITE}{path}">
<meta property="og:title" content="{esc(full_title)}"><meta property="og:description" content="{esc(desc or TAGLINE)}">
<meta property="og:image" content="{SITE}/{og_img}"><meta property="og:type" content="website">
<link rel="icon" href="/assets/img/logo.jpg">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Yeseva+One&family=Roboto:ital,wght@0,400;0,500;0,700;1,400&family=Aref+Ruqaa:wght@400;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/style.css">
</head><body>
<header class="site-header"><div class="wrap">
<a class="brand" href="/"><img src="/assets/img/logo.jpg" alt=""><span><b>Shakshuka</b><small>Tunisian-American · DMV</small></span></a>
<button class="menu-btn" aria-expanded="false" aria-controls="nav">Menu</button>
<nav class="main" id="nav">{nav}</nav>
</div></header>
<div class="tile-band" aria-hidden="true"></div>
<main>{body}</main>
{footer()}
<script src="/assets/site.js"></script>
</body></html>"""
    out = OUT / path.strip("/") / "index.html" if path != "/" else OUT / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(prefix(doc))
    return path

def prefix(text):
    """Rewrite root-relative URLs for a sub-folder deployment."""
    if not BASE: return text
    return (text.replace('href="/', f'href="{BASE}/').replace("src=\"/", f"src=\"{BASE}/")
                .replace("url(/", f"url({BASE}/").replace("src='/", f"src='{BASE}/")
                .replace(f'href="{BASE}/{BASE.strip("/")}', f'href="{BASE}'))

def footer():
    soc = "".join(f'<a href="{u}" target="_blank" rel="noopener">{k.title()}</a>' for k, u in SOCIALS.items())
    return f"""<footer><div class="wrap">
<div class="cols">
<div><a class="brand" href="/"><span><b>Shakshuka</b><small>Reimagining community</small></span></a>
<p style="margin-top:16px;max-width:38ch">A Tunisian-American community and cultural initiative in Washington, DC, Maryland and Virginia. A registered 501(c)(3) public charity, EIN 92-3134851.</p></div>
<div><h4>Explore</h4><a href="/about/">About us</a><a href="/team/">Our board</a><a href="/events/">Events</a><a href="/tunisia/">Tunisian organizations & works</a><a href="/blog/">Blog</a></div>
<div><h4>Take part</h4><a href="/membership/">Become a member</a><a href="/donate/">Donate</a><a href="/volunteer/">Volunteer</a><a href="/recipes/">Share a recipe</a><a href="/cookbook/">The cookbook</a></div>
<div><h4>Contact</h4><a href="mailto:{CONTACT_EMAIL}">{CONTACT_EMAIL}</a><a href="/contact/">Contact form</a>{soc}</div>
</div>
<div class="fine"><span>© {TODAY.year} Shakshuka.org · Washington, DC</span><span><a href="/credits/">Photo credits</a> · <a href="/contact/">Privacy & contact</a></span></div>
</div></footer>"""

def img(name, alt="", cls="", sm=False, loading="lazy"):
    return f'<img src="/assets/img/{name}.jpg" alt="{esc(alt)}"{f" class={chr(34)}{cls}{chr(34)}" if cls else ""} loading="{loading}">'

def credit(key):
    for k, t, a, l in PHOTO_CREDITS:
        if k == key: return f'<span class="photo-credit">Photo: {esc(a)}, {l}, via Wikimedia Commons</span>'
    return ""

def event_card(ev):
    past = is_past(ev)
    price = "Free" if ev.get("free") else (f"From ${min(p for _, p in ev['tickets'])}" if ev.get("tickets") else "")
    return f"""<a class="card" href="/events/{ev['slug']}/">{img(ev['img']+'-sm' if (OUT/'assets/img'/(ev['img']+'-sm.jpg')).exists() else ev['img'], ev['title'])}
<div class="body"><div class="meta"><span{' class=past' if past else ''}>{fmt_date(ev['date'])}</span><span class="tag{' red' if not past else ''}">{esc(ev['kind'])}</span></div>
<h3>{esc(ev['title'])}</h3><p>{esc(ev['summary'])}</p>
<div class="more">{'See how it went →' if past else (price + ' · Reserve →' if price else 'Details →')}</div></div></a>"""

def event_row(ev):
    d = dt.date.fromisoformat(ev["date"]); past = is_past(ev)
    btn = "" if past else f'<span class="btn{" blue" if ev.get("free") else ""}">{"RSVP" if ev.get("free") else "Reserve"}</span>'
    return f"""<a class="ev-row" href="/events/{ev['slug']}/"><div class="date"><b>{d.day}</b><span>{d.strftime('%b %Y')}</span></div>
<div><h3>{esc(ev['title'])}</h3><p>{esc(ev['venue'])}{' · ' + esc(ev['time']) if ev.get('time') else ''}</p></div>{btn}</a>"""

def form_hidden(subject, next_path="/thanks/"):
    return f'<input type="hidden" name="_subject" value="{esc(subject)}"><input type="hidden" name="_next" value="{SITE}{next_path}"><input type="hidden" name="_captcha" value="false"><input type="text" name="_honey" style="display:none">'

# ---------------------------------------------------------------- pages ----

def build_home():
    upcoming = [e for e in EVENTS if not is_past(e) and not e.get("draft")]
    recent = [e for e in EVENTS if is_past(e)][:3]
    up_html = "".join(event_row(e) for e in upcoming) if upcoming else f"""<div class="pillar tile-corner"><h3>Next season is cooking</h3><p>Nothing on the calendar at this moment. Our cooking classes, film nights and the yearly Iftar are announced to members and newsletter readers first.</p>
<form class="inline-form" style="margin-top:18px" action="{FORM_ACTION}" method="POST">{form_hidden('Newsletter signup')}<input type="email" name="email" placeholder="you@example.com" required aria-label="Email"><button class="btn">Tell me first</button></form></div>"""
    body = f"""
<section class="hero"><div class="bg" style="background-image:url(/assets/img/sidi-bou-said-doors.jpg)"></div>
<div class="wrap"><div class="in"><span class="ar">شكشوكة</span>
<h1>Tunisians of the DMV, and everyone who loves Tunisia, <em>around one table</em>.</h1>
<p>Shakshuka is a Tunisian-American community and cultural initiative in Washington, DC, Maryland and Virginia. Cooking classes, film nights, Iftars, sing-alongs, and a place to belong.</p>
<div class="btn-row"><a class="btn saffron" href="/events/">See our events</a><a class="btn light" href="/membership/">Become a member</a></div></div></div>
<div class="credit">Doors of Sidi Bou Said · SvenZ, CC BY-SA 2.5</div></section>

<section class="tile-bg"><div class="wrap">
<div class="sec-head center"><div class="kicker">Why “Shakshuka”</div><h2>A dish, and a way of seeing a community</h2>
<p>Peppers, tomatoes, eggs, harissa: nothing alike, and better together. The dish is our metaphor for the Tunisians, Tunisian-Americans and friends of Tunisia who make up our corner of the DMV, about 5,000 of us.</p></div>
<div class="grid g3">
<div class="pillar tile-corner"><div class="num">01</div><h3>Fostering community</h3><p>Bringing together Tunisians and lovers of Tunisian culture in the DMV, so that nobody has to explain where Nabeul is or why Friday means couscous.</p></div>
<div class="pillar tile-corner"><div class="num">02</div><h3>Bridging the gap</h3><p>Keeping the community connected to Tunisia as it changes: its films, its music, its new voices and its old recipes.</p></div>
<div class="pillar tile-corner"><div class="num">03</div><h3>Showing the new Tunisia</h3><p>Cultural and educational events, through an apolitical lens, open to everyone regardless of origin or faith.</p></div>
</div></div></section>

<section class="band-sand"><div class="wrap">
<div class="sec-head"><div class="kicker">Calendar</div><h2>Upcoming</h2></div>
<div class="ev-list">{up_html}</div>
<div class="sec-head" style="margin-top:56px"><div class="kicker">Recently</div><h2>What we have been up to</h2></div>
<div class="grid g3">{''.join(event_card(e) for e in recent)}</div>
<p style="margin-top:28px"><a class="btn ghost" href="/events/">All events, past and upcoming</a></p>
</div></section>

<section><div class="wrap"><div class="split">
<div class="text"><div class="kicker">Food first</div><h2>Discovering Tunisian Cuisine</h2>
<p class="lede">The 147-page cookbook by Judith Dwan Hallet, Raoudha Guellali Ben Taarit and Hasna Trabelsi, with photographs by Stanley Ira Hallet. Joan Nathan called it “awesome and authentic”.</p>
<p>Signed first-edition copies are sold through Shakshuka, and every copy supports our programs. We are also collecting the community's own recipes for a second book.</p>
<div class="btn-row" style="margin-top:22px"><a class="btn" href="/cookbook/">Get the cookbook</a><a class="btn ghost" href="/recipes/">Share a family recipe</a></div></div>
<figure class="pic framed">{img('tunisian-meal','A Tunisian table: couscous, brik, salads')}<figcaption>{credit('tunisian-meal')}</figcaption></figure>
</div></div></section>

<section class="band-blue tile-bg"><div class="wrap">
<div class="stats"><div><b>2023</b><span>Founded in DC</span></div><div><b>18+</b><span>Events since 2024</span></div><div><b>~5,000</b><span>Tunisians in the DMV</span></div><div><b>501(c)(3)</b><span>Donations deductible</span></div></div>
</div></section>

<section><div class="wrap"><div class="split rev">
<div class="text"><div class="kicker">Beyond the DMV</div><h2>Tunisian organizations and works we love</h2>
<p class="lede">Associations, shops, authors and artists, in the United States and in Tunisia, that keep the culture alive. A growing directory, with room for yours.</p>
<div class="btn-row" style="margin-top:22px"><a class="btn blue" href="/tunisia/">Browse the directory</a></div></div>
<figure class="pic framed">{img('kairouan','Courtyard of the Great Mosque of Kairouan')}<figcaption>{credit('kairouan')}</figcaption></figure>
</div></div></section>

<section class="band-red tile-bg saffron"><div class="wrap center">
<h2>Help us set a bigger table</h2>
<p class="lede" style="margin:14px auto 28px;color:#fff">Membership from $50 a year brings free cooking classes and movie tickets. Donations of any size let us host more, and more often. Both are tax-deductible.</p>
<div class="btn-row"><a class="btn light" href="/membership/">Join as a member</a><a class="btn saffron" href="/donate/">Donate</a><a class="btn light" href="/volunteer/">Volunteer</a></div>
</div></section>
"""
    page("/", ORG, body, "Tunisian-American community and cultural initiative in Washington, DC, Maryland and Virginia. Cooking classes, film nights, Iftars, sing-alongs and a place to belong.")

def build_about():
    body = f"""
<section class="page-hero"><div class="bg" style="background-image:url(/assets/img/tunis-medina.jpg)"></div><div class="wrap in">
<div class="kicker">About</div><h1>Reimagining community</h1>
<p>Shakshuka was born in 2023 out of a simple wish: that Tunisians in the Washington area, and everyone who loves Tunisia, would have a place to find each other.</p></div></section>

<section><div class="wrap"><div class="split">
<div class="text"><h2>Our story</h2>
<p>There are around 5,000 Tunisians in DC, Maryland and Virginia. Many arrived for school or work, many were born here to Tunisian parents, and many more are Americans who fell in love with the country through a trip, a friend, a marriage or a plate of food. Until recently there was no regular place for all of them to meet.</p>
<p>A group of friends started Shakshuka in 2023 as a volunteer, apolitical initiative. We registered as a nonprofit, became a 501(c)(3) public charity, and started cooking. Our first online class in September 2024 sold out; so did the first film night at the Avalon a month later. Since then we have hosted Iftars for over a hundred guests, a calligraphy workshop at the Ambassador's residence, sing-alongs in public libraries and screenings at the Embassy of France, and co-sponsored exhibitions with the Embassy of Tunisia.</p>
<p>We are run entirely by volunteers. Ticket sales, memberships and donations pay for venues, films, chefs and the website.</p></div>
<figure class="pic framed">{img('sidi-bou-said-gate','Blue gate, Sidi Bou Said')}<figcaption>{credit('sidi-bou-said-gate')}</figcaption></figure>
</div></div></section>

<section class="band-sand tile-bg"><div class="wrap">
<div class="sec-head center"><div class="kicker">Mission</div><h2>Three things we do</h2></div>
<div class="grid g3">
<div class="pillar"><h3>Foster community</h3><p>Regular gatherings, a members' circle, and a warm welcome for newcomers to the DMV. If you just landed at Dulles, write to us.</p></div>
<div class="pillar"><h3>Bridge the gap</h3><p>Programs that connect us to Tunisia as it is today: contemporary cinema, new music, young chefs and artists, alongside the classics.</p></div>
<div class="pillar"><h3>Show the new Tunisia</h3><p>Cultural and educational events that present Tunisia through an apolitical lens, open to all backgrounds and faiths.</p></div>
</div></div></section>

<section><div class="wrap narrow">
<blockquote class="quote">“Shakshuka isn't just a delicious dish from Tunisia. It's a metaphor for the diversity and richness of our community: a melting pot of backgrounds, ideas and people, better together.”<cite>Team Shakshuka</cite></blockquote>
<h2 style="margin:56px 0 16px">What we organize</h2>
<div class="grid g2">
<div><h3>Cooking classes</h3><p>Live online classes with Tunisian chefs, four so far, from s'han tounsi to lablabi. Members get free seats.</p></div>
<div><h3>Film nights</h3><p>Contemporary and classic Tunisian cinema at the Avalon Theatre and partner embassies, often with the director in the room.</p></div>
<div><h3>Iftar</h3><p>A yearly Ramadan dinner for everyone, whatever their faith. Our largest gathering of the year.</p></div>
<div><h3>Music & workshops</h3><p>Sing-alongs of Malouf and Hedi Jouini, calligraphy, and whatever the community asks for next.</p></div>
</div>
<h2 style="margin:56px 0 16px">Legal and financial</h2>
<p>Shakshuka is a registered 501(c)(3) organization (EIN 92-3134851) based in Washington, DC. Donors can deduct contributions under IRC Section 170; the IRS has determined that we are a public charity under the same section. We publish our events, our board and our spending priorities openly.</p>
<div class="btn-row" style="margin-top:26px"><a class="btn" href="/team/">Meet the board</a><a class="btn ghost" href="/contact/">Contact us</a></div>
</div></section>
"""
    page("/about/", "About", body, "Shakshuka is a volunteer-run Tunisian-American cultural initiative founded in Washington, DC in 2023. Our story, mission and legal status.")

def build_team():
    people = "".join(f"""<div class="person">{img(p['img'], p['name'])}<h3>{esc(p['name'])}</h3><div class="role">{esc(p['role'])}</div><p>{esc(p['bio'])}</p></div>""" for p in TEAM)
    body = f"""
<section class="page-hero"><div class="bg" style="background-image:url(/assets/img/dar-cherait.jpg)"></div><div class="wrap in">
<div class="kicker">Team Shakshuka</div><h1>Connection. Knowledge. Passion. Commitment.</h1>
<p>A group of volunteers committed to a sense of community, connectedness and a deep appreciation for Tunisia, and to keeping the door open for whoever wants to join.</p></div></section>
<section><div class="wrap"><div class="team">{people}</div></div></section>
<section class="band-sand tile-bg"><div class="wrap center"><h2>Want to help run things?</h2><p class="lede" style="margin:14px auto 26px">We need hands for events, photography, social media, translation and bookkeeping. A few hours a month makes a difference.</p><a class="btn" href="/volunteer/">Volunteer with us</a></div></section>
"""
    page("/team/", "Our board", body, "The volunteer board of Shakshuka.org, the Tunisian-American community of the DMV.")

def build_events():
    upcoming = [e for e in EVENTS if not is_past(e) and not e.get("draft")]
    past = sorted([e for e in EVENTS if is_past(e)], key=lambda e: e["date"], reverse=True)
    years = sorted({e["date"][:4] for e in past}, reverse=True)
    up_html = "".join(event_card(e) for e in upcoming) if upcoming else f"""<div class="pillar tile-corner" style="grid-column:1/-1"><h3>No dates announced yet</h3><p>Members and newsletter readers hear first, and members get early seats. Meanwhile browse what we did last season below.</p>
<form class="inline-form" style="margin-top:18px" action="{FORM_ACTION}" method="POST">{form_hidden('Newsletter signup')}<input type="email" name="email" placeholder="you@example.com" required aria-label="Email"><button class="btn">Notify me</button></form></div>"""
    past_html = ""
    for y in years:
        past_html += f'<h2 style="margin:48px 0 20px">{y}</h2><div class="grid g3">' + "".join(event_card(e) for e in past if e["date"].startswith(y)) + "</div>"
    body = f"""
<section class="page-hero"><div class="bg" style="background-image:url(/assets/img/el-jem.jpg)"></div><div class="wrap in">
<div class="kicker">Events</div><h1>Cook, watch, sing, break bread</h1>
<p>Everything we host, from online cooking classes to Iftar for a hundred. Reserve your seat online; free events only need an RSVP.</p></div></section>
<section><div class="wrap"><div class="sec-head"><div class="kicker">Upcoming</div><h2>Reserve your seat</h2></div><div class="grid g3">{up_html}</div></div></section>
<section class="band-sand tile-bg"><div class="wrap"><div class="sec-head"><div class="kicker">Past events</div><h2>Where we have been</h2><p>Every event so far has sold out or filled the room. Here is the record.</p></div>{past_html}</div></section>
<section><div class="wrap center"><h2>Have an idea for an event?</h2><p class="lede" style="margin:14px auto 26px">A film we should screen, a chef we should invite, a venue that would host us. We build the calendar with the community.</p><a class="btn ghost" href="/contact/">Suggest an event</a></div></section>
"""
    page("/events/", "Events", body, "Upcoming and past events of Shakshuka.org: Tunisian cooking classes, film screenings, Iftar dinners, sing-alongs and workshops in the DC area.")
    for e in EVENTS: build_event(e)

def build_event(ev):
    past = is_past(ev)
    # reservation box
    if past:
        res = '<span class="past-badge">This event has passed</span><p class="note">Want to know about the next one? <a href="/membership/">Members</a> hear first.</p>'
    elif ev.get("free"):
        res = f"""<div class="price">Free</div><p class="note">RSVP so we can plan seats and lyric sheets. Donations welcome on the day.</p>
<form class="nice" style="margin-top:14px" action="{FORM_ACTION}" method="POST">{form_hidden('RSVP: ' + ev['title'], '/thanks/')}<input type="hidden" name="event" value="{esc(ev['title'])}">
<div><label>Name</label><input name="name" required></div><div><label>Email</label><input type="email" name="email" required></div>
<div><label>Guests (including you)</label><select name="guests"><option>1</option><option>2</option><option>3</option><option>4</option><option>5+</option></select></div>
<button class="btn blue">RSVP</button></form>"""
    else:
        tk = "".join(f"<div><span>{esc(n)}</span><b>${p}</b></div>" for n, p in ev["tickets"])
        res = f"""<div class="price">From ${min(p for _, p in ev['tickets'])}</div><div class="tickets">{tk}</div>
<a class="btn" style="margin-top:16px" href="{esc(ev['reserve_url'])}" target="_blank" rel="noopener">Reserve your seat</a>
<p class="note">Secure checkout. 100% of the ticket goes to Shakshuka; the processor's fee is covered by an optional tip at checkout. Members: use the code from your welcome email.</p>"""
    draft = '<div class="draft-banner">Draft example: not published. Shows the reservation flow for a ' + ('free' if ev.get('free') else 'paid') + ' event.</div>' if ev.get("draft") else ""
    maps = f'<a href="https://www.google.com/maps/search/?api=1&query={esc(ev["venue"] + ", " + ev["address"]).replace(" ", "+")}" target="_blank" rel="noopener">Map</a>' if ev.get("address") and "Online" not in ev["venue"] else ""
    body = f"""{draft}
<section><div class="wrap">
<div class="kicker"><a href="/events/" style="text-decoration:none;color:inherit">Events</a> · {esc(ev['kind'])}</div>
<h1 style="max-width:20ch;margin-bottom:28px">{esc(ev['title'])}</h1>
<div class="ev-hero">
<div>{img(ev['img'], ev['title'], loading='eager')}<div class="prose" style="margin-top:30px">{ev['body']}</div></div>
<aside class="ev-facts"><div class="tag{' red' if not past else ''}">{'Past event' if past else 'Upcoming'}</div>
<dl><dt>When</dt><dd>{fmt_date(ev['date'], True)}{('<br>' + esc(ev['time'])) if ev.get('time') else ''}</dd><dt>Where</dt><dd>{esc(ev['venue'])}{('<br><small>' + esc(ev['address']) + '</small>') if ev.get('address') else ''} {maps}</dd></dl>
{res}</aside></div>
</div></section>
<section class="band-sand tight"><div class="wrap"><div class="sec-head"><h2 style="font-size:1.6rem">More events</h2></div><div class="grid g3">{''.join(event_card(e) for e in EVENTS if e is not ev and not e.get('draft'))[:3] if False else ''.join(event_card(e) for e in [x for x in EVENTS if x is not ev and not x.get('draft')][:3])}</div></div></section>
"""
    page(f"/events/{ev['slug']}/", ev["title"], body, ev["summary"], f"assets/img/{ev['img']}.jpg")

def build_tunisia():
    icons = {"placeholder": "✦"}
    cards = ""
    for t in TUNISIA:
        if True:
            ext = t["url"].startswith("http")
            cls = "card" + (" logo" if t.get("logo") else "") + (" portrait" if t.get("portrait") else "")
            src = f"/assets/img/{t['img']}.{'png' if t.get('logo') else 'jpg'}" if t.get('img') else None
            pic = f'<img src="{src}" alt="{esc(t["name"])}" loading="lazy">' if src else f'<div class="cover"><span>{esc(t["name"])}</span><small>{esc(t["where"])}</small></div>'
            cards += f"""<a class="{cls}" data-t="{t['type']}" href="{t['url']}"{' target="_blank" rel="noopener"' if ext else ''}>{pic}
<div class="body"><div class="meta"><span class="tag {'olive' if t['type']=='org' else 'gold' if t['type']=='work' else 'red'}">{ {'org':'Organization','work':'Shop','book':'Book','artist':'Artist'}[t['type']] }</span></div><h3>{esc(t['name'])}</h3><p style="color:var(--muted);font-size:.85rem">{esc(t['where'])}</p><p>{esc(t['text'])}</p><div class="more">{'Visit →' if ext else 'Read more →'}</div></div></a>"""
    body = f"""
<section class="page-hero"><div class="bg" style="background-image:url(/assets/img/barber-wall.jpg)"></div><div class="wrap in">
<div class="kicker">Tunisia</div><h1>Tunisian organizations and works worth knowing</h1>
<p>Associations, shops, books and artists keeping Tunisian culture alive, in the United States and at home. Curated by Shakshuka, growing with your suggestions.</p></div></section>
<section><div class="wrap">
<div class="filters" role="tablist"><button class="on" data-t="all">All</button><button data-t="org">Organizations</button><button data-t="work">Shops & makers</button><button data-t="artist">Artists</button><button data-t="book">Books</button></div>
<div class="dir">{cards}</div>
</div></section>
<section class="band-sand tile-bg" id="suggest"><div class="wrap narrow">
<div class="sec-head"><div class="kicker">Suggest an addition</div><h2>Who are we missing?</h2><p>Tell us about a Tunisian organization, business, artist or project. We review every suggestion and feature the ones that fit: Tunisian or Tunisia-focused, active, and open to the community.</p></div>
<form class="nice" action="{FORM_ACTION}" method="POST">{form_hidden('Directory suggestion')}
<div class="row"><div><label>Your name</label><input name="name" required></div><div><label>Your email</label><input type="email" name="email" required></div></div>
<div class="row"><div><label>Name of the organization / work / artist</label><input name="entry" required></div><div><label>Website or social link</label><input name="link" type="url" placeholder="https://"></div></div>
<div><label>Type</label><select name="type"><option>Organization</option><option>Business or maker</option><option>Artist</option><option>Film, book or project</option><option>Other</option></select></div>
<div><label>Why should it be here?</label><textarea name="why" required></textarea></div>
<div><button class="btn">Send suggestion</button></div></form>
</div></section>
"""
    page("/tunisia/", "Tunisian organizations & works", body, "A curated directory of Tunisian organizations, makers, artists and works in the United States and Tunisia, by Shakshuka.org.", "assets/img/barber-wall.jpg")

def build_membership():
    body = f"""
<section class="page-hero"><div class="bg" style="background-image:url(/assets/img/brik.jpg)"></div><div class="wrap in">
<div class="kicker">Membership</div><h1>Join the Shakshuka circle</h1>
<p>Members make the calendar possible, hear about events first, and get free seats at cooking classes and film nights. Membership is yearly and tax-deductible.</p></div></section>
<section><div class="wrap">
<div class="plans">
<div class="plan"><div class="kicker">Tier Spéciale</div><div class="price">$50<small> / year</small></div><p style="color:var(--muted)">The basic membership</p>
<ul><li>Newsletters and community emails</li><li>Early invitations to workshops and programs</li><li>1 free seat at a Shakshuka cooking class</li><li>40% off additional cooking classes</li><li>1 free movie ticket, 25% off up to 5 more</li><li>Access to the members' forum</li></ul>
<a class="btn ghost" href="/contact/?topic=membership-50">Join at $50</a></div>
<div class="plan best"><span class="best-tag">Best value</span><div class="kicker">Tier Fabuleux</div><div class="price">$100<small> / year</small></div><p style="color:var(--muted)">The Shakshuka VIP experience</p>
<ul><li>Everything in Spéciale</li><li>2 free cooking classes</li><li>2 free movie tickets (different films), 25% off up to 5 more</li><li>Early access to community events and the Iftar</li><li>Our thanks, and a bigger table for everyone</li></ul>
<a class="btn" href="/contact/?topic=membership-100">Join at $100</a></div>
</div>
<p class="center" style="margin-top:30px;color:var(--muted);font-size:.9rem">Membership payments will move to a secure online checkout (see <a href="/donate/">Donate</a>). Until then, write to us and we will send you the link.</p>
</div></section>
<section class="band-sand tile-bg"><div class="wrap narrow center"><h2>Not ready to join?</h2><p class="lede" style="margin:14px auto 26px">Sign up for the newsletter and come to a free event first. We will still save you a plate.</p>
<form class="inline-form" style="justify-content:center" action="{FORM_ACTION}" method="POST">{form_hidden('Newsletter signup')}<input type="email" name="email" placeholder="you@example.com" required aria-label="Email"><button class="btn">Subscribe</button></form></div></section>
"""
    page("/membership/", "Membership", body, "Become a member of Shakshuka.org from $50 a year: free cooking classes, movie tickets and early invitations.")

def build_donate():
    body = f"""
<section class="page-hero"><div class="bg" style="background-image:url(/assets/img/couscous.jpg)"></div><div class="wrap in">
<div class="kicker">Donate</div><h1>Help us make a difference for a greater community</h1>
<p>Your gift preserves Tunisian heritage and culture in the DMV, lets us host more events more often, and keeps a volunteer organization running. Shakshuka is a 501(c)(3) public charity; donations are tax-deductible.</p></div></section>
<section><div class="wrap"><div class="split">
<div class="text"><h2>Choose an amount</h2>
<form class="nice" action="{FORM_ACTION}" method="POST">{form_hidden('Donation pledge')}
<div><label>Frequency</label><div class="amounts"><label><input type="radio" name="frequency" value="One time" checked><span>One time</span></label><label><input type="radio" name="frequency" value="Monthly"><span>Monthly</span></label><label><input type="radio" name="frequency" value="Yearly"><span>Yearly</span></label></div></div>
<div><label>Amount</label><div class="amounts"><label><input type="radio" name="amount" value="50" checked><span>$50</span></label><label><input type="radio" name="amount" value="100"><span>$100</span></label><label><input type="radio" name="amount" value="200"><span>$200</span></label><label><input type="radio" name="amount" value="1000"><span>$1,000</span></label><label><input type="radio" name="amount" value="other"><span>Other</span></label></div></div>
<div class="row"><div><label>Name</label><input name="name" required></div><div><label>Email</label><input type="email" name="email" required></div></div>
<button class="btn">Continue to secure payment</button>
<p class="hint">You will be taken to our payment page (Zeffy, zero fees for nonprofits). A receipt for your taxes follows by email.</p></form></div>
<div><div class="pillar tile-corner"><h3>What your gift pays for</h3><ul style="padding-left:20px;margin-top:10px;line-height:1.9"><li><b>$50</b> covers a chef's ingredients for one online class</li><li><b>$100</b> brings a Tunisian film to a DC screen for one night</li><li><b>$200</b> seats a family who could not otherwise afford the Iftar</li><li><b>$1,000</b> sponsors a season of sing-alongs in public libraries</li></ul></div>
<p style="margin-top:22px;font-size:.9rem;color:var(--muted)">Shakshuka is a registered 501(c)(3) organization, EIN 92-3134851. Donors can deduct contributions under IRC Section 170; the IRS has determined that we are a public charity under the same section.</p></div>
</div></div></section>
"""
    page("/donate/", "Donate", body, "Support Shakshuka.org, the Tunisian-American community of the DMV. Tax-deductible, one time or monthly.")

def build_cookbook():
    body = f"""
<section><div class="wrap"><div class="split rev" style="align-items:start">
<div class="text"><div class="kicker">The cookbook</div><h1 style="font-size:clamp(2rem,4.5vw,3.2rem)">Discovering Tunisian Cuisine: A Journey of Food and Culture</h1>
<p class="lede" style="margin-top:18px">By Judith Dwan Hallet, Raoudha Guellali Ben Taarit and Hasna Trabelsi. Photographs by Stanley Ira Hallet. First edition 2019, 147-page stitched hardcover, signed.</p>
<p>More than a cookbook: a personal journal of six decades spent in Tunisia, pairing recipes with the landscapes and the people behind them. Brik, couscous, mechouia, the Mediterranean staples of lemon, tomato, pepper and herb, and the kitchen essentials hard to find in America, such as preserved lemons and <em>oumelleh</em> pickles, all in American measurements.</p>
<blockquote class="quote" style="margin:26px 0">“Awesome and authentic, both visually and content-wise.”<cite>Joan Nathan, James Beard and Julia Child Award-winning food writer</cite></blockquote>
<div class="pillar" style="margin-top:10px"><div style="display:flex;justify-content:space-between;align-items:baseline;gap:16px;flex-wrap:wrap"><div><b style="font-family:var(--display);font-size:2rem;color:var(--ink)">$36</b> <span style="color:var(--muted)">signed copy, limited</span></div><a class="btn" href="https://www.shakshuka.org/product-page/discovering-tunisian-cuisine-cookbook" target="_blank" rel="noopener">Purchase now</a></div>
<p class="hint" style="margin-top:12px;font-size:.85rem;color:var(--muted)">ISBN 978-1-7923-1830-6 · Publisher: Spirit of Place / Spirit of Design, Inc., Washington, DC. Proceeds support Shakshuka's programs.</p></div></div>
<figure class="pic framed" style="max-width:420px;margin:0 auto">{img('cookbook','Cover of Discovering Tunisian Cuisine', loading='eager')}</figure>
</div></div></section>
<section class="band-sand tile-bg"><div class="wrap"><div class="split">
<div class="text"><div class="kicker">Next</div><h2>The community cookbook</h2><p>We are collecting recipes from Tunisians across the DC area and beyond: where your dish comes from, when it is served, how to find the ingredients here, and the family story that goes with it. Every recipe will be tested before it is printed.</p><div class="btn-row" style="margin-top:20px"><a class="btn" href="/recipes/">Submit a recipe</a></div></div>
<figure class="pic framed">{img('blog-couscous','Making couscous by hand at the Kairouan Couscous Festival, 2025')}<figcaption>Kairouan Couscous Festival, 2025. Photo: Shakshuka</figcaption></figure>
</div></div></section>
"""
    page("/cookbook/", "Discovering Tunisian Cuisine", body, "Signed copies of Discovering Tunisian Cuisine by Judith Dwan Hallet, Raoudha Guellali Ben Taarit and Hasna Trabelsi, sold to support Shakshuka.org.", "assets/img/cookbook.jpg")

def build_recipes():
    body = f"""
<section class="page-hero"><div class="bg" style="background-image:url(/assets/img/ojja.jpg)"></div><div class="wrap in">
<div class="kicker">Call for recipes</div><h1>Your grandmother's recipe belongs in a book</h1>
<p>We are building a Tunisian recipe collection for the Shakshuka community in the DC area and beyond. Tell us the region it comes from, the season or occasion, where to find the ingredients in the US, and the story behind it.</p></div></section>
<section><div class="wrap narrow">
<form class="nice" action="{FORM_ACTION}" method="POST" enctype="multipart/form-data">{form_hidden('Recipe submission')}
<div class="row"><div><label>Your name</label><input name="name" required></div><div><label>Email</label><input type="email" name="email" required></div></div>
<div class="row"><div><label>Recipe name</label><input name="recipe" required></div><div><label>Category</label><select name="category"><option>Appetizers & beverages</option><option>Breads</option><option>Soups and stews</option><option>Salads</option><option>Side dishes</option><option>Main dishes</option><option>Breakfast</option><option>Desserts</option><option>Other</option></select></div></div>
<div class="row"><div><label>Region</label><select name="region"><option>Coastal Tunisia</option><option>Inland Tunisia</option><option>Desert south</option><option>Other / family blend</option></select></div><div><label>Season or occasion</label><select name="season"><option>All seasons</option><option>Spring</option><option>Summer</option><option>Fall</option><option>Winter</option><option>Ramadan / Eid</option><option>Weddings & celebrations</option></select></div></div>
<div><label>Ingredients (with US sourcing tips)</label><textarea name="ingredients" required></textarea></div>
<div><label>Method</label><textarea name="method" required style="min-height:180px"></textarea></div>
<div><label>The story: your family, your town, your tradition</label><textarea name="story"></textarea></div>
<div><label>Photo (optional)</label><input type="file" name="attachment" accept="image/*"><p class="hint">Recipes go through review and testing before publication. By submitting you allow Shakshuka to publish the recipe with your name.</p></div>
<div><button class="btn">Send my recipe</button></div></form>
</div></section>
"""
    page("/recipes/", "Call for recipes", body, "Submit your family's Tunisian recipe to the Shakshuka community cookbook.", "assets/img/ojja.jpg")

def build_blog():
    cards = ""
    for p in BLOG:
        cards += f"""<a class="card" href="{p['url']}" target="_blank" rel="noopener">{img(p['img'], p['title'])}<div class="body"><div class="meta"><span>{fmt_date(p['date'])}</span><span class="past">{esc(p['author'])}</span></div><h3>{esc(p['title'])}</h3><p>{esc(p['summary'])}</p><div class="more">Read on shakshuka.org →</div></div></a>"""
    body = f"""
<section class="page-hero"><div class="bg" style="background-image:url(/assets/img/harissa.jpg)"></div><div class="wrap in">
<div class="kicker">Shak Blog</div><h1>Recipes, films, and the red gold</h1>
<p>Stories from the Shakshuka test kitchen and from our events. Posts open on our current blog while we move the archive here.</p></div></section>
<section><div class="wrap"><div class="grid g3">{cards}</div></div></section>
"""
    page("/blog/", "Blog", body, "The Shakshuka blog: Tunisian recipes, harissa history and event stories.", "assets/img/harissa.jpg")

def build_volunteer():
    body = f"""
<section class="page-hero"><div class="bg" style="background-image:url(/assets/img/carthage.jpg)"></div><div class="wrap in">
<div class="kicker">Volunteer</div><h1>Bring a dish, bring a skill</h1><p>Shakshuka is run entirely by volunteers. Whether you have one evening a season or a few hours a week, there is a place for you.</p></div></section>
<section><div class="wrap"><div class="split">
<div class="text"><h2>Where we need help</h2><ul><li><b>Events:</b> check-in, setup, hosting, photography</li><li><b>Kitchen:</b> chefs and home cooks for classes and the Iftar</li><li><b>Stories:</b> writing, social media, translation (Arabic, French)</li><li><b>Back office:</b> bookkeeping, grant writing, membership</li><li><b>Music:</b> musicians and singers for the sing-alongs</li></ul></div>
<form class="nice" action="{FORM_ACTION}" method="POST">{form_hidden('Volunteer signup')}
<div class="row"><div><label>Name</label><input name="name" required></div><div><label>Email</label><input type="email" name="email" required></div></div>
<div><label>I can help with</label><input name="skills" placeholder="events, cooking, photos, translation…"></div>
<div><label>Anything else</label><textarea name="message"></textarea></div><div><button class="btn">Count me in</button></div></form>
</div></div></section>
"""
    page("/volunteer/", "Volunteer", body, "Volunteer with Shakshuka.org, the Tunisian-American community of the DMV.", "assets/img/carthage.jpg")

def build_contact():
    body = f"""
<section><div class="wrap"><div class="split" style="align-items:start">
<div class="text"><div class="kicker">Contact</div><h1 style="font-size:clamp(2rem,4.5vw,3.2rem)">Say hello</h1>
<p class="lede" style="margin:18px 0">Uniting the Tunisian community of the DMV, about 5,000 of us across Washington, DC, Maryland and Virginia. New in town, have a question, want to partner? Write to us.</p>
<p><a href="mailto:{CONTACT_EMAIL}">{CONTACT_EMAIL}</a></p>
<p style="margin-top:20px;font-size:.9rem;color:var(--muted)">We only use your details to answer you and, if you tick the box, to send the newsletter. No lists are sold or shared.</p></div>
<form class="nice" action="{FORM_ACTION}" method="POST">{form_hidden('Contact form')}
<div class="row"><div><label>First name</label><input name="first" required></div><div><label>Last name</label><input name="last"></div></div>
<div><label>Email</label><input type="email" name="email" required></div>
<div><label>Topic</label><select name="topic" id="topic"><option value="general">General</option><option value="membership-50">Membership · Tier Spéciale ($50)</option><option value="membership-100">Membership · Tier Fabuleux ($100)</option><option value="event">Event idea or partnership</option><option value="press">Press</option></select></div>
<div><label>Message</label><textarea name="message" required></textarea></div>
<div><label style="display:flex;gap:10px;align-items:center;text-transform:none;letter-spacing:0;font-weight:600"><input type="checkbox" name="newsletter" value="yes" style="width:auto">Also subscribe me to the newsletter</label></div>
<div><button class="btn">Send</button></div></form>
</div></div></section>
<script>const t=new URLSearchParams(location.search).get('topic');if(t){{const s=document.getElementById('topic');if([...s.options].some(o=>o.value===t))s.value=t}}</script>
"""
    page("/contact/", "Contact", body, "Contact Shakshuka.org, the Tunisian-American community of the DMV.")

def build_misc():
    page("/thanks/", "Thank you", """<section><div class="wrap narrow center"><div class="kicker">Received</div><h1>Shukran, merci, thank you</h1><p class="lede" style="margin:18px auto 28px">Your message is in. A volunteer will get back to you within a few days. Meanwhile, see what is coming up.</p><div class="btn-row"><a class="btn" href="/events/">Events</a><a class="btn ghost" href="/">Home</a></div></div></section>""", "Thank you")
    rows = "".join(f"<tr><td><img src='/assets/img/{k}-sm.jpg' alt='' style='width:90px;border-radius:8px'></td><td>{esc(t)}</td><td>{esc(a)}</td><td>{l}</td></tr>" for k, t, a, l in PHOTO_CREDITS)
    page("/credits/", "Photo credits", f"""<section><div class="wrap narrow"><div class="kicker">Credits</div><h1 style="font-size:2.4rem">Photo credits</h1>
<p class="lede" style="margin:16px 0 28px">Photographs of Tunisia on this site come from Wikimedia Commons under Creative Commons licences, with thanks to the photographers. Event artwork, film stills and portraits belong to their respective owners and are used to document Shakshuka's events. The Hallet photograph, the cookbook cover and the couscous festival photo are courtesy of their authors.</p>
<table class="credits"><tr><th></th><th>Image</th><th>Author</th><th>Licence</th></tr>{rows}</table></div></section>""", "Photo credits")
    (OUT / "404.html").write_text(f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta http-equiv="refresh" content="0;url={BASE}/"><title>Not found</title></head><body><p>Page not found. <a href="/">Back home</a>.</p></body></html>""")
    # sitemap + robots
    urls = [p.relative_to(OUT).parent for p in OUT.rglob("index.html") if "review" not in str(p)]
    sm = "\n".join(f"<url><loc>{SITE}/{str(u) + '/' if str(u) != '.' else ''}</loc></url>" for u in urls)
    (OUT / "sitemap.xml").write_text(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{sm}\n</urlset>')
    (OUT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n")
    (OUT / ".nojekyll").write_text("")

def build_review():
    """Unlisted review page for the board (not in nav or sitemap)."""
    src = ROOT / "ref-review-page.html"
    if not src.exists(): return
    body = src.read_text()
    doc = '<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex"><link rel="icon" href="' + BASE + '/assets/img/logo.jpg"></head><body>' + body + '</body></html>'
    out = OUT / "review" / "index.html"; out.parent.mkdir(parents=True, exist_ok=True); out.write_text(doc)
    sent = OUT / "review" / "sent" / "index.html"; sent.parent.mkdir(parents=True, exist_ok=True)
    sent.write_text('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex"><title>Sent</title><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Yeseva+One&family=Roboto&display=swap"><style>body{margin:0;background:#fcf7f1;color:#4a3f48;font:18px/1.6 Roboto,sans-serif;display:grid;place-items:center;min-height:100vh;padding:24px;text-align:center}h1{font:400 2.4rem "Yeseva One",serif;color:#1f1b22;margin:0 0 12px}a{color:#5e2246}</style></head><body><div><h1>Sent. Shukran, Leila!</h1><p>Your answers are on their way to Ines. She will get back to you within a day or two.</p><p><a href="' + BASE + '/">Back to the new site</a></p></div></body></html>')

def main():
    (OUT / "assets").mkdir(parents=True, exist_ok=True)
    (OUT / "assets/style.css").write_text(prefix(CSS))
    (OUT / "assets/site.js").write_text(JS)
    # clean generated pages (keep assets)
    for p in OUT.iterdir():
        if p.name in ("assets", "CNAME"): continue
        shutil.rmtree(p) if p.is_dir() else p.unlink()
    build_home(); build_about(); build_team(); build_events(); build_tunisia(); build_membership()
    build_donate(); build_cookbook(); build_recipes(); build_blog(); build_volunteer(); build_contact(); build_misc(); build_review()
    n = len(list(OUT.rglob("index.html")))
    print(f"built {n} pages → {OUT}")

if __name__ == "__main__":
    main()
