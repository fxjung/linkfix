# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:light
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.11.4
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# + tags=[]
import re
from urllib import parse as urlparse

# + tags=[]
url = "https://www.amazon.de/-/en/Daniel-Kahneman/dp/0141033576/ref=pd_bxgy_img_2/262-9154491-2481339?pd_rd_w=pCiBU&pf_rd_p=289750ef-2548-403a-9263-64d1c3b3297e&pf_rd_r=2VJBHPB80CGVAHVNEJJH&pd_rd_r=c7627827-98fc-4170-8b85-9f3de2edf6ab&pd_rd_wg=bO9Oz&pd_rd_i=0141033576&psc=1"
# url = "https://www.amazon.de/gp/product/0141983760/ref=ppx_yo_dt_b_asin_title_o01_s00?ie=UTF8&psc=1"
# url = "https://www.amazon.de/-/en/kwmobile-E14-Lamp-Socket-Switch/dp/B08DV3VMGY/?_encoding=UTF8&pd_rd_w=kKEhO&pf_rd_p=b13b9983-c004-46e8-a0ad-74f2b4573e23&pf_rd_r=R3PPNGQHF0R3Y54DBM6T&pd_rd_r=880d9593-5fc1-4dc8-9c60-80c339166a63&pd_rd_wg=LdcAy&ref_=pd_gw_ci_mcx_mr_hp_atf_m"
url = "https://www.amazon.de/Microsoft-Family-Mehrere-Tablets-Jahresabonnement/dp/B09BQ2CDZ2?smid=A3JWKAKR8XB7XF&pf_rd_r=50PWM6A2DJHPEWPDDQCZ&pf_rd_p=3b794984-d134-42bc-b58c-0745841d4769&pd_rd_r=86d3e9e1-205f-4179-a01c-0b0de96f4b30&pd_rd_w=BmxCs&pd_rd_wg=0xnRE&ref_=pd_gw_unk"

# + tags=[]
parsed = urlparse.urlparse(url)
s = parsed.geturl()

hostname = parsed.hostname

if "amazon" in hostname:
    path = parsed.path

    match = re.search(r"/[dg]p/(product/)?([0-9a-zA-Z]+)/?", path)

    asin = match[2]
    new_url = f"https://{hostname}/dp/{asin}/"
new_url

# + tags=[]
path
# -
