# Import the necessary libraries
import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd

# Setup web page
st.set_page_config(
     page_title="Snowflake Snowpark for Python",
     layout="wide",
     menu_items={
         'Get Help': 'https://developers.snowflake.com',
         'About': "This app is developed by dash[dot]desai[at]snowflake[dot]com"
     }
)

# Set the URL 
repo_anaconda_com_url = 'https://repo.anaconda.com/pkgs/snowflake/'
# Make a GET request to the URL
response = requests.get(repo_anaconda_com_url)
# Parse the HTML content
soup = BeautifulSoup(response.content, 'html.parser')

package_names, package_summaries, package_versions, package_licenses, os1, os2, os3, os4, os5, os6, docs, gits = [],[],[],[],[],[],[],[],[],[],[],[]

packages = soup.find("table").find_all("tr")
for package in packages:
    package_name = package.find("td", class_ = 'packagename')
    if package_name:
        package_names.append(package_name.text)
        package_versions.append(package.find("td", class_ = 'version').text)
        package_licenses.append(package.find("td", class_ = 'license').text)
        package_summaries.append(package.find("td", class_ = 'summary').text)

        os1.append(package.find_all("td")[5].text)
        os2.append(package.find_all("td")[6].text)
        os3.append(package.find_all("td")[7].text)
        os4.append(package.find_all("td")[8].text)
        os5.append(package.find_all("td")[9].text)
        os6.append(package.find_all("td")[10].text)

        docs_link = package.find_all("td")[2].a
        docs.append(f"<a href=\'{docs_link['href']}\' target=\'_blank\'>☞</a>" if docs_link else '')

        gits_link = package.find_all("td")[3].a
        gits.append(f"<a href=\'{gits_link['href']}\' target=\'_blank\'>☞</a>" if gits_link else '')

data = pd.DataFrame(list(zip(package_names,package_versions,package_licenses,os1,os2,os3,os4,os5,os6,package_summaries,docs,gits)),
columns=['Package Name','Latest Version','License','linux-64','linux-aarch64','osx-64','osx-arm64','win-64','noarch','Summary','Docs','GitHub'])

st.subheader(f"Snowflake Snowpark for Python -- Conda Channel with {data.shape[0] - 1} Packages")
st.write("Welcome to the Snowflake conda channel, maintained and supported by Anaconda.", unsafe_allow_html = True)
st.write("This channel has been built for use with <a href='https://www.snowflake.com/snowpark-for-python/'>Snowpark for Python</a>. By accessing or using the contents herein, you acknowledge and agree that you have read, understood, and agree to be bound by the <a href='https://legal.anaconda.com/policies/en/?name=terms-of-service#embedded-end-customer-terms' target='_blank'>Embedded End Customer Terms</a> to <a href='https://legal.anaconda.com/policies/en/?name=terms-of-service' target='_blank'>Anaconda's Terms of Service</a>.", unsafe_allow_html=True)
st.caption(f"App developed by dash.desai@snowflake.com  |  Original Source: https://repo.anaconda.com/pkgs/snowflake/")

with st.expander("Snowpark for Python Resources"):
    st.write("<a href='https://github.com/snowflakedb/snowpark-python'>Source Code</a>", unsafe_allow_html = True)
    st.write("<a href='https://docs.snowflake.com/en/developer-guide/snowpark/python/index.html'>Developer Guide</a>", unsafe_allow_html = True)
    st.write("<a href='https://docs.snowflake.com/en/developer-guide/snowpark/reference/python/index.html'>API Reference</a>", unsafe_allow_html = True)
    st.write("<a href='https://github.com/Snowflake-Labs/snowpark-python-demos'>Demos</a>", unsafe_allow_html = True)

st.write(data.style.set_table_styles([{'selector': 'th', 'props': [('text-align', 'left')]}]).to_html(escape = False), use_container_width=True, unsafe_allow_html = True)
