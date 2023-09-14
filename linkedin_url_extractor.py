import sys
import time
import pandas as pd
from bs4 import BeautifulSoup
import requests, json, lxml
import random
# Load the Excel file
csv_file_path = './Payment FollowUp Doculens - Data.csv'
data=pd.read_csv(csv_file_path)

output_csv_file="CFOdata-1.csv"
batch_size=100

user_agent_list = [
  'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15',
  'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
  'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
  'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0',
  'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
]


def linkedin_url_extractor(sq):
    params = {
        "q": (" ").join(sq) + " LinkedIn" ,  # query example
        "hl": "en",  # language
    }
    for _ in user_agent_list:
        # Pick a random user agent
        user_agent = random.choice(user_agent_list)
    headers = {
        "User-Agent": user_agent
    }
    html = requests.get("https://www.google.com/search", params=params, headers=headers, timeout=30)
    soup = BeautifulSoup(html.text, 'lxml')
    if html.status_code != 200 :
        sys.exit(1)
    time.sleep(5)
    data =[]
    for result in soup.select(".tF2Cxc"):
        title = result.select_one(".DKV0Md").text
        try:
            snippet = result.select_one(".lEBKkf span").text
        except:
            snippet = None
        links = result.select_one(".yuRUbf a")["href"]

        data.append({
            "title": title,
            "snippet": snippet,
            "links": links
        })
    if len(data)>0:
        print(data[0]['links'])
        return data[0]['links']
    return ""


def process_and_save_batch(batch_df, output_csv_file):
    with open(output_csv_file, 'a') as f:
        for index, row in batch_df.iterrows():
            # Perform your processing on the row here
            sq=[]
            for col in ['First Name','Last Name','EMAIL']:
                if pd.notna(row[col]) and row[col] != "":
                    sq.append(row[col])
            time.sleep(5)
            linkedin_extracted=linkedin_url_extractor(sq)
            time.sleep(5)
            if 'linkedin' in linkedin_extracted:
                row['Linkedin_url'] = linkedin_extracted
            else:
                row['Linkedin_url'] = ""
            f.write(','.join(map(str, row)) + '\n')



for i in range(0, len(data), batch_size):
    batch_df = data.iloc[i : i + batch_size]
    process_and_save_batch(batch_df, output_csv_file)
    print(f"Processed batch {i // batch_size + 1} and saved to {output_csv_file}")
    time.sleep(10)

print("Processing and appending batches completed.")