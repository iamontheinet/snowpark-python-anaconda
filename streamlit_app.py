# Import the necessary libraries
import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd

# Setup web page
st.set_page_config(
     page_title="Snowpark Python Packages in Snowflake Conda Channel",
     layout="wide",
     menu_items={
         'Get Help': 'https://developers.snowflake.com',
         'About': "This app is developed by dash.desai@snowflake.com"
     }
)

def get_packages_data(url):
    # Make a GET request to the URL
    response = requests.get(repo_anaconda_com_url)
    # Parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')
    packages = soup.find("table").find_all("tr")
    return packages

def write_package_details(col, package, linux_64, linux_aarch64, osx_64, osx_arm64, win_64, noarch):
    p_name = package.find("td", class_ = 'packagename').text
    p_version = package.find("td", class_ = 'version').text
    p_license = package.find("td", class_ = 'license').text
    p_summary = package.find("td", class_ = 'summary').text
    p_docs_link = package.find_all("td")[2].a
    p_gits_link = package.find_all("td")[3].a

    col.subheader(p_name)
    doc_link = f"<a href=\'{p_docs_link['href']}\' target=\'_blank\'>Docs</a>" if p_docs_link else "Docs: N/A"
    git_link = f"<a href=\'{p_gits_link['href']}\' target=\'_blank\'>GitHub</a>" if p_gits_link else "GitHub: N/A"
    docs_and_git_links = f"{doc_link} | {git_link}"
    col.caption(f"Latest version: {p_version} | License: {p_license if p_license else 'N/A'} | {docs_and_git_links}", unsafe_allow_html = True)
    col.caption(f"linux-64: {'✅' if linux_64 else 'N/A'} | linux-aarch64: {'✅' if linux_aarch64 else 'N/A'} | osx-64: {'✅' if osx_64 else 'N/A'} | osx-arm64: {'✅' if osx_arm64 else 'N/A'} | win-64: {'✅' if win_64 else 'N/A'} | noarch: {'✅' if noarch else 'N/A'}")
    col.write(p_summary)
    return 1

def display_data_as_blocks(packages, this_is_a_test=False):
    col1, col2, col3 = st.columns(3, gap='small')
    p_container = st.container()
    col_index = 0
    p_index = 0
    for i in range(0,total_packages):
        package = packages[i]
        package_name = package.find("td", class_ = 'packagename')
        if package_name:
            linux_64 = package.find_all("td")[5].text
            linux_aarch64 = package.find_all("td")[6].text
            osx_64 = package.find_all("td")[7].text
            osx_arm64 = package.find_all("td")[8].text
            win_64 = package.find_all("td")[9].text
            noarch = package.find_all("td")[10].text

            # 'linux-64','linux-aarch64','osx-64','osx-arm64','win-64','noarch'
            if ((linux_64 and p_linux_64) or \
                (linux_aarch64 and p_linux_aarch64) or \
                (osx_64 and p_osx_64) or \
                (osx_arm64 and p_osx_arm64) or \
                (win_64 and p_win_64) or \
                (noarch and p_noarch)):

                with p_container:
                    col = col1 if col_index == 1 else col2 if col_index == 2 else col3
                    p_index += write_package_details(col, package, linux_64, linux_aarch64, osx_64, osx_arm64, win_64, noarch)               

                if (p_index % 3) == 0:
                    col1, col2, col3 = st.columns(3, gap='small')
                    p_container = st.container()
                    col_index = 0
                else:
                    col_index += 1

        if this_is_a_test and p_index == 9:
            break;

st.header(f"Snowpark Python Packages in Snowflake Conda Channel")
st.caption(f"App developed by [Dash](https://twitter.com/iamontheinet)")
st.write(f"This application lists the Python packages from the Snowflake Conda channel that is maintained and supported by Anaconda. The Snowflake Cond channel has been built for use with <a href='https://www.snowflake.com/snowpark-for-python/'>Snowpark for Python</a>. By accessing or using the contents in the channel, you acknowledge and agree that you have read, understood, and agree to be bound by the <a href='https://legal.anaconda.com/policies/en/?name=terms-of-service#embedded-end-customer-terms' target='_blank'>Embedded End Customer Terms</a> to <a href='https://legal.anaconda.com/policies/en/?name=terms-of-service' target='_blank'>Anaconda's Terms of Service</a>.", unsafe_allow_html=True)

repo_anaconda_com_url = 'https://repo.anaconda.com/pkgs/snowflake/'
packages = get_packages_data(repo_anaconda_com_url)
total_packages = len(packages)
st.write(f"Total packages as of today = **{total_packages}**. The curated packages in Snowflake Cond channel are available for you to use in <a href='https://docs.snowflake.com/en/developer-guide/snowpark/python/creating-udfs.html'>User-Defined Functions</a>, <a href='https://docs.snowflake.com/en/developer-guide/udf/python/udf-python-tabular-functions.html'>User-Defined Table Functions</a>, and <a href='https://docs.snowflake.com/en/sql-reference/stored-procedures-python.html'>Stored Procedures</a> after you <a href='https://docs.snowflake.com/en/developer-guide/udf/python/udf-python-packages.html#getting-started'>accept the terms</a>.", unsafe_allow_html=True)

st.markdown("___")
st.caption("Filter packages by platform. (Note: It applies OR operator.)")
with st.container():
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    with col1:
        p_linux_64 = st.checkbox('linux-64',value=True)
    with col2:
        p_linux_aarch64 = st.checkbox('linux-aarch64')
    with col3:
        p_osx_64 = st.checkbox('osx-64')
    with col4:
        p_osx_arm64 = st.checkbox('osx-arm64')
    with col5:
        p_win_64 = st.checkbox('win-64')
    with col6:
        p_noarch = st.checkbox('noarch')

st.markdown("___")
display_data_as_blocks(packages)
st.markdown("---")
st.caption(f"Conda Channel Source: https://repo.anaconda.com/pkgs/snowflake/")

# def organize_data(packages):
#     package_names, package_summaries, package_versions, package_licenses, os1, os2, os3, os4, os5, os6, docs, gits = [],[],[],[],[],[],[],[],[],[],[],[]
#     for package in packages:
#         package_name = package.find("td", class_ = 'packagename')
#         if package_name:
#             package_names.append(package_name.text)
#             package_versions.append(package.find("td", class_ = 'version').text)
#             package_licenses.append(package.find("td", class_ = 'license').text)
#             package_summaries.append(package.find("td", class_ = 'summary').text)

#             os1.append(package.find_all("td")[5].text)
#             os2.append(package.find_all("td")[6].text)
#             os3.append(package.find_all("td")[7].text)
#             os4.append(package.find_all("td")[8].text)
#             os5.append(package.find_all("td")[9].text)
#             os6.append(package.find_all("td")[10].text)

#             docs_link = package.find_all("td")[2].a
#             docs.append(f"<a href=\'{docs_link['href']}\' target=\'_blank\'>☞</a>" if docs_link else '')

#             gits_link = package.find_all("td")[3].a
#             gits.append(f"<a href=\'{gits_link['href']}\' target=\'_blank\'>☞</a>" if gits_link else '')

#     data = pd.DataFrame(list(zip(package_names,package_versions,package_licenses,os1,os2,os3,os4,os5,os6,package_summaries,docs,gits)),
#     columns=['Package Name','Latest Version','License','linux-64','linux-aarch64','osx-64','osx-arm64','win-64','noarch','Summary','Docs','GitHub'])
#     return data

# def display_data_as_list(data):
#     st.write(data.style.set_table_styles([{'selector': 'th', 'props': [('text-align', 'left')]}]).to_html(escape = False), use_container_width=True, unsafe_allow_html = True)

# with st.container():
#     st.subheader(f"Snowpark for Python Resources")
#     st.write("<a href='https://github.com/snowflakedb/snowpark-python'>Source Code</a>", unsafe_allow_html = True)
#     st.write("<a href='https://docs.snowflake.com/en/developer-guide/snowpark/python/index.html'>Developer Guide</a>", unsafe_allow_html = True)
#     st.write("<a href='https://docs.snowflake.com/en/developer-guide/snowpark/reference/python/index.html'>API Reference</a>", unsafe_allow_html = True)
#     st.write("<a href='https://github.com/Snowflake-Labs/snowpark-python-demos'>Demos</a>", unsafe_allow_html = True)