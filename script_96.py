import requests, argparse,sys, os
from pprint import pprint
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin
from datetime import datetime
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
def form_submit(form_details, url, value):
    target_url = urljoin(url, form_details["action"])
    inputs = form_details["inputs"]
    data = {}
    for input in inputs:
        if input["type"] == "text" or input["type"] == "search":
            input["value"] = value
        input_name = input.get("name")
        input_value = input.get("value")
        if input_name and input_value:
            data[input_name] = input_value
    print(f"[*] Submitting malicious payload to {target_url}")
    print(f"[*] Data: {data}")
    if form_details["method"] == "post":
        return requests.post(target_url, data=data)
    else:
        return requests.get(target_url, params=data)
def xss_scan(url):
    forms = get_forms(url)
    print(f"[*] Detected {len(forms)} forms on {url}")
    js_payload = "<script>alert('hi')</script>"
    is_vulnerable = False
    for form in forms:
        form_details = get_form_details(form)
        content = form_submit(form_details, url, js_payload).content.decode()
        if js_payload in content:
            print(f"[!] XSS Vulnerability detected on {url}")
            print(f"[*] Form details:")
            pprint(form_details)
            is_vulnerable = True
    return is_vulnerable
if __name__ == "__main__":
    if sys.argv[1] == "-u" or sys.argv[1] == "--url":
        parser = argparse.ArgumentParser()
        parser.add_argument("-u", "--url", help="URL to check for XSS vulnerabilities")
        args = parser.parse_args()
        url = args.url
        print("\n" + "-"*70)
        print("XSS Vulnerability scanner")
        print("Time started: " + str(datetime.now()))
        print("-"*70 + "\n")
        if xss_scan(url) == True:
            print("\n[!] " + url + " is vulnerable to XSS")
            print("-"*70 + "\n")
        else:
            print("\n[!] " + url + " is NOT vulnerable to XSS")
            print("-"*70 + "\n")
    else:
        pass
    if sys.argv[1] == "-l" or sys.argv[1] == "--list":
        parser = argparse.ArgumentParser()
        parser.add_argument("-l", "--list", help="List of URL to check for XSS vulnerabilities")
        args = parser.parse_args()
        urls = open(args.list).read().splitlines()
        print("\n" + "-"*70)
        print("XSS Vulnerability bulk scanner")
        print("Time started: " + str(datetime.now()))
        print("-"*70 + "\n")
        for url in urls:
            if xss_scan(url) == True:
                print("\n[!] " + url + " is vulnerable to XSS")
                print("-"*70 + "\n")
            else:
                print("\n[!] " + url + " is NOT vulnerable to XSS")
                print("-"*70 + "\n")
    else:
        sys.exit()