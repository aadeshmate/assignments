
import requests
from bs4 import BeautifulSoup
import json


def download_faq(url):
    response = requests.get(
        url,
        headers={"User-Agent": "Python FAQ RAG learning project"},
        timeout=20
    )
    response.raise_for_status()

    soup = BeautifulSoup(response.content, "html.parser")

    all_faqs = []

    # Each FAQ question is an h3 heading
    question_elements = soup.select(
        "div.body section section h3"
    )

    print(question_elements,"\n")

    for heading in question_elements:

        # Extract the question text
        question_link = heading.find("a", class_="toc-backref")

        if not question_link:
            continue

        question = question_link.get_text(strip=True)

        answer_parts = []

        # Read the content following the question heading
        for element in heading.find_next_siblings():

            # Stop if another heading starts
            if element.name in ["h2", "h3"]:
                break

            # Extract answer text from relevant HTML elements
            if element.name in [
                "p", "ul", "ol", "blockquote", "pre", "table"
            ]:
                text = element.get_text(
                    separator=" ",
                    strip=True
                )

                if text:
                    answer_parts.append(text)

        answer = "\n\n".join(answer_parts)

        if answer:
            all_faqs.append({
                "question": question,
                "answer": answer,
                "source": url
            })

    print(f"Extracted {len(all_faqs)} FAQs")

    return all_faqs


if __name__ == "__main__":

    targets_urls = [
        "https://docs.python.org/3/faq/general.html",
        "https://docs.python.org/3/faq/programming.html"
    ]

    all_faqs = []

    for url in targets_urls:
        try:
            faqs = download_faq(url)
            all_faqs.extend(faqs)

        except requests.exceptions.RequestException as e:
            print(f"Failed to fetch {url}: {e}")

    with open("faqs.json", "w", encoding="utf-8") as file:
        json.dump(
            all_faqs,
            file,
            indent=4,
            ensure_ascii=False
        )

    print(f"Saved {len(all_faqs)} FAQs to faqs.json")
