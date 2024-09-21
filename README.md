## DISCLAIMER

This project is an independent work and is not affiliated, associated, authorized, endorsed by, or in any way officially connected with the Modrinth team, their products, or their services. The use of the name "Modrinth" is solely for the purposes of identifying the API services provided by Modrinth and for facilitating understanding of the functionality of this project.

All product and company names, logos, and brands are property of their respective owners. The use of these names, logos, and brands does not imply endorsement or sponsorship. This project solely interacts with Modrinth’s publicly available API for educational and informational purposes. 

By using this project, you acknowledge that the developers are not responsible for any damages, losses, or legal issues that may arise from its use, including but not limited to issues relating to API usage, rate limiting, or other terms and conditions set forth by the Modrinth platform.

For any official or legal concerns, please contact the Modrinth team directly.

---

# Modrinth Revenue Dashboard

This project automates the process of fetching daily revenue data from the [Modrinth API](https://modrinth.com) and displaying it on a web page. The data includes the total platform revenue, creator revenue, and a calculated Modrinth revenue, which represents 25% of the total revenue. The python script pulls from the API and populates the html page.

## Features:
- **Automated Data Fetching**: Pulls revenue data from the Modrinth API once a day using a cron job.
- **Detailed Revenue Breakdown**:
  - Total revenue for the day
  - Creator revenue
  - Modrinth revenue (calculated as 25% of total revenue)
- **User-Agent Compliance**: Sends a uniquely-identifying `User-Agent` header as required by the Modrinth API.
- **Responsive Webpage**: Displays data in a clean, easy-to-read table format with custom styling, including currency formatting, colored `$` symbols, and styled borders.

## Installation(Ubuntu 22.04):

### 1. Update system and install Nginx

1. Update your system's package list and install Nginx:
   ```bash
   sudo apt update
   sudo apt install nginx
   ```

2. Start and enable Nginx to start at boot:
   ```bash
   sudo systemctl start nginx
   sudo systemctl enable nginx
   ```

### 2. Install Python3 and Pip3

You’ll need Python 3 and Pip3 to run the script and install dependencies.

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

## Set Up the Web Page Directory and Files

### 1. Create a Directory for the Web Page

1. Create a directory where the HTML file and python script for the revenue dashboard will be stored (this is where Nginx will serve the webpage from):
   ```bash
   sudo mkdir -p /var/www/modrinth
   ```

2. Change the ownership of the directory to ensure that the script has write access:
   ```bash
   sudo chown -R $USER:$USER /var/www/modrinth
   ```

3. Set the correct permissions for the directory:
   ```bash
   sudo chmod -R 755 /var/www/modrinth
   ```
   Change into the newly created directory:
   ```bash
   cd /var/www/modrinth
   ```
   
5. Clone the GitHub repository containing the project files:
   ```bash
   git clone https://github.com/Sinister-git/Modrinth-Revenue.git
   ```

6. After cloning, you should see a new python file:
   ```bash
   ls
   ```

### 2. Create a Blank HTML File

Create the initial blank HTML file that will be updated by the Python script later.

1. Create the file:
   ```bash
   sudo touch /var/www/modrinth/index.html
   ```

2. Set the correct permissions for the HTML file:
   ```bash
   sudo chmod 664 /var/www/modrinth/index.html
   ```

### 3. Set Up the Nginx Configuration

Create a configuration file for Nginx to serve the revenue dashboard from `/var/www/modrinth`.

1. Create a new Nginx configuration file:
   ```bash
   sudo nano /etc/nginx/sites-available/modrinth.conf
   ```

2. Add the following configuration to serve the HTML page from `/var/www/modrinth`:

   ```nginx
   server {
       listen 80;
       server_name your_domain_or_IP;

       root /var/www/modrinth;
       index index.html;

       location / {
           try_files $uri $uri/ =404;
       }
   }
   ```

3. Enable the new configuration by creating a symbolic link:
   ```bash
   sudo ln -s /etc/nginx/sites-available/modrinth.conf /etc/nginx/sites-enabled/
   ```

4. Test the Nginx configuration for syntax errors:
   ```bash
   sudo nginx -t
   ```

5. Reload Nginx to apply the changes:
   ```bash
   sudo systemctl reload nginx
   ```

At this point, Nginx should serve the blank `index.html` file from `/var/www/modrinth` when you visit your server's IP or domain.

### 2. Make the Script Executable

Ensure the script has executable permissions:
```bash
chmod +x /var/www/modrinth/update_page.py
```

---

### Customizing the User-Agent Header

Modrinth’s API requires a unique `User-Agent` header to identify your application. It is essential to modify the User-Agent string to represent your specific project or use case in compliance with Modrinth's API usage policy.

To customize the User-Agent, follow these steps:

1. **Open the Python script**: 
   Locate and open the `update_page.py` script from the cloned repository in your preferred text editor.

   ```bash
   nano /var/www/modrinth/update_page.py
   ```

2. **Locate the User-Agent line**: 
   In the script, find the section where the `User-Agent` is set in the headers. It should look something like this:

   ```python
   headers = {
       'User-Agent': 'yourusername/project_name/version (contact_info)'
   }
   ```

3. **Modify the User-Agent string**: 
   Replace the default `User-Agent` value with something unique that clearly identifies your project. Here are a few examples:

   - **Good**: `yourusername/revenue_dashboard/1.0`
   - **Better**: `yourusername/revenue_dashboard/1.0 (https://yourwebsite.com)`
   - **Best**: `yourusername/revenue_dashboard/1.0 (yourname@yourwebsite.com)`

   This will allow Modrinth’s API maintainers to contact you if necessary, without blocking your traffic.

4. **Save and exit the script**: 
   Once you've made the changes, save the file and exit the text editor (in `nano`, press `CTRL+O` to save and `CTRL+X` to exit).


### 3. Test the Script

Run the script manually to check if it works:
```bash
python3 /var/www/modrinth/update_page.py
```

After running the script, visit your server's IP or domain to see if the HTML page is correctly generated and displayed.

## Set Up the Cron Job

To automate the process of updating the page daily, you’ll set up a cron job.

1. Open the crontab editor:
   ```bash
   crontab -e
   ```

2. Add the following line to run the script once every day at midnight:
   ```bash
   0 0 * * * /usr/bin/python3 /var/www/modrinth/update_page.py
   ```

   If you want to run it daily at a specific time (e.g., 3 AM), use:
   ```bash
   0 3 * * * /usr/bin/python3 /var/www/modrinth/update_page.py
   ```

3. Save and exit the crontab editor.
