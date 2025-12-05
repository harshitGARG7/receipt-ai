# app.py
import streamlit as st
from PIL import Image
import os
import json
from datetime import datetime
import pandas as pd
from ocr import extract_text_from_image
from llm import parse_receipt

st.set_page_config(page_title='Receipt Expense Tracker', layout='wide')
# Ensure images folder exists
os.makedirs('images', exist_ok=True)


DB_FILE = 'db.json'


if 'db' not in st.session_state:
    if os.path.exists(DB_FILE):
        with open(DB_FILE,'r') as f:
            st.session_state.db = json.load(f)
    else:
        st.session_state.db = []


st.title('Receipt Expense Tracker (GenAI MVP)')


with st.sidebar:
    st.header('Upload')
    uploaded = st.file_uploader('Upload receipt image', type=['png','jpg','jpeg'])
    if uploaded is not None:
        img = Image.open(uploaded)
        # save image
        ts = datetime.now().strftime('%Y%m%d%H%M%S')
        filename = f'images/receipt_{ts}.png'
        img.save(filename)
        st.image(img, caption='Uploaded receipt', use_column_width=True)
        if st.button('Run OCR & Parse'):
            with st.spinner('Running OCR...'):
                text = extract_text_from_image(img)
            st.code(text[:1000])
            with st.spinner('Parsing with AI...'):
                parsed = parse_receipt(text)
            st.json(parsed)
            # save to DB
            entry = {
            'id': ts,
            'image': filename,
            'text': text,
            'parsed': parsed
            }
            st.session_state.db.append(entry)
            with open(DB_FILE,'w') as f:
                json.dump(st.session_state.db, f, indent=2)
            st.success('Saved')


# Main area: dashboard
st.header('Dashboard')
if st.session_state.db:
    df_rows = []
    for e in st.session_state.db:
        p = e['parsed']
        total = None
        try:
            total = float(str(p.get('total') or '0').replace(',',''))
        except Exception:
            total = 0
        df_rows.append({
        'id': e['id'],
        'store': p.get('store'),
        'date': p.get('date'),
        'category': p.get('category'),
        'total': total,
        'image': e['image']
        })
    df = pd.DataFrame(df_rows)
    st.subheader('Recent Receipts')
    st.dataframe(df[['id','store','date','category','total']].sort_values('id', ascending=False))


    st.subheader('Analytics')
    col1, col2 = st.columns(2)
    with col1:
        st.metric('Total spent', f"₹{df['total'].sum():.2f}")
        st.bar_chart(df.groupby('category')['total'].sum())
    with col2:
        st.line_chart(df.groupby('id')['total'].sum())


    st.subheader('Receipt Gallery')
    for e in reversed(st.session_state.db[-12:]):
        st.write('---')
        cols = st.columns([1,2])
        with cols[0]:
            st.image(e['image'], width=150)
        with cols[1]:
            st.json(e['parsed'])
else:
    st.write('No receipts yet — upload one from the sidebar.')