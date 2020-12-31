function create_scorecard() {
    let course = document.getElementById("Course");
    if(course.innerHTML !=="No course selected"){


    let players = document.getElementById("player_content_div");
    let player_list = [];



    for (let player of players.children) {
        player_list.push(player.id)
    }

    let j_players = JSON.stringify(player_list);

    let new_url = "http://127.0.0.1:5000/scorecard/play" + "?" + "course=" + course.innerHTML;
    new_url += "&players=" + j_players;

    window.location.href = new_url;

}
    else{
        alert("Please select a Course")
    }
}




function delete_player(id) {

    let button = document.getElementById(id);
    let player = document.getElementById(id.replace("button", ""));

    button.remove();
    player.remove();

}

function get_player() {


    let player_name = document.getElementById("player_search").value;

    if (player_name && friends.includes(player_name)) {
        let container_block = document.getElementById("player_content_div");
        let player_amount = $('#player_content_div > div').length

        let block_to_insert = document.createElement("div");
        block_to_insert.setAttribute("id", player_name)
        block_to_insert.className = "player-text";
        block_to_insert.innerHTML = "Player " + (player_amount + 1) + ": " + player_name;

        let delete_button = document.createElement("button");
        delete_button.setAttribute("class", "btn btn-danger btn-sm");
        delete_button.setAttribute("type", "button");
        delete_button.setAttribute("style", "float: right");
        delete_button.setAttribute("id", player_name + "button");
        delete_button.setAttribute("onclick", "delete_player(this.id)");
        delete_button.innerHTML = "Remove";

        block_to_insert.appendChild(delete_button);
        container_block.appendChild(block_to_insert);

        let player_element = document.getElementById("player_search");
        player_element.value = null;
    }

}
