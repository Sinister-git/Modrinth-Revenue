## DISCLAIMER

This project is an independent work and is not affiliated, associated, authorized, endorsed by, or in any way officially connected with the Modrinth team, their products, or their services. The use of the name "Modrinth" is solely for the purposes of identifying the API services provided by Modrinth and for facilitating understanding of the functionality of this project.

All product and company names, logos, and brands are property of their respective owners. The use of these names, logos, and brands does not imply endorsement or sponsorship. This project solely interacts with Modrinth’s publicly available API for educational and informational purposes. 

By using this project, you acknowledge that the developers are not responsible for any damages, losses, or legal issues that may arise from its use, including but not limited to issues relating to API usage, rate limiting, or other terms and conditions set forth by the Modrinth platform.

For any official or legal concerns, please contact the Modrinth team directly.

---

# Modrinth Revenue Dashboard

This project automates the process of fetching daily revenue data from the [Modrinth API](https://modrinth.com) and displaying it on a web page. The data includes the total platform revenue, creator revenue, and a calculated Modrinth revenue (25% of total revenue). The Python script fetches data daily, stores it locally in a JSON file to retain historical data beyond the API's 30-day limit, and generates paginated HTML pages served by Nginx.

# Demo

Modrinth revenue demo: https://modrinth.citrus-mc.com/

## Features:
- **Automated Data Fetching**: Pulls revenue data from the Modrinth API daily using a cron job.
- **Historical Data Storage**: Stores data locally in `revenue_data.json` to maintain records beyond the API's 30-day limit.
- **Paginated Display**: Shows 30 days per page with a page selector (e.g., "1, 2, 3, 4, 5, 6") for navigating historical data.
- **Detailed Revenue Breakdown**:
  - Total revenue for the day
  - Creator revenue
  - Modrinth revenue (calculated as 25% of total revenue)
- **User-Agent Compliance**: Sends a uniquely-identifying `User-Agent` header as required by the Modrinth API.
- **Responsive Webpage**: Displays data in a clean, easy-to-read table with custom styling, including currency formatting, colored `$` symbols, styled borders, and proper Unicode arrow display (`↓`).

## Installation (Ubuntu 22.04)

### 1. Update System and Install Nginx

1. Update your system's package list and install Nginx:
   ```bash
   sudo apt update
   sudo apt install nginx
   ```

2. Start and enable Nginx to run at boot:
   ```bash
   sudo systemctl start nginx
   sudo systemctl enable nginx
   ```

### 2. Install Python 3 and Pip

The script requires Python 3 and Pip to run and install dependencies.

1. Install Python 3 and Pip:
   ```bash
   sudo apt install python3 python3-pip
   ```

2. Verify the installation:
   ```bash
   python3 --version
   pip3 --version
   ```

### 3. Install the `requests` Library

The Python script uses the `requests` library to fetch data from the Modrinth API.

1. Install the `requests` library:
   ```bash
   pip3 install requests
   ```

### 4. Set Up the Web Page Directory and Files

1. Create a directory for the web files (where Nginx will serve the pages):
   ```bash
   sudo mkdir -p /var/www/modrinth
   ```

2. Set ownership and permissions to allow the script to write files:
   ```bash
   sudo chown -R www-data:www-data /var/www/modrinth
   sudo chmod -R 755 /var/www/modrinth
   ```

3. Change into the directory:
   ```bash
   cd /var/www/modrinth
   ```

4. Clone the GitHub repository containing the project files:
   ```bash
   git clone https://github.com/Sinister-git/Modrinth-Revenue.git
   mv Modrinth-Revenue/* .
   rmdir Modrinth-Revenue
   ```

5. Verify the script is present:
   ```bash
   ls
   ```
   You should see `update_page.py` and possibly `README.md`.

6. Make the script executable (optional, for running with `./update_page.py`):
   ```bash
   chmod +x /var/www/modrinth/update_page.py
   ```

### 5. Set Up the Nginx Configuration

Configure Nginx to serve the generated HTML pages from `/var/www/modrinth`.

1. Create a new Nginx configuration file:
   ```bash
   sudo nano /etc/nginx/sites-available/modrinth.conf
   ```

2. Add the following configuration:
   ```nginx
   server {
       listen 80;
       server_name your_domain_or_IP;

       root /var/www/modrinth;
       index index.html;

       location / {
           try_files $uri $uri/ =404;
       }
       charset utf-8;
   }
   ```

3. Enable the configuration by creating a symbolic link:
   ```bash
   sudo ln -s /etc/nginx/sites-available/modrinth.conf /etc/nginx/sites-enabled/
   ```

4. Test the Nginx configuration for syntax errors:
   ```bash
   sudo nginx -t
   ```

5. Restart Nginx to apply the changes:
   ```bash
   sudo systemctl restart nginx
   ```

### 6. Customizing the User-Agent Header

The Modrinth API requires a unique `User-Agent` header. Customize it to identify your project.

1. Open the Python script:
   ```bash
   nano /var/www/modrinth/update_page.py
   ```

2. Locate the `USER_AGENT` variable (near the top):
   ```python
   USER_AGENT = "User-Agent': 'yourusername/project_name/version (contact_info)"
   ```

3. Replace it with a unique string, e.g.:
   ```python
   USER_AGENT = "yourusername/revenue_dashboard/1.0 (yourname@yourwebsite.com)"
   ```

4. Save and exit (`Ctrl+O`, `Enter`, `Ctrl+X` in `nano`).

### 7. Test the Script

Run the script manually to generate the initial HTML pages and populate `revenue_data.json`:

```bash
python3 /var/www/modrinth/update_page.py
```

If the script is executable with a shebang (`#!/usr/bin/env python3`), you can run:
```bash
/var/www/modrinth/update_page.py
```

Check that `index.html` and `revenue_data.json` are created:
```bash
ls /var/www/modrinth
```

Visit `http://your_domain_or_IP/` to verify the dashboard displays correctly with pagination and proper arrow characters (`↓ Daily Revenue ↓`).

### 8. Set Up the Cron Job

Automate daily updates with a cron job.

1. Open the crontab editor:
   ```bash
   crontab -e
   ```

2. Add a line to run the script daily at midnight:
   ```bash
   0 0 * * * /usr/bin/python3 /var/www/modrinth/update_page.py
   ```

3. Save and exit. Verify the cron job:
   ```bash
   crontab -l
   ```

## Troubleshooting

- **Script Fails to Run**:
  - Ensure Python 3 and `requests` are installed:
    ```bash
    pip3 install requests
    ```
  - Check for errors in the script output and verify the API URL and `USER_AGENT`.

- **Page Not Displaying**:
  - Confirm Nginx is running:
    ```bash
    sudo systemctl status nginx
    ```
  - Check file permissions:
    ```bash
    sudo chown -R www-data:www-data /var/www/modrinth
    sudo chmod -R 755 /var/www/modrinth
    ```

- **Incorrect Arrow Display (`â†“`)**:
  - Verify `index.html` contains `<meta charset="UTF-8">`.
  - Ensure Nginx serves UTF-8 (`charset utf-8;` in the config).
  - Re-run the script to regenerate HTML files.

For further assistance, check the [GitHub Issues](https://github.com/Sinister-git/Modrinth-Revenue/issues) page or contact the project maintainers.
