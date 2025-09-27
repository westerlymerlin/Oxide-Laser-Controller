#!/bin/bash

# script to retsrat the services

echo "
**** stoping gunicorn and python app ****
"
/bin/sudo /bin/systemctl stop gunicorn.service

echo "
**** stopping nginx ****
"
/bin/sudo /bin/systemctl stop nginx

echo "
**** staring nginx ****
"
/bin/sudo /bin/systemctl start nginx

echo "
**** starting gunicorn and python app ****
"
/bin/sudo /bin/systemctl start gunicorn.service

echo "
******** restart completed ********
"
