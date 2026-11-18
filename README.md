# Job Hunter: a Claude Code job-search toolkit

Drop in your CV and Claude Code becomes your job-search team. It searches job boards for fresh postings that fit you, scores each one against your CV, writes a tailored CV and cover letter per job, has a critic and a recruiter agent tear them apart and fix them, and tracks every application and email reply in one spreadsheet. Works for any role, any city.

## Quick start
1. Install [Claude Code](https://claude.com/claude-code) and download this repo (green **Code** button → **Download ZIP**, or `git clone`).
2. Put your CV in the folder as `cv-master.docx`, `cv-master.pdf` or `cv-master.txt`.
3. Open the folder in Claude Code and say **"set me up"**. Claude reads your CV, drafts `profile.md` (target roles, city, level, skills, salary floor) and asks you to confirm it.
4. Say **"run the search"**. You get a numbered shortlist with a tailored CV and cover letter ready in `applications/` for each job.
5. Apply yourself, or reply "apply to 1, 3" and Claude fills the forms in your browser (it stops for logins, CAPTCHAs and anything it can't answer).

Optional: connect Gmail and say **"check my emails"** to track replies, or "prep me for <company>" for interview questions with model answers.

## What's inside
| File | What it does |
|---|---|
| `CLAUDE.md` | The job-lead playbook: setup, search, tailor, review, shortlist, apply, track |
| `profile.md` | Your search settings (filled in on first run) |
| `answers.md` | Standard answers for application forms (address, notice period, etc.) |
| `applications.csv` | Tracker of every job found, prepared, applied and replied |
| `.claude/agents/` | job-scout, cv-optimizer, cv-critic, recruiter, hiring-manager, email-tracker |
| `reports/build_success_matrix.py` | Reply and interview rates by role family, match score and source, so you can focus where callbacks come from |

## Built-in rules
- Never invents experience, skills, dates or numbers. Tailoring only reorders, emphasises and rewords what is in your CV.
- Never logs in, creates accounts or enters passwords. Only applies to jobs you name.
- Email applications are saved as Gmail drafts, never sent.

## Privacy
Your CV, answers, tracker and `applications/` folder stay on your computer. If you fork this repo, keep them out of it (the `.gitignore` already excludes CV files and the applications folder).
