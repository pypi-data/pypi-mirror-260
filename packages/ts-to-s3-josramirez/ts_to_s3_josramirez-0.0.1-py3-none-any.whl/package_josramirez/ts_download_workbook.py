#!/usr/bin/python
'''Tableau Server download workbooks, Author Jose Ramirez (mailto:josramirez@healthfirst.org)
Requirements:
  - tableauserverclient
  - boto3
  - yaml
  - os
  - logging
Python:
  - 3.7.3
Usage:
  - script to download two twbx from tableau server from remote path, upload both twbx to S3 and delete local copies of downloaded files after upload 
'''

import tableauserverclient as TSC
import boto3
import logging
import os
import yaml

#creating logging 

logging.basicConfig(filename='ts_download_workbook_logs.log', level=logging.DEBUG, format = '%(asctime)s - %(message)s', datefmt='%Y-%m-%d,%H:%M:%S %p') #config for logging
#tableau signin functions 

def tableau_server_signin(token_name, token_secret, base_url):
    authorization = TSC.PersonalAccessTokenAuth(token_name, token_secret)
    connection = TSC.Server(base_url, use_server_version=True)
    connection.auth.sign_in(authorization)
    return connection


def download_twbx(connection, workbook_id, path):
    response = connection.workbooks.download(workbook_id, filepath=path, no_extract=False)
    print("\nDownloaded the file to {0}.".format(response))
    return response


def download_multiple_twbx(connection, workbook_id_2, path):
    response = connection.workbooks.download(workbook_id_2, filepath=path, no_extract=False)
    print("\nDownloaded the file to {0}.".format(response))
    return response


#function to delete downloaded .twbx file locally after upload to s3

def delete_first_file(path):
    config_location = 'ts_download_workbook_config_file.yml'
    config = read_yaml_config(config_location)
    path = config['path']
    os.remove(path)
    return path

def delete_second_file(second_twbx_path):
    config_location = 'ts_download_workbook_config_file.yml'
    config = read_yaml_config(config_location)
    second_twbx_path = config['path_of_second_twbx']
    os.remove(second_twbx_path)
    return second_twbx_path

#function to read .yaml config file

def read_yaml_config(file):
    with open('ts_download_workbook_config_file.yml', 'r') as file:
        output = yaml.safe_load(file)
    return output

#function to upload downloaded .twbx file to specified s3 bucket
def upload_s3():
    config_location = 'ts_download_workbook_config_file.yml'
    config = read_yaml_config(config_location)
    wbk1 = config['path']
    wbk2 = config['path_of_second_twbx']
    Bucket = config['bucket']
    Key = config['key']
    Key2 = config['key2']
    session = boto3.Session(profile_name = 'saml')
    s3 = session.resource('s3')
    s3.meta.client.upload_file(wbk1, Bucket, Key, ExtraArgs=None,Callback=None,Config=None)
    s3.meta.client.upload_file(wbk2, Bucket, Key2, ExtraArgs=None,Callback=None,Config=None)


def main():
    config_location = 'ts_download_workbook_config_file.yml'
    config = read_yaml_config(config_location)
    server_url = config['server_url'] 
    token_name = config['token_name']
    token_secret = config['token_secret']
    first_wrkbk_id = config['wrkbk_id'] 
    second_wrkbk_id = config['second_wrkbk_id']                    
    dwnld_path = config['dwnld_path']
    path = config['path']
    second_twbx_path = config['path_of_second_twbx']

    # sign in
    try:
        connection = tableau_server_signin(token_name, token_secret, server_url)
    except Exception:
        print('Connection attempt to Tableau Server failed. Please verify authentication details.')
    else:
        print('Connection to Tableau Server successful. Now downloading the .twbx file to the specified path..')

    # download twbx - must have datasource embedded to open in reader
        
    try:
        file_path = download_twbx(connection, first_wrkbk_id, dwnld_path)
    except Exception:
        print('There was an error downloading the first workbook.')
    else:
        print('First workbook was successfully download.')

    try:
        new_file_path = download_multiple_twbx(connection, second_wrkbk_id, dwnld_path)
    except Exception:
        print('There was an error downloading the second workbook.')
    else:
        print('The second workbook file was successfully downloaded to file path. Now uploading to S3..')

    #move twbx to s3 bucket

    try:
        upload_path = upload_s3()
    except Exception:
        print('There was an error uploading the .twbx file to S3.')
    else:
        print('The .twbx file was successfully uploaded to the specified S3 bucket.')

    # deleting local copy of .twbx file from remote location
    
    path = config['path']
    second_twbx_path = config['path_of_second_twbx']

    try:
        delete_first_file(path)
    except Exception:
        print('There was an error deleting the .twbx file from the directory.')
    else:
        print('First file deleted. Now deleting the second file.')

    try:
        delete_second_file(second_twbx_path)
    except Exception:
        print('There was an error deleting the second .twbx file from the directory.')
    else:
        print('The downloaded .twbx file has been successfully deleted from the directory. End of script.')
        
        
    logging.info(main)


if __name__ == '__main__':
    main()