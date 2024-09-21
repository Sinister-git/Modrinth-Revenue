import requests
from datetime import datetime

API_URL = "https://api.modrinth.com/v3/payout/platform_revenue"
USER_AGENT = "User-Agent': 'yourusername/project_name/version (contact_info)"  # Replace with your information

# Function to fetch data from Modrinth API with User-Agent header
def fetch_data():
    headers = {
        'User-Agent': USER_AGENT
    }

    response = requests.get(API_URL, headers=headers)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")
        return None

def generate_html(data):
    total_revenue = float(data.get("all_time", 0))
    daily_data = data.get("data", [])
    
    # Start with HTML structure and CSS styles
    html_content = f"""
    <html>
    <head>
        <title>Modrinth Revenue Data</title>
        <style>
            /* Set background color and text alignment */
            body {{
                background-color: #262626;  /* Light grey background */
                font-family: Arial, sans-serif;  /* Font style */
                color: #FFFFFF;  /* Text color */
                text-align: center;  /* Center all content */
                padding: 20px;  /* Padding around the page */
            }}
            
            /* Header styles */
            h1 {{
                font-size: 36px;  /* Font size for main header */
                color: #4CAF50;  /* Green color for headers */
            }}
            
            h2 {{
                font-size: 28px;  /* Smaller header */
                color: #FFFFFF;  /* Grey color for sub-headers */
            }}
            
            /* Style the revenue table */
            table {{
                width: auto;  /* Make the table take up 80% of the page width */
                margin: 0 auto;  /* Center the table horizontally */
                border-collapse: collapse;  /* Collapse borders */
                font-size: 18px;  /* Font size for table */
                table-layout: auto;
            }}
            
            th, td {{
                padding: 12px;  /* Padding inside the table cells */
                border: 1px solid #393939;  /* Light grey borders */
                text-align: right;  /* Align text to the right for numbers */
            }}

            th.date {{
                text-align: left;  /* Align "Date" header to the left */
            }}
            
            th {{
                background-color: #4CAF50;  /* Green background for table headers */
                color: black;  /* White text for headers */
            }}

            .dollar-sign {{
                color: green;
            }}
            
            tr:nth-child(even) {{
                background-color: #383838;  /* Light grey background for even rows */
            }}
        </style>
    </head>
    <body>
        <h1>Modrinth Revenue (All-Time)</h1>
        <h2>Total Revenue: <span class="dollar-sign">$</span> {total_revenue:,.2f}</h2>
        
        <h2>Daily Revenue</h2>
        <table>
             <tr>
                <th class="date">Date</th>
                <th>Total Revenue</th>
                <th>Creator Revenue</th>
                <th>Modrinth Revenue</th>
            </tr>
    """
    
    # Loop through daily data and populate the table
    for entry in daily_data:
        date = datetime.utcfromtimestamp(entry['time']).strftime('%B %d, %Y')
        revenue = float(entry['revenue'])
        creator_revenue = float(entry['creator_revenue'])

        modrinth_revenue = revenue * 0.25

        # Populate the table rows
        html_content += f"<tr><td style='text-align:left'>{date}</td><td><span class='dollar-sign'>$</span> {revenue:,.2f}</td><td><span class='dollar-sign'>$</span> {creator_revenue:,.2f}</td><td><span class='dollar-sign'>$</span> {modrinth_revenue:,.2f}</td></tr>"
    
    # Close the table and body tags
    html_content += """
        </table>
    </body>
    </html>
    """
    
    return html_content

if __name__ == "__main__":
    # Fetch the data and process it
    data = fetch_data()
    if data:
        # Use data to generate your HTML page
        html_content = generate_html(data)
        try:
            with open("/var/www/modrinth/index.html", "w") as f:
                f.write(html_content)
            print(f"Page successfully updated at {datetime.now()}")
        except Exception as e:
            print(f"Failed to update the page: {e}")
