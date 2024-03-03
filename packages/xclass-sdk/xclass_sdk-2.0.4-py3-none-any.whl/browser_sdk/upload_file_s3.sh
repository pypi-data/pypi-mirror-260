#!/bin/bash

# Set your AWS S3 bucket name
S3_BUCKET="app.xclass.edu.vn"

# Check if parameter is provided
if [ $# -ne 1 ]; then
    echo "Usage: $0 [prod|dev]"
    exit 1
fi

# Set the upload path based on the parameter
if [ "$1" == "prod" ]; then
    UPLOAD_PATH="$S3_BUCKET/prod"
elif [ "$1" == "dev" ]; then
    UPLOAD_PATH="$S3_BUCKET/dev"
else
    echo "Invalid parameter: $1. Use 'prod' or 'dev'."
    exit 1
fi

# Get the local folder path
LOCAL_FOLDER=$(dirname "$0")

# Iterate through files in the local folder
for file in "$LOCAL_FOLDER"/*; do
    if [ -f "$file" ]; then
        # Extract the filename from the path
        filename=$(basename "$file")

        # Upload the file to S3 bucket
        echo "Uploading $filename to s3://$UPLOAD_PATH/$filename"
        aws s3 cp "$file" "s3://$UPLOAD_PATH/$filename"
    fi
done

echo "All files uploaded to S3!"
