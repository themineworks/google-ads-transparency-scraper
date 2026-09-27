#!/usr/bin/env python3
"""Every ad a domain runs, from the public Ads Transparency Center. Python, Node.js and cURL clients for the Google Ads Transparency Scraper on Apify, pay per result.

Command-line client for the themineworks/google-ads-transparency actor on Apify: runs it, waits for it
to finish and saves every result as JSON and CSV. Flags map 1:1 to the actor's input.
Free Apify account and API token: https://console.apify.com/sign-up
Docs and pricing: https://themineworks.com/actors/google-ads-transparency/
"""
import argparse, csv, json, os, sys
from apify_client import ApifyClient

ACTOR = "themineworks/google-ads-transparency"


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--token", default=os.environ.get("APIFY_TOKEN"), help="Apify API token (or set APIFY_TOKEN)")
    ap.add_argument("--out", default="results", help="Output basename, writes .json and .csv")
    ap.add_argument("--domains", help="Comma-separated. Website domains to look up, for example ['nike.com', 'adidas.com']")
    ap.add_argument("--region", help="Country to scope the ad archive to")
    ap.add_argument("--max-ads-per-domain", type=int, help="Cap per domain")
    a = ap.parse_args()
    if not a.token:
        sys.exit("Provide --token or set APIFY_TOKEN. Free token: https://console.apify.com/sign-up")

    run_input = {}
    if a.domains: run_input["domains"] = [s.strip() for s in a.domains.split(",") if s.strip()]
    if a.region is not None: run_input["region"] = a.region
    if a.max_ads_per_domain is not None: run_input["maxAdsPerDomain"] = a.max_ads_per_domain

    client = ApifyClient(a.token)
    print(f"Running {ACTOR} ...")
    run = client.actor(ACTOR).call(run_input=run_input)
    items = list(client.dataset(run["defaultDatasetId"]).iterate_items())

    with open(a.out + ".json", "w", encoding="utf-8") as f:
        json.dump(items, f, indent=2, ensure_ascii=False)
    keys = []
    for it in items:
        keys += [k for k in it if k not in keys]
    if items:
        with open(a.out + ".csv", "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=keys, extrasaction="ignore")
            w.writeheader()
            for it in items:
                w.writerow({k: json.dumps(v, ensure_ascii=False) if isinstance(v, (list, dict)) else v for k, v in it.items()})
    print(f"Done: {len(items)} results saved to {a.out}.json and {a.out}.csv")


if __name__ == "__main__":
    main()
