import pdfplumber
import streamlit as st
import pandas as pd

st.title("PDF Table Extractor")
uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])

class Headers:
    def r_header(self):
        head =[]
        with pdfplumber.open(uploaded_file) as pdf:
            for page in pdf.pages:
                words = page.extract_words(x_tolerance=2, keep_blank_chars=True, split_at_punctuation=':')

                for word in words:
                    if word['text'] == 'Release Details':
                        t_name = word
                for word in words:
                    w1 = t_name
                    w2 = word

                    if 11.78 < (w2['top'] - w1['top']) < 12:
                        head.append(w2['text'])
                header = {key: [] for key in head}
                return header

    def c_header(self):
        head = []
        with pdfplumber.open(uploaded_file) as pdf:
            for page in pdf.pages:
                words = page.extract_words(x_tolerance=2, keep_blank_chars=True)

                for word in words:
                    if word['text'] == 'Component Details:':
                        t_name = word
                for word in words:
                    w1 = t_name
                    w2 = word

                    if 11.78 < (w2['top'] - w1['top']) < 12:
                        head.append(w2['text'])
                header = {key: [] for key in head}
                return header
head = Headers()

class Data(Headers):
    def r_data(self):
        new = []
        r = head.r_header()
        with pdfplumber.open(uploaded_file) as pdf:
            for page in pdf.pages:
                words = page.extract_words()
                text = page.extract_text()

                # table range
                start_word = "Release"  # Replace with the word you want to start from
                end_word = "Component"  # Replace with the word you want to stop at

                # Find the index of the starting word and the ending word using a for loop and enumerate
                start_index = None
                end_index = None
                encap = []
                for i, word in enumerate(words):
                    if word['text'] == start_word:
                        start_index = i
                    if word['text'] == end_word:
                        end_index = i

                # Check if both words were found
                if start_index is not None and end_index is not None:
                    # Loop through the words between the start and end words
                    for i in range(start_index + 1, end_index):  # Start from the next word after start_word
                        encap.append(words[i])
                    table = encap

                t_name = None
                for word in words:
                    if word['text'] == 'Release' and word['bottom'] - word['top'] <= 9:
                        t_name = word
                        break

                if not t_name:
                    continue

                for word in words:
                    w1 = t_name
                    w2 = word

                    if abs(w2['top'] - w1[
                        'top'] - 250.85) < 1e-2:  # Allow small tolerance for floating-point comparison
                        new.append(w2)
                row = []
                lines = text.split('\n')
                for line in lines:
                    for word in words:
                        if 24.5 < word['top'] - new[0]['top'] < 34.6 and word['text'] in line:
                            row.append(word)
            seen = set()
            unique_data = []
            l = []
            for item in row:
                item_tuple = tuple(item.items())
                if item_tuple not in seen:
                    seen.add(item_tuple)
                    unique_data.append(item)
            mod_row = unique_data
            prev_x1 = None
            for word in mod_row:
                x0 = word['x0']
                text = word['text']

                if prev_x1 is not None:
                    wordspace = x0 - prev_x1
                    if wordspace > 52.42199999999995:
                        l.append(' ')
                        l.append(text)
                    elif 3.524000000000057 < wordspace < 52.42199999999995:
                        l.append(text)
                    else:
                        l[-1] += ' ' + text
                else:
                    l.append(text)
                prev_x1 = word['x1']
            for key, value in zip(r.keys(), l):
                r[key].append(value)

            if table[-1]['top'] > 460:
                d_l = []
                r_l = []
                for j in table:
                    row_space = j['top'] - new[1]['top']
                    if 70 < row_space < 80 and j['top'] < 460:
                        d_l.append(j)
                        seen = set()
                        unique_data = []
                        for item in d_l:
                            item_tuple = tuple(item.items())
                            if item_tuple not in seen:
                                seen.add(item_tuple)
                                unique_data.append(item)
                        d_l = unique_data
                        prev_x1 = None
                        for word in d_l:
                            x0 = word['x0']
                            text = word['text']

                            if prev_x1 is not None:
                                wordspace = x0 - prev_x1
                                if wordspace > 52.42199999999995:
                                    r_l.append(' ')
                                    r_l.append(text)
                                elif 3.524000000000057 < wordspace < 52.42199999999995:
                                    r_l.append(text)
                                else:
                                    r_l[-1] += ' ' + text
                            else:
                                r_l.append(text)
                            prev_x1 = word['x1']
                for key, value in zip(r.keys(), r_l[-9:]):
                    r[key].append(value)
            df = pd.DataFrame(r)
            df.set_index('Item', inplace=True)
            st.write(df)

    def c_data(self):
        new = []
        c = head.c_header()
        with pdfplumber.open(uploaded_file) as pdf:
            for page in pdf.pages:
                words = page.extract_words()
                text = page.extract_text()

                for word in words:
                    if word['text'] == 'Details:':
                        t_name = word
                    if word['text'] == 'Import/Export':
                        stop = word['top']
                for word in words:
                    w1 = t_name
                    w2 = word

                    if 11.78 < (w2['top'] - w1['top']) < 12:  # Allow small tolerance for floating-point comparison
                        new.append(w2)
                start_word = new[-1]['text']  # Replace with the word you want to start from
                end_word = "Information:"  # Replace with the word you want to stop at

                # Find the index of the starting word and the ending word using a for loop and enumerate
                start_index = None
                end_index = None
                encap = []
                for i, word in enumerate(words):
                    if word['text'] == start_word:
                        start_index = i
                    if word['text'] == end_word:
                        end_index = i

                # Check if both words were found
                if start_index is not None and end_index is not None:
                    # Loop through the words between the start and end words
                    for i in range(start_index + 1, end_index):  # Start from the next word after start_word
                        encap.append(words[i])
                    table = encap
            l = []
            prev_x1 = None
            for word in table:
                x0 = word['x0']
                text = word['text']

                if word['text'] == 'Import/Export':
                    l.append(' ')
                    break

                if prev_x1 is not None:
                    wordspace = x0 - prev_x1

                    if wordspace > 135:
                        l.append(' ')
                        l.append(text)

                    elif -506 < wordspace < -470 or -403 < wordspace < -390:
                        l.append(' ')
                        l.append(text)
                    elif wordspace < 0:
                        l.append(' ')
                        l.append(' ')
                        l.append(text)
                    elif 13.33 < wordspace < 165:
                        l.append(text)

                    else:
                        l[-1] += ' ' + text
                else:
                    l.append(text)
                prev_x1 = word['x1']
            if l[-2] == 'Mfg code :':
                m = (l[:len(l) - 1])
                print(m)
            else:
                m = l
                print(m)

            # Process the list in chunks of 7
            for i in range(0, len(m), 7):
                chunk = m[i:i + 7]  # Take 7 elements at a time
                if len(chunk) == 7:  # Ensure it's a complete chunk
                    for key, value in zip(c.keys(), chunk):
                        c[key].append(value)
            df = pd.DataFrame(c)
            df.set_index('Item',inplace = True)
            st.write(df)
d = Data()
#Release_Details table button
if st.button("Extract: Release Details"):
    d.r_data()

#Component_Details table button
if st.button("Extract: Component Details"):
    d.c_data()