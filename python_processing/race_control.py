from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from config import Config
from event_creator import create_race
from series_prcessing import get_races, series_processing, regenerate_artifacts
from typing import Callable
from pathlib import Path
from shutil import rmtree
from common import backup_series
import os
import json
import functools
print = functools.partial(print, flush=True)  # Always flush prints


def select_race() -> dict:
    races = get_races()
    choices = list()
    race: dict
    for race in races:
        choice = Choice(race, name=race["name"])
        choices.append(choice)

    race = inquirer.select(
        message="Select a Race:",
        choices=choices,
        default=None,
    ).execute()
    return race


def view_race():
    race: dict = select_race()
    if 'challenge' in race:
        race['challenge'] = 'Removed for clarity...'

    print(json.dumps(race, indent=2, ensure_ascii=False))
    main()


def confirm(this: str, the_thing: Callable):
    proceed = inquirer.confirm(message=f"{this}, Proceed?", default=False).execute()
    if proceed:
        the_thing()


def purge_artifacts():
    files = Config.series.gen_html_path.glob('*')
    for file in files:
        if file.name.startswith('.'):
            continue
        print(f'Deleting: {file}')
        if file.is_file():
            os.remove(file)
        elif file.is_dir():
            rmtree(file)
    main('Regenerate artifacts')


def login_as():
    Config.rouvy.email = inquirer.text(
        message="Rouvy email:",
        long_instruction="Enter Rouvy email",
    ).execute()
    Config.rouvy.password = inquirer.secret(
        message="Rouvy password:",
        transformer=lambda _: "[hidden]",
        long_instruction="Enter Rouvy password",
    ).execute()
    print_env()


def create_events():
    race: dict = select_race()
    race_number = race['number']
    print(f"Preview of {race_number}")
    create_race(race_number, test_mode=True)
    print(f"Events will be created by {Config.rouvy.email}, you can change this in the previous menu.")
    proceed = inquirer.confirm(message="Look good? Proceed with event creation?", default=False).execute()
    if proceed:
        create_race(race_number, test_mode=False)


def main(default=None):
    print('')
    backups: list = sorted(Path(Config.series.data_path, 'Backup').glob(f'{Config.series.series_path.name}_*.tar.gz'))
    if len(backups) == 0:
        print("No backups found")
    else:
        print(f'Last backup: {backups[-1].name}')

    action = inquirer.select(
        message="What do you want to do?:",
        choices=["Backup Series", "Series Processing", "Regenerate artifacts",
                 "Add Race", "View Race", "Purge artifacts", "Delete Race", "Login As", "Create Events", "Quit"],
        default=default,
    ).execute()

    if action == "Backup Series":
        backup_series()
    elif action == "View Race":
        view_race()
    elif action == "Series Processing":
        series_processing()
    elif action == "Regenerate artifacts":
        regenerate_artifacts()
    elif action == "Purge artifacts":
        confirm('Purge artifacts', purge_artifacts)
    elif action == "Login As":
        login_as()
    elif action == "Create Events":
        create_events()
    elif action == "Quit":
        exit(0)
    else:
        print("Not currently implemented")
    main()


def print_env():
    print(f"\n{'*'*100}")
    print(f"Series name:     {Config.series.name}")
    print(f"Path:            {Config.series.series_path}")
    print(f"Path (abs):      {os.path.normpath(Config.series.series_path.absolute())}")
    print(f"Generated:       {Config.series.gen_html_path}")
    print(f"Generated (abs): {os.path.normpath(Config.series.gen_html_path.absolute())}")
    print(f"Rouvy User:      {Config.rouvy.email}")
    print(f"{'*'*100}")
    print("Check the above is as expected, if not quit now, incorrect paths will cause unintended doom")
    print("You have been warned!")
    print(f"{'*'*100}")


if __name__ == "__main__":
    print_env()
    main()
