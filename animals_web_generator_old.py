import json
import logging
from typing import Any, Union, List, Dict
from pathlib import Path

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')


def load_data(file_path: Union[str, Path]) -> Any:
    try:
        with open(file_path, "r", encoding="utf-8") as handle:
            return json.load(handle)
    except FileNotFoundError:
        logging.error(f"Die Datei unter {file_path} wurde nicht gefunden.")
        return None
    except json.JSONDecodeError:
        logging.error(f"Die Datei unter {file_path} ist keine gültige JSON-Datei.")
        return None


def process_and_print_animals(animals_data: List[Dict[str, Any]]):
    if not isinstance(animals_data, list):
        logging.error("Die JSON-Daten sind keine Liste. Verarbeitung nicht möglich.")
        return

    for i, animal in enumerate(animals_data):
        output_lines = []

        name = animal.get('name')
        if name:
            output_lines.append(f"Name: {name}")

        characteristics = animal.get('characteristics')
        if characteristics and isinstance(characteristics, dict):
            diet = characteristics.get('diet')
            if diet:
                output_lines.append(f"Diet: {diet}")

            animal_type = characteristics.get('type')
            if animal_type:
                output_lines.append(f"Type: {animal_type}")

        locations = animal.get('locations')
        if locations and isinstance(locations, list) and locations:
            output_lines.append(f"Location: {locations[0]}")

        if output_lines:
            # Sortieren, damit die Ausgabe immer konsistent ist
            # Annahme: 'Name' soll immer zuerst kommen.
            output_lines.sort(key=lambda x: not x.startswith("Name"))
            print("\n".join(output_lines))
            if i < len(animals_data) - 1:
                print()


if __name__ == "__main__":
    file_to_load = 'animals_data.json'
    all_animals = load_data(file_to_load)

    if all_animals:
        process_and_print_animals(all_animals)