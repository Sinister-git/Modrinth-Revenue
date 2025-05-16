import requests
import json
import os
from datetime import datetime

API_URL = "https://api.modrinth.com/v3/payout/platform_revenue"
USER_AGENT = "User-Agent': 'yourusername/project_name/version (contact_info)"  # Replace with your information
OUTPUT_DIR = "/your/dir/modrinth"
DATA_FILE = "/your/dir/modrinth/revenue_data.json"

# Function to fetch data from Modrinth API with User-Agent header
def fetch_data():
    headers = {'User-Agent': USER_AGENT}
    response = requests.get(API_URL, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")
        return None

# Function to load or initialize local data
def load_local_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading local data: {e}")
    return {"all_time": 0, "data": []}

# Function to save data to local JSON file
def save_local_data(data):
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"Local data saved to {DATA_FILE}")
    except Exception as e:
        print(f"Error saving local data: {e}")

# Function to merge API data into local data, avoiding duplicates
def update_local_data(api_data):
    local_data = load_local_data()
    api_daily_data = api_data.get("data", [])
    
    # Update total revenue
    local_data["all_time"] = float(api_data.get("all_time", local_data["all_time"]))
    
    # Get existing timestamps in local data
    existing_times = {entry["time"] for entry in local_data["data"]}
    
    # Append new entries not already present
    for entry in api_daily_data:
        if entry["time"] not in existing_times:
            local_data["data"].append(entry)
            existing_times.add(entry["time"])
    
    # Sort data by timestamp descending
    local_data["data"].sort(key=lambda x: x["time"], reverse=True)
    
    save_local_data(local_data)
    return local_data

# Function to generate HTML for a single page
def generate_page_html(total_revenue, page_data, page_num, total_pages):
    html_content = f"""
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Modrinth Revenue Data - Page {page_num}</title>
        <style>
            body {{
                background-color: #262626;
                font-family: Arial, sans-serif;
                color: #FFFFFF;
                text-align: center;
                padding: 20px;
            }}
            h1 {{
                font-size: 36px;
                color: #4CAF50;
            }}
            h2 {{
                font-size: 28px;
                color: #FFFFFF;
            }}
            table {{
                width: auto;
                margin: 0 auto;
                border-collapse: collapse;
                font-size: 18px;
                table-layout: auto;
            }}
            th, td {{
                padding: 12px;
                border: 1px solid #393939;
                text-align: right;
            }}
            th.date {{
                text-align: left;
            }}
            th {{
                background-color: #4CAF50;
                color: black;
            }}
            .dollar-sign {{
                color: green;
            }}
            tr:nth-child(even) {{
                background-color: #383838;
            }}
            header {{
                display: flex;
                justify-content: flex-end;
                align-items: center;
                padding: 10px 20px;
                color: white;
            }}
            .powered-by {{
                display: flex;
                align-items: center;
                margin-left: auto;
            }}
            .powered-by img {{
                width: 40px;
                height: 40px;
                border-radius: 50%;
                margin-right: 5px;
                vertical-align: middle;
            }}
            a {{
                color: #097F25;
                text-decoration: none;
            }}
            .pagination {{
                margin-top: 20px;
                font-size: 18px;
            }}
            .pagination a {{
                margin: 0 10px;
                color: #4CAF50;
            }}
            .pagination a.current {{
                color: #FFFFFF;
                font-weight: bold;
                text-decoration: underline;
            }}
        </style>
    </head>
    <body>
    <header>
        <div class="powered-by">
            <a href="https://github.com/Sinister-git/Modrinth-Revenue" target="_blank">
                <img src="https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png" alt="GitHub Logo">
                <b>Powered by Modrinth Revenue</b>
            </a>
        </div>
    </header>
    <h1>Modrinth Revenue Dashboard</h1>
    <h2>Total Revenue: <span class="dollar-sign">$</span> {total_revenue:,.2f}</h2>
    <h2>\u2193 Daily Revenue \u2193</h2>
    <table>
        <tr>
            <th class="date">Date</th>
            <th>Total Revenue</th>
            <th>Creator Revenue</th>
            <th>Modrinth Revenue</th>
        </tr>
    """
    
    for entry in page_data:
        date = datetime.utcfromtimestamp(entry['time']).strftime('%B %d, %Y')
        revenue = float(entry['revenue'])
        creator_revenue = float(entry['creator_revenue'])
        modrinth_revenue = revenue * 0.25
        html_content += f"<tr><td style='text-align:left'>{date}</td><td><span class='dollar-sign'>$</span> {revenue:,.2f}</td><td><span class='dollar-sign'>$</span> {creator_revenue:,.2f}</td><td><span class='dollar-sign'>$</span> {modrinth_revenue:,.2f}</td></tr>"

    html_content += """
    </table>
    <div class="pagination">
    """
    
    for i in range(1, total_pages + 1):
        if i == page_num:
            html_content += f'<a href="#" class="current">{i}</a>'
        else:
            filename = "index.html" if i == 1 else f"page{i}.html"
            html_content += f'<a href="/{filename}">{i}</a>'
    
    html_content += """
    </div>
    </body>
    </html>
    """
    
    return html_content

# Function to generate all paginated HTML pages
def generate_all_pages(data):
    total_revenue = float(data.get("all_time", 0))
    daily_data = data.get("data", [])
    days_per_page = 30
    
    total_pages = (len(daily_data) + days_per_page - 1) // days_per_page
    
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    for page_num in range(1, total_pages + 1):
        start_idx = (page_num - 1) * days_per_page
        end_idx = start_idx + days_per_page
        page_data = daily_data[start_idx:end_idx]
        
        html_content = generate_page_html(total_revenue, page_data, page_num, total_pages)
        
        filename = "index.html" if page_num == 1 else f"page{page_num}.html"
        filepath = os.path.join(OUTPUT_DIR, filename)
        
        try:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(html_content)
            print(f"Generated page {page_num} at {filepath}")
        except Exception as e:
            print(f"Failed to write page {page_num}: {e}")

if __name__ == "__main__":
    api_data = fetch_data()
    if api_data:
        local_data = update_local_data(api_data)
        generate_all_pages(local_data)
        print(f"Pages successfully updated at {datetime.now()}")
    else:
        print("No data to process.")
