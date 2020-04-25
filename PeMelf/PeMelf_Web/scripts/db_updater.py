from main.models import Document_download
import os

def update_db_file(name,path_to_file,usr_token):
    path_to_file = os.path.join(path_to_file,name)
    file_obj = Document_download(name=name,path_to_file=path_to_file,
                                user_token=usr_token)

    file_obj.save()
