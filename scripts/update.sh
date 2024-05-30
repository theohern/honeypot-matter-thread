zip honeypot-matter-thread.zip -r honeypot-matter-thread > /dev/null
mv honeypot-matter-thread.zip Documents
cd Documents
scp launch.sh honeypot-matter-thread.zip clean.sh basehttpadapter.py root@192.168.1.29:/home/user
