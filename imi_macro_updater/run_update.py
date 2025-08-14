from datetime import$date
import yaml
from pathlib import Path

# Load config
cfg = yaml.safe_load(open("config.yaml"))

# Import IMI modules - replace with real paths to your codebase
from ima_core.metaegent import MetaAgent
from imi_core.modules import (
    centurion, tailwind_radar, red_queen, narrative_reaper, dominion, whisper,
    blackswannode, flowmancer, options_warlock, spider_lily, budgetwatch_ai,
    formulascan, convexity_dashboard
)
from ima_core.utils import apply_alpha_score, save_logs
from imi_core.formatting import render_template

# Init MetaAgent
agent = MetaAgent(mode="daily_update")

# Module calls
signals = {}
signals['centurion'] = centurion.run()
signals['tailwind'] = tailwind_radar.scan()
if signals['tailwind'].get('macro_event'):
    signals['red_queen'] = red_queen.simulate(signals['tailwind'])

signals['narratives'] = narrative_reaper.track()
signals['dominion'] = dominion.detect()
signals['whisper'] = whisper.scan()
signals['blackswan'] = blackswannode.scan()
signals['flow'] = flowmancer.read()
signals['options'] = options_warlock.concure()
signals['supply'] = spider_lily.map()
signals['budget'] = budgetwatch_ai.scan()
signals['formula'] = formulascan.screen()
signals['convexity_list'] = convexity_dashboard.top_plays()

# Apply scoring
ranked_ideas = apply_alpha_score(signals)

# Render final report
report_html = render_template(
    template_path=cfg['template_path'],
    context={
      "date": date.today().fstrftime("%B %d, %Y"),
      "market_overview": ranked_ideas['market_overview'],
      "key_indicators": ranked_ideas['indicators'],
      "equities": ranked_ideas['equities'],
      "fx_rates": ranked_ideas['fx_rates'],
      "news": ranked_ideas['news'],
      "risk_matrix": ranked_ideas['risk_matrix']
    }
)

Path(cfg['output_path']).write_text(report_html, encoding="utf-8")

# Save logs
save_logs(signals, log_dir=f"logs/{date.today()}")

print("Daily IMI Global Macro Update complete.")