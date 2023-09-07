import streamlit as st
import pandas as pd
import requests
import snowflake.connector
from urllib.error import URLError


st.title('New')
st.header('Breakfast Menu')
st.text(' 🥣 Omega 3 & Blueberry Oatmeal')
st.text(' 🥗 Kale, Spinach & Rocket Smoothie')
st.text(' 🐔 Hard-Boiled Free-Range Egg')
st.text('🥑🍞 Avocado Toast')

st.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = pd.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')


# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = st.multiselect('Pick some fruits:', list(my_fruit_list.index),['Avocado', 'Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]


st.dataframe(fruits_to_show)

#New Section to display fruityvice api response
st.header('Fruityvice Fruit Advice!')
try:
  fruit_choice = st.text_input('What fruit would you like information about?', 'Kiwi')
  if not fruit_choice:
    st.error("Please select a fruit to get information.")
  else:
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
    fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
    st.dataframe(fruityvice_normalized)

execept URLError as e:
  st.error()

st.stop()


my_cnx = snowflake.connector.connect(**st.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("select * from fruit_load_list")
my_data_row = my_cur.fetchall()
st.header("The fruit load list contains:")
st.dataframe(my_data_row)

#Allow the end user to add a fruit to the list
add_my_fruit = st.text_input("What fruit would you like to add?", "jackfruit")
st.write('Thanks for adding ', add_my_fruit)


my_cur.execute("insert into fruit_load_list values ('from streamlit')")




