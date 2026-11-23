# Publish guide

Click-by-click. Written for someone who has never used GitHub or Zenodo. Do not start
until `docs/VERIFY_CHECKLIST.md` is done.

Total time: about 45 minutes for GitHub and Zenodo, plus 20 minutes for the preprint.

---

## Copy-ready text (everything you will be asked to paste)

**Repository name**
```
clinical-lab-aerosol-biorisk-reference
```

**Short description (GitHub "Description" box, Zenodo "Description" summary line)**
```
An open, procedure-level BRACE scoring instrument for aerosol biorisk at the clinical laboratory bench, mapped to ISO 35001:2019, with reference scores, evidence grades and control sets for seven routine bench steps.
```

**Title (Zenodo, preprint)**
```
Clinical Laboratory Aerosol Biorisk Reference: a procedure-level BRACE scoring instrument, reference scores and evidence map
```

**Author block (exactly, everywhere)**
```
Oyekunle Adedamola Oyeniyi
ORCID: 0000-0002-1978-6133
Affiliation: Independent Researcher, Pullman, Washington, USA
Email: adedamolaoyekunleniyi@gmail.com
```

**Keywords**
```
biorisk management; clinical laboratory; infectious aerosol; laboratory-acquired infection; ISO 35001; biosafety cabinet; evidence grading; sentinel laboratory
```

**Licence**
```
Creative Commons Attribution 4.0 International (CC BY 4.0)
```

---

## Part 1 — GitHub (15 minutes)

GitHub is where the project files live publicly. A repository is a project folder that
lives online and keeps every past version.

1. Go to https://github.com and sign in as **DrAdedamola**.
2. Click the **+** at the top right, then **New repository**.
3. **Repository name:** paste the name from above.
4. **Description:** paste the short description from above.
5. Choose **Public**.
6. Do **not** tick "Add a README file", "Add .gitignore" or "Choose a license". The project
   already has all three and ticking them creates a conflict.
7. Click **Create repository**.
8. GitHub now shows a page of commands. Ignore it. Come back here and tell me the
   repository exists, and I will push the files for you — or, if you would rather do it
   yourself, download the project folder and use GitHub Desktop
   (https://desktop.github.com) to drag it in and click **Publish**.

**If you want me to push it for you**, you will need to give me a token. A token is a
temporary password that lets me upload on your behalf and that you can cancel at any time.

- Create it at https://github.com/settings/tokens/new
- **Note:** `biorisk reference push`
- **Expiration:** 7 days
- **Tick exactly one box:** `repo`
- Click **Generate token**, copy it, and paste it to me in chat.
- **Revoke it afterwards** at https://github.com/settings/tokens — click **Delete** beside it.

I never write a token into a file and never print it back to you.

9. Once the files are pushed, on the repository page click **Releases** on the right, then
   **Create a new release**. Tag `v1.0`, title `Instrument v1.0 and reference scores`,
   then **Publish release**.

## Part 2 — Zenodo and your DOI (15 minutes)

Zenodo is a free, permanent repository run by CERN. It gives your work a DOI: a permanent
citation number, like a library call number that never changes.

The easy route, which also makes every future release automatic:

1. Go to https://zenodo.org and click **Sign up**, then **Sign up with GitHub**. Use the
   same GitHub account.
2. Once signed in, click your name at the top right, then **GitHub**.
3. You will see a list of your repositories with toggles. Find
   `clinical-lab-aerosol-biorisk-reference` and switch its toggle **On**.
4. Go back to GitHub and create the release as in step 9 above. If you already created it,
   create a `v1.0.1` release instead; Zenodo only picks up releases made after the toggle
   is on.
5. Within a few minutes Zenodo creates a record and mints a DOI. Find it under
   **Uploads** on Zenodo.
6. Click **Edit** on the record and check: title, your name, your ORCID, licence CC BY 4.0,
   keywords, and the description. Click **Publish**.
7. Copy the DOI. It looks like `10.5281/zenodo.XXXXXXX`. Paste it into:
   - `README.md`, under **Citation**
   - `CITATION.cff`, as a new `doi:` field
   - `report/technical_report.md`
   Then make a `v1.0.2` release so the repository and the record agree. Tell me the DOI and
   I will make those edits for you.

**What the two DOIs mean.** Zenodo gives you a *concept* DOI that always points at the
newest version, and a *version* DOI for each release. Cite the concept DOI in your CV.
Cite the version DOI when you mean this exact version.

## Part 3 — The preprint (20 minutes, you must do this yourself)

I cannot submit a preprint for you. Submission is an attestation that you are the author
and the work is yours, and automating an attestation would put a false statement into a
permanent record. What I can do is have everything ready so your part is attesting, not
assembling.

**Where to send it.** This is a methods and evidence paper about clinical laboratory
practice, so **medRxiv** is the natural home: https://www.medrxiv.org/submit-a-manuscript

- Subject area: Occupational and Environmental Health, or Pathology.
- You will be asked for a competing-interests statement, a funding statement (none), and a
  data-availability statement. Use:
  ```
  All data, code and the scoring instrument are openly available at
  https://github.com/DrAdedamola/clinical-lab-aerosol-biorisk-reference and archived at
  Zenodo, DOI [paste it here].
  ```
- medRxiv screens submissions; expect a few days.
- Tell them about AI assistance if asked. The honest statement is in the README and it is
  true: AI assisted with code, wrangling, literature triage and drafting mechanics; every
  analytic decision, score and citation is yours and was checked by you.

**Before you submit,** the manuscript abstract must be in your own words. It is marked
`[VERIFY-D2]` in `report/manuscript.md` for exactly that reason.

## Part 4 — Log it the same day

Publications that are not logged the day they happen are the ones that go missing when you
need them. For each step record: what, the URL or DOI, the date, and a saved PDF or
screenshot of the confirmation.

| Item | URL or DOI | Date | Confirmation saved |
|---|---|---|---|
| GitHub repository | | | |
| GitHub release v1.0 | | | |
| Zenodo concept DOI | | | |
| Zenodo version DOI | | | |
| medRxiv submission | | | |
| medRxiv posted | | | |

---

## What was automated and what was not

Nothing has been pushed anywhere. Every step above is waiting for you, because the
verification gate has not been passed and no tokens have been supplied. When you are ready,
say so and I will do Parts 1 and 2 with you.
