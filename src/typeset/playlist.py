import os
import yaml
from dataclasses import dataclass
from fpdf.fonts import FontFace
from typeset.utils import FPDF, font_name, typeset_body, get_body, get_profile, base_color


@dataclass
class SongInPlaylist:

    order: int
    name: str
    key: str | None
    note: str | None
    title: str
    input_file: str
    split_lines: list[int]
    bpm: int | None

    @classmethod
    def from_dict(cls, order: int, d: dict) -> "SongInPlaylist":
        name = d["name"]
        profile = get_profile(name)
        x = cls(
            order=order,
            name=d["name"],
            key=d.get("key", None),
            note=d.get("note", None),
            title=profile["title"],
            input_file=profile["input_file"],
            split_lines=profile.get("split_lines", []),
            bpm=profile.get("bpm", None),
        )
        return x


@dataclass
class Playlist:
    name: str
    title: str
    subtitle: str | None
    songs: list[SongInPlaylist]
    output_path: str


def get_playlist(name: str) -> Playlist:
    input_filename = os.path.join("playlist", "input", f"{name}.yaml")
    with open(input_filename, "r") as fp:
        data = yaml.load(fp, Loader=yaml.SafeLoader)
    x = Playlist(
        name=name,
        title=str(data["title"]),
        subtitle=data.get("subtitle", None),
        songs=[
            SongInPlaylist.from_dict(i+1, s) for i, s in enumerate(data["songs"])
        ],
        output_path=os.path.join("playlist", "output", f"{name}.pdf"),
    )
    return x


class PlaylistPDF(FPDF):

    def __init__(self, pll: Playlist) -> None:
        super().__init__(orientation="P", unit="mm", format="A4")
        self.add_font(fname=f"/System/Library/Fonts/{font_name}.ttc", style="I", uni=True)
        self.add_font(fname=f"/System/Library/Fonts/{font_name}.ttc", style="B", uni=True)
        self.p = pll
        self.current_song: SongInPlaylist | None = None

    def header(self):
        # Rendering logo:
        # self.image("../docs/fpdf2-logo.png", 10, 8, 33)
        # Setting font: helvetica bold 15
        self.set_font(font_name, style="B", size=20)
        # Moving cursor to the right:
        # self.cell(80)
        # Printing title:
        self.set_text_color(*base_color)
        if self.current_song is None:
            self.cell(0, 10, text=self.p.title, border=0, align="L")
        else:
            self.cell(0, 10, text=self.current_song.title, border=0, align="L")
        self.set_font(font_name, style="I", size=16)
        if self.current_song is None:
            # self.cell(0, 10, f"{len(self.p.songs)} songs", border=0, align="R")
            pass
        else:
            self.cell(0, 10, f"{self.current_song.order}", border=0, align="R")
        # Performing a line break:
        self.ln(10)

    def footer(self):
        # Position cursor at 1.5 cm from bottom:
        self.set_y(-15)
        self.set_font(font_name, style="I", size=16)
        self.set_text_color(*base_color)
        self.cell(0, 10, f"Page {self.page_no()}/{{nb}}", align="L")
        if self.current_song.order > 1:
            self.cell(0, 10, self.p.title, border=0, align="R")


def typeset_playlist(p: Playlist) -> None:
    pdf = PlaylistPDF(pll=p)
    pdf.current_song = None
    pdf.add_page()
    pdf = typeset_toc(pdf, p)
    for s in p.songs:
        pdf.current_song = s
        pdf.add_page()
        pdf.set_font(family=font_name, style="B", size=16)
        pdf = typeset_body(pdf, get_body(s.input_file), s.split_lines)
    pdf.output(name=p.output_path)


def typeset_toc(pdf: FPDF, p: Playlist) -> FPDF:
    pdf.set_font(family=font_name, style="B", size=12)
    if p.subtitle is not None:
        pdf.ln(h=6)
        pdf.set_text_color(*base_color)
        pdf.cell(text=p.subtitle)
        pdf.ln(h=10)
    headings_style = FontFace(emphasis="BOLD", fill_color=(220, 240, 220))
    with pdf.table(
        col_widths=(8, 40, 8, 30),
        headings_style=headings_style,
    ) as table:
        header = table.row()
        header.cell("Pořadí")
        header.cell("Název")
        header.cell("Tónina")
        header.cell("Poznámky")
        for s in p.songs:
            row = table.row()
            row.cell(str(s.order))
            row.cell(s.title)
            row.cell(s.key)
            row.cell(s.note)
    return pdf
