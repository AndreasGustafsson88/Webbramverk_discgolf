function show_tab(tab_id){
    var nodes = document.getElementById("profile_content").childNodes;
    for(let i = 0; i < nodes.length; i++){
        if(nodes[i].nodeName.toLowerCase()==="div"){

            nodes[i].style.display ="none";
        }
    }
    document.getElementById(tab_id).style.display="inline";
}


function show_friends(){

    var show_friends = document.getElementById("friends_id");

    for(let key in friends){
        var block_to_insert = document.createElement("div");
        block_to_insert.setAttribute("id", key+'1');
        var remove_button = document.createElement("input");
        remove_button.setAttribute("type", "image");
        remove_button.setAttribute("id", key);
        remove_button.setAttribute("class", "action remove");
        remove_button.setAttribute("src", "/assets/img/baseline_delete_black_24dp.png");
        remove_button.style.height="100%"
        block_to_insert.setAttribute("class", "col-container w100 center-content-h friend_column");
        block_to_insert.style.height="50px"
        var friend_name = document.createElement('p');
        friend_name.setAttribute('id', 'friend_name_id')
        friend_name.innerHTML = friends[key];
        var friend_link = document.createElement("a");
        friend_link.setAttribute("href","/profile_page/" + key);
        friend_link.setAttribute('id', 'friend_link_id')
        friend_link.innerHTML = key;
        block_to_insert.appendChild(friend_name)
        block_to_insert.appendChild(friend_link);
        block_to_insert.appendChild(remove_button);
        show_friends.appendChild(block_to_insert);

    }

}


$('#profile_picture_input').change(() => {
  var file = $('#profile_picture_input').val().split('/').pop().split('\\').pop();
  if (file) {
    $('#settings-profile-picture-filename').text(truncate(file, 10));}
  else {
    $('#settings-profile-picture-filename').text("No file choosen");}
});

function truncate(string, maxChars) {
  if (string.length <= maxChars) {
    return string}
  else {
    var regex = new RegExp("^(.{" + Math.floor((maxChars / 3) * 2).toString() + "}).*(.{" + Math.floor(maxChars / 3).toString() + "}\\..*)$", 'm')
    return string.replace(regex, "$1 ... $2")}
}


