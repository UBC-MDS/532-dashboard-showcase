import json
from collections import defaultdict
from pathlib import Path
from getpass import getpass

import github


api_token = getpass('GitHub api token: ')
g = github.Github(api_token)
repos = defaultdict(dict)
repo_names = [
    'obesity-explorer-R',
    'dsci-532_group_02',
    'dsci532-group3-R',
    'dsci_532_group_04_R',
    'dash_of_spice-R',
    'MDS_Winery_Dashboard',
    'Movie_Selection',
    'dsci-532_group08',
    'career_deciscion_aid-r',
    'happy-dash',
    '532-group11',
    'DSCI_532_Group_12',
    'DSCI_532_Group13_Crime',
    '532_Dashboard_Project_Group_14',
    'DSCI_532_Group15_wine',
    'DSCI532-Group16-R',
    'DSCI532_Group17',
    'DSCI_532_Group18_Allstars',
    'Mental-Health-in-Tech-Dashboard',
    'dsci-532_group-20',
    '532-Group21',
    '532_Group_22',
    'dsci_532_group23',
    'dsci_532_group_24',
    'mds532_viz_group25',
    'DSCI_532_group26']

def main():
    for repo_name in repo_names:
        repo = g.get_repo('UBC-MDS/' + repo_name)
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
    return topics 

if __name__ == '__main__':
    main()