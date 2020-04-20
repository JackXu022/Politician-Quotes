# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

# -*- coding: utf-8 -*-
import json
import os
import requests
# if "pip3 install dotenv" doesn't work try "pip3 install python-dotenv"
from dotenv import load_dotenv
load_dotenv()
'''
This sample makes a call to the Bing Image Search API with a text query and returns relevant images with data.
Documentation: https: // docs.microsoft.com/en-us/azure/cognitive-services/bing-web-search/
'''
def image_search(query):
    # Add your Bing Search V7 subscription key and endpoint to your environment variables.
    subscriptionKey = os.environ["BING_SEARCH_V7_SUBSCRIPTION_KEY"]
    endpoint = os.environ["BING_SEARCH_V7_ENDPOINT"] + "/images/search"

    # Query to search for
    # query = input("input query term: ")

    # Construct a request
    mkt = 'en-US'
    params = {'q': query, 'mkt': mkt}
    headers = {'Ocp-Apim-Subscription-Key': subscriptionKey}

    # Call the API
    try:
        response = requests.get(endpoint, headers=headers, params=params)
        response.raise_for_status()

        # print("\nHeaders:\n")
        # print(response.headers)
        # output the image link:
        return response.json()['value'][0]['contentUrl']
    except Exception as ex:
        raise ex
