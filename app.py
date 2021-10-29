"""
This application contains the code related to the
Trend Analysis for different environments (Dev, Prod, Integ and DryRun).
"""

__author__ = 'Surendra Reddy'
__version__ = '1.0'
__maintainer__ = 'Surendra Reddy'
__email__ = 'surendraelectronics@gmail.com'
__status__ = 'Prototype'

print('# ' + '=' * 78)
print('Author: ' + __author__)
print('Version: ' + __version__)
print('Maintainer: ' + __maintainer__)
print('Email: ' + __email__)
print('Status: ' + __status__)
print('# ' + '=' * 78)


# Modules
import streamlit as st
import requests
from datetime import datetime , timedelta
import pandas as pd
import streamlit.components.v1 as components
from pyecharts.charts import Liquid
from pyecharts import options as opts
from st_radial import st_radial
import hydralit as hy
from streamlit_lottie import st_lottie

# Utils Pkgs
import codecs

# INSERT YOUR API  KEY WHICH YOU PASTED IN YOUR secrets.toml file 
api_key =  ''

url = 'http://api.openweathermap.org/data/2.5/weather?q={}&appid={}'
url_1 = 'https://api.openweathermap.org/data/2.5/onecall/timemachine?lat={}&lon={}&dt={}&appid={}'

# Page Config details
st.set_page_config(
        page_title = '☁Weather',
        page_icon = "☁",
        layout = "wide",
        initial_sidebar_state = "expanded"
    )

contact_form = """
<form action="https://formsubmit.co/surendraelectronics@gmail.com" method="POST">
     <input type="hidden" name="_captcha" value="false">
     <input type="text" name="name" placeholder="Your name" required>
     <input type="email" name="email" placeholder="Your email" required>
     <textarea name="message" placeholder="Your message here"></textarea>
     <button type="submit">Send</button>
</form>
"""

app = hy.HydraApp(title='☁Weather')

# Function for LATEST WEATHER DATA
def getweather(city):
    result = requests.get(url.format(city, api_key))     
    if result:
        json = result.json()
        #st.write(json)
        country = json['sys']['country']
        temp = json['main']['temp'] - 273.15
        temp_feels = json['main']['feels_like'] - 273.15
        humid = json['main']['humidity'] - 273.15
        icon = json['weather'][0]['icon']
        lon = json['coord']['lon']
        lat = json['coord']['lat']
        des = json['weather'][0]['description']
        res = [country, round(temp,1),round(temp_feels,1),
                humid,lon,lat,icon,des]
        return res , json
    else:
        print("error in search !")

def renderReport():
    HtmlFile = open("./Basic_Example.html", 'r', encoding='utf-8')
    source_code = HtmlFile.read() 
    #print(source_code)
    components.html(source_code,width=700,height=500)

# Function for HISTORICAL DATA
def get_hist_data(lat,lon,start):
    res = requests.get(url_1.format(lat,lon,start,api_key))
    data = res.json()
    temp = []
    for hour in data["hourly"]:
        t = hour["temp"]
        temp.append(t)     
    return data , temp

def load_lottieurl(url: str):
    """Load the image of lottie

    Args:
        url (str): url of the lottie

    Returns:
        [type]: json object return
    """
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# Let's write the Application
# Custom Components Fxn
def st_calculator(calc_html,width=700,height=500):
	calc_file = codecs.open(calc_html,'r')
	page = calc_file.read()
	components.html(page,width=width,height=height,scrolling=False)



# embed streamlit docs in a streamlit app
#components.iframe("https://cdnjs.cloudflare.com/ajax/libs/Trumbowyg/2.25.1/trumbowyg.min.js",width=1000,height=700)

def apply_css(file_name):
    """Apply the css to contact form
    """
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


@app.addapp(title='Home',icon="🏠")
def my_home():
    # st.write("""
    #         ## Weather Application
    #         Display's the latest wheather report of user selected city 
    #         and last 5 days temperature details.
    #         """)
    url = "https://assets10.lottiefiles.com/packages/lf20_57ui5yd5.json"
    lottie_url = url
    lottie_json = load_lottieurl(lottie_url)
    st_cont = st.sidebar.container()
    with st_cont:
        st_lottie(lottie_json,height =100,width =200)
        st.sidebar.write("""
                    ## Weather Application Details
                    """)

    st.header('☁ Get Weather Details')   
    #st.markdown('https://openweathermap.org/api') 

    col1, col2 = st.columns([2,2])

    with col1:
        city_name = st.text_input("Enter a city name", value = 'Bangalore')
    with col2:  
        if city_name:
            st.write('')
            st.write('')
            show_details = st.expander(label='Weather Details')
            with show_details:
                res , json = getweather(city_name)
                st.subheader("Current weather")
                st.write([round(res[1],2)][0])
                # Create liquid chart
                customer_satisfaction=(
                    Liquid()
                    .add('lq',[round(res[1],2)/100], center=["15%", "35%"])    
                )
                # Export to html
                customer_satisfaction.render(('./Basic_Example.html')) 
                renderReport()
            
    if city_name:
        start_date_string = st.date_input("Today's Date")      
        show_hist = st.expander(label = 'Last 5 Days History',expanded=True)
        with show_hist:                
                #start_date_string = str('2021-06-26')
                date_df = []
                max_temp_df = []
                for i in range(5):
                    date_Str = start_date_string - timedelta(i)
                    start_date = datetime.strptime(str(date_Str),"%Y-%m-%d")
                    timestamp_1 = datetime.timestamp(start_date)
                    #res , json = getweather(city_name)
                    his , temp = get_hist_data(res[5],res[4],int(timestamp_1))
                    date_df.append(date_Str)
                    max_temp_df.append(max(temp) - 273.5)
                    
                df = pd.DataFrame()
                df['Date'] = date_df
                df['Max temp'] = max_temp_df
                print(df['Date'][0])
                print(max_temp_df)                
                first_kpi, second_kpi, third_kpi, fourth_kpi,fifth_kpi= st.columns(5)
                with first_kpi:
                    #st.markdown("**👇Date**")
                    st.subheader(df['Date'][0])
                    st_radial('°C1', value=round(max_temp_df[0]))
                with second_kpi:
                    st.subheader(df['Date'][1])
                    #st.markdown("**👇Day2**")
                    st_radial('°C2', value=round(max_temp_df[1]))
                with third_kpi:
                    #st.markdown("**👇Day3**")
                    st.subheader(df['Date'][2])
                    st_radial('°C3', value=round(max_temp_df[2]))
                with fourth_kpi:
                    #st.markdown("**👇Day4**")
                    st.subheader(df['Date'][3])
                    st_radial('°C4', value=round(max_temp_df[3]))
                with fifth_kpi:
                    #st.markdown("**👇Day5**")
                    st.subheader(df['Date'][4])
                    st_radial('°C5', value=round(max_temp_df[4])) 
                st.table(df)              

        st.map(pd.DataFrame({'lat' : [res[5]] , 'lon' : [res[4]]},columns = ['lat','lon']))


@app.addapp(title='Contact', icon="📈")
def Contact():
    url = "https://assets10.lottiefiles.com/packages/lf20_57ui5yd5.json"
    lottie_url = url
    lottie_json = load_lottieurl(lottie_url)
    st_cont = st.sidebar.container()
    with st_cont:
        st_lottie(lottie_json,height =100,width =200)
        st.sidebar.write("""
                    ## Weather Application Details
                    """)
    st.header(":mailbox: Get In Touch With Me!")
    st.markdown(contact_form,unsafe_allow_html=True)
    apply_css("style/style.css")

# main function call
if __name__ == '__main__':
    #main()
    app.run()
