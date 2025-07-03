import json
import logging
from typing import Any, Union, List, Dict
from pathlib import Path

# Configure logging for clear feedback
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')


def load_data(file_path: Union[str, Path]) -> Any:
    """
    Loads and decodes JSON data from a given file path.

    Args:
        file_path: The path to the JSON file.

    Returns:
        The decoded JSON data, or None if an error occurs.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as handle:
            return json.load(handle)
    except FileNotFoundError:
        logging.error(f"The file at {file_path} was not found.")
        return None
    except json.JSONDecodeError:
        logging.error(f"The file at {file_path} is not a valid JSON file.")
        return None


def generate_animal_cards_html(animals_data: List[Dict[str, Any]]) -> str:
    """
    Generates HTML card snippets for each animal in the provided list.

    Args:
        animals_data: A list of dictionaries, where each dictionary represents an animal.

    Returns:
        A string containing the concatenated HTML for all animal cards.
    """
    if not isinstance(animals_data, list):
        logging.error("The JSON data is not a list. Processing cannot continue.")
        return ""

    card_html_list = []
    for animal in animals_data:
        # Start the card item
        lines = ['<li class="cards__item">']

        # Add the title
        name = animal.get('name', 'Unnamed Animal')
        lines.append(f'  <div class="card__title">{name}</div>')
        lines.append('  <p class="card__text">')

        # Add characteristics
        characteristics = animal.get('characteristics', {})
        diet = characteristics.get('diet')
        if diet:
            lines.append(f'    <strong>Diet:</strong> {diet}<br/>')

        locations = animal.get('locations')
        if locations:
            lines.append(f'    <strong>Location:</strong> {locations[0]}<br/>')

        animal_type = characteristics.get('type')
        if animal_type:
            lines.append(f'    <strong>Type:</strong> {animal_type}')

        # Close the tags
        lines.append('  </p>')
        lines.append('</li>')
        card_html_list.append("\n".join(lines))

    return "\n".join(card_html_list)


def create_html_file(content: str, template_path: str, output_path: str) -> None:
    """
    Reads an HTML template, injects content, and writes it to a new HTML file.

    Args:
        content: The HTML content string to inject into the template.
        template_path: The path to the HTML template file.
        output_path: The path where the final HTML file will be saved.
    """
    try:
        with open(template_path, 'r', encoding='utf-8') as f:
            template = f.read()

        final_html = template.replace('__REPLACE_ANIMALS_INFO__', content)

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(final_html)
        logging.info(f"Successfully created HTML file at: {output_path}")

    except FileNotFoundError:
        logging.error(f"Template file not found at: {template_path}")
    except Exception as e:
        logging.error(f"An error occurred during HTML file creation: {e}")


if __name__ == "__main__":
    JSON_FILE = 'animals_data.json'
    TEMPLATE_FILE = 'animals_template.html'
    OUTPUT_FILE = 'animals.html'

    all_animals_data = load_data(JSON_FILE)

    if all_animals_data:
        animal_cards_content = generate_animal_cards_html(all_animals_data)
        if animal_cards_content:
            create_html_file(animal_cards_content, TEMPLATE_FILE, OUTPUT_FILE)