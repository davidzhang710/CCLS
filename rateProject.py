import streamlit as st
import pandas as pd
import time

def findHeader(df):
    newList = []
    for i in range(0,len(df.index)-1):
        counter = 0
        for cell in df.iloc[i]:
            if pd.isnull(cell):
                counter += 1
        newList.append(counter)
    minVal = min(newList)
    firstindex = newList.index(minVal)
    lastindex = len(newList) - newList[::-1].index(minVal)
    df.columns = df.iloc[firstindex]
    df = df[firstindex+1:lastindex]
    return df

def GRIdf(df,GRI):
    for i in range(0, len(df.index) - 1):
        for index, cell in enumerate(df.iloc[i]):
            if type(cell) is int or type(cell) is float:
                df.iat[i, index] = cell * (1+GRI/100)
    return df

st.set_page_config(layout="wide")
st.title("Rate Table Generator")
uploaded_file = st.file_uploader("Choose a file")
current, proposed = st.tabs(['Current','Proposed'])
with st.sidebar:
    st.title("Options Manager")

    if uploaded_file is not None:
        GRI = st.slider("GRI %",0,20)
        st.button("Apply GRI")
        st.write("---")
        st.checkbox("Include Standard Headers")
        st.checkbox("Apply Standard Accessorials")

if uploaded_file is not None:
    with current:
        data = pd.read_excel(uploaded_file)
        df = findHeader(data)
        st.dataframe(df)
    with proposed:
        if GRI == 0:
            st.warning("Please select GRI %")
        else:
            st.success(f'A GRI of {GRI}% have been applied.')
            downloaddf = GRIdf(df,GRI)
            if st.button("Save Data"):
                with st.spinner(text="In progress..."):
                    time.sleep(3)
                    downloaddf.to_excel("Rate Table.xlsx", index = False, header = True)
                    with open("Rate Table.xlsx", 'rb') as my_file:
                        st.download_button(label='Download', data=my_file, file_name='Rate Table.xlsx',
                                       mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            st.dataframe(downloaddf)

