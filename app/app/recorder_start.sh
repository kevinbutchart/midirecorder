#!/bin/bash
disablemmcled
/app/midirecorder.py&
/app/player_server.py&
wait -n # wait till either process exits

# relying on the container to restart
