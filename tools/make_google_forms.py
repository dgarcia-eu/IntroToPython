#!/usr/bin/env python3
"""
Create this year's four daily feedback forms in Google Forms.

    python tools/make_google_forms.py --dry-run   # show the payloads, call nothing
    python tools/make_google_forms.py             # create, publish, record the URLs

What it does, in order:

  1. reads the questionnaire from feedback-form/questions.toml
  2. creates one Google Form per day via forms.create
  3. adds the questions via forms.batchUpdate
  4. publishes each form via forms.setPublishSettings
  5. writes each form's responder URL and id back into feedback-form/forms.toml

Then run tools/make_feedback.py to regenerate the redirect pages. The QR codes
on the slides do not change and never need reprinting: they point at this
repository, which forwards to whatever these URLs turn out to be.

Step 4 is not optional housekeeping. Forms created through the API after
30 June 2026 default to UNPUBLISHED, so a form that is created but not
published looks fine in Drive and refuses students at the door. That is
exactly the failure you would discover at 09:35 on the second morning of the
course, so this script publishes explicitly and then verifies by re-reading
the form back from the API.

Credentials
-----------
Needs a Google OAuth client, once. See feedback-form/GOOGLE_SETUP.md.
Nothing secret is stored in this repository: the client secret and the
refresh token both live under ~/.config/introtopython/.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import tomllib

CONFIG = "feedback-form/forms.toml"
QUESTIONS = "feedback-form/questions.toml"

CONF_DIR = os.path.expanduser("~/.config/introtopython")
CLIENT_SECRET = os.path.join(CONF_DIR, "google_client_secret.json")
TOKEN = os.path.join(CONF_DIR, "google_token.json")

# forms.body is enough to create, edit and publish. The responses scope is
# requested here too so that fetching answers later reuses the same consent
# instead of sending David back through the browser a second time.
SCOPES = [
    "https://www.googleapis.com/auth/forms.body",
    "https://www.googleapis.com/auth/forms.responses.readonly",
]


def load(path: str) -> dict:
    with open(path, "rb") as fh:
        return tomllib.load(fh)


def question_text(q: dict, day: int) -> str:
    """Question 4 asks something different on Day 4. See questions.toml."""
    return q.get(f"text_day{day}", q["text"])


def build_items(questions: dict, day: int) -> list[dict]:
    items = []
    for q in questions["question"]:
        question: dict = {"required": bool(q.get("required", False))}
        if q["type"] == "scale":
            question["scaleQuestion"] = {
                "low": q["min"],
                "high": q["max"],
                "lowLabel": q["min_label"],
                "highLabel": q["max_label"],
            }
        elif q["type"] == "free_text":
            question["textQuestion"] = {"paragraph": True}
        else:
            sys.exit(f"unknown question type {q['type']!r} in {QUESTIONS}")
        items.append({
            "title": question_text(q, day),
            "questionItem": {"question": question},
        })
    return items


def set_targets(path: str, results: dict[int, tuple[str, str]]) -> None:
    """Write target/form_id back per day, leaving every comment untouched.

    forms.toml is hand-maintained and its comments carry the instructions for
    next year, so it is edited line by line rather than re-serialised.
    """
    lines = open(path, encoding="utf-8").read().splitlines(keepends=True)
    out: list[str] = []
    day: int | None = None
    for line in lines:
        m = re.match(r"\s*day\s*=\s*(\d+)", line)
        if m:
            day = int(m.group(1))
        if day in results and re.match(r"\s*target\s*=", line):
            url, form_id = results[day]
            out.append(f'target = "{url}"\n')
            out.append(f'form_id = "{form_id}"\n')
            day = None
            continue
        if re.match(r"\s*form_id\s*=", line):
            continue  # rewritten above
        out.append(line)
    open(path, "w", encoding="utf-8").write("".join(out))


def credentials():
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow

    creds = None
    if os.path.exists(TOKEN):
        creds = Credentials.from_authorized_user_file(TOKEN, SCOPES)
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    if not creds or not creds.valid:
        if not os.path.exists(CLIENT_SECRET):
            sys.exit(f"No OAuth client at {CLIENT_SECRET}.\n"
                     f"See feedback-form/GOOGLE_SETUP.md for the one-time setup.")
        creds = InstalledAppFlow.from_client_secrets_file(
            CLIENT_SECRET, SCOPES).run_local_server(port=0)
    os.makedirs(CONF_DIR, exist_ok=True)
    with open(TOKEN, "w", encoding="utf-8") as fh:
        fh.write(creds.to_json())
    os.chmod(TOKEN, 0o600)
    return creds


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--year", type=int, help="override the year in forms.toml")
    ap.add_argument("--dry-run", action="store_true",
                    help="print exactly what would be sent, contact nothing")
    args = ap.parse_args()

    os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
    cfg, questions = load(CONFIG), load(QUESTIONS)
    year = args.year or cfg["year"]

    plans = []
    for form in cfg["form"]:
        day = form["day"]
        plans.append({
            "day": day,
            "title": questions["title"].format(course=cfg["course"], day=day),
            "document_title": f"{cfg['course']} {year} - Feedback Day {day}",
            "description": questions["intro"].strip(),
            "items": build_items(questions, day),
        })

    if args.dry_run:
        for p in plans:
            print(f"\n=== Day {p['day']} " + "=" * 52)
            print(f"  form title : {p['title']}")
            print(f"  drive name : {p['document_title']}")
            print(f"  description: {p['description'][:70]}...")
            for i, item in enumerate(p["items"], 1):
                q = item["questionItem"]["question"]
                kind = ("scale %d-%d [%s .. %s]" % (
                    q["scaleQuestion"]["low"], q["scaleQuestion"]["high"],
                    q["scaleQuestion"]["lowLabel"], q["scaleQuestion"]["highLabel"])
                    if "scaleQuestion" in q else "paragraph text")
                req = "required" if q["required"] else "optional"
                print(f"   {i}. [{kind}, {req}]\n      {item['title']}")
        print(f"\nDry run: nothing was created. {len(plans)} forms would be made for {year}.")
        return 0

    from googleapiclient.discovery import build
    service = build("forms", "v1", credentials=credentials())

    results: dict[int, tuple[str, str]] = {}
    problems: list[str] = []
    for p in plans:
        created = service.forms().create(body={"info": {
            "title": p["title"], "documentTitle": p["document_title"]}}).execute()
        form_id = created["formId"]

        requests = [
            {"updateFormInfo": {
                "info": {"description": p["description"]}, "updateMask": "description"}},
            # Set this explicitly, never rely on the default. The API defaults
            # emailCollectionType to DO_NOT_COLLECT for a personal Google
            # account but to VERIFIED for a Google Workspace account, so on a
            # university Workspace account the form would quietly start
            # recording who answered. The form promises anonymity in its own
            # description, and this is the line that makes that true.
            {"updateSettings": {
                "settings": {"emailCollectionType": "DO_NOT_COLLECT"},
                "updateMask": "emailCollectionType"}},
        ]
        for index, item in enumerate(p["items"]):
            requests.append({"createItem": {"item": item, "location": {"index": index}}})
        service.forms().batchUpdate(formId=form_id, body={"requests": requests}).execute()

        service.forms().setPublishSettings(formId=form_id, body={
            "publishSettings": {"publishState": {
                "isPublished": True, "isAcceptingResponses": True}}}).execute()

        # Read it back. A form that was created but silently not published is
        # the failure this whole step exists to prevent, so do not take the
        # write's word for it.
        back = service.forms().get(formId=form_id).execute()
        state = back.get("publishSettings", {}).get("publishState", {})
        url = back.get("responderUri", "")
        email = back.get("settings", {}).get("emailCollectionType", "?")
        ok = state.get("isPublished") and state.get("isAcceptingResponses")
        anon = email == "DO_NOT_COLLECT"
        print(f"  Day {p['day']}  {'published' if ok else 'NOT PUBLISHED'}  "
              f"{len(back.get('items', []))} questions  "
              f"{'anonymous' if anon else 'COLLECTS EMAIL (' + email + ')'}\n"
              f"        {url}")
        if not ok:
            print(f"        publishState came back as {json.dumps(state)}")
        if not anon:
            problems.append(f"Day {p['day']}: form is set to {email}, not DO_NOT_COLLECT. "
                            f"It would record who answered, and the form text promises "
                            f"it does not. Fix before showing the QR code.")
        results[p["day"]] = (url, form_id)

    set_targets(CONFIG, results)
    print(f"\nWrote {len(results)} responder URLs into {CONFIG}.")
    if problems:
        print("\nPROBLEMS:")
        for prob in problems:
            print(f"  - {prob}")
        return 1
    print("Next: python tools/make_feedback.py   (regenerates the redirect pages;\n"
          "      the QR codes do not change)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
