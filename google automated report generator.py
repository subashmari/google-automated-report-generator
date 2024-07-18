from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import os
import time
from datetime import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

class LaunchChrome:
    def __init__(self):
        self.user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36"
        self.generated_files = []

    def browser_launch(self):
        print("Before initializing the driver.")
        options = Options()
        p = {"download.default_directory": os.path.join(os.getcwd(), "report")}
        options.add_experimental_option("prefs", p)
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--disable-extensions")
        options.add_argument("--proxy-server='direct://'")
        options.add_argument("--proxy-bypass-list=*")
        options.add_argument("--start-maximized")
        options.add_argument("--ignore-certificate-errors")
        options.add_argument("--allow-running-insecure-content")
        options.add_argument("user-agent=" + self.user_agent)
        service = Service(executable_path="path/to/chromedriver")  # Provide the path to chromedriver
        service.start()
        driver = webdriver.Chrome(service=service, options=options)
        print("After initializing the driver.")
        driver.get("https://pentest-tools.com/pricing?utm_campaign=ab-home-tools-cta&utm_source=homepage-v1&utm_medium=website&utm_content=main-button&utm_term=start-pentesting-now")
        driver.maximize_window()

    def login_page(self, driver):
        driver.find_element(By.XPATH, "//a[text()=' Log in ']").click()
        time.sleep(3)
        driver.find_element(By.XPATH, "//input[@type='email']").send_keys("youraccount@gmail.com")
        driver.find_element(By.XPATH, "//input[@type='password']").send_keys("passwords")
        driver.find_element(By.XPATH, "//button[@type='submit']").click()
        time.sleep(10)
        driver.switch_to.frame(driver.find_element(By.XPATH, "//iframe[@data-test-id='interactive-frame']"))
        driver.find_element(By.XPATH, "//div[@id='interactive-close-button']").click()
        driver.switch_to.default_content()

    def scans(self, driver):
        driver.find_element(By.XPATH, "//span[text()='Scans']").click()
        time.sleep(3)
        driver.find_element(By.XPATH, "//a[@class='!ptt-btn-primary !ptt-mt-5 !ptt-w-fit']").click()
        driver.find_element(By.XPATH, "//h4[text()='Website Vulnerability Scanner']").click()
        target_input = driver.find_element(By.XPATH, "//input[@name='target']")
        target_input.clear()
        target_input.send_keys("https://console.cloud.google.com/projectselector2/net-security/securitypolicies/list?_ga=2.10069245.936492860.1607995107-366914458.1596215128&pli=1&supportedpurview=project")
        driver.find_element(By.XPATH, "//label[@class='col-xs-12 no-padding']//span[@class='lbl small']").click()
        driver.find_element(By.XPATH, "//span[contains(text(),'I am authorized to scan this target and I agree to')]").click()
        driver.find_element(By.XPATH, "//span[@id='start_button_text']").click()

    def download_report(self, driver):
        time.sleep(50)
        driver.find_element(By.XPATH, "//a[@id='download_result_link']").click()
        driver.find_element(By.XPATH, "//button[text()='Export']").click()
        time.sleep(5)
        latest_file = self.get_latest_file(os.path.join(os.getcwd(), "report"), ".pdf")

        # Format the current date
        current_date = datetime.now().strftime("%d_%m_%Y")

        if latest_file and latest_file.lower().endswith(".pdf"):
            old_report_file = os.path.join(os.getcwd(), "report", f"Nurture_RestoreMe_{current_date}(Page Sessions).pdf")
            if os.path.exists(old_report_file):
                os.remove(old_report_file)
            new_report_file = os.path.join(os.getcwd(), "report", f"Nurture_RestoreMe_{current_date}(Page Sessions).pdf")
            os.rename(latest_file, new_report_file)
            self.generated_files.append(new_report_file)
        else:
            if latest_file:
                print(f"The latest file is not a PDF file: {latest_file}")
            else:
                print("No PDF file found in the download directory.")
        time.sleep(20)

    @staticmethod
    def send_email_with_attachment(attachment_files, date_range):
        gmail_username = "reid@gmail.com"
        app_password = "password"

        # Create a multipart message
        msg = MIMEMultipart()
        msg["From"] = gmail_username
        msg["To"] = "toaddress@gmail.com"
        msg["Subject"] = f"Nurture Restore Me App Analytics Report - {date_range}"

        # Add body to email
        body = "Hello Dr.Garg and Adriana,\n\n" \
               "Attached is the analytics for the last 7 days " + date_range + " Also, this one has the page view analytics & User Acquisition reports.\n\n" \
               "Let us know if you have any queries.\n\n" \
               "Thank You"
        msg.attach(MIMEText(body, "plain"))

        # Attach files
        for attachment_file in attachment_files:
            with open(attachment_file, "rb") as f:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(f.read())
            encoders.encode_base64(part)
            part.add_header("Content-Disposition", f"attachment; filename= {os.path.basename(attachment_file)}",)
            msg.attach(part)

        # Log in to server using secure context and send email
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(gmail_username, app_password)
            server.sendmail(gmail_username, "youraccount@gmail.com", msg.as_string())

    @staticmethod
    def get_latest_file(directory, extension):
        files = [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith(extension)]
        return max(files, key=os.path.getctime) if files else None

# Usage
chrome_launcher = LaunchChrome()
chrome_launcher.browser_launch()
chrome_launcher.login_page()
chrome_launcher.scans()
chrome_launcher.download_report()
chrome_launcher.send_email_with_attachment(chrome_launcher.generated_files, "date range")  # Provide appropriate date range
