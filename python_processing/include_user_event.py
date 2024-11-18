import sys
from pathlib import Path
from datetime import datetime, timezone
import series_prcessing


def log_text(s: str):
    logfile = Path('php_triggered_python.log')
    now = datetime.now(timezone.utc)
    with logfile.open('a', encoding='utf-8') as f:
        f.write(f"{now}\t{s}\n")


if __name__ == '__main__':
    if len(sys.argv) != 3:
        log_text(f'{sys.argv[0]} called with unexpected arguments: {sys.argv[1:]}\n'
                 f'{" "*26}\tExpected: ### [TRUE | FALSE]')
        exit(1)

    log_text(f"{sys.argv[0]} called with {sys.argv[1:]}")

    try:
        existing: bool = sys.argv[2] == 'TRUE'
        race_number = int(sys.argv[1])
        if existing:
            series_prcessing.refresh_known_events(race_number)
        else:
            series_prcessing.collect_event_data(race_number)
        series_prcessing.generate_all_races_html()
        series_prcessing.generate_league_table_html()
    except Exception as e:
        log_text(f"[ERROR] {str(e)}")
        exit(1)

    log_text(f"Refresh completed successfully")
