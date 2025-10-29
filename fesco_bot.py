from flask import Flask, send_file
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import io, time, requests

app = Flask(__name__)

@app.route('/download-bill/<ref_no>')
def download_bill(ref_no):
    # FESCO website URL — change if needed
    url = "https://bill.pitc.com.pk/fescobill/general"

    # Setup headless Chrome
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)

    # Input reference number
    ref_input = driver.find_element("id", "refno")
    ref_input.clear()
    ref_input.send_keys(ref_no)

    # Submit the form
    driver.find_element("id", "submitbtn").click()
    time.sleep(5)  # wait for bill to load

    # Find the download button (update selector if needed)
    pdf_link = driver.find_element("xpath", "//a[contains(@href, '.pdf')]").get_attribute("href")

    # Close browser
    driver.quit()

    # Download PDF file
    response = requests.get(pdf_link)
    if response.status_code != 200:
        return "Error downloading bill", 500

    # Send file to browser
    return send_file(
        io.BytesIO(response.content),
        mimetype='application/pdf',
        as_attachment=True,
        download_name=f"{ref_no}_fesco_bill.pdf"
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
