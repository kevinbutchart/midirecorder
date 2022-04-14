var prInstance = (function() {
    var showOnlyFavourites = false
    var mainsocket = new WebSocket('ws://' + location.host + '/main')


    mainsocket.onmessage = function(event) {
       //var new_recordings = document.getElementById('new_recordings')
       //new_row = new_recordings.insertRow(0)
       //new_row.innerHTML = event.data
        msg = JSON.parse(event.data)
        if (msg.command == 'reload') {
            location.reload() 
        }   
    }
    return {
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
            mainsocket.send(JSON.stringify(cmd))
        },

        play : function(id)
        {  
            var cmd = {
                "command" : "play",
                "id" : id
            }
            mainsocket.send(JSON.stringify(cmd))
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
            mainsocket.send(JSON.stringify(cmd))
        },
        start_metronome : function(bpm, beats, volume)
        {
            var cmd = {
                "command" : "start_metronome",
                "bpm" : bpm,
                "beats" : beats,
                "volume" : volume
            }
            mainsocket.send(JSON.stringify(cmd))
        },
        stop_metronome : function()
        {    
            var cmd = {
                "command" : "stop_metronome"
            }
            mainsocket.send(JSON.stringify(cmd))
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
        }
    };
})();
