from definitions import *
from utils import game_position

import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import matplotlib.patheffects as path_effects

def plot_on_map(digsites, image_path, output_image_path, title, show_labels=True, show_radius=True, radius=CAVECLAW_RADIUS, best_spots=None):
    digsites = digsites.copy()

    img = mpimg.imread(image_path)
    x_min, x_max = MAP_BOUNDS['x_min'], MAP_BOUNDS['x_max']
    y_min, y_max = MAP_BOUNDS['y_min'], MAP_BOUNDS['y_max']

    plt.figure(figsize=(10, 10))

    # Plot the image using extent to align it to world coordinates
    plt.imshow(img, extent=[x_min, x_max, y_min, y_max], origin='upper')

    

    # Plot best spots if provided
    if best_spots:
        for i, (count, bx, by, covered_sites) in enumerate(best_spots):
            color = BEST_POINT_COLORS[i % len(BEST_POINT_COLORS)]
            x = [entry['world_x'] for entry in covered_sites]
            y = [entry['world_y'] for entry in covered_sites]
            digsites = [ds for ds in digsites if ds not in covered_sites]

            plt.scatter(x, y, c=color, edgecolor='black', s=100, label='Dig-site')
            if show_labels:
                for entry in covered_sites:
                    plt.text(entry['world_x'], entry['world_y'], entry['id'], fontsize=4, color='black', ha='center', va='center')

            plt.plot(bx, by, '+', markersize=12, markeredgewidth=2, color=color, label=f'Best Spot {i+1}: {count} Dig-sites ({game_position(world_x=bx, world_y=by)})')
            if show_radius:
                circle = plt.Circle(
                    (bx, by),
                    radius,
                    color='yellow',
                    fill=False,
                    linestyle='--',
                    alpha=0.4
                )
                plt.gca().add_patch(circle)
            if show_labels:
                text = plt.text(bx, by + 2, f'B{i+1}', fontsize=8, color=color, ha='center', va='center')
                text.set_path_effects([
                    path_effects.Stroke(linewidth=1, foreground="black"),  # the "edge"
                    path_effects.Normal()  # the original text
                ])

    # Plot remaining digsites
    x = [entry['world_x'] for entry in digsites]
    y = [entry['world_y'] for entry in digsites]
    plt.scatter(x, y, c='gold', edgecolor='black', s=100, label='Dig-site')

    if show_labels:
        for entry in digsites:
            plt.text(entry['world_x'], entry['world_y'], entry['id'], fontsize=4, color='black', ha='center', va='center')

    plt.xlabel("World X (meters)")
    plt.ylabel("World Y (meters)")
    plt.title(title)
    plt.grid(False)
    plt.axis('equal')
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)
    plt.tight_layout()
    plt.savefig(output_image_path, dpi=300)
    plt.show(block=True)