import os
import json
import datetime
from fpdf import FPDF

font_name = "Menlo"
base_color = (0, 0, 0)
chord_color = (0, 0, 255)
lyrics_color = (0, 0, 0)


def get_today() -> str:
    today = datetime.datetime.utcnow().date().isoformat()
    return today


class SongPDF(FPDF):

    def __init__(self, profile: dict, **kwargs: dict) -> None:
        super().__init__(**kwargs)
        self.add_font(fname=f"/System/Library/Fonts/{font_name}.ttc", style="I", uni=True)
        self.add_font(fname=f"/System/Library/Fonts/{font_name}.ttc", style="B", uni=True)
        self.title = profile["title"]
        self.split_lines = profile.get("split_lines", [])
        self.bpm = profile.get("bpm", None)

    def header(self):
        # Rendering logo:
        # self.image("../docs/fpdf2-logo.png", 10, 8, 33)
        # Setting font: helvetica bold 15
        self.set_font(font_name, style="B", size=20)
        # Moving cursor to the right:
        # self.cell(80)
        # Printing title:
        self.set_text_color(*base_color)
        self.cell(0, 10, text=self.title, border=0, align="L")
        if self.bpm is not None:
            self.set_font(font_name, style="I", size=16)
            self.cell(0, 10, f"{self.bpm} bpm", border=0, align="R")
        # Performing a line break:
        self.ln(10)

    def footer(self):
        # Position cursor at 1.5 cm from bottom:
        self.set_y(-15)
        self.set_font(font_name, style="I", size=16)
        self.set_text_color(*base_color)
        self.cell(0, 10, f"Page {self.page_no()}/{{nb}}", align="L")
        # self.cell(0, 10, f"Orion Band {get_today()}", border=0, align="R")


def get_profiles() -> dict:
    with open("typeset_config.json", "r") as fp:
        profiles = json.load(fp)
        return dict(profiles)


def get_profile(name: str) -> dict:
    profiles = get_profiles()
    profile = profiles[name]
    return profile


def create_pdf(name: str, profile: dict) -> None:
    pdf = SongPDF(profile=profile, orientation="P", unit="mm", format="A4")
    pdf.add_page()
    pdf.set_font(family=font_name, style="B", size=16)
    pdf = typeset_body(pdf, get_body(profile["input_file"]))
    output_path = os.path.join("pdf", f"{name}.pdf")
    pdf.output(name=output_path)


def get_body(path: str) -> list[str]:
    with open(path, "r") as fp:
        res = fp.readlines()
        return res


def typeset_body(pdf: SongPDF, body: list[str]) -> SongPDF:
    chord_patterns = chords_list()
    print(f"{len(chord_patterns)=}")
    for i, line in enumerate(body):
        x = line.rstrip()
        if i+1 in pdf.split_lines:
            pdf.add_page()
        else:
            pdf.ln()
        icl = is_chord_line(x, patterns=chord_patterns)
        print(f"{icl}: {x}")
        if icl:
            pdf.set_text_color(*chord_color)
        else:
            pdf.set_text_color(*lyrics_color)
        pdf.cell(text=line)
    return pdf


def is_chord_line(line: str, patterns: set[str]) -> bool:
    tokens = line.split(sep=" ")
    token_chord = {is_token_chord(t, patterns) for t in tokens if len(t) > 0}
    # if any(token_chord):
    #     print(tokens)
    return all(token_chord)


def is_token_chord(token: str, patterns: set[str]) -> bool:
    result = token in patterns
    return result


def chords_list() -> set[str]:
    base_notes = {"C", "D", "E", "F", "G", "A", "H", "B"}
    shift = {"#", "b"}
    minors = {"m", "mi"}
    ext = {"7", "maj7", "4", "sus4", "dim", "dim7", "9", "+", "6"}
    base_ext = {f"{x}{e}" for x in base_notes for e in ext}
    base_minors = {f"{x}{m}" for x in base_notes for m in minors}
    base_minors_ext = {f"{x}{e}" for x in base_minors for e in ext}
    base_minors_all = base_minors | base_minors_ext
    base_shifts = {f"{x}{s}" for x in base_notes for s in shift}
    base_shifts_minors = {f"{x}{m}" for x in base_shifts for m in minors}
    base_shifts_ext = {f"{x}{e}" for x in base_shifts for e in ext}
    base_shifts_minors_ext = {f"{x}{e}" for x in base_shifts_minors for e in ext}
    base_shifts_all = base_shifts | base_shifts_minors | base_shifts_ext | base_shifts_minors_ext
    result = base_notes | base_ext | base_minors_all | base_shifts_all
    return result
