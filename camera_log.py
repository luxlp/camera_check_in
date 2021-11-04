import streamlit as st
from datetime import date
from datetime import datetime
from getpass import getuser
import pandas as pd
import sys
import numpy as np
from streamlit import errors



#computer user
user = getuser()
#dir
#data_dir = fr'C:\Users\{user}\Desktop\Projects\camera_in-out'
#files
#csv_file = f'{data_dir}./Device_sign-out_sheet.csv'
#URL
url = 'https://github.com/luxlp/camera_check_in/blob/main/Device_sign-out_sheet.csv'
#Page-Setup-----------------------------------------------------------------------------------------------------------
st.set_page_config(
    page_title='Camera Check-in/out',
    page_icon=':Jack-O-Lantern:',
    layout='wide',
    initial_sidebar_state='auto'
)

#dataframe
def load_df():
    data = pd.read_csv(url)
    df = pd.DataFrame(data)
    return df
df_ = load_df()

st.title("Camera Check-in/out :jack_o_lantern:")
# st.write(':Jack-O-Lantern:')

#set columns
main_column, s_column = st.columns(2)
#cameras in inv
camera_asset_id_ipqc = ['Quality 2','Quality 12','Quality 13','Quality 14','Quality 15']
camera_asset_id_qt = ['Quality 1']
# camera_asset_id = ['165278', 'nan', 'nan', 'nan', 'nan', 'nan']

with main_column:
    form1 = st.form(key='the-form', clear_on_submit=True)
    camera1 = form1.text_input('Enter Camera name/asset id')
    user1 = form1.text_input('Enter user name/id')
    submit1 = form1.form_submit_button('Submit')
    time_ = datetime.now().strftime('%m/%d/%y %H:%M:%S')
    today_ = date.today().strftime('%m/%d/%y')

    dict = {
            'Camera': [''],
            'User': [''],
            'Purpose': [''],
            'Check-Out': [''],
            'Return': ['']
        }

    dff = pd.DataFrame(dict)

    def purpose_change():
        if camera1 in camera_asset_id_ipqc:
            return 'Rack Shipment Record'
        elif camera1 in camera_asset_id_qt:
            return 'Quality Investigation'
        else:
            st.error(f'{camera1} Not in our database, or check spelling!')
            sys.exit(1)


    try:
        dfin = {
                'Camera': camera1,
                'User': str(user1),
                'Purpose': purpose_change(),
                'Check-Out': time_,
                'Return': np.nan
            }
    except:
        pass
   
    # def my_actions(a: bool, b: bool) -> int:
    #     return 2 * a + b

    try:
        def check():
            set = df_.loc[(df_['Camera'] == camera1) & (df_['Return'].isnull())]
            if set.size != 0:
                return set.iat[0,4]
            else:
                pass
    except:
        pass


    if submit1:
        try:
            if (camera1 in df_.values):
                if check():
                    df_.loc[(df_['Camera'] == camera1) & (df_['Return'].isnull()), 'Return'] = time_
                    #df_.to_csv(csv_file, index=False)
                else:
                    df_ = df_.append(dfin, ignore_index = True)
                    #df_.to_csv(csv_file, index=False)
            else:
                try:
                    df_ = df_.append(dfin, ignore_index = True)
                    #df_.to_csv(csv_file, index=False)
                except:
                    pass
        except ValueError:
            pass

with s_column:
    st.write(df_)

    @st.cache
    def convert_df(df):
        return df.to_csv(index = False).encode('utf-8')
    
    csv = convert_df(df_)


    st.download_button(
        label = "Download data as CSV",
        data = csv,
        file_name = f'{today_}_Camera_log.csv',
        mime = 'text/csv',
    )

        
    
