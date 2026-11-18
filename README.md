# Job Hunter (Claude Code toolkit)

A Claude Code setup that searches job boards, scores matches against your CV, tailors a CV and cover letter per job, has a critic and a "recruiter" agent review them, and tracks every application and email reply in one CSV.

## What's inside
- `CLAUDE.md`: the job-lead workflow (search → tailor → critique → recruiter check → shortlist → apply only with your approval).
- `.claude/agents/`: job-scout, cv-optimizer, cv-critic, recruiter, hiring-manager, email-tracker.
- `reports/build_success_matrix.py`: turns `applications.csv` into a success matrix (reply/interview rate by role family, match score and source).
- Templates: `cv-master.txt`, `answers.md`, `applications.csv` (header only).

## Setup
1. Install [Claude Code](https://claude.com/claude-code) and open this folder.
2. Fill in `cv-master.txt` with your real CV and `answers.md` with your standard answers.
3. Edit the target roles, city and experience rules at the top of `CLAUDE.md`.
4. Ask Claude: "run the search".

Safety rules built in: it never invents experience, never logs in or enters passwords, and only applies to jobs you name.

Your filled-in CV, answers and `applications/` folders stay local; keep personal data out of any fork you publish.
