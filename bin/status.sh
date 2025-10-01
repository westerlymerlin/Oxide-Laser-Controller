#!/bin/bash

# show status of gunicorn and nginx

echo "
**** system status of nginx and gunicorn ****
"
sudo systemctl status nginx > status.txt
sudo systemctl status gunicorn.service >> status.txt
cat status.txt
echo "
**********"
