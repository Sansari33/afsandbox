import openai
import json
from datetime import date
import yaml
from pathlib import Path

# ------------------------
# GLOBAL TOKEN USAGE TRACKER
# ------------------------
total_prompt_tokens = 0
total_completion_tokens = 0

def tracked_chat_completion(**kwargs):
    """
    Wrapper for openai.ChatCompletion.create that tracks token usage.
    """
    global total_prompt_tokens, total_completion_tokens
    response = openai.ChatCompletion.create(**kwargs)
    if 'usage' in response:
        total_prompt_tokens += response['usage'].get('prompt_tokens', 0)
        total_completion_tokens += response['usage'].get('completion_tokens', 0)
    return response

# ------------------------
# LOAD CONFIG
# ------------------------
cfg = yaml.safe_load(open("imi_macro_updater/config.yaml"))

# ------------------------
# IMPORT IMI MODULES
# ------------------------
from imi_core.metaagent import MetaAgent
from imi_core.modules import (
    centurion, tailwind_radar, red_queen, narrative_reaper, dominion, whisper,
    blackswannode, flowmancer, options_warlock, spider_lily, budgetwatch_ai,
    formulascan, convexity_dashboard
)
from imi_core.utils import apply_alpha_score, save_logs
from imi_core.formatting import render_template

# ------------------------
# RUN ORCHESTRATOR
# ------------------------
agent = MetaAgent(mode="daily_update")
signals = {}
signals['centurion'] = centurion.run()
signals['tailwind'] = tailwind_radar.scan()
if signals['tailwind'].get("macro_event"):
    signals['red_queen'] = red_queen.simulate(signals['tailwind'])
signals['narratives'] = narrative_reaper.track()
signals['dominion'] = dominion.detect()
signals['whisper'] = whisper.scan()
signals['blackswan'] = blackswannode.scan()
signals['flow'] = flowmancer.read()
signals['options'] = options_warlock.conjure()
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
        "date": date.today().strftime("%B %d, %Y"),
        "market_overview": ranked_ideas.get('market_overview', ''),
        "key_indicators": ranked_ideas.get('indicators', ''),
        "equities": ranked_ideas.get('equities', ''),
        "fx_rates": ranked_ideas.get('fx_rates', ''),
        "news": ranked_ideas.get('news', ''),
        "risk_matrix": ranked_ideas.get('risk_matrix', '')
    }
)

Path(cfg['output_path']).write_text(report_html, encoding="utf-8")
save_logs(signals, log_dir=f"logs/{date.today()}")

# ------------------------
# SAVE TOKEN USAGE DATA
# ------------------------
token_usage_data = {
    "prompt_tokens": total_prompt_tokens,
    "completion_tokens": total_completion_tokens
}

with open("token_usage.json", "w") as f:
    json.dump(token_usage_data, f)

print("\n------ TOKEN USAGE SUMMARY ------")
print(f"Prompt tokens: {total_prompt_tokens}")
print(f"Completion tokens: {total_completion_tokens}")
print(f"Total tokens: {total_prompt_tokens + total_completion_tokens}")
print("Token usage saved to token_usage.json")
