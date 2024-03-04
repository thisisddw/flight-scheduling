import sys
if "." not in sys.path:
    sys.path.append(".")

import streamlit as st
import pandas as pd
from data_analysis.record import RecordIterator, Unique, to_df_data
from io import StringIO
from itertools import chain

uploaded_files = st.file_uploader("上传log文件", type='log', accept_multiple_files=True)

@st.cache_data
def get_records(uploaded_files):
    text_ios = [StringIO(uploaded_file.getvalue().decode("utf-8")) for uploaded_file in uploaded_files]
    records = list(Unique(chain(*[RecordIterator(text_io) for text_io in text_ios])))
    return records

if len(uploaded_files) > 0:
    records = get_records(uploaded_files)

    flights_cnt = {}
    fields_cnt = {}
    for r in records:
        if r.adex['ARCID'] not in flights_cnt:
            flights_cnt[r.adex['ARCID']] = 0
        flights_cnt[r.adex['ARCID']] += 1
        for k, v in r.adex.items():
            if v != '':
                if k not in fields_cnt:
                    fields_cnt[k] = 0
                fields_cnt[k] += 1
            
    flights = sorted(list(flights_cnt.keys()), key = lambda x: flights_cnt[x], reverse=True)
    flights = [f'{f} ({flights_cnt[f]})' for f in flights]
    fields = sorted(list(fields_cnt.keys()), key = lambda x: fields_cnt[x], reverse=True)
    fields = [f'{f} ({fields_cnt[f]})' for f in fields]

    flights_shown = st.multiselect('选择航班', flights, default=flights[:3])
    fields_shown = st.multiselect('选择属性', fields, default=fields[:5])

    flights_shown = [x.split(' ')[0] for x in flights_shown]
    fields_shown = [x.split(' ')[0] for x in fields_shown]

    df_data, idx = to_df_data(records, flights_shown, fields_shown)
    df = pd.DataFrame(df_data, index = idx)
    st.dataframe(df)
