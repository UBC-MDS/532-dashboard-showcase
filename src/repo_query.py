import json
from collections import defaultdict
from pathlib import Path
from getpass import getpass

import github


api_token = getpass('GitHub api token: ')
g = github.Github(api_token)
repos = defaultdict(dict)

# Although we could regex search the beginning of the name,
# it is quicker to just list the repos since the regex search requires looking for matches
# in all repos  in the UBC-MDS organization.
# To find all repos to add, make a search like this:
# https://github.com/orgs/UBC-MDS/repositories?language=&q=DSCI-532_2025&sort=&type=all
repo_names = [
    'DSCI-532_2025_1_cookie-dash',
    'DSCI-532-2025-02-vanparks_finder',
    'DSCI-532_2025_3_QuantaTrack',
    'DSCI-532_2025_4_vdash',
    'DSCI-532_2025_5_vessel-vision',
    'DSCI-532_2025_06_pokemon-dashboard',
    'DSCI-532_2025_7_amazon_marketing',
    'DSCI-532_2025_8_rental-issue-tracker',
    'DSCI-532_2025_9_RetaiLense',
    'DSCI-532_2025_10_hong-kong-tracker',
    'DSCI-532_2025_11_world_happiness',
    'DSCI-532_2025_12_bank-marketing',
    'DSCI-532_2025_13_Maple-Eagle-Trade-Tracker',
    'DSCI-532_2025_14_CAN-US-Trade',
    'DSCI-532_2025_15_RetailPulse',
    'DSCI-532_2025_16_LongevityVisualizer',
    'DSCI-532_2025_17_pharma_spend_dashboard',
    'DSCI-532_2025_18_canadian-house-prices',
    'DSCI-532-2025-19-DataSalaries',
    'DSCI-532_2025_20_spotipy',
    'DSCI-532_2025_21_DS_Salaries',
    'DSCI-532_2025_22_nyc-arrest-tracker',
    'DSCI-532_2025_23_AQI-Dashboard',
    'DSCI-532_2025_24_police_killings',
    'DSCI-532_2025_25_Ads-Analytics',
    'DSCI-532_2025_26_SMBFinder',
    'DSCI-532_2025_27_CA_Wildfire-Dashboard',
    'DSCI-532_2025_28_commuting-insights',
    'DSCI-532_2025_29_e-commerce-dashboard',
    'DSCI-532_2025_30_road-accident-dashboard',
]

def main():
    for repo_name in repo_names:
        repo = g.get_repo('UBC-MDS/' + repo_name)
        repos[repo_name]['repo_url'] = f'https://github.com/UBC-MDS/{repo.name}'
        repos[repo_name]['description'] = repo.description
        repos[repo_name]['deploy_url'] = repo.homepage
        repos[repo_name]['demo_gif_url'] = find_img_path(repo)
        repos[repo_name]['topics'] = clean_topics(repo.get_topics())

    with open('data/repos.json', 'w+') as f:
        json.dump(repos, f, indent=4)


def find_img_path(repo):
    '''Find a gif or image

    Tries a standardizes location first and then searches the repo.
    '''
    print(repo.name)
    base_url = 'https://raw.githubusercontent.com/UBC-MDS/'
    try:
        gif_path = repo.get_contents('img/demo.gif').path
        return f'{base_url}{repo.name}/{repo.default_branch}/{gif_path}'
    # except github.GithubException.UnknownObjectException:
    except github.GithubException:
        print('No gif in standard location, looking elsewhere...')
        # If no gif is found in the standardized location, then search the entire repo for a gif
        contents = repo.get_contents('')
        repo_files = []
        while contents:
            file_content = contents.pop(0)
            if file_content.type == "dir":
                contents.extend(repo.get_contents(file_content.path))
            else:
                repo_files.append(file_content.path)
                pass
        # If many gifs are found in the repo return the first one
        gif_paths = [f for f in repo_files if Path(f.lower()).suffix == '.gif']
        if gif_paths:
            return f'{base_url}{repo.name}/{repo.default_branch}/{gif_paths[0]}'
        else:
            print('No gifs found, looking for images instead...')
            # If no gifs are found search for an image instead.
            # Since there might be unlreated images,
            # guess which might be the dashboard image based on the directory.
            for subdir in ['', 'img', 'imgs', 'images', 'image', 'assets', 'figures', 'doc', 'static/img', 'results/img', 'doc/images', 'data/img', 'report/img']:
                try:
                    contents = repo.get_contents(subdir)
                    file_exts = [Path(x.path.lower()).suffix for x in contents]
                    for img_ext in ['.png', '.jpg']:
                        if img_ext in file_exts:
                            # Gets the first index if there are multilple matches
                            img_path = contents[file_exts.index(img_ext)].path 
                            return f'{base_url}{repo.name}/{repo.default_branch}/{img_path}'
                except github.GithubException:
                    # Gracefuly skip when subdir is not found
                    pass
            print('Could not find a gif or an image, returning a placeholder instead.')
            return 'https://plotly.github.io/images/dash.png'


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
