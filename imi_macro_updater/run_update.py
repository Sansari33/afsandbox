import sys
import yaml
from pathlib import Path

cfg = yaml.safe_load(open("imi_macro_updater/config.yaml"))

imi_path = Path(cfg["imi_modules_path"]).resolve()
sys.path.append(str(imi_path))

from macro_report import run_macro_research, render_report

data = run_macro_research(
    calendar=cfg["data_sources"]["macro_calendar"],
    equities=cfg["data_sources"]["equities_feed"],
    fx=cfg["data_sources"]["fx_feed"],
    news=cfg["data_sources"]["news_archive"]
)

html = render_report(data, template_path=cfg["template_path"])
Path(cfg["output_path"]).write_text(html, encoding="utf-8")

print(f"Updated macro report at {cfg['output_path']}")