import json
from collections import defaultdict
from pathlib import Path
from getpass import getpass

import github


api_token = getpass('GitHub api token: ')
g = github.Github(api_token)
repos = defaultdict(dict)
repo_names = [
    'DSCI-532_2024_1_TBtracker',
    'DSCI-532_2024_2_pollution-tracker',
    'DSCI-532_2024_3_world-happiness-tracker',
    'DSCI-532_2024_4_crime-tracker',
    'DSCI-532_2024_5_HomeScope',
    'DSCI-532_2024_6_Green-Development-Planner',
    'DSCI-532_2024_7_ds-compensation',
    'DSCI-532_2024_8_DriveDeepDive',
    'DSCI-532_2024_9_solar-savers',
    'DSCI-532_2024_10_vanweather',
    'DSCI-532_2024_11_spotify-popularity',
    'DSCI-532_2024_12_bigmac',
    'DSCI-532_2024_13_Juno',
    'DSCI-532_2024_14_mds_saves_america',
    'DSCI-532_2024_15_dreamhouse',
    'DSCI-532_2024_16_SilentEpidemic',
    'DSCI-532_2024_17_Global-CO2-Emissions-Tracker',
    'DSCI-532_2024_18_VancouverAirbnbPrices',
    'DSCI-532_2024_19_food-price-tracker',
    'DSCI-532_2024_20_hotspot',
    'DSCI-532_2024_21_Job-Postings',
    'DSCI-532_2024_22_flightfinder',
]

def main():
    for repo_name in repo_names:
        repo = g.get_repo('UBC-MDS/' + repo_name)
        repos[repo_name]['repo_url'] = f'https://github.com/UBC-MDS/{repo.name}'
        repos[repo_name]['description'] = repo.description
        repos[repo_name]['homepage'] = repo.homepage
        repos[repo_name]['image_url'] = find_img_path(repo)
        repos[repo_name]['topics'] = clean_topics(repo.get_topics())

    with open('repos.json', 'w+') as f:
        json.dump(repos, f, indent=4)
 

def find_img_path(repo):
    '''Find a gif or image, I should have standardized the naming for this...'''
    print(repo.name)
    # Search the entire repo for a gif
    contents = repo.get_contents('')
    repo_files = []
    while contents:
        file_content = contents.pop(0)
        if file_content.type == "dir":
            contents.extend(repo.get_contents(file_content.path))
        else:
            repo_files.append(file_content.path)
            pass
    # If any gifs are found in the repo return the first one
    gif_paths = [f for f in repo_files if Path(f.lower()).suffix == '.gif']
    if gif_paths:
        return f'https://raw.githubusercontent.com/UBC-MDS/{repo.name}/{repo.default_branch}/{gif_paths[0]}'
        
    # If no gifs are found search for an image instead.
    # Since there might be unlreated images,
    # guess which might be the dashboard image based on the directory.
    for subdir in ['', 'img', 'imgs', 'images', 'image', 'assets', 'figures', 'doc', 'static/img', 'results/img', 'doc/images']:
        try:
            contents = repo.get_contents(subdir)
            file_exts = [Path(x.path.lower()).suffix for x in contents]
            for img_ext in ['.png', '.jpg']:
                if img_ext in file_exts:
                    # Gets the first index if there are multilple matches
                    img_path = contents[file_exts.index(img_ext)].path 
                    return f'https://raw.githubusercontent.com/UBC-MDS/{repo.name}/{repo.default_branch}/{img_path}'
        except github.GithubException:
            # Gracefuly skip when subdir is not found
            pass
    print('Could not find an image, returning a placeholder instead.')
    return 'https://www.probytes.net/wp-content/uploads/2018/10/dash-logo-300.png'


def clean_topics(topics):
    if 'sliders' in topics:
        topics[topics.index('sliders')] = 'slider'
    if 'range-slider' in topics:
        topics.append('slider')
    if 'slider-range' in topics:
        topics[topics.index('slider-range')] = 'range-slider'
        topics.append('slider')
    if 'radio-buttons' in topics:
        topics[topics.index('radio-buttons')] = 'radiobutton'
    if 'radiobuttons' in topics:
        topics[topics.index('radiobuttons')] = 'radiobutton'
    if 'leaflet' in topics:
        topics.append('map')
    if 'chloropleth' in topics:
        topics[topics.index('chloropleth')] = 'choropleth'
    if 'world-map' in topics:
        topics[topics.index('world-map')] = 'map'
    if 'bar-charts' in topics:
        topics[topics.index('bar-charts')] = 'barplot'
    if 'barplots' in topics:
        topics[topics.index('barplots')] = 'barplot'
    if 'scatter-plot' in topics:
        topics[topics.index('scatter-plot')] = 'scatterplot'
    if 'line-chart' in topics:
        topics[topics.index('line-chart')] = 'lineplot'
    if 'linechart' in topics:
        topics[topics.index('linechart')] = 'lineplot'
    if 'plotly-python' in topics:
        topics[topics.index('plotly-python')] = 'plotly'
    if 'dash' in topics:
        topics.remove('dash')
    if 'plotly-dash' in topics:
        topics.remove('plotly-dash')
    if 'plotly-dash' in topics:
        topics.remove('plotly-dash')
    if 'dashboard' in topics:
        topics.remove('dashboard')
    if 'data-science' in topics:
        topics.remove('data-science')
    if 'data-visualization' in topics:
        topics.remove('data-visualization')
    if 'data-analysis' in topics:
        topics.remove('data-analysis')
    return topics 

if __name__ == '__main__':
    main()