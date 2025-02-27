#Libraries Used
import re
import pdfplumber
import pandas as pd
from collections import namedtuple
import streamlit as st

#WEB APP title
st.title("PDF Table Extractor")

#file input stored as uploaded_file
uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])


#Release_Details function
def Release_Details(uploaded_file):
    ReleaseDetail = namedtuple('ReleaseDetail',
                               ['Item', 'Material', 'Package', 'Full_TrCd', 'Lot_Num', 'Target_Qty_U_M', 'CRD',
                                'Unit_Price',
                                'Net_Value', 'Arena_Item_No', 'Config_No', 'Latest_Pkg_No'])


    Release_Detail = []

    #REGEX for fetching Release_Details DATA
    pattern1 = re.compile(
        r"^(?P<Item>\d+)\s+"                  
        r"(?P<Material>[A-Z0-9-]+)"
        r"(?P<Package>\s)"
        r"(?P<Full_TrCd>[A-Z0-9]+)\s+"
        r"(?P<Lot_Num>[\d.]+)\s+"
        r"(?P<Target_qty>\d+)\s*EA\s+"
        r"(?P<CRD>\d{2}/\d{2}/\d{4})\s+"
        r"(?P<Unit_Price>[\d.]+)\s+"
        r"(?P<Net_Value>[\d.,]+)"
    )
    pattern1_2 = re.compile(r"Arena Item No.:\s*(.*)")
    pattern1_3 = re.compile(r"Config No:\d*(.*)")
    pattern1_4 = re.compile(r"Latest Pkg Revision.:\s*(.*)")

    with pdfplumber.open(uploaded_file) as pdf:
        for page in pdf.pages:
            text = page.extract_text()

            if 'Release Details' in text:
                lines = text.split('\n')
                for line in lines:
                    match = pattern1_2.search(line)
                    if match:
                        Arena_t = match.group(1)

            if 'Release Details' in text:
                lines = text.split('\n')
                for line in lines:
                    match = pattern1_3.search(line)
                    if match:
                        Config_t = match.group(1)

            if 'Release Details' in text:
                lines = text.split('\n')
                for line in lines:
                    match = pattern1_4.search(line)
                    if match:
                        Latest_t = match.group(1)

            if 'Release Details' in text:
                lines = text.split('\n')
                for line in lines:
                    match = pattern1.search(line)
                    if match:
                        item_t = match.group(1)
                        material_t = match.group(2)
                        package_t = match.group(3)
                        Full_Tr_t = {match.group(4)}
                        Lot_Num_t = match.group(5)
                        Target_Quantity = match.group(6)
                        CRD_t = match.group(7)
                        Uni_P_t = match.group(8)
                        Net_val_t = match.group(9)

                        Release_Detail.append(ReleaseDetail(item_t,
                                                            material_t,
                                                            package_t,
                                                            Full_Tr_t,
                                                            Lot_Num_t,
                                                            Target_Quantity,
                                                            CRD_t,
                                                            Uni_P_t,
                                                            Net_val_t,
                                                            Arena_t,
                                                            Config_t,
                                                            Latest_t
                                                            ))
    df = pd.DataFrame(Release_Detail)
    df.set_index('Item', inplace=True)
    df = df.fillna('')
    st.write(df)


#Component_Details function
def Component_Details(uploaded_file):

    ComponentDetail = namedtuple('ComponentDetail',
                                 ['Item', 'Comp_TraceCode', 'Comp_Batch', 'Comp_Qty', 'Comp_Mat_No',
                                  'Comp_Ordering_Part','Markings'])

    Component_Detail = []

    # REGEX for fetching Component_Details DATA
    pattern2 = re.compile(
        r"^(?P<Item>[1-9])?\s*"
        r"(?P<TraceCode>[A-Z0-9-]{10})\s+"
        r"(?P<Comp_batch>\d+\.\d+)?\s*"
        r"(?P<Comp_Qty>\d+)?\s*" 
        r"(?P<Comp_Mat>[A-Z0-9-]+)?\s*"
        r"(?P<Comp_Order>[A-Z0-9-]*)?\s*"
        r"(?P<Marking>Mfg code :.*)?\s*$"
    )

    with pdfplumber.open(uploaded_file) as pdf:
        for page in pdf.pages:
            text = page.extract_text()

            if 'Component Details' in text:
                lines = text.split('\n')
                for line in lines:
                    match = pattern2.search(line)
                    if match:
                        item_t1 = match.group(1)
                        trace_t1 = match.group(2)
                        batch_t1 = match.group(3)
                        qty_t1 = match.group(4)
                        Mat_t1 = match.group(5)
                        ordering_t1 = match.group(6)
                        Marking_t1 = match.group(7)

                        Component_Detail.append(ComponentDetail(item_t1,
                                                                trace_t1,
                                                                batch_t1,
                                                                qty_t1,
                                                                Mat_t1,
                                                                ordering_t1,
                                                                Marking_t1
                                                                ))
        df = pd.DataFrame(Component_Detail)
        df.set_index('Item',inplace = True)
        df = df.fillna('')
        df.index = df.index.fillna(' ')
        st.write(df)


#Release_Details table button
if st.button("Extract: Release Details"):
    Release_Details(uploaded_file)

#Component_Details table button
if st.button("Extract: Component Details"):
    Component_Details(uploaded_file)

clear = st.empty()
col1, col2 = st.columns([3, 1])
with col2:
    if st.button("Clear Output"):
        clear.empty()
        #2.502
        #2.5020000000000095
        #