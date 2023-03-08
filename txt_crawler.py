import requests
import json

# set up the URL to retrieve tags from the Docker Hub API

docker_repo = 'nvidia/cuda'
url = f"https://hub.docker.com/v2/repositories/{docker_repo}/tags?page_size=100"

# initialize variables to track the current page and total number of pages
current_page = 1
total_pages = 1

# open a file to write the tag names to
with open('cuda_tags.txt', 'w') as f:

    # loop over all pages of tags
    while current_page <= total_pages:

        # retrieve the current page of tags from the API
        response = requests.get(url + '&page=' + str(current_page))
        data = json.loads(response.content)
        json_str = json.dumps(data)
        # print(json_str)
        #
        # break

        res_obj = data.get('results')
        if res_obj is None:
            break

        # extract the tag names from the current page and write them to the file
        for result in res_obj:
            f.write(result['name'] + '\n')

        # update the variables to move to the next page, if there is one
        current_page += 1
        total_pages = data['count'] // 100 + 1

# print a message to indicate that the script has finished running
print('Done.')