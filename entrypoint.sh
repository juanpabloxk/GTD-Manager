#!/bin/sh

env >> /etc/environment

su - root

echo -e "#!/bin/sh\ncd /app && python3 main.py" > /etc/periodic/15min/run_app
chmod +rwx /etc/periodic/15min/run_app

# execute CMD
echo "$@"
exec "$@"
