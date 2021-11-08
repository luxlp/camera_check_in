import pandas as pd
from github import Github
from github import InputGitTreeElement
from datetime import datetime

url = 'https://github.com/luxlp/camera_check_in/blob/main/Device_sign-out_sheet.csv'

#dataframe
def load_df():
    data = pd.read_csv(url, on_bad_lines='skip')
    df = pd.DataFrame(data)
    return df
df_ = load_df()

df2 = df_.to_csv(sep=',', index=False)

file_list = [df2]
file_name = ['Device_sign-out_sheet.csv']

commit_message = 'test python'

#github connection
user = "luxlp"
password = "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"
git = Github(user, password)

#connect to repo
repo = git.get_user().get_repo('camera_check_in')

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
        commit_message = 'Data Updated - ' + datetime.now().strftime('%Y-%m-%d %H:%M:%S')

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

updategitfile(file_name, file_list, user, password, 'camera_check_in', 'heads/main')

