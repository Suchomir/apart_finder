from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

opt = Options()
opt.add_argument("--disable-infobars")
opt.add_argument("start-maximized")
opt.add_argument("--disable-extensions")
opt.add_experimental_option(
            "detach", True)


driver = webdriver.Chrome(options=opt)

#Property IDs: 0-any 1-house 2-guesthouse 3-apartment 4-hotel
#Room type: 0-any 1-Private room 2-Entire house/apartment

# Room Types
rooms = {0:'', 1:'&room_types%5B%5D=Private%20room', 2:'&room_types%5B%5D=Entire%20home%2Fapt'}

# Example Data
city = 'Szczecin'
country = 'Poland'
check_in = '2024-03-15'
check_out = '2024-03-17'
adults = 2
children = 0
infants = 0
pets = 0
currency_type = 'USD'
price_min = 50
price_max = 10000
property_type_num = 0
room = 0
nights = int(check_out.split('-')[2]) - int(check_in.split('-')[2])
wait_3_sec = WebDriverWait(driver, 3)

#Set language and currency

driver.get("https://airbnb.com")

wait_3_sec.until(EC.element_to_be_clickable((By.CLASS_NAME, "_z5mecy")))

select_language_currency = driver.find_element(By.CLASS_NAME, "_z5mecy")
select_language_currency.click()

wait_3_sec.until(EC.element_to_be_clickable((By.XPATH, "//*[text()='United States']")))

language = driver.find_element(By.XPATH, "//div[text()='United States']")
language.click()

# wait_3_sec.until(EC.element_to_be_clickable((By.CLASS_NAME, "_z5mecy")))

# select_language_currency = driver.find_element(By.CLASS_NAME, "_z5mecy")
# select_language_currency.click()

# wait_3_sec.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Currency']")))

# select_currency = driver.find_element(By.XPATH, "//button[text()='Currency']")
# select_currency.click() 

# wait_3_sec.until(EC.element_to_be_clickable((By.XPATH,f"//div[starts-with(.,'{currency_type}')]")))

# currency = driver.find_element(By.XPATH,f"//div[starts-with(.,'{currency_type}')]")
# currency.click()

# Go to our main page
driver.get(f'https://www.airbnb.com/s/{city}--{country}/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&query={city}%2C%20{country}&date_picker_type=calendar&checkin={check_in}&checkout={check_out}&adults={adults}&children={children}&infants={infants}&pets={pets}&source=structured_search_input_header&search_type=filter_change&price_filter_num_nights={nights}&l2_property_type_ids%5B%5D={property_type_num}&price_min={price_min}&price_max={price_max}{rooms[room]}')
main_tab = driver.current_window_handle
airbnb_houses = {}
# Get data from houses
more_pages = True
is_true = True
counter = 1
# Get number of all apartments
wait_3_sec.until(EC.presence_of_all_elements_located((By.XPATH, '//a[@class="l1ovpqvx atm_1y33qqm_1ggndnn_10saat9 atm_17zvjtw_zk357r_10saat9 atm_w3cb4q_il40rs_10saat9 atm_1cumors_fps5y7_10saat9 atm_52zhnh_1s82m0i_10saat9 atm_jiyzzr_1d07xhn_10saat9 c1ackr0h atm_c8_fkimz8 atm_g3_11yl58k atm_fr_4ym3tx atm_cs_qo5vgd atm_9s_1txwivl atm_h_1h6ojuz atm_fc_1h6ojuz atm_bb_idpfg4 atm_3f_glywfm atm_5j_1ssbidh atm_26_1j28jx2 atm_7l_ujz1go atm_vy_1vi7ecw atm_e2_1vi7ecw atm_gi_idpfg4 atm_gz_logulu atm_h0_logulu atm_l8_idpfg4 atm_uc_1dtz4sb atm_kd_glywfm atm_uc_glywfm__1rrf6b5 atm_26_rmqrjm_1nos8r_uv4tnr atm_tr_kv3y6q_csw3t1 atm_26_rmqrjm_csw3t1 atm_9j_73adwj_1o5j5ji atm_3f_glywfm_jo46a5 atm_l8_idpfg4_jo46a5 atm_gi_idpfg4_jo46a5 atm_3f_glywfm_1icshfk atm_kd_glywfm_19774hq atm_uc_x37zl0_1w3cfyq atm_26_rmqrjm_1w3cfyq atm_70_1jt8dgi_1w3cfyq atm_uc_glywfm_1w3cfyq_1rrf6b5 atm_uc_x37zl0_18zk5v0 atm_26_rmqrjm_18zk5v0 atm_70_1jt8dgi_18zk5v0 atm_uc_glywfm_18zk5v0_1rrf6b5 dir dir-ltr"]')))
pages = driver.find_elements(By.XPATH, '//a[@class="l1ovpqvx atm_1y33qqm_1ggndnn_10saat9 atm_17zvjtw_zk357r_10saat9 atm_w3cb4q_il40rs_10saat9 atm_1cumors_fps5y7_10saat9 atm_52zhnh_1s82m0i_10saat9 atm_jiyzzr_1d07xhn_10saat9 c1ackr0h atm_c8_fkimz8 atm_g3_11yl58k atm_fr_4ym3tx atm_cs_qo5vgd atm_9s_1txwivl atm_h_1h6ojuz atm_fc_1h6ojuz atm_bb_idpfg4 atm_3f_glywfm atm_5j_1ssbidh atm_26_1j28jx2 atm_7l_ujz1go atm_vy_1vi7ecw atm_e2_1vi7ecw atm_gi_idpfg4 atm_gz_logulu atm_h0_logulu atm_l8_idpfg4 atm_uc_1dtz4sb atm_kd_glywfm atm_uc_glywfm__1rrf6b5 atm_26_rmqrjm_1nos8r_uv4tnr atm_tr_kv3y6q_csw3t1 atm_26_rmqrjm_csw3t1 atm_9j_73adwj_1o5j5ji atm_3f_glywfm_jo46a5 atm_l8_idpfg4_jo46a5 atm_gi_idpfg4_jo46a5 atm_3f_glywfm_1icshfk atm_kd_glywfm_19774hq atm_uc_x37zl0_1w3cfyq atm_26_rmqrjm_1w3cfyq atm_70_1jt8dgi_1w3cfyq atm_uc_glywfm_1w3cfyq_1rrf6b5 atm_uc_x37zl0_18zk5v0 atm_26_rmqrjm_18zk5v0 atm_70_1jt8dgi_18zk5v0 atm_uc_glywfm_18zk5v0_1rrf6b5 dir dir-ltr"]')
num_of_pages = int(pages[-1].text)
pages[-1].click()
wait_3_sec.until(EC.presence_of_all_elements_located((By.XPATH, '//div[@data-testid="card-container"]')))
elements_on_last_page = driver.find_elements(By.XPATH, '//div[@data-testid="card-container"]')

wait_3_sec.until(EC.presence_of_all_elements_located((By.XPATH, '//a[@class="l1ovpqvx atm_1y33qqm_1ggndnn_10saat9 atm_17zvjtw_zk357r_10saat9 atm_w3cb4q_il40rs_10saat9 atm_1cumors_fps5y7_10saat9 atm_52zhnh_1s82m0i_10saat9 atm_jiyzzr_1d07xhn_10saat9 c1ackr0h atm_c8_fkimz8 atm_g3_11yl58k atm_fr_4ym3tx atm_cs_qo5vgd atm_9s_1txwivl atm_h_1h6ojuz atm_fc_1h6ojuz atm_bb_idpfg4 atm_3f_glywfm atm_5j_1ssbidh atm_26_1j28jx2 atm_7l_ujz1go atm_vy_1vi7ecw atm_e2_1vi7ecw atm_gi_idpfg4 atm_gz_logulu atm_h0_logulu atm_l8_idpfg4 atm_uc_1dtz4sb atm_kd_glywfm atm_uc_glywfm__1rrf6b5 atm_26_rmqrjm_1nos8r_uv4tnr atm_tr_kv3y6q_csw3t1 atm_26_rmqrjm_csw3t1 atm_9j_73adwj_1o5j5ji atm_3f_glywfm_jo46a5 atm_l8_idpfg4_jo46a5 atm_gi_idpfg4_jo46a5 atm_3f_glywfm_1icshfk atm_kd_glywfm_19774hq atm_uc_x37zl0_1w3cfyq atm_26_rmqrjm_1w3cfyq atm_70_1jt8dgi_1w3cfyq atm_uc_glywfm_1w3cfyq_1rrf6b5 atm_uc_x37zl0_18zk5v0 atm_26_rmqrjm_18zk5v0 atm_70_1jt8dgi_18zk5v0 atm_uc_glywfm_18zk5v0_1rrf6b5 dir dir-ltr"]')))
pages = driver.find_elements(By.XPATH, '//a[@class="l1ovpqvx atm_1y33qqm_1ggndnn_10saat9 atm_17zvjtw_zk357r_10saat9 atm_w3cb4q_il40rs_10saat9 atm_1cumors_fps5y7_10saat9 atm_52zhnh_1s82m0i_10saat9 atm_jiyzzr_1d07xhn_10saat9 c1ackr0h atm_c8_fkimz8 atm_g3_11yl58k atm_fr_4ym3tx atm_cs_qo5vgd atm_9s_1txwivl atm_h_1h6ojuz atm_fc_1h6ojuz atm_bb_idpfg4 atm_3f_glywfm atm_5j_1ssbidh atm_26_1j28jx2 atm_7l_ujz1go atm_vy_1vi7ecw atm_e2_1vi7ecw atm_gi_idpfg4 atm_gz_logulu atm_h0_logulu atm_l8_idpfg4 atm_uc_1dtz4sb atm_kd_glywfm atm_uc_glywfm__1rrf6b5 atm_26_rmqrjm_1nos8r_uv4tnr atm_tr_kv3y6q_csw3t1 atm_26_rmqrjm_csw3t1 atm_9j_73adwj_1o5j5ji atm_3f_glywfm_jo46a5 atm_l8_idpfg4_jo46a5 atm_gi_idpfg4_jo46a5 atm_3f_glywfm_1icshfk atm_kd_glywfm_19774hq atm_uc_x37zl0_1w3cfyq atm_26_rmqrjm_1w3cfyq atm_70_1jt8dgi_1w3cfyq atm_uc_glywfm_1w3cfyq_1rrf6b5 atm_uc_x37zl0_18zk5v0 atm_26_rmqrjm_18zk5v0 atm_70_1jt8dgi_18zk5v0 atm_uc_glywfm_18zk5v0_1rrf6b5 dir dir-ltr"]')
pages[0].click()

num_of_all_apartments = (num_of_pages-1)*18 + len(elements_on_last_page)

while more_pages:
    wait_3_sec.until(EC.presence_of_all_elements_located((By.XPATH, '//div[@data-testid="card-container"]')))
    elements = driver.find_elements(By.XPATH, '//div[@data-testid="card-container"]')
    for house in elements:

        assert len(driver.window_handles) == 1
        wait_3_sec.until(EC.element_to_be_clickable((house)))
        house.click()
        

        wait_3_sec.until(EC.number_of_windows_to_be(2))

        for tab_handle in driver.window_handles:
            if tab_handle != main_tab:
                driver.switch_to.window(tab_handle)
                break

        if is_true:
            wait_3_sec.until(EC.element_to_be_clickable((By.XPATH, '//button[@aria-label="Close"]')))
            btn = driver.find_element(By.XPATH, '//button[@aria-label="Close"]')
            btn.click()
            is_true = False
 
        wait_3_sec.until(EC.presence_of_element_located((By.XPATH, '//h1[@class="hpipapi atm_7l_1kw7nm4 atm_c8_1x4eueo atm_cs_1kw7nm4 atm_g3_1kw7nm4 atm_gi_idpfg4 atm_l8_idpfg4 atm_kd_idpfg4_pfnrn2 i1pmzyw7 atm_9s_1nu9bjl dir dir-ltr"]')))
        property_name = driver.find_element(By.XPATH, '//h1[@class="hpipapi atm_7l_1kw7nm4 atm_c8_1x4eueo atm_cs_1kw7nm4 atm_g3_1kw7nm4 atm_gi_idpfg4 atm_l8_idpfg4 atm_kd_idpfg4_pfnrn2 i1pmzyw7 atm_9s_1nu9bjl dir dir-ltr"]').text
        wait_3_sec.until(EC.presence_of_element_located((By.XPATH, '//h1[@class="hpipapi atm_7l_1kw7nm4 atm_c8_1x4eueo atm_cs_1kw7nm4 atm_g3_1kw7nm4 atm_gi_idpfg4 atm_l8_idpfg4 atm_kd_idpfg4_pfnrn2 dir dir-ltr"]')))
        property_type = driver.find_element(By.XPATH, '//h1[@class="hpipapi atm_7l_1kw7nm4 atm_c8_1x4eueo atm_cs_1kw7nm4 atm_g3_1kw7nm4 atm_gi_idpfg4 atm_l8_idpfg4 atm_kd_idpfg4_pfnrn2 dir dir-ltr"]').text
    
        try:
            wait_3_sec.until(EC.presence_of_all_elements_located((By.XPATH, '//span[@class="_tyxjp1"]')))
            night_price = driver.find_elements(By.XPATH, '//span[@class="_tyxjp1"]')[1].text
        except:
            try:
                wait_3_sec.until(EC.presence_of_all_elements_located((By.XPATH, '//span[@class="_1y74zjx"]')))
                night_price = driver.find_elements(By.XPATH, '//span[@class="_1y74zjx"]')[1].text
            except:
                continue

        wait_3_sec.until(EC.presence_of_element_located((By.XPATH, '//span[@class="_j1kt73"]')))
        total_price = driver.find_elements(By.XPATH, '//span[@class="_j1kt73"]')[1].text
        host = driver.find_element(By.XPATH, '//div[@class="t1pxe1a4 atm_c8_8ycq01 atm_g3_adnk3f atm_fr_rvubnj atm_cs_qo5vgd dir dir-ltr"]').text.split()[2:]
        host = ' '.join(host)

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        try:
            wait_3_sec.until(EC.presence_of_element_located((By.XPATH, '//span[@class="_tyxjp1"]')))
            rating = driver.find_element(By.XPATH, '//span[@class="_12si43g"]').text.replace('·','')
        except:
            rating = "No rating yet"

        wait_3_sec.until(EC.presence_of_all_elements_located((By.XPATH, '//div[@class="is50c2g atm_gq_xvenqj dir dir-ltr"]')))
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
                    

        wait_3_sec.until(EC.presence_of_all_elements_located((By.XPATH, '//h3[@class="hpipapi atm_7l_1kw7nm4 atm_c8_1x4eueo atm_cs_1kw7nm4 atm_g3_1kw7nm4 atm_gi_idpfg4 atm_l8_idpfg4 atm_kd_idpfg4_pfnrn2 dir dir-ltr"]')))
        self_check_in = driver.find_elements(By.XPATH, '//h3[@class="hpipapi atm_7l_1kw7nm4 atm_c8_1x4eueo atm_cs_1kw7nm4 atm_g3_1kw7nm4 atm_gi_idpfg4 atm_l8_idpfg4 atm_kd_idpfg4_pfnrn2 dir dir-ltr"]')[0].text

        is_self_check_in = False
        if "check-in" in self_check_in:
            is_self_check_in = True

        driver.execute_script("window.scrollTo(document.body.scrollHeight, 0);")

        try:
            wait_3_sec.until(EC.element_to_be_clickable((By.XPATH, '//button[@aria-label="Translate place description"]')))
            translate = driver.find_element(By.XPATH, '//button[@aria-label="Translate place description"]')
            translate.click()
        except:
            pass

        wait_3_sec.until(EC.presence_of_all_elements_located((By.XPATH, '//span[@class="cn5lml1 dir dir-ltr"]')))
        show_more = driver.find_elements(By.XPATH, '//span[@class="cn5lml1 dir dir-ltr"]')

        if len(show_more) == 4:
            wait_3_sec.until(EC.element_to_be_clickable((show_more[0])))
            show_more[0].click()

        try:
            wait_3_sec.until(EC.presence_of_element_located((By.XPATH, '//div[@data-section-id="DESCRIPTION_MODAL"]')))
            description = driver.find_element(By.XPATH, '//div[@data-section-id="DESCRIPTION_MODAL"]').text
            wait_3_sec.until(EC.element_to_be_clickable((By.XPATH, '//button[@aria-label="Close"]')))
            btn = driver.find_element(By.XPATH, '//button[@aria-label="Close"]')
            btn.click()
        except:
            try:
                description = driver.find_element(By.XPATH, '//div[@data-section-id="DESCRIPTION_DEFAULT"]').text
                wait_3_sec.until(EC.element_to_be_clickable((By.XPATH, '//button[@aria-label="Close"]')))
                btn = driver.find_element(By.XPATH, '//button[@aria-label="Close"]')
                btn.click()
            except:
                pass

        current_house = {'property_name':property_name, 'property_type':property_type, 'night_price':night_price,
                        'total_price':total_price,'host':host, 'rating':rating, 'check_in':check_in,
                        'check_out':check_out, 'max_guests':max_guests, "self_check_in":str(is_self_check_in), "description":description, "url":driver.current_url}

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
        wait_3_sec.until(EC.element_to_be_clickable((By.XPATH, '//a[@aria-label="Next"]')))
        next_page = driver.find_element(By.XPATH, '//a[@aria-label="Next"]')
        next_page.click()
    except:
        break

driver.quit()

df = pd.DataFrame(airbnb_houses).T

custom_header = ["Property Name","Property Type","Night Price","Total Price","Host","Rating","Check-in","Checkout before","Max guests","Self Check-in","Description","Url"]
df.to_excel('apartments.xlsx', index_label='No.', na_rep='N/A', header=custom_header)
