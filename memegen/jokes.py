"""
Meme template definitions and dev/startup joke bank for DevMemes.

Each MEME entry: (template_key, category, [text_field_1, text_field_2, ...])
"""

# ── Template definitions ──────────────────────────────────────────────────────
# render types: top_bottom | drake | two_button | four_panel | bottom_only |
#               sign | handshake

TEMPLATES = {
    "drake": {
        "name": "Drake Hotline Bling",
        "url": "https://i.imgflip.com/30b1gx.jpg",
        "render": "drake",
        "labels": ["Drake Rejects:", "Drake Approves:"],
    },
    "this_is_fine": {
        "name": "This Is Fine",
        "url": "https://i.imgflip.com/wxica.jpg",
        "render": "bottom_only",
        "labels": ["Caption:"],
    },
    "one_does_not": {
        "name": "One Does Not Simply",
        "url": "https://i.imgflip.com/1bij.jpg",
        "render": "top_bottom",
        "labels": ["Top text:", "Bottom text:"],
    },
    "two_buttons": {
        "name": "Two Buttons",
        "url": "https://i.imgflip.com/1g8my4.jpg",
        "render": "two_button",
        "labels": ["Button 1 (left):", "Button 2 (right):"],
    },
    "change_my_mind": {
        "name": "Change My Mind",
        "url": "https://i.imgflip.com/24y43o.jpg",
        "render": "sign",
        "labels": ["Sign text:"],
    },
    "expanding_brain": {
        "name": "Expanding Brain",
        "url": "https://i.imgflip.com/1jwhww.jpg",
        "render": "four_panel",
        "labels": ["Panel 1 (small brain):", "Panel 2:", "Panel 3:", "Panel 4 (galaxy brain):"],
    },
    "surprised_pikachu": {
        "name": "Surprised Pikachu",
        "url": "https://i.imgflip.com/2kbn1e.jpg",
        "render": "top_bottom",
        "labels": ["Top text:", "Bottom text:"],
    },
    "mocking_spongebob": {
        "name": "Mocking SpongeBob",
        "url": "https://i.imgflip.com/1otk96.jpg",
        "render": "top_bottom",
        "labels": ["Original statement:", "Mocking response:"],
    },
    "waiting_skeleton": {
        "name": "Waiting Skeleton",
        "url": "https://i.imgflip.com/2fm6x.jpg",
        "render": "top_bottom",
        "labels": ["Waiting for:", "Time elapsed:"],
    },
    "success_kid": {
        "name": "Success Kid",
        "url": "https://i.imgflip.com/1bhk.jpg",
        "render": "top_bottom",
        "labels": ["Top text:", "Bottom text:"],
    },
    "disaster_girl": {
        "name": "Disaster Girl",
        "url": "https://i.imgflip.com/23ls.jpg",
        "render": "top_bottom",
        "labels": ["Top text:", "Bottom text:"],
    },
    "epic_handshake": {
        "name": "Epic Handshake",
        "url": "https://i.imgflip.com/28j0te.jpg",
        "render": "handshake",
        "labels": ["Left arm:", "Right arm:", "Handshake (result):"],
    },
    "ancient_aliens": {
        "name": "Ancient Aliens",
        "url": "https://i.imgflip.com/26am.jpg",
        "render": "top_bottom",
        "labels": ["Top text:", "Bottom text:"],
    },
    "y_u_no": {
        "name": "Y U No",
        "url": "https://i.imgflip.com/1e.jpg",
        "render": "top_bottom",
        "labels": ["Y U NO...:", "Bottom:"],
    },
    "first_world": {
        "name": "First World Problems",
        "url": "https://i.imgflip.com/1e7ql7.jpg",
        "render": "top_bottom",
        "labels": ["Top text:", "Bottom text:"],
    },
}

CATEGORIES = ["All", "Debugging", "Git", "Meetings", "Startup Life", "Stack Overflow", "Deployment"]

# ── Joke bank ─────────────────────────────────────────────────────────────────
# (template_key, category, [text1, text2, ...])

MEMES = [

    # ══════════════════════════════════════════════════════════════════════════
    # DEBUGGING
    # ══════════════════════════════════════════════════════════════════════════
    ("drake", "Debugging", [
        "READING THE ERROR MESSAGE",
        "GOOGLING THE EXACT SAME ERROR MESSAGE WORD FOR WORD",
    ]),
    ("drake", "Debugging", [
        "USING THE DEBUGGER LIKE A PROFESSIONAL",
        "ADDING console.log('HERE 1') console.log('HERE 2') UNTIL IT WORKS",
    ]),
    ("drake", "Debugging", [
        "FIXING THE ROOT CAUSE",
        "WRAPPING EVERYTHING IN TRY/CATCH AND CALLING IT FIXED",
    ]),
    ("drake", "Debugging", [
        "WRITING UNIT TESTS BEFORE SHIPPING",
        "HOPING QA FINDS IT BEFORE THE CLIENT DOES",
    ]),
    ("one_does_not", "Debugging", [
        "ONE DOES NOT SIMPLY",
        "DEBUG SOMEONE ELSE'S CODE WITHOUT QUESTIONING EVERY DECISION THEY MADE",
    ]),
    ("one_does_not", "Debugging", [
        "ONE DOES NOT SIMPLY",
        "GOOGLE AN ERROR AND FIND AN ANSWER THAT ISN'T FROM 2014",
    ]),
    ("waiting_skeleton", "Debugging", [
        "WAITING FOR THE BUG THAT 'ONLY HAPPENS IN PRODUCTION' TO REPRODUCE LOCALLY",
        "IT NEVER DOES",
    ]),
    ("success_kid", "Debugging", [
        "SPENT 8 HOURS DEBUGGING",
        "IT WAS A MISSING SEMICOLON",
    ]),
    ("success_kid", "Debugging", [
        "RANDOMLY DELETED A LINE OF CODE",
        "BUG DISAPPEARED. NOT TOUCHING IT.",
    ]),
    ("surprised_pikachu", "Debugging", [
        "WRITES ZERO TESTS AND SHIPS DIRECTLY TO PRODUCTION",
        "WHEN PROD BREAKS AT 3AM ON A SATURDAY",
    ]),
    ("this_is_fine", "Debugging", [
        "THE CODE WORKS BUT NOBODY KNOWS WHY AND WE'RE AFRAID TO TOUCH IT",
    ]),
    ("this_is_fine", "Debugging", [
        "THE BUG DISAPPEARS WHEN YOU TRY TO SHOW IT TO YOUR MANAGER",
    ]),
    ("ancient_aliens", "Debugging", [
        "IT WAS WORKING PERFECTLY YESTERDAY",
        "COSMIC RAYS",
    ]),
    ("ancient_aliens", "Debugging", [
        "THE BUG ONLY APPEARS ON TUESDAYS BETWEEN 2-3PM",
        "TIMEZONE ISSUES",
    ]),
    ("mocking_spongebob", "Debugging", [
        "JUST REBOOT THE SERVER AND IT'LL FIX THE ROOT CAUSE",
        "JuSt ReBoOt ThE sErVeR aNd iT'll FiX tHe RoOt CaUsE",
    ]),
    ("y_u_no", "Debugging", [
        "BUG REPORT",
        "INCLUDE STEPS TO REPRODUCE??",
    ]),
    ("first_world", "Debugging", [
        "MY CODE WORKS PERFECTLY ON MY MACHINE",
        "BUT NOWHERE ELSE IN THE KNOWN UNIVERSE",
    ]),

    # ══════════════════════════════════════════════════════════════════════════
    # GIT
    # ══════════════════════════════════════════════════════════════════════════
    ("drake", "Git", [
        "MEANINGFUL COMMIT MESSAGES DESCRIBING THE CHANGE AND WHY",
        "git commit -m 'fix'",
    ]),
    ("drake", "Git", [
        "CREATING A FEATURE BRANCH WITH A DESCRIPTIVE NAME",
        "PUSHING DIRECTLY TO MAIN BECAUSE 'IT'S JUST A SMALL CHANGE'",
    ]),
    ("drake", "Git", [
        "GIT PULL BEFORE STARTING WORK",
        "GIT PUSH --FORCE AFTER 3 DAYS OF LOCAL COMMITS",
    ]),
    ("expanding_brain", "Git", [
        "git commit -m 'fix bug'",
        "git commit -m 'fix fix'",
        "git commit -m 'FINAL FIX PLEASE WORK'",
        "git push --force --no-verify",
    ]),
    ("expanding_brain", "Git", [
        "WRITE DESCRIPTIVE COMMIT MESSAGES",
        "WRITE 'fix'",
        "WRITE 'asdf'",
        "WRITE '.' AND NEVER SPEAK OF IT AGAIN",
    ]),
    ("two_buttons", "Git", [
        "SQUASH ALL COMMITS INTO ONE CLEAN MERGE",
        "PRESERVE EVERY 'WIP WIP WIP' COMMIT FOR HISTORICAL ACCURACY",
    ]),
    ("one_does_not", "Git", [
        "ONE DOES NOT SIMPLY",
        "RESOLVE A MERGE CONFLICT WITHOUT ACCIDENTALLY DELETING SOMEONE'S WEEK OF WORK",
    ]),
    ("surprised_pikachu", "Git", [
        "FORCE PUSHES TO MAIN WITHOUT WARNING",
        "WHEN THREE TEAMMATES LOSE ALL THEIR LOCAL CHANGES",
    ]),
    ("waiting_skeleton", "Git", [
        "WAITING FOR THE CODE REVIEW ON THE PR I OPENED 8 DAYS AGO",
        "IT HAS 2 LINES CHANGED",
    ]),
    ("this_is_fine", "Git", [
        "THE ENTIRE TEAM PUSHES DIRECTLY TO MAIN AND NOBODY USES BRANCHES",
    ]),
    ("success_kid", "Git", [
        "FINALLY RESOLVED THE MERGE CONFLICT",
        "INTRODUCED 3 NEW BUGS IN THE PROCESS",
    ]),
    ("mocking_spongebob", "Git", [
        "IT'S JUST A TINY CHANGE, I'LL DO IT DIRECTLY IN MAIN",
        "iT's JuSt A tInY cHaNgE, I'll Do It DiReCtLy In MaIn",
    ]),
    ("disaster_girl", "Git", [
        "ME",
        "THE PRODUCTION DATABASE AFTER GIT PUSH --FORCE TO MAIN",
    ]),

    # ══════════════════════════════════════════════════════════════════════════
    # MEETINGS
    # ══════════════════════════════════════════════════════════════════════════
    ("drake", "Meetings", [
        "RESOLVING IT IN A 2-SENTENCE SLACK MESSAGE",
        "SCHEDULING A 1-HOUR MEETING TO 'ALIGN ON THE SYNERGY'",
    ]),
    ("drake", "Meetings", [
        "A 15-MINUTE STANDUP THAT TAKES 15 MINUTES",
        "A 15-MINUTE STANDUP THAT ACCIDENTALLY BECOMES SPRINT PLANNING",
    ]),
    ("drake", "Meetings", [
        "SENDING THE DESIGN FEEDBACK VIA EMAIL",
        "BOOKING A 2-HOUR CALL TO DISCUSS THE BUTTON COLOR",
    ]),
    ("one_does_not", "Meetings", [
        "ONE DOES NOT SIMPLY",
        "LEAVE A SPRINT PLANNING MEETING KNOWING EXACTLY WHAT NEEDS TO BE BUILT",
    ]),
    ("one_does_not", "Meetings", [
        "ONE DOES NOT SIMPLY",
        "SIT THROUGH A 3-HOUR ROADMAP REVIEW WITHOUT QUESTIONING ALL LIFE CHOICES",
    ]),
    ("two_buttons", "Meetings", [
        "THIS MEETING COULD HAVE BEEN AN EMAIL",
        "THIS EMAIL THREAD COULD HAVE BEEN A 5-MINUTE CALL",
    ]),
    ("change_my_mind", "Meetings", [
        "DAILY STANDUPS ARE JUST STATUS REPORTS DELIVERED WHILE STANDING. CHANGE MY MIND.",
    ]),
    ("change_my_mind", "Meetings", [
        "MOST SPRINT RETROSPECTIVES IDENTIFY THE SAME PROBLEMS EVERY SINGLE SPRINT. CHANGE MY MIND.",
    ]),
    ("waiting_skeleton", "Meetings", [
        "WAITING FOR STAKEHOLDERS TO APPROVE THE MOCKUPS SUBMITTED 3 WEEKS AGO",
        "DESIGN TRENDS HAVE EVOLVED TWICE SINCE THE SUBMISSION DATE",
    ]),
    ("surprised_pikachu", "Meetings", [
        "BOOKS 7 HOURS OF BACK-TO-BACK MEETINGS ON EVERY DEVELOPER'S CALENDAR",
        "WHEN SPRINT VELOCITY HITS AN ALL-TIME LOW",
    ]),
    ("this_is_fine", "Meetings", [
        "SPRINT REVIEW, RETRO, PLANNING, AND 2 SYNCS ALL SCHEDULED FOR THE SAME FRIDAY",
    ]),
    ("epic_handshake", "Meetings", [
        "PRODUCT MANAGERS",
        "ENGINEERING LEADS",
        "CALLING EVERY FEATURE A 'QUICK WIN'",
    ]),
    ("first_world", "Meetings", [
        "I HAVE 6 HOURS OF MEETINGS TODAY",
        "AND A 4-HOUR FEATURE ESTIMATE DUE BY EOD",
    ]),
    ("mocking_spongebob", "Meetings", [
        "WE NEED TO SCHEDULE A MEETING TO PLAN THE ROADMAP",
        "We NeEd To ScHeDuLe A mEeTiNg To PlAn ThE rOaDmAp",
    ]),

    # ══════════════════════════════════════════════════════════════════════════
    # STARTUP LIFE
    # ══════════════════════════════════════════════════════════════════════════
    ("drake", "Startup Life", [
        "UNLIMITED PTO",
        "NOBODY TAKES PTO BECAUSE THE TEAM IS TOO UNDERSTAFFED TO COVER ABSENCES",
    ]),
    ("drake", "Startup Life", [
        "COMPETITIVE MARKET-RATE SALARY",
        "BELOW-MARKET SALARY + EQUITY IN A COMPANY VALUED AT 'FUTURE POTENTIAL'",
    ]),
    ("drake", "Startup Life", [
        "A CLEARLY DEFINED JOB DESCRIPTION",
        "FULL-STACK + DEVOPS + DESIGNER + PM + CUSTOMER SUPPORT + ON-CALL 24/7",
    ]),
    ("drake", "Startup Life", [
        "WE'RE A PROFESSIONAL COMPANY WITH HEALTHY WORK-LIFE BALANCE",
        "WE'RE LIKE A FAMILY HERE",
    ]),
    ("this_is_fine", "Startup Life", [
        "RUNWAY IS 6 WEEKS, THE PRODUCT DOESN'T WORK, AND WE JUST PIVOTED AGAIN",
    ]),
    ("this_is_fine", "Startup Life", [
        "WE ARE PRE-REVENUE, PRE-PRODUCT, AND PRE-IDEA BUT THE VIBES ARE IMMACULATE",
    ]),
    ("this_is_fine", "Startup Life", [
        "LEAD DEVELOPER JUST GAVE 2 WEEKS NOTICE AND THEY WERE THE ONLY ONE WHO UNDERSTOOD THE CODEBASE",
    ]),
    ("one_does_not", "Startup Life", [
        "ONE DOES NOT SIMPLY",
        "JOIN A STARTUP AND NOT END UP DOING THE JOB OF 4 PEOPLE FOR THE SALARY OF 0.5",
    ]),
    ("one_does_not", "Startup Life", [
        "ONE DOES NOT SIMPLY",
        "SAY YES TO EVERY FEATURE REQUEST AND STILL SHIP ON TIME",
    ]),
    ("expanding_brain", "Startup Life", [
        "SOFTWARE ENGINEER",
        "FULL-STACK ENGINEER",
        "FULL-STACK + DEVOPS ENGINEER",
        "FULL-STACK + DEVOPS + DESIGN + PM + SALES + SUPPORT + JANITORIAL SERVICES",
    ]),
    ("expanding_brain", "Startup Life", [
        "IT'S A MOBILE APP",
        "IT'S AN AI-POWERED MOBILE APP",
        "IT'S A BLOCKCHAIN AI-POWERED MOBILE APP",
        "IT'S A BLOCKCHAIN AI SAAS B2B2C MOBILE PLATFORM IN THE METAVERSE",
    ]),
    ("change_my_mind", "Startup Life", [
        "EVERY STARTUP MVP IS JUST A TODO APP WITH A $20/MONTH SUBSCRIPTION. CHANGE MY MIND.",
    ]),
    ("change_my_mind", "Startup Life", [
        "ADDING 'AI-POWERED' TO YOUR PITCH DECK WHEN IT'S JUST AN IF STATEMENT. CHANGE MY MIND.",
    ]),
    ("surprised_pikachu", "Startup Life", [
        "CEO PROMISES A FEATURE TO THE CLIENT THAT HASN'T BEEN STARTED OR DESIGNED",
        "WHEN THE ENGINEERING TEAM MISSES THE DEADLINE",
    ]),
    ("disaster_girl", "Startup Life", [
        "ME",
        "BURNING THROUGH 18 MONTHS OF SEED FUNDING WITH NO PRODUCT-MARKET FIT",
    ]),
    ("epic_handshake", "Startup Life", [
        "FOUNDER WHO CAN'T CODE",
        "VC FUND WITH NO TECHNICAL DUE DILIGENCE",
        "CALLING EVERYTHING 'AI-POWERED'",
    ]),
    ("y_u_no", "Startup Life", [
        "STARTUP FOUNDER",
        "JUST DEFINE WHAT THE MVP ACTUALLY IS??",
    ]),
    ("ancient_aliens", "Startup Life", [
        "HOW IS THIS STARTUP VALUED AT $50M",
        "NO REVENUE. NO USERS. VIBES.",
    ]),

    # ══════════════════════════════════════════════════════════════════════════
    # STACK OVERFLOW
    # ══════════════════════════════════════════════════════════════════════════
    ("drake", "Stack Overflow", [
        "READING THE FULL ANSWER AND UNDERSTANDING WHAT IT DOES",
        "COPY-PASTING THE ACCEPTED ANSWER WITHOUT READING A SINGLE LINE",
    ]),
    ("drake", "Stack Overflow", [
        "ASKING A WELL-FORMATTED QUESTION WITH A MINIMAL REPRODUCIBLE EXAMPLE",
        "PASTING YOUR ENTIRE 800-LINE FILE AS THE QUESTION",
    ]),
    ("drake", "Stack Overflow", [
        "UNDERSTANDING WHY THE SOLUTION WORKS",
        "CHANGING VARIABLE NAMES UNTIL IT COMPILES AND SHIPPING IT",
    ]),
    ("one_does_not", "Stack Overflow", [
        "ONE DOES NOT SIMPLY",
        "ASK A QUESTION ON STACK OVERFLOW WITHOUT BEING TOLD TO SEARCH FIRST",
    ]),
    ("one_does_not", "Stack Overflow", [
        "ONE DOES NOT SIMPLY",
        "FIND A STACK OVERFLOW ANSWER THAT WORKS WITHOUT THREE DEPRECATED DEPENDENCIES",
    ]),
    ("waiting_skeleton", "Stack Overflow", [
        "WAITING FOR MY STACK OVERFLOW QUESTION TO GET AN ANSWER",
        "IT WAS CLOSED AS 'DUPLICATE' AND THE DUPLICATE HAS NO ANSWER EITHER",
    ]),
    ("surprised_pikachu", "Stack Overflow", [
        "COPY-PASTES A 2012 STACK OVERFLOW ANSWER INTO A 2024 PRODUCTION CODEBASE",
        "WHEN IT BREAKS IN THE LATEST NODE.JS VERSION",
    ]),
    ("change_my_mind", "Stack Overflow", [
        "SENIOR DEVELOPER = A DEVELOPER WHO KNOWS WHICH STACK OVERFLOW ANSWERS ARE WRONG. CHANGE MY MIND.",
    ]),
    ("this_is_fine", "Stack Overflow", [
        "THE ONLY RELEVANT ANSWER WAS POSTED IN 2011 AND SAYS 'DO NOT DO THIS IN PRODUCTION'",
    ]),
    ("mocking_spongebob", "Stack Overflow", [
        "JUST READ THE DOCUMENTATION",
        "JuSt ReAd ThE dOcUmEnTaTiOn",
    ]),
    ("ancient_aliens", "Stack Overflow", [
        "HOW IS A 2009 STACK OVERFLOW ANSWER STILL THE BEST SOLUTION?",
        "LEGACY CODE NEVER DIES",
    ]),
    ("success_kid", "Stack Overflow", [
        "FOUND THE EXACT SAME BUG ON STACK OVERFLOW",
        "THE ANSWER HAS 847 UPVOTES AND WAS POSTED YESTERDAY",
    ]),
    ("first_world", "Stack Overflow", [
        "I COPY-PASTED THE STACK OVERFLOW ANSWER",
        "NOW I HAVE TWO PROBLEMS",
    ]),

    # ══════════════════════════════════════════════════════════════════════════
    # DEPLOYMENT
    # ══════════════════════════════════════════════════════════════════════════
    ("drake", "Deployment", [
        "DEPLOYING ON MONDAY MORNING AFTER THOROUGH STAGING VALIDATION",
        "DEPLOYING FRIDAY AT 4:45PM BEFORE A 3-DAY WEEKEND",
    ]),
    ("drake", "Deployment", [
        "A PROPER ROLLBACK PLAN WITH TESTED PROCEDURES",
        "'WE'LL FIX IT FORWARD' — CEO, EVERY TIME",
    ]),
    ("drake", "Deployment", [
        "INCREMENTAL FEATURE FLAGS FOR SAFE ROLLOUT",
        "YOLO DEPLOY TO 100% OF USERS AND SEE WHAT HAPPENS",
    ]),
    ("this_is_fine", "Deployment", [
        "PROD IS DOWN. PAGERDUTY IS GOING OFF. CEO IS ON THE CALL. THIS IS FINE.",
    ]),
    ("this_is_fine", "Deployment", [
        "JUST A QUICK CONFIG CHANGE IN PRODUCTION. NO NEED TO TEST IT.",
    ]),
    ("one_does_not", "Deployment", [
        "ONE DOES NOT SIMPLY",
        "DEPLOY ON A FRIDAY AFTERNOON AND ENJOY A PEACEFUL WEEKEND",
    ]),
    ("one_does_not", "Deployment", [
        "ONE DOES NOT SIMPLY",
        "MAKE A 'QUICK DATABASE MIGRATION' WITHOUT LOCKING THE TABLE FOR 20 MINUTES",
    ]),
    ("surprised_pikachu", "Deployment", [
        "SKIPS STAGING AND DEPLOYS UNTESTED CODE DIRECTLY TO PRODUCTION",
        "WHEN THE SITE GOES DOWN IMMEDIATELY",
    ]),
    ("success_kid", "Deployment", [
        "DEPLOYED TO PRODUCTION ON FRIDAY",
        "NOTHING BROKE. NOT TOUCHING ANYTHING ELSE EVER.",
    ]),
    ("expanding_brain", "Deployment", [
        "UNIT TESTS",
        "INTEGRATION TESTS",
        "MANUAL TESTING IN STAGING",
        "LET USERS FIND THE BUGS IN PRODUCTION — IT'S CALLED BETA TESTING",
    ]),
    ("two_buttons", "Deployment", [
        "SKIP THE DEPLOY AND MISS THE SPRINT GOAL",
        "DEPLOY ON FRIDAY AND RUIN YOUR WEEKEND",
    ]),
    ("disaster_girl", "Deployment", [
        "ME",
        "THE PROD DATABASE WITH NO BACKUPS AFTER RUNNING DROP TABLE",
    ]),
    ("ancient_aliens", "Deployment", [
        "WORKS PERFECTLY ON LOCALHOST",
        "INSTANTLY CATCHES FIRE IN PRODUCTION",
    ]),
    ("waiting_skeleton", "Deployment", [
        "WAITING FOR THE CI/CD PIPELINE",
        "22 MINUTES AND COUNTING",
    ]),
    ("y_u_no", "Deployment", [
        "FRIDAY DEPLOY",
        "JUST NOT HAPPEN??",
    ]),
    ("change_my_mind", "Deployment", [
        "IF IT WORKS IN STAGING, IT'LL DEFINITELY WORK IN PRODUCTION. CHANGE MY MIND.",
    ]),
    ("epic_handshake", "Deployment", [
        "DEVS WHO SKIPPED TESTING",
        "OPS WHO SKIPPED MONITORING",
        "BLAMING EACH OTHER WHEN PROD GOES DOWN",
    ]),
]
