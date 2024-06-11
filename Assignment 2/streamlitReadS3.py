import streamlit as st
import boto3
from credentials import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION, BUCKET_NAME

def list_s3_files(bucket):
    try:
        s3 = boto3.client(
            's3',
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
            region_name=AWS_REGION
        )
        response = s3.list_objects_v2(Bucket=bucket)
        if 'Contents' in response:
            files = [obj['Key'] for obj in response['Contents']]
            return files
        else:
            return []
    except Exception as e:
        st.error(f"Error listing files: {e}")
        return []

def generate_s3_url(bucket, file_name):
    s3 = boto3.client(
        's3',
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name=AWS_REGION
    )
    url = s3.generate_presigned_url(
        ClientMethod='get_object',
        Params={'Bucket': bucket, 'Key': file_name},
        ExpiresIn=3600  # URL expiry time in seconds
    )
    return url

st.title('Read Files from S3')
files = list_s3_files(BUCKET_NAME)

if files:
    file_name = st.selectbox('Select a file', files)
    if file_name:
        file_url = generate_s3_url(BUCKET_NAME, file_name)
        st.markdown(f'[Open {file_name}]({file_url})')
else:
    st.write('No files found in the bucket.')
