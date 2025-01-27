from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
import time
import sys
import streamlit as st
import os
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Set page configuration
st.set_page_config(
    page_title="Custom Page",
    page_icon="🌟",
    layout="centered",  # Options: "centered", "wide"
    initial_sidebar_state="collapsed"
)


st.header('E-Manifest Tracker')


# Directory to save uploaded files


tab1, tab2, tab3= st.tabs(['DOCS UPLOAD', "PARS (ACI)", "PAPS (ACE)"])

# search_pars = st.button('Search', key = 'search_pars')
# search_truck = st.button('Search', key = 'search_truck')

with tab1:
    UPLOAD_DIR = "C:/Users/sarap/OneDrive - parachas/Attachments"  #"C:/Users/sarap/manifest_tracker/uploaded_pdfs"
    if not os.path.exists(UPLOAD_DIR):
        os.makedirs(UPLOAD_DIR)

    with st.form("file_upload_form"):
        truck_number = st.text_input("Enter Truck Number:")
        driver_name = st.text_input("Enter Driver Name:")
        uploaded_file = st.file_uploader("Upload a file", type=["pdf"])
        submitted = st.form_submit_button("Submit")

    def send_email(sender_email, sender_password, recipient_email, subject, message):
        # Create a multipart message object
        msg = MIMEMultipart('alternative')
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = subject

        # Create both plain text and HTML versions of the email
        text = 'This is a plain text email.'
        html = f'<html><body><>{message}</h1></body></html>'

        # Attach the plain text and HTML versions to the email
        part1 = MIMEText(text, 'plain')
        part2 = MIMEText(html, 'html')
        msg.attach(part1)
        msg.attach(part2)

        # SMTP server settings for Outlook
        smtp_server = 'smtp.office365.com'
        smtp_port = 587

        try:
            # Create a secure SSL/TLS connection to the SMTP server
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()

            # Login to your Outlook email account
            server.login(sender_email, sender_password)

            # Send the email
            server.sendmail(sender_email, recipient_email, msg.as_string())

            print("Email sent successfully!")

        except smtplib.SMTPException as e:
            print("Error sending email:", str(e))

        finally:
            # Close the connection to the SMTP server
            server.quit()

    # Example usage
    sender_email = 'saraparacha@parachas247.onmicrosoft.com'
    sender_password = 'Pokemon45678930'
    recipient_email = 'sara.paracha@outlook.com'
    subject = f"{truck_number}_{driver_name}"
    message = 'This is an HTML email sent using smtplib and Outlook.'

    if submitted:
        if uploaded_file is not None and truck_number.strip() and driver_name.strip():
            # Get current date
            current_date = datetime.now().strftime("%Y-%m-%d")

            # Create the new file name
            file_extension = uploaded_file.name.split(".")[-1]
            new_file_name = f"{truck_number}_{driver_name}_{current_date}.{file_extension}"

            # Save the file locally with the new name
            file_path = os.path.join(UPLOAD_DIR, new_file_name)
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            st.success(f"File uploaded successfully and saved as '{new_file_name}'!")
            send_email(sender_email, sender_password, recipient_email, subject, message)

        else:
            st.error("Please fill in all fields and upload a valid file.")





with tab2:
    pars = st.text_input('Enter PARS# only last 6 digits', key='pars')
    search_pars = st.button('Search', key = 'search_pars')
    st.write('OR')
    truck = st.text_input('Enter Truck# ', key='truck')
    search_truck = st.button('Search', key = 'search_truck')

    if search_pars:
        st.write("Checking through pars#...")
        options = Options()
        options.add_argument('--headless')
        chromedrivepath = r"C:\Users\sarap\chromedriver-win64\chromedriver.exe"
        finalpath = chromedrivepath.replace('\\',"/")
        service = Service(executable_path = finalpath)
        driver = webdriver.Chrome(service = service)#, options=options)
        url = 'https://ace.avaal.com/manifest/profile/login.jsp'
        user = "dfh"
        passs = "dfh@12345"
        driver.get(url)

        # add user
        driver.find_element(By.XPATH, '//*[@id="username"]').send_keys(user)
        time.sleep(1)
        # add password
        driver.find_element(By.XPATH, '//*[@id="password"]').send_keys(passs)
        time.sleep(1)
        # click sigin button
        driver.find_element(By.XPATH, '//*[@id="btnLogin"]').click()
        time.sleep(1)
        #click aci trips
        driver.find_element(By.XPATH, '//*[@id="topnav"]/div/span[10]/span/a').click()
        time.sleep(1)
        #pars input
        driver.find_element(By.XPATH, '//*[@id="hidenSearchForm"]/td[1]/table/tbody/tr[1]/td[2]/input').send_keys(pars)
        time.sleep(1)
        #click search to look for pars
        driver.find_element(By.XPATH, '//*[@id="SearchButtonSection"]').click()
        time.sleep(1)
        #click on pars to open trip
        while True:
            try:
                driver.find_element(By.XPATH, '//*[@id="datatable"]/tbody/tr/td[2]/a').click()
                time.sleep(1)
                break
            except NoSuchElementException:
                st.write("PARS not found. Try contacting customs team")
                driver.quit()
                st.stop()
            
          
        # #click print button
        driver.find_element(By.XPATH, '//*[@id="printBtn"]').click()
        time.sleep(1)
        # click to send aci by email
        print('child html opened')

        #enter iframe for send email to driver 
        iframe=driver.find_element(By.XPATH,'//*[@id="windowSize"]/tbody/tr[2]/td[2]/div/div/table/tbody/tr/td/iframe')
        driver.switch_to.frame(iframe)
        time.sleep(1)

        #click send email to driver
        txt=driver.find_element(By.XPATH, '/html/body/div[1]/button[2]').click()
        time.sleep(1)

        #click send
        txt=driver.find_element(By.XPATH, '/html/body/div/button[1]').click()
        time.sleep(1)

        driver.quit()
        st.write('aci sent')
        
    
    if search_truck:
        st.write("Checking through truck#...")
        options = Options()
        options.add_argument('--headless')
        chromedrivepath = r"C:\Users\sarap\chromedriver-win64\chromedriver.exe"
        finalpath = chromedrivepath.replace('\\',"/")
        service = Service(executable_path = finalpath)
        driver = webdriver.Chrome(service = service)#, options=options)
        url = 'https://ace.avaal.com/manifest/profile/login.jsp'
        user = "dfh"
        passs = "dfh@12345"
        driver.get(url)

        # add user
        driver.find_element(By.XPATH, '//*[@id="username"]').send_keys(user)
        time.sleep(1)
        # add password
        driver.find_element(By.XPATH, '//*[@id="password"]').send_keys(passs)
        time.sleep(1)
        # click sigin button
        driver.find_element(By.XPATH, '//*[@id="btnLogin"]').click()
        time.sleep(1)
        #click aci trips
        driver.find_element(By.XPATH, '//*[@id="topnav"]/div/span[10]/span/a').click()
        time.sleep(1)
        #truck  input
        driver.find_element(By.XPATH, '//*[@id="hidenSearchForm"]/td[1]/table/tbody/tr[2]/td[2]/input').send_keys(truck)
        time.sleep(1)
        #click search to look for pars
        driver.find_element(By.XPATH, '//*[@id="SearchButtonSection"]').click()
        time.sleep(1)
        #click on pars to open trip
        driver.find_element(By.XPATH, '//*[@id="datatable"]/tbody/tr/td[2]/a').click()
        time.sleep(1)         
        # #click print button
        driver.find_element(By.XPATH, '//*[@id="printBtn"]').click()
        time.sleep(1)
        # click to send aci by email
        print('child html opened')

        #enter iframe for send email to driver 
        iframe=driver.find_element(By.XPATH,'//*[@id="windowSize"]/tbody/tr[2]/td[2]/div/div/table/tbody/tr/td/iframe')
        driver.switch_to.frame(iframe)
        time.sleep(1)

        #click send email to driver
        txt=driver.find_element(By.XPATH, '/html/body/div[1]/button[2]').click()
        time.sleep(1)

        #click send
        txt=driver.find_element(By.XPATH, '/html/body/div/button[1]').click()
        time.sleep(1)

        driver.quit()
        st.write('aci sent')

        



with tab3:
    paps = st.text_input('Enter PAPS# ', key='paps')
    search_paps = st.button('Search', key = 'search_paps')
    st.write('OR')
    truck_ace = st.text_input('Enter Truck# ', key='truck_ace')
    search_truck_ace = st.button('Search', key = 'search_truck_ace')

    if search_paps:
        st.write("Checking through paps#...")
        options = Options()
        options.add_argument('--headless')
        chromedrivepath = r"C:\Users\sarap\chromedriver-win64\chromedriver.exe"
        finalpath = chromedrivepath.replace('\\',"/")
        service = Service(executable_path = finalpath)
        driver = webdriver.Chrome(service = service)#, options=options)
        url = 'https://ace.avaal.com/manifest/profile/login.jsp'
        user = "dfh"
        passs = "dfh@12345"
        driver.get(url)

        # add user
        driver.find_element(By.XPATH, '//*[@id="username"]').send_keys(user)
        time.sleep(1)
        # add password
        driver.find_element(By.XPATH, '//*[@id="password"]').send_keys(passs)
        time.sleep(1)
        # click sigin button
        driver.find_element(By.XPATH, '//*[@id="btnLogin"]').click()
        time.sleep(1)
        #click ace trips
        driver.find_element(By.XPATH, '//*[@id="topnav"]/div/span[1]/span/a').click()
        time.sleep(1)
        #paps input
        driver.find_element(By.XPATH, '//*[@id="hidenSearchForm"]/td[1]/table/tbody/tr[1]/td[2]/input').send_keys(paps)
        time.sleep(1)
        #click search to look for paps
        driver.find_element(By.XPATH, '//*[@id="SearchButtonSection"]').click()
        time.sleep(1)
        #click on paps to open trip
        while True:
            try:
                driver.find_element(By.XPATH, '//*[@id="datatable"]/tbody/tr/td[2]/a').click()
                time.sleep(1)
                break
            except NoSuchElementException:
                st.write("PAPS not found. Try searching through Truck#")
                driver.quit()
                st.stop()
            
          
        # #click print button
        driver.find_element(By.XPATH, '/html/body/div[7]/button[2]').click()
        time.sleep(1)
        # click to send aci by email
        print('child html opened')

        #enter iframe for send email to driver 
        iframe=driver.find_element(By.XPATH,'//*[@id="windowSize"]/tbody/tr[2]/td[2]/div/div/table/tbody/tr/td/iframe')
        driver.switch_to.frame(iframe)
        time.sleep(1)

        #click send email to driver
        txt=driver.find_element(By.XPATH, '/html/body/div[1]/button[2]').click()
        time.sleep(1)

        #click send
        txt=driver.find_element(By.XPATH, '/html/body/div/button[1]').click()
        time.sleep(1)

        driver.quit()
        st.write('ace sent')
        
    
    if search_truck_ace:
        st.write("Checking through truck#...")
        options = Options()
        options.add_argument('--headless')
        chromedrivepath = r"C:\Users\sarap\chromedriver-win64\chromedriver.exe"
        finalpath = chromedrivepath.replace('\\',"/")
        service = Service(executable_path = finalpath)
        driver = webdriver.Chrome(service = service)#, options=options)
        url = 'https://ace.avaal.com/manifest/profile/login.jsp'
        user = "dfh"
        passs = "dfh@12345"
        driver.get(url)

        # add user
        driver.find_element(By.XPATH, '//*[@id="username"]').send_keys(user)
        time.sleep(1)
        # add password
        driver.find_element(By.XPATH, '//*[@id="password"]').send_keys(passs)
        time.sleep(1)
        # click sigin button
        driver.find_element(By.XPATH, '//*[@id="btnLogin"]').click()
        time.sleep(1)
        #truck  input
        driver.find_element(By.XPATH, '//*[@id="hidenSearchForm"]/td[1]/table/tbody/tr[2]/td[2]/input').send_keys(truck_ace)
        time.sleep(1)
        #click search to look for paps
        driver.find_element(By.XPATH, '//*[@id="SearchButtonSection"]').click()
        time.sleep(1)
        #click on paps to open trip
        driver.find_element(By.XPATH, '//*[@id="datatable"]/tbody/tr/td[2]/a').click()
        time.sleep(1)         
        # #click print button
        driver.find_element(By.XPATH, '/html/body/div[7]/button[2]').click()
        time.sleep(1)
        # click to send aci by email
        print('child html opened')

        #enter iframe for send email to driver 
        iframe=driver.find_element(By.XPATH,'//*[@id="windowSize"]/tbody/tr[2]/td[2]/div/div/table/tbody/tr/td/iframe')
        driver.switch_to.frame(iframe)
        time.sleep(1)

        #click send email to driver
        txt=driver.find_element(By.XPATH, '/html/body/div[1]/button[2]').click()
        time.sleep(1)

        #click send
        txt=driver.find_element(By.XPATH, '/html/body/div/button[1]').click()
        time.sleep(1)

        driver.quit()
        st.write('ace sent')

        

    















    # if st.button('PAPS (ACE)'):
    #     st.text_input('Enter your truck#')


































# # Create buttons side by side
# col1, col2 = st.columns(2)

# with col1:
#     st.markdown('<div class="custom-buttons">', unsafe_allow_html=True)
#     if st.button("Button 1"):
#         st.write("Button 1 clicked!")
#     st.markdown('</div>', unsafe_allow_html=True)

# with col2:
#     st.markdown('<div class="custom-buttons">', unsafe_allow_html=True)
#     if st.button("Button 2"):
#         st.write("Button 2 clicked!")
#     st.markdown('</div>', unsafe_allow_html=True)
