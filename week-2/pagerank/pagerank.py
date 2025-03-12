import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(link for link in pages[filename] if link in pages)

    return pages


def corpus_key(corpus: dict[str, set], i: int):
    """Returns an specific corpus page by its index"""
    return tuple(corpus.keys())[i]


def transition_model(corpus: dict[str, set], page: str, damping_factor: float):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """

    # Checks whether other pages links this page
    page_is_linked = False
    for links in corpus.values():
        if page in links:
            page_is_linked = True
            break

    # If the page is not linked or damping factor is over the threshold then a return a random page from the entire corpus
    if random.random() > damping_factor or not page_is_linked:
        return corpus_key(corpus, random.randint(0, len(corpus) - 1))

    # We return a random page linked from the current page
    return list(corpus[page])[random.randint(0, len(corpus[page]) - 1)]


def sample_pagerank(corpus: dict[str, set], damping_factor: float, n: int):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    remaining_samples = n
    current_page = corpus_key(corpus, random.randint(0, len(corpus) - 1))

    # Initialize the dictionary to store the page rank values
    pagerank = {}
    for page in corpus.keys():
        pagerank[page] = 0

    while remaining_samples:
        remaining_samples -= 1

        # Calculates next page from current page
        current_page = transition_model(corpus, current_page, damping_factor)
        pagerank[current_page] += 1 / n

    return pagerank


def iterate_pagerank(corpus: dict[str, set], damping_factor: float):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    pagerank = {}

    # Initialize the dictionary to store the page rank values
    for page in corpus.keys():
        pagerank[page] = 1 / len(corpus)

    def probability(page: str):
        return ((1 - damping_factor) / len(corpus)) + damping_factor * sum(
            set(
                # Current page probability / number of links
                pagerank[i] / len(corpus[i])
                for i in corpus.keys()
                if page in corpus[i]
            )
        )
    
    # Previous probability for first page
    prev = 0

    # We balance each page probability until convergence
    while abs(prev - pagerank[corpus_key(corpus, 0)]) > 0.001:
        prev = pagerank[corpus_key(corpus, 0)]
        for page in corpus:
            pagerank[page] = probability(page)

    return pagerank

if __name__ == "__main__":
    main()
