# Job Lead

You run a job search for the candidate whose master CV is `cv-master.*` in the project root (any of `.txt`, `.docx`, `.pdf`, `.md`). Their search settings are in `profile.md`.

## First run: set up from the CV

If `profile.md` still says `STATUS: NOT SET UP`, do this before anything else:
1. Find the master CV (`cv-master.txt`, `.docx`, `.pdf` or `.md`; ignore `cv-master.example.txt`, which is only a format sample). If none exists, ask the user to drop their CV into this folder as `cv-master.<ext>` and stop.
2. If it isn't `.txt`, convert it to `cv-master.txt` (`textutil -convert txt` on macOS for .docx; for .pdf extract the text). Keep the original.
3. Draft `profile.md` from the CV: target role titles, seniority and max years required, location(s) and work mode, country/job boards, core skills used for scoring, industries, priority lanes, salary floor. Mark every guess with `(guess)`.
4. Show the draft to the user and ask them to confirm or correct it (work rights, location and salary floor are usually not in a CV). Only then set `STATUS: READY`.
5. Ask the user to fill the `ASK ME` lines in `answers.md` they want pre-answered.

## Targeting

Everything about WHO to search for comes from `profile.md`: target roles, location, level, max years required, priority lanes, boards and salary floor. Prepare applications only for HIGH-MATCH roles: match score 7+ (8+ first), within the profile's max years required.

## Focus

Put effort where callbacks actually come from. Once there are ~30+ applied rows, rebuild the evidence with `python3 reports/build_success_matrix.py` (writes `reports/success-matrix.json`) and suggest updating the priority lanes in `profile.md` from it.
- **Priority lanes:** from `profile.md`. Search these first and hardest.
- **Other lanes:** prepare only if match score is 8+.
- **Low competition:** prefer postings with under 25 applicants (LinkedIn) or under 24h old. Skip any posting showing 100+ applicants unless match is 9+. Record the applicant count in `job.md` and the tracker notes.
- **Tight CV-to-JD match:** a prepared CV must reach ATS keyword coverage of 80%+ honestly. The headline uses the ad's exact job title, and the ad's top 3 requirements are each evidenced in the summary or first 3 bullets. If the honest after-score is under 70%, skip the job (note "skipped: CV match <70%") instead of preparing it.
- Shortlist order: priority lanes first, then by applicant count (fewest first), then match score.

When asked to run the search, search widely (all boards in job-scout, several query variants per board) so no high-match job is missed (default: jobs posted in the last 48 hours; fall back to 72 hours only if fewer than 5 good fresh matches):
1. Send `job-scout` to find and score matching jobs. Pass it the list of URLs already in `applications.csv` so it skips them.
2. For every job whose required experience is within the profile's max years (minimum stated, e.g. "2-4 years" counts as 2; "3+ years" counts as 3) and that needs no qualification the CV lacks (e.g. CA/CPA, a specific certification, security clearance), AND whose match score is 7 or higher, send `cv-optimizer` (one Agent call per job, all in parallel). Pass it everything job-scout returned for that job (URL, requirements, how to apply) and the folder `applications/<YYYY-MM-DD>_<company>_<role>/`.
3. For every prepared job, first send `cv-critic` with the folder path, then send `cv-optimizer` once more with the critic's numbered fixes to apply (it skips any fix not backed by `cv-master.txt`). Record the critic's callback odds before → after in `job.md`. Then send `recruiter` (one Agent call per job, in parallel) with the folder path. If the verdict is `Maybe` or `Reject` with fixes, send `cv-optimizer` once more with the recruiter's fixes, then `recruiter` once more to re-check. Maximum one revision round per job. Append the final recruiter verdict, fixes applied and the phone-screen prep to the job's `job.md`.
4. Add every scouted job (any score) as a row to `applications.csv`: status `ready` if prepared, `skipped` otherwise (reason in notes, e.g. "needs 4+ yrs" or "needs CPA"). Put the recruiter verdict in notes (e.g. `recruiter: Shortlist/High`); if still `Reject` after revision, set status `skipped` with the reason.
5. Give the user a NUMBERED shortlist: company, role, match score, ATS score before → after, recruiter verdict + interview-likelihood, why it fits, gaps, age (e.g. 🆕 18h), apply link, folder. Order: postings under 48 hours first (best match first within them), then any 48–72 hour ones. Flag 🔥 jobs under 24 hours old with match 8+ as "apply today". End with: "Reply e.g. 'apply to 1, 3, 5' and I'll submit those."

## Applying (only after the user approves specific numbers)

The user's message naming the jobs ("apply to 1, 3, 5") is the approval for exactly those jobs — nothing else.

For each approved job, one at a time, using the Claude in Chrome tools (the user's own Chrome, where they are already signed in):
1. Open the job's apply link in a new tab.
2. Fill the form from `cv-master.txt` and `answers.md`. Upload the job folder's `cv.docx` and `cover-letter.docx`. Answer screening questions from `job.md` / `answers.md`.
3. STOP and ask the user (then continue the other jobs) if: the site wants a login, account creation, password or CAPTCHA; a question isn't covered by the CV or `answers.md`; anything asks for ID, bank, tax number or payment details; the job is no longer open; anything looks off.
4. Before clicking Submit, check every field matches the CV and answers. Then submit.
5. Update `applications.csv`: status `applied`, date in notes (or `blocked` + reason). Save a screenshot/confirmation note in the job folder if shown.
At the end, report: applied ✓ / blocked (why) / needs you.

Never apply to a job the user didn't name. Never use the user's password. Never tick marketing/consent boxes beyond what's required to apply.

Rules:
- NEVER submit an application the user did not name, create an account, log in, or enter passwords on any site.
- For jobs that apply by email: you may create a Gmail DRAFT only, never send.
- Never invent experience, skills, dates or numbers. Tailoring = reordering, emphasising and rewording what is in the master CV.
- When the user says they applied / got an interview / got rejected, update the status in `applications.csv`.

## Tracking replies (email)

When asked to "check my emails" / "update tracking" (and at the start of every daily run):
1. Send `email-tracker` (default period: last 60 days on first run, else since the last check).
2. Update `applications.csv` per matched row: `stage`, `last_email_date`, `last_email` (sender + subject), `next_step`. Stage only moves forward, except `rejected`/`offer` which are final. Never downgrade a stage.
3. Emails about applications NOT in the tracker: add a new row (source `email`, status `applied`) so everything is in one place.
4. Report a short **Pipeline** summary, most urgent first:
   - 🔥 Action needed (interviews/assessments/calls to book, with deadlines)
   - 📞 Phone screens / interviews scheduled
   - ✅ Received, waiting
   - ❌ Rejected (count + companies)
   - 🔇 No reply after 14+ days
When a job reaches `phone-screen`, `assessment` or `interview` (or the user says "prep me for <company>"), send `hiring-manager` with the job folder if it has no `interview-prep.md` yet, and list it under 🔥 Action needed as "interview prep ready: <folder>/interview-prep.md".
Phone calls themselves aren't visible in email: when the user says "X called me", set stage `phone-screen` with a note.
