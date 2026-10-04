import urllib.request
import json
import pandas as pd
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

urls = [
    "https://raw.githubusercontent.com/joshuaswords/US-Superstore-Sales-Analysis/main/Sample%20-%20Superstore.csv",
    "https://raw.githubusercontent.com/datasets/sample-superstore/master/SampleSuperstore.csv",
    "https://raw.githubusercontent.com/mochen862/power-bi-portfolio-project/master/Sample%20-%20Superstore.csv",
    "https://raw.githubusercontent.com/amankharwal/Website-data/master/Sample%20-%20Superstore.csv",
    "https://raw.githubusercontent.com/yungshun317/superstore-sales-analysis/master/Sample%20-%20Superstore.csv",
    "https://raw.githubusercontent.com/harisawan27/US-Superstore-Analysis-in-Excel/main/Sample%20-%20Superstore.csv",
    "https://raw.githubusercontent.com/kirenz/datasets/master/sample_superstore.csv",
    "https://raw.githubusercontent.com/plotly/datasets/master/superstore.csv"
]

dest = r"D:\Downloads\retail-business-intelligence\data\raw\superstore_raw.csv"

success = False
for url in urls:
    try:
        print(f"Trying: {url}")
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, context=ctx) as resp, open(dest, 'wb') as out_file:
            out_file.write(resp.read())
        
        df = pd.read_csv(dest, encoding='latin1')
        print(f"Loaded successfully! Shape: {df.shape}")
        print("Columns:", df.columns.tolist())
        if df.shape[0] >= 9000 and "Order ID" in df.columns:
            print(">>> VERIFIED AUTHENTIC SUPERSTORE DATASET FOUND! <<<")
            success = True
            break
    except Exception as e:
        print(f"Failed: {e}")

if not success:
    # Try GitHub search API
    print("Trying GitHub Search API...")
    search_url = "https://api.github.com/search/code?q=filename:Sample+-+Superstore.csv+extension:csv"
    req = urllib.request.Request(search_url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req, context=ctx) as response:
            data = json.loads(response.read().decode())
            print(f"Found {len(data.get('items', []))} items in search")
            for item in data.get('items', []):
                raw_url = item['html_url'].replace('github.com', 'raw.githubusercontent.com').replace('/blob/', '/')
                print(f"Trying search result: {raw_url}")
                try:
                    req2 = urllib.request.Request(raw_url, headers={'User-Agent': 'Mozilla/5.0'})
                    with urllib.request.urlopen(req2, context=ctx) as r, open(dest, 'wb') as f:
                        f.write(r.read())
                    df = pd.read_csv(dest, encoding='latin1')
                    if df.shape[0] >= 9000 and "Order ID" in df.columns:
                        print(">>> SUCCESS VIA SEARCH API! <<<")
                        print("Shape:", df.shape)
                        print("Columns:", df.columns.tolist())
                        success = True
                        break
                except Exception as err:
                    print("Download item error:", err)
    except Exception as e:
        print("Search API failed:", e)
