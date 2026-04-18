"""Auto-seed realistic IU data on first run if DB is empty."""
from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session
from models import Student, Event, Attendance, EventCode


def utcnow():
    return datetime.now(timezone.utc).replace(tzinfo=None)


def seed_data(db: Session):
    if db.query(Student).count() > 0:
        return

    now = utcnow()
    days_since_sunday = (now.weekday() + 1) % 7
    week_start = (now - timedelta(days=days_since_sunday)).replace(
        hour=0, minute=0, second=0, microsecond=0
    )

    # ── Events (realistic IU events across all campuses) ─────────────────────
    events = [
        Event(
            title="Luddy School AI & Innovation Summit",
            category="Tech",
            description=(
                "Join Luddy School faculty, students, and industry partners to explore "
                "the future of artificial intelligence, human-computer interaction, and "
                "data science. Keynotes, panels, and live demos."
            ),
            campus="IU Bloomington",
            event_url="https://luddy.indiana.edu/events",
            check_in_code="LUDDY2025",
            points=25,
            event_date=week_start + timedelta(days=1, hours=9),
        ),
        Event(
            title="IU Kelley Business Career Expo",
            category="Career",
            description=(
                "Connect with 80+ employers from finance, consulting, marketing, "
                "and tech. Bring copies of your resume. Business professional attire required."
            ),
            campus="IU Bloomington",
            event_url="https://kelley.iu.edu/events",
            check_in_code="KELLEY25",
            points=20,
            event_date=week_start + timedelta(days=1, hours=13),
        ),
        Event(
            title="IUPUI Research Showcase",
            category="Academic",
            description=(
                "Graduate and undergraduate students from IUPUI present their research "
                "across disciplines including medicine, engineering, liberal arts, and STEM. "
                "Open to all IU community members."
            ),
            campus="IU Indianapolis",
            event_url="https://research.iu.edu/events",
            check_in_code="IUPUIRC5",
            points=15,
            event_date=week_start + timedelta(days=2, hours=10),
        ),
        Event(
            title="Wellness & Mental Health Workshop",
            category="Health",
            description=(
                "IU Health Center hosts an interactive workshop on stress management, "
                "mindfulness techniques, and building resilience. Free snacks provided."
            ),
            campus="IU Bloomington",
            event_url="https://healthcenter.iu.edu",
            check_in_code="WELLNS25",
            points=10,
            event_date=week_start + timedelta(days=2, hours=14),
        ),
        Event(
            title="IU East STEM Networking Night",
            category="Career",
            description=(
                "Students from computer science, biology, chemistry, and math connect "
                "with regional employers. Hosted at the IU East Science Building atrium."
            ),
            campus="IU East",
            event_url="https://iue.iu.edu/events",
            check_in_code="IUEAST25",
            points=15,
            event_date=week_start + timedelta(days=2, hours=17),
        ),
        Event(
            title="Luddy Hacks Hackathon Kickoff",
            category="Tech",
            description=(
                "Opening ceremony for the 24-hour Luddy Hacks hackathon. Team formation, "
                "sponsor introductions, project pitches, and dinner. All skill levels welcome."
            ),
            campus="IU Bloomington",
            event_url="https://iuhacks.io",
            check_in_code="LHACKS25",
            points=30,
            event_date=week_start + timedelta(days=3, hours=9),
        ),
        Event(
            title="IU South Bend Arts & Culture Fair",
            category="Cultural",
            description=(
                "Celebrating diversity through art, music, dance, and cultural performances "
                "by student organizations. Includes food trucks and vendor booths."
            ),
            campus="IU South Bend",
            event_url="https://iusb.edu/events",
            check_in_code="SBARTS5",
            points=10,
            event_date=week_start + timedelta(days=3, hours=12),
        ),
        Event(
            title="IU Kokomo Entrepreneurship Pitch Night",
            category="Career",
            description=(
                "Students pitch startup ideas to a panel of local investors and IU faculty. "
                "Top three teams win seed funding and mentorship opportunities."
            ),
            campus="IU Kokomo",
            event_url="https://iuk.iu.edu/events",
            check_in_code="KOKOPIT5",
            points=20,
            event_date=week_start + timedelta(days=3, hours=18),
        ),
        Event(
            title="IU Northwest Community Leadership Forum",
            category="Social",
            description=(
                "Panel discussion with community leaders, IU faculty, and students on "
                "civic engagement, public policy, and social impact in Northwest Indiana."
            ),
            campus="IU Northwest",
            event_url="https://iun.iu.edu/events",
            check_in_code="NWLEAD5",
            points=15,
            event_date=week_start + timedelta(days=4, hours=11),
        ),
        Event(
            title="IU Southeast Tech & Coding Bootcamp",
            category="Tech",
            description=(
                "A full-day intensive coding workshop covering Python, web development, "
                "and database fundamentals. Beginner-friendly with take-home projects."
            ),
            campus="IU Southeast",
            event_url="https://ius.iu.edu/events",
            check_in_code="SECODE5",
            points=20,
            event_date=week_start + timedelta(days=4, hours=9),
        ),
        Event(
            title="IU Columbus Diversity & Inclusion Summit",
            category="Cultural",
            description=(
                "Annual summit featuring keynote speakers, workshops, and panel discussions "
                "celebrating diversity, equity, and inclusion across the IU system."
            ),
            campus="IU Columbus",
            event_url="https://iuc.iu.edu/events",
            check_in_code="IUCDIV5",
            points=15,
            event_date=week_start + timedelta(days=4, hours=13),
        ),
        Event(
            title="IU Fort Wayne Engineering Design Expo",
            category="Academic",
            description=(
                "Engineering students showcase their senior capstone projects. "
                "Judges from industry evaluate designs for innovation, feasibility, and impact."
            ),
            campus="IU Fort Wayne",
            event_url="https://iufw.iu.edu/events",
            check_in_code="FWEXPO5",
            points=20,
            event_date=week_start + timedelta(days=5, hours=10),
        ),
        Event(
            title="Maurer School of Law Mock Trial",
            category="Academic",
            description=(
                "Pre-law and law students argue a simulated civil case before a panel of "
                "practicing attorneys and alumni judges. Open for observation."
            ),
            campus="IU Bloomington",
            event_url="https://law.indiana.edu/events",
            check_in_code="LAWMOCK5",
            points=15,
            event_date=week_start + timedelta(days=5, hours=14),
        ),
        Event(
            title="IU Indianapolis Health Sciences Symposium",
            category="Health",
            description=(
                "Medical, nursing, and public health students present research posters "
                "and case studies. Sponsored by IU School of Medicine and IUPUI Health."
            ),
            campus="IU Indianapolis",
            event_url="https://medicine.iu.edu/events",
            check_in_code="HEALTH25",
            points=20,
            event_date=week_start + timedelta(days=5, hours=9),
        ),
        Event(
            title="IU Sustainability & Green Campus Expo",
            description=(
                "Learn about IU's carbon neutrality goals, sustainability initiatives, "
                "and how students can get involved. Features electric vehicle demos and recycling drives."
            ),
            category="Social",
            campus="IU Bloomington",
            event_url="https://sustain.indiana.edu",
            check_in_code="GREEN25",
            points=10,
            event_date=week_start + timedelta(days=6, hours=11),
        ),
        # ── 32 additional events spread over next 30 days ────────────────────
        Event(
            title="Little 500 Kickoff Party",
            category="Sports",
            campus="IU Bloomington",
            check_in_code="LITTLE500",
            points=15,
            event_date=now + timedelta(days=1, hours=16),
        ),
        Event(
            title="IU Career Fair: STEM Edition",
            category="Career",
            campus="IU Bloomington",
            check_in_code="STEMFAIR",
            points=20,
            event_date=now + timedelta(days=2, hours=10),
        ),
        Event(
            title="Lotus World Music & Arts Festival",
            category="Cultural",
            campus="IU Bloomington",
            check_in_code="LOTUS25",
            points=15,
            event_date=now + timedelta(days=3, hours=14),
        ),
        Event(
            title="Undergraduate Research Symposium",
            category="Academic",
            campus="IU Bloomington",
            check_in_code="UGRSYMP5",
            points=20,
            event_date=now + timedelta(days=4, hours=9),
        ),
        Event(
            title="IU Basketball Watch Party",
            category="Sports",
            campus="IU Bloomington",
            check_in_code="BBALL25",
            points=10,
            event_date=now + timedelta(days=4, hours=19),
        ),
        Event(
            title="Study Abroad Information Fair",
            category="Academic",
            campus="IU Bloomington",
            check_in_code="STUDYAB5",
            points=10,
            event_date=now + timedelta(days=5, hours=11),
        ),
        Event(
            title="Kelley Consulting Case Competition",
            category="Career",
            campus="IU Bloomington",
            check_in_code="KELCASE5",
            points=25,
            event_date=now + timedelta(days=6, hours=9),
        ),
        Event(
            title="Data Science & ML Workshop",
            category="Tech",
            campus="IU Bloomington",
            check_in_code="DATASCI5",
            points=20,
            event_date=now + timedelta(days=7, hours=13),
        ),
        Event(
            title="Latino Heritage Month Celebration",
            category="Cultural",
            campus="IU Indianapolis",
            check_in_code="LATINO25",
            points=10,
            event_date=now + timedelta(days=8, hours=17),
        ),
        Event(
            title="IU Day of Service: Community Volunteer",
            category="Social",
            campus="IU Indianapolis",
            check_in_code="DAYSERV5",
            points=15,
            event_date=now + timedelta(days=9, hours=8),
        ),
        Event(
            title="Medical School Open House",
            category="Academic",
            campus="IU Indianapolis",
            check_in_code="MEDOPEN5",
            points=20,
            event_date=now + timedelta(days=10, hours=10),
        ),
        Event(
            title="Cybersecurity Awareness Workshop",
            category="Tech",
            campus="IU Indianapolis",
            check_in_code="CYBER25",
            points=15,
            event_date=now + timedelta(days=11, hours=14),
        ),
        Event(
            title="IU East Community Art Exhibition",
            category="Cultural",
            campus="IU East",
            check_in_code="IUEART5",
            points=10,
            event_date=now + timedelta(days=12, hours=12),
        ),
        Event(
            title="Financial Wellness Seminar",
            category="Health",
            campus="IU East",
            check_in_code="FINWEL5",
            points=10,
            event_date=now + timedelta(days=13, hours=15),
        ),
        Event(
            title="IU Kokomo Science Fair",
            category="Academic",
            campus="IU Kokomo",
            check_in_code="KOKSCI5",
            points=15,
            event_date=now + timedelta(days=14, hours=10),
        ),
        Event(
            title="Northwest Student Leadership Summit",
            category="Social",
            campus="IU Northwest",
            check_in_code="NWSLS25",
            points=20,
            event_date=now + timedelta(days=15, hours=9),
        ),
        Event(
            title="South Bend Civic Engagement Forum",
            category="Social",
            campus="IU South Bend",
            check_in_code="SBCEF25",
            points=15,
            event_date=now + timedelta(days=16, hours=13),
        ),
        Event(
            title="Southeast Business Pitch Competition",
            category="Career",
            campus="IU Southeast",
            check_in_code="SEBPC25",
            points=25,
            event_date=now + timedelta(days=17, hours=14),
        ),
        Event(
            title="Columbus Nursing Clinical Showcase",
            category="Academic",
            campus="IU Columbus",
            check_in_code="COLNRS5",
            points=20,
            event_date=now + timedelta(days=18, hours=10),
        ),
        Event(
            title="Fort Wayne Engineering Career Night",
            category="Career",
            campus="IU Fort Wayne",
            check_in_code="FWECN25",
            points=20,
            event_date=now + timedelta(days=19, hours=17),
        ),
        Event(
            title="IU Mental Health Awareness Walk",
            category="Health",
            campus="IU Bloomington",
            check_in_code="MHWALK5",
            points=10,
            event_date=now + timedelta(days=20, hours=8),
        ),
        Event(
            title="Open Source Contribution Day",
            category="Tech",
            campus="IU Bloomington",
            check_in_code="OPENSR5",
            points=20,
            event_date=now + timedelta(days=21, hours=10),
        ),
        Event(
            title="IU vs Purdue Rivalry Tailgate",
            category="Sports",
            campus="IU Bloomington",
            check_in_code="RIVTAL5",
            points=15,
            event_date=now + timedelta(days=22, hours=12),
        ),
        Event(
            title="AI Ethics Panel Discussion",
            category="Tech",
            campus="IU Bloomington",
            check_in_code="AIETHIC5",
            points=15,
            event_date=now + timedelta(days=23, hours=14),
        ),
        Event(
            title="Asian Pacific Heritage Showcase",
            category="Cultural",
            campus="IU Indianapolis",
            check_in_code="APHA2025",
            points=10,
            event_date=now + timedelta(days=24, hours=16),
        ),
        Event(
            title="Free Flu Shot & Health Screening",
            category="Health",
            campus="IU Bloomington",
            check_in_code="FLUSHOOT",
            points=10,
            event_date=now + timedelta(days=25, hours=9),
        ),
        Event(
            title="Greek Life Philanthropy Fair",
            category="Social",
            campus="IU Bloomington",
            check_in_code="GREEKPH5",
            points=10,
            event_date=now + timedelta(days=26, hours=11),
        ),
        Event(
            title="Resume & LinkedIn Workshop",
            category="Career",
            campus="IU Indianapolis",
            check_in_code="RESLINK5",
            points=15,
            event_date=now + timedelta(days=27, hours=13),
        ),
        Event(
            title="IU Sustainability Earth Week",
            category="Social",
            campus="IU Bloomington",
            check_in_code="EARTHWK5",
            points=10,
            event_date=now + timedelta(days=28, hours=10),
        ),
        Event(
            title="International Student Welcome Mixer",
            category="Cultural",
            campus="IU Bloomington",
            check_in_code="INTLMIX5",
            points=10,
            event_date=now + timedelta(days=29, hours=18),
        ),
        Event(
            title="Midnight Run Charity 5K",
            category="Sports",
            campus="IU Bloomington",
            check_in_code="MIDRUN25",
            points=15,
            event_date=now + timedelta(days=30, hours=0),
        ),
        Event(
            title="App Development Bootcamp",
            category="Tech",
            campus="IU Southeast",
            check_in_code="APPBOOT5",
            points=20,
            event_date=now + timedelta(days=30, hours=9),
        ),
    ]
    db.add_all(events)
    db.flush()

    # ── Students (25 realistic IU students across all campuses) ───────────────
    students = [
        # IU Bloomington (8)
        Student(name="Aiden Ramirez",     iu_username="aramirez",  campus="IU Bloomington",
                major="Computer Science", year="Junior"),
        Student(name="Sofia Chen",         iu_username="schen",     campus="IU Bloomington",
                major="Informatics", year="Senior"),
        Student(name="Marcus Williams",    iu_username="mwilliams", campus="IU Bloomington",
                major="Business", year="Junior"),
        Student(name="Priya Patel",        iu_username="ppatel",    campus="IU Bloomington",
                major="Mathematics", year="Sophomore"),
        Student(name="Ethan Kowalski",     iu_username="ekowalski", campus="IU Bloomington",
                major="Computer Science", year="Senior"),
        Student(name="Olivia Thompson",    iu_username="othompson", campus="IU Bloomington",
                major="Psychology", year="Freshman"),
        Student(name="James Okonkwo",      iu_username="jokonkwo",  campus="IU Bloomington",
                major="Informatics", year="Graduate"),
        Student(name="Emma Nguyen",        iu_username="enguyen",   campus="IU Bloomington",
                major="Biology", year="Junior"),
        # IU Indianapolis (5)
        Student(name="Carlos Rivera",      iu_username="crivera",   campus="IU Indianapolis",
                major="Nursing", year="Senior"),
        Student(name="Fatima Al-Rashid",   iu_username="falrashid", campus="IU Indianapolis",
                major="Computer Science", year="Sophomore"),
        Student(name="Tyler Brooks",       iu_username="tbrooks",   campus="IU Indianapolis",
                major="Business", year="Junior"),
        Student(name="Amara Osei",         iu_username="aosei",     campus="IU Indianapolis",
                major="Public Health", year="Graduate"),
        Student(name="Liam Fitzgerald",    iu_username="lfitzgerald", campus="IU Indianapolis",
                major="Biology", year="Sophomore"),
        # IU East (2)
        Student(name="Hannah Kim",         iu_username="hkim",      campus="IU East",
                major="Psychology", year="Junior"),
        Student(name="Noah Patterson",     iu_username="npatterson", campus="IU East",
                major="Computer Science", year="Freshman"),
        # IU Kokomo (2)
        Student(name="Zoe Hernandez",      iu_username="zhernandez", campus="IU Kokomo",
                major="Business", year="Senior"),
        Student(name="Ben Okafor",         iu_username="bokafor",   campus="IU Kokomo",
                major="Mathematics", year="Junior"),
        # IU Northwest (2)
        Student(name="Layla Singh",        iu_username="lsingh",    campus="IU Northwest",
                major="Informatics", year="Graduate"),
        Student(name="Diego Morales",      iu_username="dmorales",  campus="IU Northwest",
                major="Social Work", year="Senior"),
        # IU South Bend (2)
        Student(name="Chloe Baker",        iu_username="cbaker",    campus="IU South Bend",
                major="Education", year="Junior"),
        Student(name="Lucas Johansson",    iu_username="ljohansson", campus="IU South Bend",
                major="Business", year="Sophomore"),
        # IU Southeast (2)
        Student(name="Mia Foster",         iu_username="mfoster",   campus="IU Southeast",
                major="Computer Science", year="Senior"),
        Student(name="Elijah Washington",  iu_username="ewashington", campus="IU Southeast",
                major="Criminal Justice", year="Junior"),
        # IU Columbus (1)
        Student(name="Ava Martinez",       iu_username="amartinez", campus="IU Columbus",
                major="Nursing", year="Sophomore"),
        # IU Fort Wayne (1)
        Student(name="Jack Schneider",     iu_username="jschneider", campus="IU Fort Wayne",
                major="Engineering", year="Graduate"),
    ]
    db.add_all(students)
    db.flush()

    s = students  # alias for brevity
    e = events

    # ── Attendance records (spread across the week, realistic point totals) ───
    # Format: (student_index, event_index, day_offset, hour_offset)
    checkins = [
        # Aiden — top performer: 5 events = 25+30+20+15+10 = 100 pts
        (0, 0, 1, 9),   (0, 5, 3, 9),   (0, 1, 1, 13),  (0, 2, 2, 10),  (0, 3, 2, 14),
        # Sofia — 4 events = 25+30+20+15 = 90 pts
        (1, 0, 1, 9),   (1, 5, 3, 9),   (1, 1, 1, 13),  (1, 4, 2, 17),
        # Marcus — 4 events = 25+30+15+10 = 80 pts
        (2, 0, 1, 9),   (2, 5, 3, 10),  (2, 6, 3, 12),  (2, 14, 6, 11),
        # Carlos — 3 events = 15+20+20 = 55 pts
        (8, 2, 2, 10),  (8, 13, 5, 9),  (8, 7, 3, 18),
        # Priya — 3 events = 25+20+10 = 55 pts
        (3, 0, 1, 9),   (3, 1, 1, 14),  (3, 3, 2, 14),
        # Fatima — 3 events = 15+20+15 = 50 pts
        (9, 2, 2, 10),  (9, 13, 5, 9),  (9, 8, 4, 11),
        # Ethan — 3 events = 30+10+10 = 50 pts
        (4, 5, 3, 9),   (4, 3, 2, 15),  (4, 14, 6, 11),
        # Olivia — 3 events = 25+15+10 = 50 pts
        (5, 0, 1, 10),  (5, 12, 5, 14), (5, 14, 6, 12),
        # Layla — 2 events = 15+20 = 35 pts
        (17, 8, 4, 11), (17, 11, 5, 10),
        # Tyler — 2 events = 15+20 = 35 pts
        (10, 2, 2, 10), (10, 13, 5, 10),
        # James — 2 events = 30+10 = 40 pts
        (6, 5, 3, 9),   (6, 6, 3, 12),
        # Hannah — 2 events = 15+20 = 35 pts
        (13, 4, 2, 17), (13, 9, 4, 9),
        # Diego — 2 events = 15+10 = 25 pts
        (18, 8, 4, 11), (18, 6, 3, 13),
        # Amara — 2 events = 20+15 = 35 pts
        (11, 13, 5, 9), (11, 2, 2, 11),
        # Emma — 2 events = 25+15 = 40 pts
        (7, 0, 1, 10),  (7, 12, 5, 14),
        # Noah — 2 events = 15+20 = 35 pts
        (14, 4, 2, 17), (14, 9, 4, 9),
        # Liam — 2 events = 20+15 = 35 pts
        (12, 13, 5, 9), (12, 8, 4, 12),
        # Zoe — 1 event = 20 pts
        (15, 7, 3, 18),
        # Ben — 1 event = 20 pts
        (16, 7, 3, 19),
        # Chloe — 1 event = 10 pts
        (19, 6, 3, 12),
        # Lucas — 1 event = 10 pts
        (20, 6, 3, 13),
        # Mia — 1 event = 20 pts
        (21, 9, 4, 9),
        # Elijah — 1 event = 20 pts
        (22, 9, 4, 10),
        # Ava — 1 event = 15 pts
        (23, 10, 4, 13),
        # Jack — 1 event = 20 pts
        (24, 11, 5, 10),
    ]

    records = []
    seen = set()
    for (si, ei, day, hour) in checkins:
        key = (si, ei)
        if key in seen:
            continue
        seen.add(key)
        records.append(Attendance(
            student_id=s[si].id,
            event_id=e[ei].id,
            points_earned=e[ei].points,
            checked_in_at=week_start + timedelta(days=day, hours=hour, minutes=(si * 3 + ei) % 45),
        ))

    db.add_all(records)

    # ── Seed event_codes table ────────────────────────────────────────────────
    for ev in events:
        db.add(EventCode(
            event_id=ev.id,
            event_name=ev.title,
            code=ev.check_in_code,
            set_by="system",
            updated_at=utcnow(),
        ))

    db.commit()
    print(
        "[EngageIU] Seeded {} events, {} students, {} attendance records.".format(
            len(events), len(students), len(records)
        )
    )

if __name__ == "__main__":
    from database import SessionLocal
    db = SessionLocal()
    try:
        seed_data(db)
    finally:
        db.close()

