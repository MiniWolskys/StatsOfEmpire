echo "Enter your user :"
read user

echo "export AWS_PROFILE=$user" > $VIRTUAL_ENV/bin/postactivate
echo "unset AWS_PROFILE" > $VIRTUAL_ENV/bin/predeactivate