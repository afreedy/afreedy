"""Render GitHub's contribution calendar using only standard-library code."""
import json
import os
from pathlib import Path
import urllib.request

query = 'query { user(login:"afreedy") { contributionsCollection { contributionCalendar { totalContributions weeks { contributionDays { date contributionCount weekday } } } } } }'
if os.environ.get('GITHUB_TOKEN'):
    request = urllib.request.Request('https://api.github.com/graphql', data=json.dumps({'query': query}).encode(), headers={'Authorization': 'Bearer '+os.environ['GITHUB_TOKEN'], 'Content-Type': 'application/json', 'User-Agent': 'afreedy-profile'})
    with urllib.request.urlopen(request, timeout=30) as response:
        payload = json.load(response)
else:
    import sys
    payload = json.loads(Path(sys.argv[1]).read_text())
if payload.get('errors'): raise RuntimeError('GitHub contribution query failed')
calendar = payload['data']['user']['contributionsCollection']['contributionCalendar']
weeks = calendar['weeks']
colors = ['#edf0f3', '#ffd1e4', '#ffa0c8', '#f3599c', '#cf1f6b']
svg = ['<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="245" viewBox="0 0 1000 245" role="img" aria-label="GitHub contribution calendar">', '<rect width="1000" height="245" rx="18" fill="#ffffff"/>', '<text x="30" y="40" font-family="Arial,sans-serif" font-size="23" font-weight="700" fill="#14171b">GitHub contributions</text>', f'<text x="970" y="39" text-anchor="end" font-family="Arial,sans-serif" font-size="15" fill="#53606b">{calendar["totalContributions"]:,} GitHub contributions</text>']
for column, week in enumerate(weeks):
    for day in week['contributionDays']:
        count = day['contributionCount']
        level = 0 if count == 0 else 1 if count <= 3 else 2 if count <= 9 else 3 if count <= 19 else 4
        svg.append(f'<rect x="{30+column*17}" y="{65+day["weekday"]*17}" width="13" height="13" rx="3" fill="{colors[level]}"><title>{day["date"]}: {count} contributions</title></rect>')
svg.append('<text x="30" y="215" font-family="Arial,sans-serif" font-size="13" fill="#53606b">GitHub-reported activity • refreshed daily • contribution counts are not a measure of code quality</text></svg>')
Path('assets/contributions.svg').write_text(''.join(svg))
print('Rendered contribution calendar')
