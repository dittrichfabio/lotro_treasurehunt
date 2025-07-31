import math
import numpy as np
from definitions import CAVECLAW_RADIUS, MAP_BOUNDS

def find_best_locations_simple(digsites, radius=CAVECLAW_RADIUS, top_n=5, grid_step=1):
    x_min, x_max = MAP_BOUNDS['x_min'], MAP_BOUNDS['x_max']
    y_min, y_max = MAP_BOUNDS['y_min'], MAP_BOUNDS['y_max']

    digsites = digsites.copy()
    best_points = []

    for i, _ in enumerate(range(top_n)):
        print(f"Finding best spot {i+1}. Number of uncovered dig-sites: {len(digsites)}")
        if not digsites:
            break

        best_count = -1
        best_center = None
        best_covered = []

        # Grid search over the map area
        for gx in np.arange(x_min, x_max + 1, grid_step):
            for gy in np.arange(y_min, y_max + 1, grid_step):
                covered = [ds for ds in digsites if math.hypot(ds['world_x'] - gx, ds['world_y'] - gy) <= radius]
                if len(covered) > best_count:
                    best_count = len(covered)
                    best_center = (gx, gy)
                    best_covered = covered

        if best_center:
            best_points.append((best_count, *(int(x) for x in best_center), best_covered))
            digsites = [ds for ds in digsites if ds not in best_covered]

    return best_points


def find_best_locations_greedy(digsites, radius=CAVECLAW_RADIUS, top_n=5, grid_step=1):
    coords = np.array([(entry['world_x'], entry['world_y']) for entry in digsites])
    if len(coords) == 0:
        return []

    x_min, x_max = MAP_BOUNDS['x_min'], MAP_BOUNDS['x_max']
    y_min, y_max = MAP_BOUNDS['y_min'], MAP_BOUNDS['y_max']

    best_total_covered = 0
    best_sequence = []

    # Step 1: Scan grid for all best "first" points
    best_first_spots = []
    max_covered = 0

    x_range = range(int(x_min), int(x_max) + 1, grid_step)
    y_range = range(int(y_min), int(y_max) + 1, grid_step)
    total_points = len(x_range) * len(y_range)
    checked_points = 0

    print("Scanning grid for top first-best locations...")

    for i, x in enumerate(x_range):
        for y in y_range:
            distances = np.linalg.norm(coords - np.array([x, y]), axis=1)
            covered = distances <= radius
            count = np.sum(covered)
            if count > max_covered:
                max_covered = count
                best_first_spots = [((x, y), set(np.where(covered)[0]))]
            elif count == max_covered:
                best_first_spots.append(((x, y), set(np.where(covered)[0])))
            checked_points += 1

        if (i + 1) % 10 == 0 or i == len(x_range) - 1:
            print(f"  Progress: {checked_points}/{total_points} points checked ({100 * checked_points // total_points}%)")

    print(f"Found {len(best_first_spots)} first-best locations (each covering {max_covered} sites).")

    # Step 2: For each best first spot, run greedy exclusion strategy
    print("Evaluating each first-best location for best sequence...")

    best_total_covered = 0
    best_sequence = []

    for idx, (first_spot, first_indices) in enumerate(best_first_spots):
        print(f"  Evaluating sequence {idx + 1}/{len(best_first_spots)}...")
        covered_indices = set(first_indices)
        selected_points = [(*first_spot, covered_indices.copy())]

        for _ in range(top_n - 1):
            best_spot = None
            best_indices = set()
            best_new_covered = 0

            for x in x_range:
                for y in y_range:
                    distances = np.linalg.norm(coords - np.array([x, y]), axis=1)
                    covered = set(np.where(distances <= radius)[0])
                    new_covered = covered - covered_indices
                    if len(new_covered) > best_new_covered:
                        best_new_covered = len(new_covered)
                        best_spot = (x, y, new_covered)
                        best_indices = new_covered

            if best_spot is None:
                break
            selected_points.append(best_spot)
            covered_indices |= best_indices

        # Calculate total coverage for the sequence
        total_coverage = len(covered_indices)
        if total_coverage > best_total_covered:
            best_total_covered = total_coverage
            best_sequence = selected_points

    # Prepare the final result with (count, (x, y)) format
    results = []
    for spot in best_sequence:
        distances = np.linalg.norm(coords - np.array(spot[0:2]), axis=1)
        count = np.sum(distances <= radius)
        results.append((int(count), *spot))

    print(f"Best sequence covers {best_total_covered} unique digsites.")
    return results

