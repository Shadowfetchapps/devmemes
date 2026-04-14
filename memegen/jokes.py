"""
Meme template definitions and dev/startup joke bank for DevMemes.

Each MEME entry: (template_key, category, [text_field_1, text_field_2, ...])
"""

# ── Template definitions ──────────────────────────────────────────────────────
# render types:
#   top_bottom | drake | two_button | four_panel | bottom_only
#   side_by_side | three_vertical | distracted_bf | three_labels | sign | handshake

TEMPLATES = {
    # ── Classic two-zone ──────────────────────────────────────────────────────
    "drake": {
        "name": "Drake Hotline Bling",
        "url": "https://i.imgflip.com/30b1gx.jpg",
        "render": "drake",
        "labels": ["Drake Rejects:", "Drake Approves:"],
    },
    "one_does_not": {
        "name": "One Does Not Simply",
        "url": "https://i.imgflip.com/1bij.jpg",
        "render": "top_bottom",
        "labels": ["Top text:", "Bottom text:"],
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
    "batman_slap": {
        "name": "Batman Slapping Robin",
        "url": "https://i.imgflip.com/9ehk.jpg",
        "render": "top_bottom",
        "labels": ["Robin says:", "Batman's reply:"],
    },
    "most_interesting": {
        "name": "Most Interesting Man",
        "url": "https://i.imgflip.com/1bh8.jpg",
        "render": "top_bottom",
        "labels": ["I don't always...:", "But when I do...:"],
    },
    "hide_harold": {
        "name": "Hide The Pain Harold",
        "url": "https://i.imgflip.com/gk5el.jpg",
        "render": "top_bottom",
        "labels": ["Top text:", "Bottom text:"],
    },
    "is_this_pigeon": {
        "name": "Is This A Pigeon",
        "url": "https://i.imgflip.com/1o00in.jpg",
        "render": "top_bottom",
        "labels": ["Person label:", "\"Is this a [x]?\":"],
    },
    "always_has_been": {
        "name": "Always Has Been",
        "url": "https://i.imgflip.com/46e43q.png",
        "render": "top_bottom",
        "labels": ["Discovery:", "Response:"],
    },
    "philosoraptor": {
        "name": "Philosoraptor",
        "url": "https://i.imgflip.com/h7.jpg",
        "render": "top_bottom",
        "labels": ["If...:", "...then?:"],
    },
    "they_same": {
        "name": "They're The Same Picture",
        "url": "https://i.imgflip.com/2za3u1.jpg",
        "render": "top_bottom",
        "labels": ["Top text:", "Bottom:"],
    },
    # ── Special multi-zone ────────────────────────────────────────────────────
    "this_is_fine": {
        "name": "This Is Fine",
        "url": "https://i.imgflip.com/wxica.jpg",
        "render": "bottom_only",
        "labels": ["Caption:"],
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
    "gru_plan": {
        "name": "Gru's Plan",
        "url": "https://i.imgflip.com/26jxvz.jpg",
        "render": "four_panel",
        "labels": ["Step 1:", "Step 2:", "Step 2 (realisation):", "Step 3 (uh oh):"],
    },
    "epic_handshake": {
        "name": "Epic Handshake",
        "url": "https://i.imgflip.com/28j0te.jpg",
        "render": "handshake",
        "labels": ["Left arm:", "Right arm:", "Handshake (result):"],
    },
    "woman_yelling_cat": {
        "name": "Woman Yelling At Cat",
        "url": "https://i.imgflip.com/345v97.jpg",
        "render": "side_by_side",
        "labels": ["Woman (left panel):", "Cat (right panel):"],
    },
    "tuxedo_pooh": {
        "name": "Tuxedo Winnie Pooh",
        "url": "https://i.imgflip.com/1c1uej.jpg",
        "render": "side_by_side",
        "labels": ["Casual version (left):", "Fancy version (right):"],
    },
    "distracted_bf": {
        "name": "Distracted Boyfriend",
        "url": "https://i.imgflip.com/1ur9b0.jpg",
        "render": "distracted_bf",
        "labels": ["New shiny thing:", "Developer (boyfriend):", "Current project (girlfriend):"],
    },
    "panik_kalm": {
        "name": "Panik Kalm Panik",
        "url": "https://i.imgflip.com/3qqcim.png",
        "render": "three_vertical",
        "labels": ["PANIK:", "KALM:", "PANIK AGAIN:"],
    },
    "left_exit": {
        "name": "Left Exit 12 Off Ramp",
        "url": "https://i.imgflip.com/22bdq6.jpg",
        "render": "three_labels",
        "labels": ["Car (you/team):", "Straight road (sensible choice):", "Exit (what you do instead):"],
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
        "JuSt ReBoOt ThE sErVeR aNd It'lL fIx ThE rOoT cAuSe",
    ]),
    ("y_u_no", "Debugging", [
        "BUG REPORT",
        "INCLUDE STEPS TO REPRODUCE??",
    ]),
    ("first_world", "Debugging", [
        "MY CODE WORKS PERFECTLY ON MY MACHINE",
        "BUT NOWHERE ELSE IN THE KNOWN UNIVERSE",
    ]),
    ("batman_slap", "Debugging", [
        "WE SHOULD JUST DELETE THE FAILING TESTS",
        "NO.",
    ]),
    ("batman_slap", "Debugging", [
        "THE BUG IS PROBABLY IN THEIR CODE, NOT OURS",
        "WRONG.",
    ]),
    ("hide_harold", "Debugging", [
        "ACHIEVED 100% CODE COVERAGE",
        "BY WRITING TESTS THAT DON'T ASSERT ANYTHING",
    ]),
    ("hide_harold", "Debugging", [
        "FIXED THE PRODUCTION BUG",
        "BY REVERTING TO A COMMIT FROM 3 MONTHS AGO",
    ]),
    ("philosoraptor", "Debugging", [
        "IF ALL YOUR TESTS PASS",
        "BUT NONE TEST THE RIGHT THING, ARE THEY PASSING?",
    ]),
    ("philosoraptor", "Debugging", [
        "IF A BUG HAPPENS IN PROD",
        "AND NOBODY'S ON CALL, IS IT REALLY A BUG?",
    ]),
    ("woman_yelling_cat", "Debugging", [
        "YOUR LAST COMMIT BROKE THE ENTIRE BUILD",
        "my tests pass locally",
    ]),
    ("woman_yelling_cat", "Debugging", [
        "WHY IS THERE NO ERROR HANDLING??",
        "that's what the logs are for",
    ]),
    ("panik_kalm", "Debugging", [
        "PROD IS DOWN",
        "IT WAS JUST A BAD DEPLOY — ROLLING BACK NOW",
        "WE DON'T HAVE A ROLLBACK PLAN",
    ]),
    ("panik_kalm", "Debugging", [
        "THE TEST SUITE IS FAILING",
        "IT'S JUST A FLAKY TEST — I'LL RERUN IT",
        "ALL 847 TESTS ARE NOW FAILING",
    ]),
    ("is_this_pigeon", "Debugging", [
        "DEVELOPER WHO HASN'T SLEPT IN 3 DAYS",
        "IS THIS A BUG OR A FEATURE?",
    ]),
    ("is_this_pigeon", "Debugging", [
        "ME, AFTER COPY-PASTING FROM STACK OVERFLOW",
        "IS THIS UNDERSTANDING?",
    ]),
    ("always_has_been", "Debugging", [
        "WAIT, EVERY CODEBASE IS HELD TOGETHER WITH DUCT TAPE AND PRAYERS?",
        "ALWAYS HAS BEEN",
    ]),
    ("tuxedo_pooh", "Debugging", [
        "print('debug')",
        "Implementing a structured logging framework with distributed tracing",
    ]),
    ("tuxedo_pooh", "Debugging", [
        "it works on my machine",
        "the application exhibits environment-specific behavioural inconsistencies",
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
        "iT's JuSt A tInY cHaNgE, I'lL dO iT dIrEcTlY iN mAiN",
    ]),
    ("disaster_girl", "Git", [
        "ME",
        "THE PRODUCTION DATABASE AFTER GIT PUSH --FORCE TO MAIN",
    ]),
    ("batman_slap", "Git", [
        "I'LL JUST QUICKLY PUSH THIS TO MAIN, IT'S ONLY ONE LINE",
        "NO YOU WON'T.",
    ]),
    ("batman_slap", "Git", [
        "LET'S JUST SKIP CODE REVIEW FOR THIS ONE",
        "ABSOLUTELY NOT.",
    ]),
    ("gru_plan", "Git", [
        "REBASE ONTO MAIN SO MY BRANCH IS UP TO DATE",
        "RESOLVE THE 12 MERGE CONFLICTS",
        "RESOLVE THE 12 MERGE CONFLICTS",
        "ACCIDENTALLY DELETE SOMEONE ELSE'S FEATURE",
    ]),
    ("woman_yelling_cat", "Git", [
        "YOUR BRANCH IS 47 COMMITS BEHIND MAIN",
        "i'll just rebase real quick",
    ]),
    ("tuxedo_pooh", "Git", [
        "git push --force",
        "git push --force-with-lease --verify",
    ]),
    ("tuxedo_pooh", "Git", [
        "git commit -m 'stuff'",
        "git commit -m 'refactor(auth): extract token validation to reduce coupling'",
    ]),
    ("always_has_been", "Git", [
        "WAIT, NOBODY ON THE TEAM ACTUALLY READS GIT HISTORY?",
        "ALWAYS HAS BEEN",
    ]),
    ("panik_kalm", "Git", [
        "ACCIDENTALLY COMMITTED .env TO PUBLIC REPO",
        "DELETED IT IN THE NEXT COMMIT — NOBODY WILL NOTICE",
        "GIT HISTORY IS PERMANENT AND FOREVER",
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
        "A 15-MINUTE STANDUP THAT ACCIDENTALLY BECOMES SPRINT PLANNING FOR 90 MINUTES",
    ]),
    ("one_does_not", "Meetings", [
        "ONE DOES NOT SIMPLY",
        "LEAVE A SPRINT PLANNING MEETING KNOWING EXACTLY WHAT NEEDS TO BE BUILT",
    ]),
    ("two_buttons", "Meetings", [
        "THIS MEETING COULD HAVE BEEN AN EMAIL",
        "THIS EMAIL THREAD COULD HAVE BEEN A 5-MINUTE CALL",
    ]),
    ("change_my_mind", "Meetings", [
        "DAILY STANDUPS ARE JUST STATUS REPORTS DELIVERED WHILE STANDING. CHANGE MY MIND.",
    ]),
    ("change_my_mind", "Meetings", [
        "SPRINT RETROSPECTIVES IDENTIFY THE SAME PROBLEMS EVERY SINGLE SPRINT. CHANGE MY MIND.",
    ]),
    ("waiting_skeleton", "Meetings", [
        "WAITING FOR STAKEHOLDERS TO APPROVE MOCKUPS SUBMITTED 3 WEEKS AGO",
        "DESIGN TRENDS HAVE EVOLVED TWICE SINCE THE SUBMISSION",
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
        "I HAVE 7 HOURS OF MEETINGS TODAY",
        "AND A 4-HOUR FEATURE ESTIMATE DUE BY EOD",
    ]),
    ("mocking_spongebob", "Meetings", [
        "WE NEED TO SCHEDULE A MEETING TO PLAN THE ROADMAP",
        "We NeEd To ScHeDuLe A mEeTiNg To PlAn ThE rOaDmAp",
    ]),
    ("woman_yelling_cat", "Meetings", [
        "THE STANDUP STARTS IN 5 MINUTES",
        "i'm in flow state and about to solve it",
    ]),
    ("woman_yelling_cat", "Meetings", [
        "YOUR CAMERA MUST BE ON FOR THIS MEETING",
        "i am not dressed like a person",
    ]),
    ("panik_kalm", "Meetings", [
        "THE CEO WANTS A DEMO IN 20 MINUTES",
        "THE DEMO ENVIRONMENT IS SEPARATE FROM PROD — IT'LL BE FINE",
        "NOBODY HAS TOUCHED THE DEMO ENVIRONMENT IN 6 MONTHS",
    ]),
    ("batman_slap", "Meetings", [
        "LET'S SCHEDULE A MEETING TO DISCUSS THE MEETING SCHEDULE",
        "*SLAP*",
    ]),
    ("most_interesting", "Meetings", [
        "I DON'T ALWAYS ATTEND MEETINGS",
        "BUT WHEN I DO, THEY COULD HAVE BEEN AN EMAIL",
    ]),
    ("hide_harold", "Meetings", [
        "ATTENDED A 3-HOUR STRATEGIC ALIGNMENT SESSION",
        "STILL HAVE NO IDEA WHAT WE'RE BUILDING",
    ]),
    ("always_has_been", "Meetings", [
        "WAIT, EVERY 'QUICK SYNC' TAKES AT LEAST 45 MINUTES?",
        "ALWAYS HAS BEEN",
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
        "LEAD DEV JUST GAVE 2 WEEKS NOTICE AND THEY WERE THE ONLY ONE WHO KNEW THE CODEBASE",
    ]),
    ("one_does_not", "Startup Life", [
        "ONE DOES NOT SIMPLY",
        "JOIN A STARTUP AND NOT END UP DOING THE JOB OF 4 PEOPLE FOR THE SALARY OF 0.5",
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
        "CEO PROMISES A FEATURE TO CLIENT THAT HASN'T BEEN STARTED OR DESIGNED YET",
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
    ("gru_plan", "Startup Life", [
        "DISRUPT THE INDUSTRY WITH BOLD NEW TECHNOLOGY",
        "RAISE $10M SERIES A AND HIRE 30 ENGINEERS",
        "RAISE $10M SERIES A AND HIRE 30 ENGINEERS",
        "PIVOT TO SELLING B2B SAAS TO THE SAME INDUSTRY YOU WERE DISRUPTING",
    ]),
    ("distracted_bf", "Startup Life", [
        "AI FEATURES NOBODY ASKED FOR",
        "STARTUP FOUNDERS",
        "SHIPPING THE ACTUAL MVP",
    ]),
    ("distracted_bf", "Startup Life", [
        "NEW JS FRAMEWORK",
        "ME, EVERY 6 MONTHS",
        "THE APP I'M SUPPOSED TO BE BUILDING",
    ]),
    ("woman_yelling_cat", "Startup Life", [
        "THE CLIENT WANTS THIS BY EOD TOMORROW",
        "the ticket says 'S' for small",
    ]),
    ("woman_yelling_cat", "Startup Life", [
        "WE'RE LIKE A FAMILY HERE",
        "why is everyone's PTO request being denied",
    ]),
    ("batman_slap", "Startup Life", [
        "WE SHOULD REWRITE THE WHOLE THING IN A NEW FRAMEWORK",
        "WE HAVE 3 WEEKS OF RUNWAY.",
    ]),
    ("most_interesting", "Startup Life", [
        "I DON'T ALWAYS MISS DEADLINES",
        "BUT WHEN I DO, IT'S BECAUSE THE SCOPE TRIPLED AFTER KICKOFF",
    ]),
    ("always_has_been", "Startup Life", [
        "WAIT, 'UNLIMITED PTO' IS ACTUALLY ZERO PTO WITH EXTRA STEPS?",
        "ALWAYS HAS BEEN",
    ]),
    ("panik_kalm", "Startup Life", [
        "THE CEO PROMISED THE CLIENT A FEATURE WE HAVEN'T STARTED",
        "WE HAVE 2 WEEKS — WE CAN BUILD AN MVP",
        "THE 'SMALL MVP' REQUIRES REBUILDING THE ENTIRE BACKEND",
    ]),
    ("left_exit", "Startup Life", [
        "OUR STARTUP",
        "BUILDING WHAT USERS ACTUALLY ASKED FOR",
        "ADDING AI AND CALLING IT A PIVOT",
    ]),
    ("tuxedo_pooh", "Startup Life", [
        "copy-paste from Stack Overflow",
        "leverage community-sourced solutions from distributed knowledge repositories",
    ]),
    ("they_same", "Startup Life", [
        "MVP / MINIMUM VIABLE PRODUCT",
        "STARTUP FOUNDER'S VISION FOR LAUNCH DAY",
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
    ("one_does_not", "Stack Overflow", [
        "ONE DOES NOT SIMPLY",
        "ASK A QUESTION ON STACK OVERFLOW WITHOUT BEING TOLD TO SEARCH FIRST",
    ]),
    ("waiting_skeleton", "Stack Overflow", [
        "WAITING FOR MY STACK OVERFLOW QUESTION TO GET AN ANSWER",
        "IT WAS CLOSED AS 'DUPLICATE' AND THE DUPLICATE HAS NO ANSWER EITHER",
    ]),
    ("surprised_pikachu", "Stack Overflow", [
        "COPY-PASTES A 2012 STACK OVERFLOW ANSWER INTO A 2024 PRODUCTION CODEBASE",
        "WHEN IT BREAKS IN THE LATEST FRAMEWORK VERSION",
    ]),
    ("change_my_mind", "Stack Overflow", [
        "SENIOR DEVELOPER = A DEVELOPER WHO KNOWS WHICH STACK OVERFLOW ANSWERS ARE WRONG. CHANGE MY MIND.",
    ]),
    ("this_is_fine", "Stack Overflow", [
        "THE ONLY RELEVANT ANSWER WAS POSTED IN 2011 AND IT SAYS 'DO NOT DO THIS IN PRODUCTION'",
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
    ("batman_slap", "Stack Overflow", [
        "I FOUND THE ANSWER ON STACK OVERFLOW AND CLOSED THE BROWSER TAB WITHOUT UPVOTING",
        "SHAME.",
    ]),
    ("woman_yelling_cat", "Stack Overflow", [
        "YOUR QUESTION WAS CLOSED AS A DUPLICATE",
        "the duplicate answer doesn't work either",
    ]),
    ("always_has_been", "Stack Overflow", [
        "WAIT, NOBODY ACTUALLY READS THE DOCUMENTATION?",
        "ALWAYS HAS BEEN",
    ]),
    ("left_exit", "Stack Overflow", [
        "ME",
        "READING THE FULL DOCUMENTATION",
        "GOOGLING THE ERROR AND JUMPING TO STACK OVERFLOW",
    ]),
    ("philosoraptor", "Stack Overflow", [
        "IF NOBODY DOCUMENTS THEIR CODE",
        "IS THE CODE TRULY SELF-DOCUMENTING?",
    ]),
    ("they_same", "Stack Overflow", [
        "COPY-PASTING THE ANSWER / NOT UNDERSTANDING IT",
        "JUST COPY-PASTING THE ANSWER",
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
    ("surprised_pikachu", "Deployment", [
        "SKIPS STAGING AND DEPLOYS UNTESTED CODE DIRECTLY TO PRODUCTION",
        "WHEN THE SITE GOES DOWN IMMEDIATELY",
    ]),
    ("success_kid", "Deployment", [
        "DEPLOYED TO PRODUCTION ON A FRIDAY",
        "NOTHING BROKE. NOT TOUCHING ANYTHING ELSE EVER.",
    ]),
    ("expanding_brain", "Deployment", [
        "UNIT TESTS",
        "INTEGRATION TESTS",
        "MANUAL TESTING IN STAGING",
        "LET USERS FIND THE BUGS IN PROD — IT'S CALLED CROWDSOURCED QA",
    ]),
    ("two_buttons", "Deployment", [
        "SKIP THE DEPLOY AND MISS THE SPRINT GOAL",
        "DEPLOY ON FRIDAY AND RUIN YOUR ENTIRE WEEKEND",
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
    ("change_my_mind", "Deployment", [
        "IF IT WORKS IN STAGING, IT'LL DEFINITELY WORK IN PRODUCTION. CHANGE MY MIND.",
    ]),
    ("epic_handshake", "Deployment", [
        "DEVS WHO SKIPPED TESTING",
        "OPS WHO SKIPPED MONITORING",
        "BLAMING EACH OTHER WHEN PROD GOES DOWN",
    ]),
    ("gru_plan", "Deployment", [
        "ADD FEATURE FLAGS FOR SAFE INCREMENTAL ROLLOUT",
        "CONFIGURE THE FLAGS AND DEPLOY TO 5% OF USERS",
        "CONFIGURE THE FLAGS AND DEPLOY TO 5% OF USERS",
        "THE FLAGS ARE ALL SET TO TRUE IN PROD AND NOBODY KNOWS HOW",
    ]),
    ("woman_yelling_cat", "Deployment", [
        "YOU DEPLOYED ON FRIDAY BEFORE A LONG WEEKEND??",
        "it was just a one-line config change",
    ]),
    ("panik_kalm", "Deployment", [
        "PROD IS DOWN AND THE CEO IS ON THE ALL-HANDS CALL",
        "ROLLING BACK THE LAST DEPLOY — SHOULD BE 5 MINUTES",
        "THE ROLLBACK IS ALSO FAILING",
    ]),
    ("batman_slap", "Deployment", [
        "I'LL JUST DEPLOY THIS QUICK FIX TO PROD ON A FRIDAY",
        "I WILL NOT LET YOU DO THIS.",
    ]),
    ("left_exit", "Deployment", [
        "OUR TEAM",
        "STABLE MONDAY MORNING DEPLOY WITH FULL MONITORING",
        "YOLO FRIDAY AFTERNOON DEPLOY AND LOG OFF",
    ]),
    ("most_interesting", "Deployment", [
        "I DON'T ALWAYS DEPLOY TO PRODUCTION",
        "BUT WHEN I DO, IT'S A FRIDAY AT 4:50PM",
    ]),
    ("always_has_been", "Deployment", [
        "WAIT, EVERY 'QUICK DEPLOY' TAKES DOWN PROD FOR 20 MINUTES?",
        "ALWAYS HAS BEEN",
    ]),
    ("distracted_bf", "Deployment", [
        "DEPLOYING FRIDAY BEFORE A LONG WEEKEND",
        "ME",
        "STABLE DEPLOYMENT PRACTICES",
    ]),
    ("tuxedo_pooh", "Deployment", [
        "deploy and pray",
        "execute a canary release with automated rollback triggers and full observability",
    ]),
    ("they_same", "Deployment", [
        "'JUST A QUICK HOTFIX' / 'SMALL CONFIG CHANGE'",
        "THE THING THAT TOOK PROD DOWN FOR 4 HOURS",
    ]),
]
