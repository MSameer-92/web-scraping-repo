# import requests
# import pandas as pd
# from datetime import datetime , timedelta

# url="https://data.cityofnewyork.us/resource/w7w3-xahh.json"

# one_month_ago= (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")

# params={
#     "$where": f"license_creation_date >= '{one_month_ago}'",
#     "$limit": 100,
#     "$order": "license_creation_date DESC"
# }

# response= requests.get(url , params=params)
# if response.status_code == 200:
#     data= response.json()
#     df= pd.DataFrame(data)
#     cols = [
#         "business_name",
#         "business_category",
#         "license_type",
#         "license_status",
#         "license_creation_date",
#         "contact_phone",
#         "address_building",
#         "address_street_name",
#         "address_city",
#         "address_state",
#         "address_zip",
#         "latitude",
#         "longitude"
#     ]
#     df= df[[c for c in cols if c in df.columns]]
#     df.to_csv("recent_business_licenses.csv", index=False)
#     print("Data saved to recent_business_licenses.csv")
# else:
#     print(f"Failed to fetch data. Status code: {response.status_code}")
#     print(response.text)



import requests
import pandas as pd
from datetime import datetime, timedelta

# =====================
# SETTINGS
# =====================
HEADERS = {"User-Agent": "Muhammad Sameer iamsameerai65@gmail.com"}  # ✅ zaruri hai

# Tech/Software SIC codes
SIC_CODES = ["7372", "7371", "7374", "7379"]

one_month_ago = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")

all_companies = []

# =====================
# EDGAR SE DATA LO
# =====================
for sic in SIC_CODES:
    print(f"\n🔍 SIC {sic} search kar raha hai...")

    url = f"https://efts.sec.gov/LATEST/search-index?q=%22software%22&dateRange=custom&startdt={one_month_ago}&enddt={datetime.now().strftime('%Y-%m-%d')}&forms=S-1,10-12B"

    # Company search by SIC
    company_url = f"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&SIC={sic}&dateb=&owner=include&count=40&search_text=&action=getcompany&State=NY&SIC={sic}&myowner=include&action=getcompany"

    resp = requests.get(
        f"https://efts.sec.gov/LATEST/search-index?q=software+house&forms=S-1&dateRange=custom&startdt={one_month_ago}&enddt={datetime.now().strftime('%Y-%m-%d')}",
        headers=HEADERS
    )

    if resp.status_code == 200:
        hits = resp.json().get("hits", {}).get("hits", [])
        print(f"   ✓ {len(hits)} results mile!")

        for hit in hits:
            source = hit.get("_source", {})
            all_companies.append({
                "Company Name"   : source.get("display_names", ["N/A"])[0] if source.get("display_names") else "N/A",
                "Filed Date"     : source.get("file_date", "N/A"),
                "Form Type"      : source.get("form_type", "N/A"),
                "State"          : source.get("inc_states", "N/A"),
                "CIK"            : source.get("entity_id", "N/A"),
                "Category"       : "Software/Tech"
            })
    else:
        print(f"   ❌ Failed: {resp.status_code}")

# =====================
# SAVE TO CSV
# =====================
if all_companies:
    df = pd.DataFrame(all_companies)
    df.drop_duplicates(subset=["Company Name"], inplace=True)
    df.to_csv("ny_tech_companies.csv", index=False, encoding="utf-8-sig")
    print(f"\n✅ {len(df)} tech companies saved → ny_tech_companies.csv")
    print(df.head(10))

    print(f"Before: {len(df)}")
    before = len(df)
    df.drop_duplicates(subset=["Company Name"], inplace=True)
    print(f"After : {len(df)}")
    print(f"Removed: {before - len(df)}")
else:
    print("⚠ Koi data nahi mila!")