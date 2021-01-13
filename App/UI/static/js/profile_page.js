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
        block_to_insert.setAttribute("class", "col-container w100 center-content-h");
        block_to_insert.innerHTML = friends[key];
        var friend_link = document.createElement("a");
        friend_link.setAttribute("href","/profile_page/" + key);
        friend_link.innerHTML = key;
        block_to_insert.appendChild(friend_link);
        show_friends.appendChild(block_to_insert);

    }

}

function add_friend(){

}