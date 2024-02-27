from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
from datetime import datetime

opt = Options()
opt.add_argument("--disable-infobars")
opt.add_argument("start-maximized")
opt.add_argument("--disable-extensions")
opt.add_experimental_option(
            "detach", True)


driver = webdriver.Chrome(options=opt)
wait = WebDriverWait(driver, 5)


#Property IDs: 0-any 1-house 2-guesthouse 3-apartment 4-hotel
#Room type: 0-any 1-Private room 2-Entire house/apartment

# Room Types
rooms = {0:'', 1:'&room_types%5B%5D=Private%20room', 2:'&room_types%5B%5D=Entire%20home%2Fapt'}

# Example Data
city = 'Szczecin'
country = 'Poland'
check_in = '2024-05-01'
check_out = '2024-05-05'
adults = 6
children = 0
infants = 0
pets = 2
price_min = 0
price_max = 18004
property_type_num = 1
room = 0

check_out_date = check_out.split('-')
check_in_date = check_in.split('-')

nights = (datetime(int(check_out_date[0]),int(check_out_date[1]),int(check_out_date[2])) - datetime(int(check_in_date[0]),int(check_in_date[1]),int(check_in_date[2]))).days
# Set language

driver.get("https://airbnb.com")

wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "_z5mecy")))

select_language = driver.find_element(By.CLASS_NAME, "_z5mecy")
select_language.click()

wait.until(EC.element_to_be_clickable((By.XPATH, "//*[text()='United States']")))

language = driver.find_element(By.XPATH, "//div[text()='United States']")
language.click()

# Go to our main page
url = f'https://www.airbnb.com/s/{city}--{country}/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&query={city}%2C%20{country}&date_picker_type=calendar&checkin={check_in}&checkout={check_out}&adults={adults}&children={children}&infants={infants}&pets={pets}&source=structured_search_input_header&search_type=filter_change&price_filter_num_nights={nights}&l2_property_type_ids%5B%5D={property_type_num}&price_min={price_min}&price_max={price_max}{rooms[room]}'
driver.get(url)
main_tab = driver.current_window_handle
airbnb_houses = {}
more_pages = True
is_true = True
counter = 1
# Get number of all apartments
try:
    wait.until(EC.presence_of_all_elements_located((By.XPATH, '//a[@class="l1ovpqvx atm_1y33qqm_1ggndnn_10saat9 atm_17zvjtw_zk357r_10saat9 atm_w3cb4q_il40rs_10saat9 atm_1cumors_fps5y7_10saat9 atm_52zhnh_1s82m0i_10saat9 atm_jiyzzr_1d07xhn_10saat9 c1ackr0h atm_c8_fkimz8 atm_g3_11yl58k atm_fr_4ym3tx atm_cs_qo5vgd atm_9s_1txwivl atm_h_1h6ojuz atm_fc_1h6ojuz atm_bb_idpfg4 atm_3f_glywfm atm_5j_1ssbidh atm_26_1j28jx2 atm_7l_ujz1go atm_vy_1vi7ecw atm_e2_1vi7ecw atm_gi_idpfg4 atm_gz_logulu atm_h0_logulu atm_l8_idpfg4 atm_uc_1dtz4sb atm_kd_glywfm atm_uc_glywfm__1rrf6b5 atm_26_rmqrjm_1nos8r_uv4tnr atm_tr_kv3y6q_csw3t1 atm_26_rmqrjm_csw3t1 atm_9j_73adwj_1o5j5ji atm_3f_glywfm_jo46a5 atm_l8_idpfg4_jo46a5 atm_gi_idpfg4_jo46a5 atm_3f_glywfm_1icshfk atm_kd_glywfm_19774hq atm_uc_x37zl0_1w3cfyq atm_26_rmqrjm_1w3cfyq atm_70_1jt8dgi_1w3cfyq atm_uc_glywfm_1w3cfyq_1rrf6b5 atm_uc_x37zl0_18zk5v0 atm_26_rmqrjm_18zk5v0 atm_70_1jt8dgi_18zk5v0 atm_uc_glywfm_18zk5v0_1rrf6b5 dir dir-ltr"]')))
    pages = driver.find_elements(By.XPATH, '//a[@class="l1ovpqvx atm_1y33qqm_1ggndnn_10saat9 atm_17zvjtw_zk357r_10saat9 atm_w3cb4q_il40rs_10saat9 atm_1cumors_fps5y7_10saat9 atm_52zhnh_1s82m0i_10saat9 atm_jiyzzr_1d07xhn_10saat9 c1ackr0h atm_c8_fkimz8 atm_g3_11yl58k atm_fr_4ym3tx atm_cs_qo5vgd atm_9s_1txwivl atm_h_1h6ojuz atm_fc_1h6ojuz atm_bb_idpfg4 atm_3f_glywfm atm_5j_1ssbidh atm_26_1j28jx2 atm_7l_ujz1go atm_vy_1vi7ecw atm_e2_1vi7ecw atm_gi_idpfg4 atm_gz_logulu atm_h0_logulu atm_l8_idpfg4 atm_uc_1dtz4sb atm_kd_glywfm atm_uc_glywfm__1rrf6b5 atm_26_rmqrjm_1nos8r_uv4tnr atm_tr_kv3y6q_csw3t1 atm_26_rmqrjm_csw3t1 atm_9j_73adwj_1o5j5ji atm_3f_glywfm_jo46a5 atm_l8_idpfg4_jo46a5 atm_gi_idpfg4_jo46a5 atm_3f_glywfm_1icshfk atm_kd_glywfm_19774hq atm_uc_x37zl0_1w3cfyq atm_26_rmqrjm_1w3cfyq atm_70_1jt8dgi_1w3cfyq atm_uc_glywfm_1w3cfyq_1rrf6b5 atm_uc_x37zl0_18zk5v0 atm_26_rmqrjm_18zk5v0 atm_70_1jt8dgi_18zk5v0 atm_uc_glywfm_18zk5v0_1rrf6b5 dir dir-ltr"]')
    num_of_pages = int(pages[-1].text)
    pages[-1].click()
    wait.until(EC.presence_of_all_elements_located((By.XPATH, '//div[@data-testid="card-container"]')))
    elements_on_last_page = driver.find_elements(By.XPATH, '//div[@data-testid="card-container"]')

    wait.until(EC.presence_of_all_elements_located((By.XPATH, '//a[@class="l1ovpqvx atm_1y33qqm_1ggndnn_10saat9 atm_17zvjtw_zk357r_10saat9 atm_w3cb4q_il40rs_10saat9 atm_1cumors_fps5y7_10saat9 atm_52zhnh_1s82m0i_10saat9 atm_jiyzzr_1d07xhn_10saat9 c1ackr0h atm_c8_fkimz8 atm_g3_11yl58k atm_fr_4ym3tx atm_cs_qo5vgd atm_9s_1txwivl atm_h_1h6ojuz atm_fc_1h6ojuz atm_bb_idpfg4 atm_3f_glywfm atm_5j_1ssbidh atm_26_1j28jx2 atm_7l_ujz1go atm_vy_1vi7ecw atm_e2_1vi7ecw atm_gi_idpfg4 atm_gz_logulu atm_h0_logulu atm_l8_idpfg4 atm_uc_1dtz4sb atm_kd_glywfm atm_uc_glywfm__1rrf6b5 atm_26_rmqrjm_1nos8r_uv4tnr atm_tr_kv3y6q_csw3t1 atm_26_rmqrjm_csw3t1 atm_9j_73adwj_1o5j5ji atm_3f_glywfm_jo46a5 atm_l8_idpfg4_jo46a5 atm_gi_idpfg4_jo46a5 atm_3f_glywfm_1icshfk atm_kd_glywfm_19774hq atm_uc_x37zl0_1w3cfyq atm_26_rmqrjm_1w3cfyq atm_70_1jt8dgi_1w3cfyq atm_uc_glywfm_1w3cfyq_1rrf6b5 atm_uc_x37zl0_18zk5v0 atm_26_rmqrjm_18zk5v0 atm_70_1jt8dgi_18zk5v0 atm_uc_glywfm_18zk5v0_1rrf6b5 dir dir-ltr"]')))
    pages = driver.find_elements(By.XPATH, '//a[@class="l1ovpqvx atm_1y33qqm_1ggndnn_10saat9 atm_17zvjtw_zk357r_10saat9 atm_w3cb4q_il40rs_10saat9 atm_1cumors_fps5y7_10saat9 atm_52zhnh_1s82m0i_10saat9 atm_jiyzzr_1d07xhn_10saat9 c1ackr0h atm_c8_fkimz8 atm_g3_11yl58k atm_fr_4ym3tx atm_cs_qo5vgd atm_9s_1txwivl atm_h_1h6ojuz atm_fc_1h6ojuz atm_bb_idpfg4 atm_3f_glywfm atm_5j_1ssbidh atm_26_1j28jx2 atm_7l_ujz1go atm_vy_1vi7ecw atm_e2_1vi7ecw atm_gi_idpfg4 atm_gz_logulu atm_h0_logulu atm_l8_idpfg4 atm_uc_1dtz4sb atm_kd_glywfm atm_uc_glywfm__1rrf6b5 atm_26_rmqrjm_1nos8r_uv4tnr atm_tr_kv3y6q_csw3t1 atm_26_rmqrjm_csw3t1 atm_9j_73adwj_1o5j5ji atm_3f_glywfm_jo46a5 atm_l8_idpfg4_jo46a5 atm_gi_idpfg4_jo46a5 atm_3f_glywfm_1icshfk atm_kd_glywfm_19774hq atm_uc_x37zl0_1w3cfyq atm_26_rmqrjm_1w3cfyq atm_70_1jt8dgi_1w3cfyq atm_uc_glywfm_1w3cfyq_1rrf6b5 atm_uc_x37zl0_18zk5v0 atm_26_rmqrjm_18zk5v0 atm_70_1jt8dgi_18zk5v0 atm_uc_glywfm_18zk5v0_1rrf6b5 dir dir-ltr"]')
    pages[0].click()
    num_of_all_apartments = (num_of_pages-1)*18 + len(elements_on_last_page)
except:
    elements_on_last_page = driver.find_elements(By.XPATH, '//div[@data-testid="card-container"]')
    num_of_all_apartments = len(elements_on_last_page)
    pass

while more_pages:
    time.sleep(1)
    wait.until(EC.presence_of_all_elements_located((By.XPATH, '//div[@data-testid="card-container"]')))
    elements = driver.find_elements(By.XPATH, '//div[@data-testid="card-container"]')
    for house in elements:

        house_html = house.get_attribute("innerHTML")

        doc = BeautifulSoup(house_html, "html.parser")

        property_name = doc.find("span", attrs={'data-testid': 'listing-card-name'}).text
        property_type = doc.find("div", attrs={'data-testid': 'listing-card-title'}).text
        total_price = doc.find("div", class_="_tt122m").text
        total_price = total_price.replace("total", "")
        rating = doc.find("span", class_="r1dxllyb atm_7l_18pqv07 atm_cp_1ts48j8 dir dir-ltr")
        if rating:
            rating = rating.text
            rating = rating.split(" ")
            rating = str(rating[0])
        else:
            rating = "No rating yet."

        beds_and_bedrooms = doc.find_all("span", class_="dir dir-ltr")

        for bed_or_bedroom in beds_and_bedrooms:
            if "bedroom" in bed_or_bedroom.text or "bedrooms" in bed_or_bedroom.text:
                bedrooms = bed_or_bedroom.text
            else:
                bedrooms = "No info."
                if "bed" in bed_or_bedroom.text or "beds" in bed_or_bedroom.text:
                    beds = bed_or_bedroom.text
                else:
                    beds = "No info."

        assert len(driver.window_handles) == 1
        wait.until(EC.element_to_be_clickable((house)))
        house.click()
        
        wait.until(EC.number_of_windows_to_be(2))

        for tab_handle in driver.window_handles:
            if tab_handle != main_tab:
                driver.switch_to.window(tab_handle)
                break

        if is_true:
            try:
                wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@aria-label="Close"]')))
                btn = driver.find_element(By.XPATH, '//button[@aria-label="Close"]')
                btn.click()
                is_true = False
            except:
                pass

        wait.until(EC.presence_of_all_elements_located((By.XPATH, '//div[@class="is50c2g atm_gq_xvenqj dir dir-ltr"]')))
        check_in_out_max_guests = driver.find_elements(By.XPATH, '//div[@class="is50c2g atm_gq_xvenqj dir dir-ltr"]')

        check_in = "No check-in time."
        check_out = "No checkout time."
        max_guests = "No maximum guests"

        for element in check_in_out_max_guests:
            if "Check-in" in element.text:
                check_in = element.text
            else:
                if "Checkout" in element.text:
                    check_out = element.text
                elif "maximum" in element.text:
                    max_guests = element.text

        night_price = doc.find("span", class_="_1y74zjx")

        if night_price:
            night_price = night_price.text
        else:
            night_price = doc.find("span", class_="_tyxjp1").text

        current_home_page = driver.page_source
        doc = BeautifulSoup(current_home_page, "html.parser")

        self_check_in = doc.find_all("h3", class_="hpipapi atm_7l_1kw7nm4 atm_c8_1x4eueo atm_cs_1kw7nm4 atm_g3_1kw7nm4 atm_gi_idpfg4 atm_l8_idpfg4 atm_kd_idpfg4_pfnrn2 dir dir-ltr")[0].text

        if "Self check-in" not in self_check_in:
            self_check_in = "No self check-in."

        host = doc.find("div", class_="t1pxe1a4 atm_c8_8ycq01 atm_g3_adnk3f atm_fr_rvubnj atm_cs_qo5vgd dir dir-ltr").text
        host = host.split(" ")
        host = host[2]

        try:
            wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@aria-label="Show original"]')))
        except:
            try:
                wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@aria-label="Translate place description"]')))
                translate = driver.find_element(By.XPATH, '//button[@aria-label="Translate place description"]')
                translate.click()
            except:
                pass

        description = doc.find("div", attrs={'data-section-id': 'DESCRIPTION_DEFAULT'}).text

        if description == "":
            description = "No description."
    
        current_house = {'property_name':property_name, 'property_type':property_type, 'night_price':night_price,
                        'total_price':total_price,'beds':beds, 'bedrooms': bedrooms, 'host':host, 'rating':rating, 'check_in':check_in,
                        'check_out':check_out, 'max_guests':max_guests, "self_check_in": self_check_in, "description":description, "url":driver.current_url}

        driver.close()
        driver.switch_to.window(main_tab)

        airbnb_houses[counter] = current_house

        UP = '\033[1A'
        CLEAR = '\x1b[2K'
        print(f'{counter}/{num_of_all_apartments}')
        if counter != num_of_all_apartments:
            print(UP, end=CLEAR)
        counter+=1

    try:
        wait .until(EC.element_to_be_clickable((By.XPATH, '//a[@aria-label="Next"]')))
        next_page = driver.find_element(By.XPATH, '//a[@aria-label="Next"]')
        next_page.click()
    except:
        break

driver.quit()

df = pd.DataFrame(airbnb_houses).T

custom_header = ["Property Name","Property Type","Night Price","Total Price","Beds","Bedrooms" ,"Host","Rating","Check-in","Checkout before","Max guests","Self Check-in","Description","Url"]
df.to_excel('apartments.xlsx', index_label='No.', na_rep='N/A', header=custom_header)