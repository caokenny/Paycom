# Paycom Auto Punch Script

## Overview
This script automates the punching process for Paycom's time clock system using Selenium. It logs into Paycom, waits for the appropriate times, and performs the necessary punch actions (clocking in and out).

## Features
- Automated login to Paycom
- Automated punching for:
  - Clocking in for the day
  - Clocking out for lunch
  - Clocking back in from lunch
  - Clocking out at the end of the day
- Configurable schedule
- Headless Chrome execution

## Prerequisites
### Software Requirements
- Python 3.x
- Google Chrome installed
- ChromeDriver (compatible with the installed Chrome version)

### Python Dependencies
Install the required packages using:

```sh
pip install selenium
```

## Configuration
### 1. Update Your Login Credentials
Edit the script and enter your Paycom credentials:

```python
username = "your_username"
password = "your_password"
userpin = "last_4_of_SSN"
```

### 2. Modify Punch Timing (Optional)
The script supports different punch schedules. Modify the following lists as needed:

```python
clock_times_seconds = [32400, 43200, 46800, 64800]  # Time in seconds from midnight
clock_times_string = ['9:00', '12:00', '1:00', '6:00']  # Corresponding times in human-readable format
```

If you have a different lunch break time, uncomment and modify the alternate schedule in the script.

### 3. Set Up ChromeDriver
- Download ChromeDriver from [here](https://chromedriver.chromium.org/downloads).
- Extract and place `chromedriver.exe` inside `chromedriver-win64/` (or modify the path in the script).

## How to Use
1. Ensure Google Chrome and ChromeDriver are installed.
2. On first run, set `login2FA = True` on line 37. Comment out line 45.
3. Run the script:

```sh
python Paycom.py
```

4. Enter the 2FA code. MAKE SURE TO CHECK 'Remember This Device'. Close the driver browser or exit the script.

5. Set `login2FA = False`. Uncomment line 45.

6. For the next 30 days 2FA won't be required, just run the script as normal.

```sh
python Paycom.py
```

## Disclaimer
This script is for educational and personal automation purposes only. Use it responsibly and ensure compliance with your organization's policies.