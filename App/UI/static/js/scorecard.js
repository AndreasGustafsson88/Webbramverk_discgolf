function get_player() {

    let container_block = document.getElementById("player_content_div");
    let player_amount = $('#player_content_div > div').length
    let player_name = document.getElementById("player_search").value;

    let block_to_insert = document.createElement("div");

    let delete_button = document.createElement("button");
    delete_button.className = "btn btn-danger btn-sm";
    delete_button.innerHTML = "remove";
    delete_button.type = "button";

    block_to_insert.appendChild(delete_button);
    console.log(player_name);

    block_to_insert.className = "player-text";
    block_to_insert.innerHTML = "Player " + (player_amount + 1) + ": " + player_name;

    container_block.appendChild(block_to_insert);

}