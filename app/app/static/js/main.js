var prInstance = (function() {
    const cacheName = 'pianorecordercache';

    var showOnlyFavourites = false
    var pendingCommands = []
    var mainsocket = new WebSocket('wss://' + location.host + '/main')


    mainsocket.onmessage = function(event) {
       //var new_recordings = document.getElementById('new_recordings')
       //new_row = new_recordings.insertRow(0)
       //new_row.innerHTML = event.data
        msg = JSON.parse(event.data)
        if (msg.command == 'reload') {
            location.reload()
        }
    }

    mainsocket.onconnect = function(event) {
        while (pendingCommands.length >0){
            cmd = pendingCommands.shift()
            mainsocket.send(cmd)
        }
    }

    function safe_send(str) {
        if (mainsocket.readyState == WebSocket.CLOSED
            || mainsocket.readyState == WebSocket.CLOSING) {
            pendingCommands.push(str)
            reconnect_internal()
        } else {
            mainsocket.send(str)
        }
    }
    function reconnect_internal()
    {
        if (mainsocket.readyState == WebSocket.CLOSED
            || mainsocket.readyState == WebSocket.CLOSING) {
            mainsocket = new WebSocket('wss://' + location.host + '/main')
        }
    }
    return {
        reconnect: function()
        {
            reconnect_internal()
        },
        // not used yet, needs to check if new title is unique
        update_titles : function(title)
        {
            var list = document.getElementById('titlelist');
            var option = document.createElement('option');
            option.value = title;
            list.appendChild(option);
        },

        set_title : function(recid, id)
        {
            var source = document.getElementById(id)
            var title =  source.value
            var cmd = {
                "command" : "set_title",
                "id" : recid,
                "title" : title
            }
            safe_send(JSON.stringify(cmd))
        },

        add_tag : function(id, tag_id)
        {
            var cmd = {
                "command" : "add_tag",
                "id" : id,
                "tag_id" : tag_id
            }
            safe_send(JSON.stringify(cmd))
        },

        delete_tag : function(id, tag_id)
        {
            var cmd = {
                "command" : "delete_tag",
                "id" : id,
                "tag_id" : tag_id
            }
            safe_send(JSON.stringify(cmd))
        },

        play : function(id)
        {
            var cmd = {
                "command" : "play",
                "id" : id
            }
            safe_send(JSON.stringify(cmd))
        },
        create_synth : function(id)
        {
            var cmd = {
                "command" : "create_synth",
                "id" : id
            }
            safe_send(JSON.stringify(cmd))
        },
        synth : function(id)
        {
            location.href = '/synth/' + id;
        },
        stop : function()
        {
            var cmd = {
                "command" : "stop"
            }
            safe_send(JSON.stringify(cmd))
        },
        start_metronome : function()
        {
            var cmd = {
                "command" : "start_metronome",
            }
            safe_send(JSON.stringify(cmd))
        },
        update_metronome : function(bpm, volume, loop_id)
        {
            var cmd = {
                "command" : "update_metronome",
                "bpm" : bpm,
                "volume" : volume,
                "loop_id" : loop_id
            }
            safe_send(JSON.stringify(cmd))
        },
        stop_metronome : function()
        {
            var cmd = {
                "command" : "stop_metronome"
            }
            safe_send(JSON.stringify(cmd))
        },
        setfav : function(record, id) {
            var favbutton = document.getElementById(id)
            var newval = !(favbutton.dataset.fav == 'true')
            if (newval)
                favbutton.childNodes[1].className="fas fa-star fav"
            else
                favbutton.childNodes[1].className="far fa-star fav"

            favbutton.dataset.fav = newval

            var command = "setfavourite " + record + " " + newval
            console.log(command)
        },
        removeUrlFromCache: function(url) {
            caches.open(cacheName).then(function(cache) {
                cache.matchAll(url).then(function(response) {
                    response.forEach(function(element, index, array) {
                        cache.delete(element);
                    });
                });
            })
        }
    };
})();
