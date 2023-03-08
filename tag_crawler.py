import requests
import json
import datetime
import argparse
import pandas as pd

parser = argparse.ArgumentParser()
parser.add_argument('docker_repo', nargs='?', default='nvidia/cuda', type=str)
args = parser.parse_args()

docker_repo = args.docker_repo

# set up the URL to retrieve tags from the Docker Hub API
url = f"https://hub.docker.com/v2/repositories/{docker_repo}/tags?page_size=100"

record = list()

# initialize variables to track the current page and total number of pages
current_page = 1
total_pages = 1

# loop over all pages of tags
while current_page <= total_pages:

    # retrieve the current page of tags from the API
    response = requests.get(url + '&page=' + str(current_page))
    data = json.loads(response.content)
    # json_str = json.dumps(data)

    results = data.get('results')
    if results is None:
        break

    # extract the tag names from the current page and write them to the file
    for res in results:
        tag_name = res['name']
        last_update = res['last_updated']
        last_update_date = datetime.datetime.strptime(last_update, '%Y-%m-%dT%H:%M:%S.%fZ').replace(microsecond=0)
        record.append((tag_name, last_update_date))

    # update the variables to move to the next page, if there is one
    current_page += 1
    total_pages = data['count'] // 100 + 1

    print(f"Finish Page = {current_page}")
    # break

# print a message to indicate that the script has finished running
print('Done.')

main_cols = ['tag', 'last_update']
df = pd.DataFrame(record, columns=main_cols)
cols = ['repo'] + main_cols
df['repo'] = docker_repo
df = df[cols]

df = df.sort_values(by=main_cols, ascending=[True, False]).reset_index(drop=True)
df.to_csv('nvidia_cuda_tags.csv', encoding='utf-8', index=False)
