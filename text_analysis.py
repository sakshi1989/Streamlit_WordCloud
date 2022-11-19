# from PIL import Image
# import numpy as np
import pandas as pd
# import matplotlib.pyplot as plt
import altair as alt
import streamlit as st
import re
from wordcloud import WordCloud, STOPWORDS
# Importing the StringIO module.
# from io import StringIO 

# st.write is writing a markdown
st.write('# Analyzing Shakespeare texts')

st.sidebar.header("Word Cloud Settings")

max_word = st.sidebar.slider("Max Words",10, 200, 100, 10)
max_font = st.sidebar.slider("Size of Largest word",50, 350, 60)
image_size = st.sidebar.slider("Image Width",100, 800, 400,10)
# Words stay consistent on each run
random = st.sidebar.slider("Random State",30, 100, 42)

# stopwords checkbox
stopwords_chck = st.sidebar.checkbox('Remove Stop Words?')

st.sidebar.header("Word Count Settings")
min_word = st.sidebar.slider("Minimum count of words",5, 100, 40)

# image = st.file_uploader("Choose a txt file")
# Create the dictionary to hold the label for file in drop down along with the file location
books = {" ":" ","A Mid Summer Night's Dream":"./data/summer.txt",
         "The Merchant of Venice":"./data/merchant.txt","Romeo and Juliet":"./data/romeo.txt"}        

book_selected = st.selectbox("Choose a txt file" , books.keys())   
image = books[book_selected]   

# This if statement is just preparing the data
if image != ' ' :
    # This dataset will be used to view full text
    dataset = open(image,"r").read().lower()

    # Dataset just for the word cloud and bar chart
    dataset1 = dataset
    
    if stopwords_chck :
        stopwords = set(STOPWORDS)
        stopwords.update(['us', 'one', 'will', 'said', 'now', 'well', 'man', 'may',
        'little', 'say', 'must', 'way', 'long', 'yet', 'mean',
        'put', 'seem', 'asked', 'made', 'half', 'much',
        'certainly', 'might', 'came'])

        dataset1 = " ".join([word for word in dataset1.split(' ') if word not in stopwords])
    
    dataset1 = re.sub(r'[^\w\s]','', dataset1)

tab1, tab2, tab3 = st.tabs(['Word Cloud','Bar Chart','View Text'])    

with tab1 :
    # st.write(string.punctuation)
    if image != ' ':
        # Remove punctuation & stopwords 
        # st.write(stopwords)
        # if stopwords is not None:
        #     dataset1 = " ".join([word for word in dataset1.split() if word not in stopwords])
        #     dataset1 = re.sub(r'[^\w\s]','', dataset1)           
        
        cloud = WordCloud(background_color = "white", 
                            max_words = max_word, 
                            max_font_size=max_font, 
                            # stopwords = stopwords,                             
                            random_state=random)
        wc = cloud.generate(dataset1)
        # st.write(cloud.words_)
        word_cloud = cloud.to_file('wordcloud.png')

        st.image(wc.to_array(), width = image_size)

with tab2:
    if image != ' ':        
        
        # this will return the dictionary of the word and their frequency count
        data_dict = cloud.process_text(dataset1)

        # Sort the data in descending order based on the count value (value part of the dictionary)
        word_freq={k: v for k, v in sorted(data_dict.items(), reverse=True, key=lambda value: value[1])}    
               
        # Create the dataframe with the words and their occurrence frequency
        df_freq = pd.DataFrame(list(word_freq.items()),columns = ['Words', 'Word_Count'])
 
        # Plot the bar chart where the word count should be >= min_word
        df_freq = df_freq.loc[df_freq['Word_Count'] >= min_word , :]
        # # Only use the top max_word set by the user
        # df_freq = df_freq.iloc[:max_word, :]

        # Get the maximum count of the word
        max_count = df_freq['Word_Count'].max()
        # the height of the bar should increase as the max_word increases
        scale = alt.Scale(
            domain=[min_word, max_count],            
            scheme='blues',
            type='linear'
        )
        bar_chart = alt.Chart(df_freq , title = "Bar Chart for - " + book_selected).mark_bar().encode(                
                                                    alt.X('Word_Count', title='Frequencies'),
                                                    alt.Y('Words', sort = alt.EncodingSortField(field="Word_Count", op="sum", order="descending")),
                                                    text = 'Word_Count',
                                                    color=alt.Color('Word_Count', scale=scale)
                                                               
                                                ) 
        text = bar_chart.mark_text(
                                align='left',
                                baseline='middle',                                
                                dx=3  # Nudges text to right so it doesn't appear on top of the bar
                            ).encode(
                                text='Word_Count'
                            )
        # cht_expander = st.expander('', expanded=True)
        # cht_expander.altair_chart(bar_chart + text, use_container_width=True)                            
        st.altair_chart(bar_chart + text, use_container_width=True)

with tab3:
    if image != ' ':
        st.write(dataset)         

