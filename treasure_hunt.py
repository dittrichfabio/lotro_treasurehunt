import os
import json
import click
from definitions import *
from plotting import plot_on_map
from utils import deduplicate, extract_loc_data, load_digsites
from find_best_locations import find_best_locations_simple, find_best_locations_greedy


@click.group()
def cli():
    pass

@cli.command()
def extract():
    chat_log_file = "General_20250719_1.txt"
    raw_locations = extract_loc_data(chat_log_file)
    unique_locations = deduplicate(raw_locations)
    digsites = sorted(unique_locations, key=lambda d: (-d['world_y'], d['world_x']))
    for i, digsite in enumerate(digsites, start=1):
        digsite['id'] = str(i)

    with open(DIGSITE_LOCATIONS_FILE, 'w', encoding='utf-8') as f:
        json.dump(digsites, f, indent=2)
        
    print(f"Extracted {len(digsites)} unique locations from {chat_log_file}")
    print(f"Saved to: {DIGSITE_LOCATIONS_FILE}")

@cli.command()
def plot():
    digsite_locations = load_digsites(DIGSITE_LOCATIONS_FILE)
    digsites_image_file = os.path.join(OUTPUT_IMAGE_DIR, "TreasureHuntMap_Digsites.png")

    plot_on_map(
        digsites=digsite_locations,
        image_path=BACKGROUND_IMAGE_FILE,
        output_image_path=digsites_image_file,
        title=f"Treasure Field Dig-sites",
        show_labels=True,
        show_radius=True,
        radius=CAVECLAW_RADIUS
    )

    print(f"Saved plot to: {digsites_image_file}")

@cli.command()
@click.option('--top_n', default=5, help='Path to the map image.')
@click.option('--search_type', type=click.Choice(BEST_LOCATIONS_SEARCH_TYPES), default="simple", help='Path to the map image.')
@click.option('--grid_step', default=5, help='Path to the map image.')
def best_locations(top_n, search_type, grid_step):
    digsite_locations = load_digsites(DIGSITE_LOCATIONS_FILE)
    best_spots_image_file = os.path.join(OUTPUT_IMAGE_DIR, f"TreasureHuntMap_BestSpots_{search_type}Search.png")

    if search_type == "Simple":
        best_spots = find_best_locations_simple(digsite_locations, top_n=top_n, grid_step=grid_step)
    elif search_type == "Greedy":
        best_spots = find_best_locations_greedy(digsite_locations, top_n=top_n, grid_step=grid_step)

    print("Top locations:")
    for i, (count, x, y, _) in enumerate(best_spots, 1):
        print(f"{i}. ({x:.2f}, {y:.2f}) - covers {count} sites")

    plot_on_map(
        digsites=digsite_locations,
        image_path=BACKGROUND_IMAGE_FILE,
        output_image_path=best_spots_image_file,
        title=f"Treasure Field Best Locations {search_type} Search",
        show_labels=True,
        show_radius=True,
        radius=CAVECLAW_RADIUS,
        best_spots=best_spots
    )
    print(f"Saved plot to: {best_spots_image_file}")

if __name__ == "__main__":
    cli()

