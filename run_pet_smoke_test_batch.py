import csv
import json
import os
import sys
from datetime import datetime
from pathlib import Path

from app import app, build_original_payload, generate_shortlist_payload

try:
    import gspread
except ImportError:
    gspread = None


CASES = [
    {
        "test_id": "PET001",
        "mode": "Pet Curated",
        "brief": "Dog name for playful golden retriever; easy to call at the park",
        "form_data": {
            "pet_type": "Dog",
            "discovery_style": "Balanced mix",
            "style": "Classic",
            "timeless_vs_distinctive": "Balanced",
            "familiarity_preference": "Recognizable but not overused",
            "pronunciation_importance": "Very important",
            "vibe": "Playful",
            "cultural_context": "Human names",
            "partner_alignment": "",
            "notes": "Golden retriever, goofy and loyal. Needs to be easy to call outside. Avoid names that sound like commands.",
        },
    },
    {
        "test_id": "PET002",
        "mode": "Pet Curated",
        "brief": "Cat name for elegant black cat; mysterious but not spooky",
        "form_data": {
            "pet_type": "Cat",
            "discovery_style": "Unexpected finds",
            "style": "Elegant",
            "timeless_vs_distinctive": "Mostly distinctive",
            "familiarity_preference": "A little less common",
            "pronunciation_importance": "Helpful but not absolute",
            "vibe": "Regal",
            "cultural_context": "Mythology",
            "partner_alignment": "",
            "notes": "Black cat, sleek and observant. Mysterious, but avoid Halloween/spooky cliches.",
        },
    },
    {
        "test_id": "PET003",
        "mode": "Pet Curated",
        "brief": "Horse name with steady, dignified barn energy",
        "form_data": {
            "pet_type": "Horse",
            "discovery_style": "Classic favorites",
            "style": "Classic",
            "timeless_vs_distinctive": "Mostly timeless",
            "familiarity_preference": "Recognizable but not overused",
            "pronunciation_importance": "Very important",
            "vibe": "Brave",
            "cultural_context": "Geography",
            "partner_alignment": "",
            "notes": "Bay gelding, calm and reliable. Should carry clearly in a barn or field.",
        },
    },
    {
        "test_id": "PET004",
        "mode": "Pet Curated",
        "brief": "Bird name, bright and repeatable, good for a parrot",
        "form_data": {
            "pet_type": "Bird",
            "discovery_style": "Balanced mix",
            "style": "Modern",
            "timeless_vs_distinctive": "Balanced",
            "familiarity_preference": "A little less common",
            "pronunciation_importance": "Very important",
            "vibe": "Quirky",
            "cultural_context": "Music",
            "partner_alignment": "",
            "notes": "Small parrot with a huge personality. Bright, repeatable, not too silly.",
        },
    },
    {
        "test_id": "PET005",
        "mode": "Pet Curated",
        "brief": "Rabbit name, gentle and sweet without being childish",
        "form_data": {
            "pet_type": "Rabbit",
            "discovery_style": "Balanced mix",
            "style": "Soft and romantic",
            "timeless_vs_distinctive": "Balanced",
            "familiarity_preference": "Recognizable but not overused",
            "pronunciation_importance": "Helpful but not absolute",
            "vibe": "Gentle",
            "cultural_context": "Nature",
            "partner_alignment": "",
            "notes": "Cream-colored rabbit, shy at first, very sweet. Avoid babyish names.",
        },
    },
    {
        "test_id": "PET006",
        "mode": "Pet Curated",
        "brief": "Reptile name for bearded dragon; visual/personality fit over callability",
        "form_data": {
            "pet_type": "Reptile",
            "discovery_style": "Unexpected finds",
            "style": "Uncommon but usable",
            "timeless_vs_distinctive": "Mostly distinctive",
            "familiarity_preference": "Memorable and rarer",
            "pronunciation_importance": "Not important",
            "vibe": "Regal",
            "cultural_context": "Mythology",
            "partner_alignment": "",
            "notes": "Bearded dragon with orange coloring. Strong visual name, not necessarily a call name.",
        },
    },
    {
        "test_id": "PET007",
        "mode": "Pet Curated",
        "brief": "Other pet, cozy human-style family member name",
        "form_data": {
            "pet_type": "Other",
            "discovery_style": "Classic favorites",
            "style": "Classic",
            "timeless_vs_distinctive": "Mostly timeless",
            "familiarity_preference": "Recognizable but not overused",
            "pronunciation_importance": "Very important",
            "vibe": "Sweet",
            "cultural_context": "Human names",
            "partner_alignment": "",
            "notes": "Small companion animal, very social. Want a name that feels like part of the family.",
        },
    },
    {
        "test_id": "PET008",
        "mode": "Pet Original",
        "brief": "Original dog name, two syllables, crisp and park-callable",
        "form_data": {
            "pet_type": "Dog",
            "discovery_style": "Completely original",
            "style": "Modern",
            "vibe": "Adventurous",
            "familiarity_preference": "Memorable and rarer",
            "pronunciation_importance": "Very important",
            "starting_letter": "",
            "length_preference": "Balanced 2 syllables",
            "cultural_context": "Nature",
            "avoid_feel": "Command-like, fantasy, product name, hard to say.",
            "notes": "New name for an active dog; should feel original but easy to call.",
        },
    },
    {
        "test_id": "PET009",
        "mode": "Pet Original",
        "brief": "Original cat name, sleek and distinctive",
        "form_data": {
            "pet_type": "Cat",
            "discovery_style": "Completely original",
            "style": "Elegant",
            "vibe": "Curious",
            "familiarity_preference": "Memorable and rarer",
            "pronunciation_importance": "Helpful but not absolute",
            "starting_letter": "",
            "length_preference": "Short and crisp",
            "cultural_context": "Mythology",
            "avoid_feel": "Dog-like, goofy, hard to spell.",
            "notes": "Original name for a sleek, curious cat. Distinctive sound matters more than obedience.",
        },
    },
    {
        "test_id": "PET010",
        "mode": "Pet Original",
        "brief": "Original bird name, bright and repeatable",
        "form_data": {
            "pet_type": "Bird",
            "discovery_style": "Completely original",
            "style": "Modern",
            "vibe": "Playful",
            "familiarity_preference": "Memorable and rarer",
            "pronunciation_importance": "Very important",
            "starting_letter": "",
            "length_preference": "Short and crisp",
            "cultural_context": "Music",
            "avoid_feel": "Too random, harsh, or app-name-like.",
            "notes": "Original name for a vocal bird. Should be bright, repeatable, and social.",
        },
    },
    {
        "test_id": "PET011",
        "mode": "Pet Original",
        "brief": "Original reptile name, visual and mythic without fantasy-game energy",
        "form_data": {
            "pet_type": "Reptile",
            "discovery_style": "Completely original",
            "style": "Uncommon but usable",
            "vibe": "Regal",
            "familiarity_preference": "Memorable and rarer",
            "pronunciation_importance": "Not important",
            "starting_letter": "",
            "length_preference": "Balanced 2 syllables",
            "cultural_context": "Mythology",
            "avoid_feel": "Video-game fantasy, villain, product code, hard consonant pileups.",
            "notes": "Original name for a reptile; visual symbolism and personality matter more than call response.",
        },
    },
]


FIELDNAMES = [
    "Test ID",
    "Mode",
    "Brief / Parent Request",
    "Gender",
    "Discovery Style",
    "Cultural Feel",
    "Sibling / Family Context",
    "Generated Name",
    "Pronunciation",
    "Origin / Structure",
    "Meaning / Style",
    "Why / Fit Note",
    "Rank Shown",
    "Source",
    "User Reaction",
    "Usable? (Y/N)",
    "Quality Score (1-5)",
    "Novelty Score (1-5)",
    "Fit Score (1-5)",
    "Issue Type",
    "Notes",
    "Action Needed",
]


def get_smoke_worksheet():
    sheet_id = os.getenv("GOOGLE_SMOKE_TEST_SHEET_ID", "").strip()
    credentials_json = os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON", "").strip()
    worksheet_name = os.getenv("GOOGLE_SMOKE_TEST_WORKSHEET", "Smoke Tests").strip() or "Smoke Tests"
    if not sheet_id or not credentials_json or gspread is None:
        return None

    credentials = json.loads(credentials_json)
    client = gspread.service_account_from_dict(credentials)
    spreadsheet = client.open_by_key(sheet_id)
    try:
        worksheet = spreadsheet.worksheet(worksheet_name)
    except gspread.WorksheetNotFound:
        worksheet = spreadsheet.add_worksheet(title=worksheet_name, rows=1000, cols=len(FIELDNAMES))
        worksheet.append_row(FIELDNAMES, value_input_option="USER_ENTERED")

    if not worksheet.row_values(1):
        worksheet.append_row(FIELDNAMES, value_input_option="USER_ENTERED")
    return worksheet


def append_rows_to_google_sheet(rows):
    worksheet = get_smoke_worksheet()
    if worksheet is None:
        return False
    values = [[row.get(field, "") for field in FIELDNAMES] for row in rows]
    if values:
        worksheet.append_rows(values, value_input_option="USER_ENTERED")
    return True


def row_for_item(case, item, rank, source):
    form = case["form_data"]
    return {
        "Test ID": case["test_id"],
        "Mode": case["mode"],
        "Brief / Parent Request": case["brief"],
        "Gender": form.get("pet_type", ""),
        "Discovery Style": form.get("discovery_style", ""),
        "Cultural Feel": form.get("cultural_context", ""),
        "Sibling / Family Context": form.get("partner_alignment", "") or form.get("notes", ""),
        "Generated Name": item.get("name", ""),
        "Pronunciation": item.get("pronunciation", ""),
        "Origin / Structure": item.get("origin") or item.get("structure", ""),
        "Meaning / Style": item.get("meaning") or item.get("style", ""),
        "Why / Fit Note": item.get("why") or item.get("fit_note", ""),
        "Rank Shown": rank,
        "Source": source,
        "User Reaction": "",
        "Usable? (Y/N)": "",
        "Quality Score (1-5)": "",
        "Novelty Score (1-5)": "",
        "Fit Score (1-5)": "",
        "Issue Type": "",
        "Notes": "",
        "Action Needed": "",
    }


def run_case(case):
    form = case["form_data"]
    if case["mode"] == "Pet Original":
        payload = build_original_payload(form)
        return payload["names"], "openai_or_fallback_original"
    payload = generate_shortlist_payload(form)
    source = "fallback" if payload.get("used_fallback") else "openai"
    return payload["names"], source


def main():
    append_to_sheets = "--append-to-sheets" in sys.argv
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    out_path = Path(__file__).with_name(f"namengine_pet_smoke_test_{stamp}.csv")
    rows = []
    with app.test_request_context("/"):
        for case in CASES:
            print(f"Running {case['test_id']} {case['mode']}: {case['brief']}")
            names, source = run_case(case)
            for rank, item in enumerate(names, start=1):
                rows.append(row_for_item(case, item, rank, source))

    with out_path.open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)
    print(out_path)
    if append_to_sheets:
        if append_rows_to_google_sheet(rows):
            print(f"Appended {len(rows)} rows to Google Sheets.")
        else:
            print(
                "Skipped Google Sheets append: set GOOGLE_SMOKE_TEST_SHEET_ID "
                "and GOOGLE_SERVICE_ACCOUNT_JSON.",
                file=sys.stderr,
            )
            sys.exit(2)


if __name__ == "__main__":
    main()
