"""Route evaluation for Slay the Spire map paths."""

import re
from typing import List, Dict, Tuple, Optional
from .text_extractor import read_window
from .command_executor import execute_command_sequence


def evaluate_all_routes(top_n: int = 10) -> List[Dict]:
    """
    Evaluate all possible routes to floor 15 rest sites.
    
    Returns a list of the top N routes with their scores and details.
    """
    # Read the map window
    map_content = read_window("Map")
    if map_content['error']:
        return [{'error': f"Failed to read Map window: {map_content['error']}"}]
    
    # Find all floor 15 rest sites
    rest_sites = parse_map_window(map_content['content'])
    if not rest_sites:
        return [{'error': 'No floor 15 rest sites found'}]
    
    # Collect all routes
    all_routes = []
    for x_coord in rest_sites:
        routes = get_routes_to_rest_site(x_coord)
        all_routes.extend(routes)
    
    # Score and sort routes
    scored_routes = []
    for route in all_routes:
        score = score_route(route['encounter_counts'])
        scored_routes.append({
            'score': score,
            'summary': route['summary'],
            'detail': route['detail'],
            'encounter_counts': route['encounter_counts'],
            'destination': route['destination']
        })
    
    # Sort by score descending
    scored_routes.sort(key=lambda x: x['score'], reverse=True)
    
    # Remove duplicates based on summary
    seen_summaries = set()
    unique_routes = []
    for route in scored_routes:
        if route['summary'] not in seen_summaries:
            seen_summaries.add(route['summary'])
            unique_routes.append(route)
    
    # Return top N
    return unique_routes[:top_n]


def parse_map_window(map_content: str) -> List[int]:
    """
    Parse the Map window content to find all floor 15 rest sites.
    Returns list of X coordinates.
    """
    rest_sites = []
    pattern = r'Rest Floor:15 X:(\d+)'
    
    for line in map_content.split('\n'):
        match = re.match(pattern, line.strip())
        if match:
            x_coord = int(match.group(1))
            rest_sites.append(x_coord)
    
    return rest_sites


def get_routes_to_rest_site(x_coord: int) -> List[Dict]:
    """
    Execute path command for a rest site and parse the output.
    Returns list of route dictionaries.
    """
    # Execute path command
    command = f"path 15 {x_coord}"
    results = execute_command_sequence([command], verify=True, timeout=5.0)
    
    if not results or not results[0]['success']:
        return []
    
    # Read the Output window
    output_content = read_window("Output")
    if output_content['error']:
        return []
    
    # Parse the routes from output
    return parse_path_output(output_content['content'], x_coord)


def parse_path_output(output_content: str, destination_x: int) -> List[Dict]:
    """
    Parse the path command output to extract routes.
    Returns list of route dictionaries with encounter counts.
    """
    routes = []
    lines = output_content.strip().split('\n')
    
    # Look for pairs of lines (summary, detail)
    i = 0
    while i < len(lines) - 1:
        line = lines[i].strip()
        
        # Skip lines that don't look like route summaries
        if not any(word in line for word in ['Elite', 'Monster', 'Rest', 'Shop', 'Unknown', 'Treasure', 'Emerald']):
            i += 1
            continue
        
        # Check if this looks like a summary line (has comma-separated encounters)
        if ',' in line and i + 1 < len(lines):
            summary_line = line
            detail_line = lines[i + 1].strip()
            
            # Verify detail line has the expected format (contains Floor)
            if 'Floor' in detail_line or re.search(r'\w+ \d+ \d+', detail_line):
                encounter_counts = parse_route_info(summary_line)
                routes.append({
                    'summary': summary_line,
                    'detail': detail_line,
                    'encounter_counts': encounter_counts,
                    'destination': f"15:{destination_x}"
                })
                i += 2
                continue
        
        i += 1
    
    return routes


def parse_route_info(route_line: str) -> Dict[str, int]:
    """
    Parse a route summary line to extract encounter counts.
    Example: "Elite 2, Rest 2, Unknown 1, Monster 9,"
    """
    encounter_counts = {
        'Elite': 0,
        'Emerald': 0,
        'Rest': 0,
        'Shop': 0,
        'Unknown': 0,
        'Monster': 0,
        'Treasure': 0,
    }
    
    # Split by comma and parse each encounter
    encounters = route_line.strip().rstrip(',').split(',')
    for encounter in encounters:
        encounter = encounter.strip()
        
        # Handle special case where Emerald might not have a count
        if encounter == 'Emerald':
            encounter = 'Emerald 1'
        
        # Parse encounter type and count
        match = re.match(r'(\w+)\s+(\d+)', encounter)
        if match:
            encounter_type, count = match.groups()
            if encounter_type in encounter_counts:
                encounter_counts[encounter_type] = int(count)
    
    return encounter_counts


def score_route(encounter_counts: Dict[str, int]) -> int:
    """
    Calculate the score for a route based on encounter counts.
    Formula: Elite×3 + Emerald×3 + Rest×2 + Shop×1 + Monster×1 - Unknown×1
    """
    return (encounter_counts['Elite'] * 3 +
            encounter_counts['Emerald'] * 3 +
            encounter_counts['Rest'] * 2 +
            encounter_counts['Shop'] * 1 +
            encounter_counts['Monster'] * 1 -
            encounter_counts['Unknown'] * 1)