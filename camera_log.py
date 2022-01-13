import streamlit as st
from datetime import date
from datetime import datetime
from getpass import getuser
import pandas as pd
import sys
import numpy as np
from streamlit import errors
from time import sleep

from github import Github
from github import InputGitTreeElement
from datetime import datetime, timezone


#computer user
#user = getuser()
#dir
#data_dir = fr'C:\Users\{user}\Desktop\Projects\camera_in-out'
#files
#csv_file = f'{data_dir}./Device_sign-out_sheet.csv'
#URL
url = 'https://github.com/luxlp/camera_check_in/blob/main/Device_sign-out_sheet.csv?raw=true'
t_url = 'https://github.com/luxlp/camera_check_in/blob/main/workaround.csv?raw=true'
#Page-Setup-----------------------------------------------------------------------------------------------------------
st.set_page_config(
    page_title='Camera Check-in/out',
    page_icon=':Jack-O-Lantern:',
    layout='wide',
    initial_sidebar_state='auto'
)

global df_
#dataframe
def load_df():
    data = pd.read_csv(url)
    df = pd.DataFrame(data)
    return df
df_ = load_df()

st.title("Camera Check-in/out :snowflake:")
# st.write(':Jack-O-Lantern:')

#set columns
main_column, s_column = st.columns(2)
#cameras in inv
camera_asset_id_ipqc = ['Quality 2','Quality 12','Quality 13','Quality 14','Quality 15']
camera_asset_id_qt = ['Quality 1', 'Quality 6']
camera_asset_id_wh = ['Quality 7', 'Quality 8', 'Quality 9', 'Quality 10', 'Quality 11']
# camera_asset_id = ['165278', 'nan', 'nan', 'nan', 'nan', 'nan']

with main_column:
    form1 = st.form(key='the-form', clear_on_submit=True)
    camera1 = form1.text_input('Enter Camera name/asset id')
    user1 = form1.text_input('Enter user name/id')
    submit1 = form1.form_submit_button('Submit')
    def utc_to_local(utc_dt):
        return utc_dt.replace(tzinfo=timezone.utc).astimezone(tz=None)
    def local(utc_dt):
        return utc_to_local(utc_dt).strftime('%m/%d/%y %H:%M:%S')
    def local_(utc_dt):
        return utc_to_local(utc_dt).strftime('%m/%d/%y')
    time_ = local(datetime.utcnow())
    #time_ = datetime.now().strftime('%m/%d/%y %H:%M:%S')
    today_ = local_(datetime.utcnow())

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
        elif camera1 in camera_asset_id_wh:
            return 'IQC/Rework/Inspection Record'
        elif camera1 == '':
            pass
        else:
            st.error(f'{camera1} Not in our database, or check spelling!')
            sys.exit(1)


    try:
        dfin = {
                'Camera': camera1,
                'User': user1,
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

    #GitHub process
    datat = pd.read_csv(t_url, on_bad_lines='skip')
    dft = pd.DataFrame(datat)
    
    part_one = dft.iloc[0,0]
    part_two = dft.iloc[1,0]
    part_three = dft.iloc[2,0]
    unite = str(part_one + part_two + part_three)
    
    df2_ = df_.to_csv(sep=',', index=False)

    file_list = [df2_]
    file_name = ['Device_sign-out_sheet.csv']

    commit_message = 'test python'

    #github connection
    user = "luxlp"
    password = unite
    git = Github(user, password)

    #connect to repo
    repo = git.get_user('luxlp').get_repo('camera_check_in')

    #check files in repo
    x= repo.get_contents('Device_sign-out_sheet.csv')

    #get branches
    x = repo.get_git_refs()
    for y in x:
        print(y)


    #ref
    master_ref = repo.get_git_ref("heads/main")

    def updategitfile(file_name, file_list, userid, pwd, Repo, commit_message = ''):
        if commit_message == '':
            commit_message = 'Data Updated - ' + time_

        git = Github(userid,pwd)
        repo = git.get_user().get_repo(Repo)
        master_ref = repo.get_git_ref('heads/main')
        master_sha = master_ref.object.sha
        base_tree = repo.get_git_tree(master_sha)
        element_list = list()
        for i in range(0, len(file_list)):
            element = InputGitTreeElement(file_name[i], '100644', 'blob', file_list[i])
            element_list.append(element)
        tree = repo.create_git_tree(element_list, base_tree)
        parent = repo.get_git_commit(master_sha)
        commit = repo.create_git_commit(commit_message, tree, [parent])
        master_ref.edit(commit.sha)
        print('Update complete')
    
    #update dataframe and save to CSV
    if submit1:
        try:
            if (camera1 in df_.values):
                if check():
                    df_.loc[(df_['Camera'] == camera1) & (df_['Return'].isnull()), 'Return'] = time_
                    df2_ = df_.to_csv(sep=',', index=False)
                    file_list = [df2_]
                    updategitfile(file_name, file_list, user, password, 'camera_check_in', 'heads/main')
                    #df_.to_csv(csv_file, index=False)
                else:
                    df_ = df_.append(dfin, ignore_index = True)
                    df2_ = df_.to_csv(sep=',', index=False)
                    file_list = [df2_]
                    updategitfile(file_name, file_list, user, password, 'camera_check_in', 'heads/main')
                    #df_.to_csv(csv_file, index=False)
            else:
                try:
                    df_ = df_.append(dfin, ignore_index = True)
                    df2_ = df_.to_csv(sep=',', index=False)
                    file_list = [df2_]
                    updategitfile(file_name, file_list, user, password, 'camera_check_in', 'heads/main')
                    #df_.to_csv(csv_file, index=False)
                except:
                    pass
                #finally:
                    #df2_ = df_.to_csv(sep=',', index=False)
                    #file_list = [df2_]
                    #updategitfile(file_name, file_list, user, password, 'camera_check_in', 'heads/main')
        except ValueError:
            pass
        finally:
            df2_ = df_.to_csv(sep=',', index=False)
            file_list = [df2_]
            updategitfile(file_name, file_list, user, password, 'camera_check_in', 'heads/main')

with s_column:
    st.write(df_.astype(str))
    def convert_df(df):
        return df.to_csv(index = False).encode('utf-8')
    
    csv = convert_df(df_)


    st.download_button(
        label = "Download data as CSV",
        data = csv,
        file_name = f'{today_}_Camera_log.csv',
        mime = 'text/csv',
    )
    
    #show table of cameras in stock
    st.write('Cameras ownage per Team')
    table = {'IPQC3': ['Quality 2','Quality 12','Quality 13','Quality 14','Quality 15'],
            'Quality Team': ['Quality 1', 'Quality 6', 'x', 'x', 'x'],
            'IQC': ['Quality 7', 'Quality 8', 'Quality 9', 'Quality 10', 'Quality 11']}
    df_table = pd.DataFrame(table)
    st.table(df_table)
        
    
