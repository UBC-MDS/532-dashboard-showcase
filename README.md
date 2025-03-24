# Dashboard showcase

To make it easier for students to check out their peer's dashing Dash dashboards from 532.

Each year, perform the following steps to update the dashboard data for the current cohort:

1. Update the student group's repo names in `src/app.py`, there are more details in the comments in that file
2. Run `python src/repo_query.py` to download the latest student data.
3. Run `python src/app.py` to test that the app works as expected locally.
4. Commit the updated `data/repos.json`.
5. Serve the dashboard via `render.com` pointing to the relevant commit for this year that you want deployed.
