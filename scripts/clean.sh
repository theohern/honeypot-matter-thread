ps -a | grep -E "python3 [-m,/home/user]" | awk '{print $1}' | xargs kill
