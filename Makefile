dump:
	 mysqldump --user=root -p message_db > DUMPFILENAME.sql

load:
	mysql --user=root -p  -e "CREATE DATABASE message_db;"
	mysql --user=root -p message_db < DUMPFILENAME.sql