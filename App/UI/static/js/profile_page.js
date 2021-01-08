function show_tab(tab_id){
    var nodes = document.getElementById("profile_content").childNodes;
    for(let i = 0; i < nodes.length; i++){
        if(nodes[i].nodeName.toLowerCase()==="div"){

            nodes[i].style.display ="none";
        }


    }
    document.getElementById(tab_id).style.display="inline";





}

