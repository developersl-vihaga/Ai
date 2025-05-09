import requests, argparse, sys
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
internal_urls = set()
external_urls = set()
def is_valid(url):
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)
def get_links(url):
    urls = set()
    domain_name = urlparse(url).netloc
    soup = BeautifulSoup(requests.get(url).content, "html.parser")
    for tag in soup.findAll("a"):
        href = tag.attrs.get("href")
        if href == "" or href is None:
            continue
        href = urljoin(url, href)
        parsed_href = urlparse(href)
        href = parsed_href.scheme + "://" + parsed_href.netloc + parsed_href.path
        if not is_valid(href):
            continue
        if href in internal_urls:
            continue
        if domain_name not in href:
            if href not in external_urls:
                print(f"[!] EXTERNAL URL ···>  {href}")
                external_urls.add(href)
            continue
        print(f"[+] INTERNAL URL ···>  {href}")
        urls.add(href)
        internal_urls.add(href)
    return urls
def crawl(url, max_urls):
    total_urls_visited = 0
    total_urls_visited += 1
    print(f"[*] CRAWLING ···>  {url}")
    links = get_links(url)
    for link in links:
        if total_urls_visited > int(max_urls):
            break
        crawl(link, max_urls=max_urls)
if __name__ == "__main__":
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument("-u", "--url", help="URL to crawl")
        parser.add_argument("-m", "--max", help="Maximum URLs to extract")
        parser.add_argument("-o", "--output", nargs="?")
        args = parser.parse_args()
        url = args.url
        max_urls = args.max
        output_file = args.output
        crawl(url, max_urls)
        if output_file:
                with open(output_file, "w") as f:
                    for url in internal_urls:
                        if "http" in url:
                            print(url, file=f)
                        else:
                            pass
        print("\n" + "-"*45)
        print("[*] TOTAL INTERNAL LINKS: ", len(internal_urls))
        print("[*] TOTAL EXTERNAL LINKS: ", len(external_urls))
        print("[*] TOTAL URLs: ", len(external_urls) + len(internal_urls))
        print("[*] TOTAL CRAWLED URLs: ", len(max_urls))
        print("-"*45)
    except KeyboardInterrupt:
        if output_file:
                with open(output_file, "w") as f:
                    for url in internal_urls:
                        if "http" in url:
                            print(url, file=f)
                        else:
                            pass
        print("\nAborting link extraction...")