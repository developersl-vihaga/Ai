import requests, argparse, sys
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin
from pprint import pprint
from datetime import datetime
session = requests.Session()
session.headers["User Agent"] = "Mozilla/5.0 (X11; Kali Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
def get_forms(url):
    soup = bs(requests.get(url).content, "html.parser")
    return soup.find_all("form")
def get_form_details(form):
    details = {}
    action = form.attrs.get("action", "").lower()
    method = form.attrs.get("method", "get").lower()
    inputs = []
    for input_tag in form.find_all("input"):
        input_type = input_tag.attrs.get("type", "text")
        input_name = input_tag.attrs.get("name")
        inputs.append({"type": input_type, "name": input_name})
    details["action"] = action
    details["method"] = method
    details["inputs"] = inputs
    return details
def is_vulnerable(response):
    errors = {
        "you have an error in your sql syntax;",
        "warning: mysql",
        "unclosed quotation mark after the character string",
        "quoted string not properly terminated",
        "syntax error",
    }
    for error in errors:
        if error in response.content.decode().lower():
            return True
    return False
def sqli_scan(url):
    for char in "\"'":
        new_url = f"{url}{char}"
        print(f"\n[*] Trying {new_url}\n")
        request = session.get(new_url)
        if is_vulnerable(request):
            print("[!] Potential SQLi vulnerability detected on the URL:")
            print(f"    {new_url}")
            return
    forms = get_forms(url)
    print(f"[*] Detected {len(forms)} forms on {url}")
    for form in forms:
        form_details = get_form_details(form)
        for char in "\"'":
            data = {}
            for input_tag in form_details["inputs"]:
                if input_tag["type"] == "hidden":
                    try:
                        data[input_tag["name"]] = input_tag["value"] + char
                    except:
                        pass
                elif input_tag["type"] != "submit":
                    data[input_tag["name"]] = f"test{char}"
            url = urljoin(url, form_details["action"])
            if form_details["method"] == "post":
                request = session.post(url, data=data)
            elif form_details["method"] == "get":
                request = session.get(url, params=data)
            if is_vulnerable(request):
                print("[!] Potential SQLi vulnerability detected on the page:")
                print(f"    {url}")
                print("[*] Form:")
                pprint(f"    {form_details}")
                break
if __name__ == "__main__":
    if sys.argv[1] == "-u" or sys.argv[1] == "--url":
        parser = argparse.ArgumentParser()
        parser.add_argument("-u", "--url", help="URL to scan for SQLi vulnerabilities")
        args = parser.parse_args()
        url = args.url
        print("\n" + "-"*70)
        print("SQLi Vulnerability scanner")
        print("Time started: " + str(datetime.now()))
        print("-"*70 + "\n")
        sqli_scan(url)
    else: 
        pass
    if sys.argv[1] == "-l" or sys.argv[1] == "--list":
        parser = argparse.ArgumentParser()
        parser.add_argument("-l", "--list", help="List of URL to check for SQLi vulnerabilities")
        args = parser.parse_args()
        urls = open(args.list).read().splitlines()
        print("\n" + "-"*70)
        print("SQLi vulnerability bulk scanner")
        print("Time started: " + str(datetime.now()))
        print("-"*70 + "\n")
        for url in urls:
            sqli_scan(url)
    else:
        sys.exit()