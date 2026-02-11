import logging
from typeset import playlist


logging.basicConfig(level="INFO")
p = playlist.get_playlist("svatba")
playlist.typeset_playlist(p)
logging.info(f"output saved to {p.output_path}")
