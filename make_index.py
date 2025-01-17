from pathlib import Path
from typing import Dict, List

import yaml
from maker.const import Frequency


def load_config() -> Dict:
    config_path = Path(".") / "config.yml"
    if not config_path.exists():
        raise FileNotFoundError(f"{config_path} not found")
    
    return yaml.safe_load(config_path.read_text())


def make_svg_filename(app: Dict) -> str:
    appid = app["apple_identifier"]
    frequency = Frequency(app["frequency"]).badge_value

    return f"{appid}-{frequency}.svg"


def create_index_html(filenames: List[str]) -> None:
    dist_path = Path(".") / "dist"
    dist_path.mkdir(exist_ok=True)
    index_path = dist_path / "index.html"

    li_tags = "".join(map(lambda svg: f"<li><a href=\"./{svg}\">{svg}</a></li>", filenames))
    ul_tag = f"<ul>{li_tags}</ul>"
    html = f"<!DOCTYPE html><html><body>{ul_tag}</body></html>"
    index_path.write_text(html)


def main() -> None:
    apps = load_config().get("apps", [])
    filenames = [make_svg_filename(app) for app in apps]
    create_index_html(filenames)
    print("[Created] dist/index.html")


if __name__ == "__main__":
    main()
