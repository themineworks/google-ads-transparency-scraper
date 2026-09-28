# Google Ads Transparency Scraper: Advertiser Ad Archive

Pull the ads a domain is running from Google's Ads Transparency Center archive: advertiser identifier and registered name, creative ID and asset URL, creative format, and first/last shown dates. Country-level scoping captures region-specific variations. No login, no API key, no browser automation.

**Run it on Apify:** [apify.com/themineworks/google-ads-transparency](https://apify.com/themineworks/google-ads-transparency)
**Docs, FAQ and pricing:** [themineworks.com/actors/google-ads-transparency](https://themineworks.com/actors/google-ads-transparency/)

**Price:** From $0.36 per 1,000 ads on Apify's higher plans ($0.60 on the free plan), plus a $0.005 start fee per run. Failed and empty results are never charged.

## What it returns

* Advertiser identifier and registered name per ad
* Creative ID, asset URL, and creative format
* First-shown and last-shown dates
* Country-level scoping for region-specific ad variants
* Reads the public archive directly, no login or API key
* Failed lookups are never charged

## Quick start

You need a free [Apify account](https://console.apify.com/sign-up) and its API token (Settings, API & Integrations).

### Python

```bash
pip install apify-client
```

```python
from apify_client import ApifyClient

client = ApifyClient("YOUR_APIFY_TOKEN")
run = client.actor("themineworks/google-ads-transparency").call(run_input={
    "domains": [
        "nike.com"
    ],
    "maxAdsPerDomain": 40
})

for item in client.dataset(run["defaultDatasetId"]).iterate_items():
    print(item)
```

### Node.js

```bash
npm install apify-client
```

```javascript
import { ApifyClient } from 'apify-client';

const client = new ApifyClient({ token: 'YOUR_APIFY_TOKEN' });
const run = await client.actor('themineworks/google-ads-transparency').call({
    "domains": [
        "nike.com"
    ],
    "maxAdsPerDomain": 40
});
const { items } = await client.dataset(run.defaultDatasetId).listItems();
console.log(items);
```

### cURL

One request that runs the actor and returns the results in the response (for runs under 5 minutes):

```bash
curl -X POST "https://api.apify.com/v2/acts/themineworks~google-ads-transparency/run-sync-get-dataset-items?token=YOUR_APIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"domains": ["nike.com"], "maxAdsPerDomain": 40}'
```

### Command line

This repo includes ready-made clients that save results to JSON and CSV:

```bash
python3 google_ads_transparency_scraper.py --token YOUR_APIFY_TOKEN --domains "nike.com" --max-ads-per-domain "40"
node google_ads_transparency_scraper.mjs --token YOUR_APIFY_TOKEN --domains "nike.com" --max-ads-per-domain "40"
```

## Input

| Field | Type | Default | Description |
|---|---|---|---|
| `domains` (required) | array |  | Website domains to look up, for example ["nike.com", "adidas.com"] |
| `region` | string | `"US"` | Country to scope the ad archive to |
| `maxAdsPerDomain` | integer | `100` | Cap per domain |

## Output

One row per result, as JSON, CSV, Excel or through the API.

| Field | Type | Description |
|---|---|---|
| `domain` | string | The domain that was searched |
| `advertiser_id` | string | Google's opaque advertiser ID (AR...) |
| `advertiser_name` | string | Advertiser display name as registered with Google Ads |
| `creative_id` | string | Google's opaque creative/ad ID (CR...) |
| `format` | string | image or interactive |
| `creative_url` | string | Direct URL to the ad image, or the content.js render URL for interactive/responsive ads |
| `first_shown` | string | ISO date this creative was first observed running |
| `last_shown` | string | ISO date this creative was last observed running |
| `scraped_at` | string |  |

## Use it from an AI agent

The actor works as a tool in Claude, Cursor or any MCP client through Apify's MCP server:

```
https://mcp.apify.com/?tools=themineworks/google-ads-transparency
```

## FAQ

### What is the Google Ads Transparency Center?

Google's public archive of ads served through its ad network, searchable by advertiser or by domain. It's the same tool Google makes available to anyone at adstransparency.google.com; this actor reads it as structured data.

### Do I need a Google account or API key?

No. The Ads Transparency Center is public. No login, no API key, and no browser automation is required to read it.

### Can I see how long an ad has been running?

Yes. Each ad record includes first-shown and last-shown timestamps, which is enough to tell an ad someone tested for a week from one that has been running for months.

### Can I compare ads by country?

Yes. Scope a run to a specific country to see the ad variants served in that market, then compare across countries in separate runs.

### What does it cost?

Pay per result: from $0.36 per 1,000 ads on Apify's higher plans, $0.60 on the free plan, plus a $0.005 start fee per run. Nothing is charged when a domain returns no ads.

### Can I export the results to CSV or Excel?

Yes. Every run saves to an Apify dataset you can download as JSON, CSV, Excel or XML, or read through the API. The Python and Node clients in this repo also write the results to local files.

### Can I run it on a schedule?

Yes. Save your input as a task on Apify and attach a schedule, or call the API from your own cron job. Scheduled runs are billed the same way as manual ones.

## Related scrapers

* [B2B Leads Finder](https://themineworks.com/actors/b2b-leads-finder/): Business emails and LinkedIn profiles for target companies
* [LinkedIn Company Scraper](https://themineworks.com/actors/linkedin-company-details/): Company size, industry, website, and followers without login
* [Zillow Rental Listings Scraper](https://themineworks.com/actors/zillow-rental-listings/): Scrape Zillow for-rent listings by city or zip. $1 per 1,000 results

Part of [The Mine Works](https://themineworks.com/): 151 pay-per-result scrapers with no login and no browser setup on your side.

## License

MIT © The Mine Works
