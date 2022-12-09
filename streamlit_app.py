# Import the necessary libraries
import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd

APP_ICON_URL = "snowpark-icon.png"

# Setup web page
st.set_page_config(
     page_title="Snowpark Python Packages in Snowflake Conda Channel",
     page_icon=APP_ICON_URL,
     layout="wide",
     menu_items={
         'Get Help': 'https://developers.snowflake.com',
         'About': "The source code for this application can be accessed on GitHub https://github.com/iamontheinet/snowpark-python-anaconda"
     }
)

st.markdown("""
    <style type="text/css">
    blockquote {
        margin: 1em 0px 1em -1px;
        padding: 0px 0px 0px 1.2em;
        font-size: 20px;
        border-left: 5px solid rgb(230, 234, 241);
        # background-color: rgb(129, 164, 182);
    }
    blockquote p {
        font-size: 30px;
        color: #FFFFFF;
    }
    [data-testid=stSidebar] {
        background-color: rgb(129, 164, 182);
        color: #FFFFFF;
    }
    [aria-selected="true"] {
         color: #000000;
    }
    </style>
""", unsafe_allow_html=True)

def get_packages_data(url):
    response = requests.get(repo_anaconda_com_url)
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

    col.markdown(" > " + p_name)
    doc_link = f"<a href=\'{p_docs_link['href']}\' target=\'_blank\'>Docs</a>" if p_docs_link else "Docs: N/A"
    git_link = f"<a href=\'{p_gits_link['href']}\' target=\'_blank\'>GitHub</a>" if p_gits_link else "GitHub: N/A"
    docs_and_git_links = f"{doc_link} | {git_link}"
    col.caption(f"Latest version: {p_version} | License: {p_license if p_license else 'N/A'} | {docs_and_git_links}", unsafe_allow_html = True)
    col.caption(f"linux-64: {'✅' if linux_64 else 'N/A'} | linux-aarch64: {'✅' if linux_aarch64 else 'N/A'} | osx-64: {'✅' if osx_64 else 'N/A'} | osx-arm64: {'✅' if osx_arm64 else 'N/A'} | win-64: {'✅' if win_64 else 'N/A'} | noarch: {'✅' if noarch else 'N/A'}")
    col.write(p_summary)

def display_all_packages_as_blocks(this_is_a_test=False):
    col1, col2, col3 = st.columns(3, gap='small')
    p_container = st.container()
    col_index = 0
    p_index = 0
    total_packages = len(packages)
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

            with p_container:
                col = col1 if col_index == 1 else col2 if col_index == 2 else col3
                write_package_details(col, package, linux_64, linux_aarch64, osx_64, osx_arm64, win_64, noarch)   
                p_index += 1            

            if (p_index % 3) == 0:
                col1, col2, col3 = st.columns(3, gap='small')
                p_container = st.container()
                col_index = 0
            else:
                col_index += 1

        if this_is_a_test and p_index == 9:
            break;

def display_packages_as_blocks():
    col1, col2, col3 = st.columns(3, gap='small')
    p_container = st.container()
    col_index = 0

    if 'p_start' not in st.session_state:
        st.session_state['p_start'] = 1
        st.session_state['p_end'] = 400
        st.session_state['p_total'] = len(packages)
    else:
        st.session_state['p_start'] += 400
        st.session_state['p_end'] = st.session_state['p_start'] + 400

    p_total = st.session_state['p_total']
    p_start = st.session_state['p_start']
    p_end = st.session_state['p_end'] if st.session_state['p_end'] < p_total else p_total

    for i in range(p_start,p_end):
        package = packages[i]
        package_name = package.find("td", class_ = 'packagename')
        linux_64 = package.find_all("td")[5].text
        linux_aarch64 = package.find_all("td")[6].text
        osx_64 = package.find_all("td")[7].text
        osx_arm64 = package.find_all("td")[8].text
        win_64 = package.find_all("td")[9].text
        noarch = package.find_all("td")[10].text

        with p_container:
            col = col1 if col_index == 0 else col2 if col_index == 1 else col3
            write_package_details(col, package, linux_64, linux_aarch64, osx_64, osx_arm64, win_64, noarch)             

        if (i % 3) == 0:
            col1, col2, col3 = st.columns(3, gap='small')
            p_container = st.container()
            col_index = 0
        else:
            col_index += 1

    st.markdown("---")
    st.caption(f"Packages {p_start} to {p_end-1} of {p_total} | Conda Channel Source: https://repo.anaconda.com/pkgs/snowflake/")

repo_anaconda_com_url = 'https://repo.anaconda.com/pkgs/snowflake/'
packages = get_packages_data(repo_anaconda_com_url)

page_names_to_funcs = {
    "Load packages 1 to 400": display_packages_as_blocks,
    "Load packages 401 to 800": display_packages_as_blocks,
    "Load packages 801 to 1200": display_packages_as_blocks,
    "Load packages 1201 to 1600": display_packages_as_blocks   
}
selected_page = st.sidebar.selectbox("Select range", page_names_to_funcs.keys())
st.sidebar.markdown("---")
st.sidebar.write(f"Note: For a complete list and latest version of packages available, run SQL *'SELECT package_name, max(version) FROM \"INFORMATION_SCHEMA\".\"PACKAGES\" WHERE LANGUAGE = \"python\" GROUP BY package_name ORDER BY 1*' in <a href='https://docs.snowflake.com/en/user-guide/ui-snowsight.html'>Snowsight</a> in your Snowflake account.", unsafe_allow_html = True)

with st.container():
    col1,col2,_,_ = st.columns([1,14,1,1],gap="large")
    with col1:
        st.image(APP_ICON_URL, width=80)
    with col2:
        st.header(f"Snowpark Python Packages in Snowflake Conda Channel")
st.caption(f"App developed by [Dash](https://twitter.com/iamontheinet)")
st.write(f"This application lists the Python packages from the Snowflake Conda channel that is maintained and supported by Anaconda. The Snowflake Conda channel has been built for use with <a href='https://www.snowflake.com/snowpark-for-python/'>Snowpark for Python</a>. By accessing or using the contents in the channel, you acknowledge and agree that you have read, understood, and agree to be bound by the <a href='https://legal.anaconda.com/policies/en/?name=terms-of-service#embedded-end-customer-terms' target='_blank'>Embedded End Customer Terms</a> to <a href='https://legal.anaconda.com/policies/en/?name=terms-of-service' target='_blank'>Anaconda's Terms of Service</a>.", unsafe_allow_html=True)
st.write(f"The curated packages in Snowflake Conda channel are available for you to use in <a href='https://docs.snowflake.com/en/developer-guide/snowpark/python/creating-udfs.html'>User-Defined Functions</a>, <a href='https://docs.snowflake.com/en/developer-guide/udf/python/udf-python-tabular-functions.html'>User-Defined Table Functions</a>, and <a href='https://docs.snowflake.com/en/sql-reference/stored-procedures-python.html'>Stored Procedures</a> after you <a href='https://docs.snowflake.com/en/developer-guide/udf/python/udf-python-packages.html#getting-started'>accept the terms</a>.", unsafe_allow_html=True)
st.markdown("___")

page_names_to_funcs[selected_page]()


# -------------
# st.markdown("___")
# st.caption("If you're developing locally, you can filter packages by platform. (Note: It applies an OR operator between the selected platforms.)")
# with st.container():
#     cols = st.columns(6)
#     oss = ['linux-64','linux-aarch64','osx-64','osx-arm64','win-64','noarch']
#     os_chk = []
#     for i, (col,os) in enumerate(zip(cols,oss)):
#         with col:
#             os_chk.append(st.checkbox(os,value=True) if i == 0 else st.checkbox(os))
