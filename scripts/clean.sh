#! /bin/bash

read -p "Do you want to delete only back-ups ? [y/n] : " backups

if [ $backups = "y" ]; then
	if ls back-ups/back* 1> /dev/null 2>&1 ;then
		echo "deleting only back-ups..."
		cd back-ups
		rm $(ls)
		cd ..
		echo "done."
		exit
	else :
		echo "No back-ups to delete"
		exit
	fi
fi

read -p "Are you sure to delete all files (except back-ups) [y/n] : " delete

if [ ! $delete = "y" ]; then
	echo "deletion cancelled"
	exit
fi

if [ -d ./logs ]; then
	rm -rf ./logs
	echo "deleting /logs directory"
else
	echo "directory /logs doesn't exist"
fi

if [  -d ./data ];then
	rm -rf ./data
	echo "deleting /data directory"
else
	echo "directory /data doesn't exist"
fi

read -p "Do you want to remove all the back-ups ? [y/n] : " confirmation

if [ $confirmation = "y" ];then
	if ls back-ups/back* 1> /dev/null 2>&1 ;then
		echo "deleting only back-ups..."
		cd back-ups
		rm $(ls)
		cd ..
		echo "done."
		exit
	else :
		echo "No back-ups to delete"
		exit
	fi
else
	echo "the back-ups will not be deleted"
fi

echo "To install again all directories, run 'make install'"
