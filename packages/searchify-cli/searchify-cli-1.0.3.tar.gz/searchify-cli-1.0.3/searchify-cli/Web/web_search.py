# It's a commmand line utility for run the search from the command-line.
import requests
import pyperclip
import textwrap
from dotenv import load_dotenv
import os
from pathlib import Path


def paginate_snippet(snippet):
    """Paginate the snippet into lines with a width of 80 characters."""
    snippet_lines = textwrap.wrap(snippet, width=80)
    return snippet_lines


def search(
    query, result_number, include_link, include_title, copy_link, all_results=False
):
    load_dotenv(Path.home() / ".env")
    api_key = os.getenv("API_KEY")
    search_engine_id = os.getenv("SEARCH_ENGINE_ID")
    url = f"https://www.googleapis.com/customsearch/v1?key={api_key}&cx={search_engine_id}&q={query}"

    try:
        print("Searching across web.....\n")
        response = requests.get(url)
        data = response.json()

        if "items" in data:

            results = data["items"]

            if all_results:
                max_results = min(len(results), 10)
                for i in range(max_results):
                    result = results[i]
                    snippet = result["snippet"]
                    link = result["link"]
                    title = result["title"]
                    print(f"Result {i+1}:\n")
                    print(f"Link: {link}\n")
                    print(f"Title: {title}\n")
                    print(f"Snippet: ", end="")
                    snippet_lines = paginate_snippet(snippet)
                    for line in snippet_lines:
                        print(line)
                    print()
                    print("**" * 5)
                    print()
            elif 0 < result_number <= len(results):

                result = results[result_number - 1]
                snippet = result["snippet"]
                link = result["link"]
                title = result["title"]
                print(f"Result {result_number}:")
                if include_link:
                    print(f"Link: {link}")
                    if copy_link:
                        pyperclip.copy(link)
                        print("Link Copied to the clipboard.")
                if include_title:
                    print(f"Title: {title}")
                print(f"Snippet: {snippet}")
            else:
                print(f"Error: Result number {result_number} out of range.")
        else:
            print("No results found.")
    except Exception as e:
        print("Error occurred:", e)
