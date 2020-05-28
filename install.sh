#!/bin/bash
DIR="$(dirname "$(readlink -f "$BASH_SOURCE[0]")")"

for i in "$DIR/service"/*
do
	f=$(basename $i)
	sudo systemctl stop "$f"
done

sudo cp "$DIR/bin/"* /usr/local/bin/

sudo mkdir -p /usr/local/share/midirecorder/
sudo cp -R "$DIR"/share/* /usr/local/share/midirecorder/

for i in "$DIR/service"/*
do
	f=$(basename $i)
	sudo cp "$i" /lib/systemd/system/$f
	sudo chmod 644 /lib/systemd/system/$f
	sudo systemctl enable "$f"
	sudo systemctl start "$f"
done

sudo cp -R "$DIR"/website/* /var/www/html/
