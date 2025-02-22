import requests
from bs4 import BeautifulSoup
from transformers import pipeline

TF_ENABLE_ONEDNN_OPTS = 0
# Initialize the summarization pipeline
summarizer = pipeline("summarization")


def google_search(query):
    # Perform a Google search
    url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36"
    }

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print("Error retrieving search results.")
        return

    soup = BeautifulSoup(response.text, "html.parser")

    # Extract the first search result
    first_result = soup.find("h3")
    if first_result and first_result.find_parent("a"):
        result_title = first_result.get_text()

        result_link = first_result.find_parent("a")["href"]
        print(f"Title: {result_title}")
        print(f"Link: {result_link}\n")

        # Retrieve content from the result page
        retrieve_content(result_link)
    else:
        print("No results found.")


def retrieve_content(url):
    # Fetch the content of the page
    response = requests.get(url)

    if response.status_code != 200:
        print("Error retrieving page content.")
        return

    soup = BeautifulSoup(response.text, "html.parser")

    # Extract the main content
    paragraphs = soup.find_all("p")
    content = "\n".join(
        [para.get_text() for para in paragraphs[:5]]
    )  # Get the first 5 paragraphs
    print("\n=== Content ===\n")
    print(content)

    # Summarize the content
    summarize_content(content)

    # Extract images
    images = soup.find_all("img")
    print(images)
    print("\n=== Images ===\n")
    # for img in images[:5]:  # Show only the first 5 images
    #     img_url = img["src"]
    #     print(img_url)


def summarize_content(content):
    # Summarize the content using AI
    if len(content) < 100:
        print("\nContent too short to summarize.")
        return

    # Use the summarization model
    summary = summarizer(content, max_length=150, min_length=30, do_sample=False)
    print("\n=== Summary ===\n")
    print(summary[0]["summary_text"])


# Input from user
search_query = input("Enter search term: ")
google_search(search_query)
