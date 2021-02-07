import json
import random
from collections import Counter

import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output


# Load repo data
with open('repos.json', 'r') as f:
    data=f.read()
repos = json.loads(data)
# The icon is grabbed for this group by default
repos['dsci-532_group08']['image_url'] = 'https://raw.githubusercontent.com/UBC-MDS/dsci-532_group08/main/img/dashboard_screenshot2.png'

flat_topic_list = [i for repo in repos for i in repos[repo]['topics']]
topics_with_counts = dict(sorted(Counter(flat_topic_list).items(), key=lambda item: item[1], reverse=True))
dropdown_options = [
    {'label': f'{topic} ({str(topics_with_counts[topic])})', 'value': topic}
    for topic in topics_with_counts]
# unique_topics = {i for repo in repos for i in repos[repo]['topics']}

title = 'Dashboard Showcase'
app = dash.Dash(
    __name__, title=title,
    external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container([
        dbc.Row([
            dbc.Col([
                dbc.Jumbotron([
                    html.H1(
                        title,
                        className='display-2',
                        style={'text-align': 'center', 'color': 'white'}),
                    html.Hr(className="my-2", style={'background-color': 'white', 'width': '700px'}),
                    html.P(
                        "Click a dashboard to view it on heroku. Use the dropdown to filter tags.",
                        className="lead",
                        style={'text-align': 'center', 'color': 'white'}),
                ],
                    style={'background-color': '#0d1d41',
                        'font-family': 'Ubuntu',
                        'width': '100vw',
                        'margin-left': '-63px',
                        'border-radius': '0px',
                        'padding': '20px'})])]),
        dbc.Row([
            dbc.Col([
                dcc.Dropdown(id='topic-dropdown', multi=True, options=dropdown_options,
                    placeholder='Click to select tags. The (number) is the count.',
                    style={
                        'font-family': 'Ubuntu',
                        'border-width': '0px',
                        'box-shadow': '0px',
                        'font-size': '18px'})],
                md=4)],
            justify='center'),
        html.Br(),
        dbc.Row(id='thumbnails-row'),
        html.Br(),
        html.Hr(style={'width': '50%', 'margin-left': '0px'}),
        html.P(['''
        This dashboard shows off the impressive dasboards created by students during a 4-week course in Dash for MDS DSCI-532 at UBC.
        The displayed dashboards are filtered by the intersection (AND) of the selected tags.
        The count for each tag is updated when filtering to reflect only the visible dashboards.
        This dash board looks best in a full width window and ''',
        html.A('the source can be found on GitHub.', href='https://github.com/UBC-MDS/532-dashboard-showcase')],
        style={'font-size': '14px', 'width': '50%'})],
    style={'max-width': '95%'})

@app.callback(
    Output('thumbnails-row', 'children'),
    Output('topic-dropdown', 'options'),
    Input("topic-dropdown", "value"))
def update_thumbnails(selected_topics):
    if selected_topics:
        # Return repos that match all selected topics 
        matched_repo_names = [
            repo for repo in repos
                if all(topic in repos[repo]['topics'] for topic in selected_topics)]
    else:
        # Return all repos if no topics are selected
        matched_repo_names = list(repos.keys())
        
    # Update dropdown dynamically to count tags in the visible dashboards only
    flat_topic_list = [i for repo in repos for i in repos[repo]['topics'] if repo in matched_repo_names]
    topics_with_counts = dict(sorted(Counter(flat_topic_list).items(), key=lambda item: item[1], reverse=True))
    dropdown_options = [
        {'label': f'{topic} ({str(topics_with_counts[topic])})', 'value': topic}
        for topic in topics_with_counts]
        
    # Create one image thumbnail and one hover overlay per matched repo
    images = [
        html.A(
            html.Div([
                html.Img(
                    src=repos[repo]['image_url'],
                    alt=repos[repo]['homepage'],
                    className='image'),
                html.Div(
                    html.Div([
                        html.H3(repo),
                        html.P(repos[repo]['description'], style={'font-size': '15px'})],
                        className='text'),
                    className='overlay')],
                className='container-hover'),
            href=repos[repo]['homepage'])
        for repo in matched_repo_names]
    
    # Randomize which dashboards are shown on top
    random.shuffle(images)
    # Layout images in three columns
    if len(images) == 1:
        print(1)
        return [[dbc.Col(images[0]), dbc.Col([]), dbc.Col([])], dropdown_options]
    if len(images) == 2:
        print(2)
        return [[dbc.Col(images[0]), dbc.Col(images[1]), dbc.Col([])], dropdown_options] 
    first_col_len = -(-len(images) // 3)  # Ceiling division
    second_col_len = (len(images) - first_col_len) // 2
    return [[dbc.Col(images[:first_col_len]),
                dbc.Col(images[first_col_len:-second_col_len]),
                dbc.Col(images[-second_col_len:])],
            dropdown_options]

if __name__ == '__main__':
    app.run_server(debug=True)