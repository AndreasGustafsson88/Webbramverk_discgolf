function create_scorecard() {
    let course = document.getElementById("Course");
    if(course.innerHTML !=="No course selected"){


    let players = document.getElementById("player_content_div");
    let player_list = [];



    for (let player of players.children) {
        player_list.push(player.id)
    }

    let j_players = JSON.stringify(player_list);

    let new_url = "/scorecard/play" + "?" + "course=" + course.innerHTML;
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

autocomplete(document.getElementById("user_search"), all_users, course=false, all_users=true );

        function autocomplete(inp, arr, course=false, all_user=false) {
          /*the autocomplete function takes two arguments,
          the text field element and an array of possible autocompleted values:*/
          var currentFocus;
          /*execute a function when someone writes in the text field:*/
          inp.addEventListener("input", function(e) {
              var a, b, i, val = this.value;
              /*close any already open lists of autocompleted values*/
              closeAllLists();
              if (!val) { return false;}
              currentFocus = -1;
              /*create a DIV element that will contain the items (values):*/
              a = document.createElement("DIV");
              a.setAttribute("id", this.id + "autocomplete-list");
              a.setAttribute("class", "autocomplete-items");
              /*append the DIV element as a child of the autocomplete container:*/
              this.parentNode.appendChild(a);
              /*for each item in the array...*/
              for (i = 0; i < arr.length; i++) {
                /*check if the item starts with the same letters as the text field value:*/
                if (arr[i].substr(0, val.length).toUpperCase() == val.toUpperCase()) {
                  /*create a DIV element for each matching element:*/
                  b = document.createElement("DIV");
                  /*make the matching letters bold:*/
                  b.innerHTML = "<strong>" + arr[i].substr(0, val.length) + "</strong>";
                  b.innerHTML += arr[i].substr(val.length);
                  /*insert a input field that will hold the current array item's value:*/
                  b.innerHTML += "<input type='hidden' value='" + arr[i] + "'>";
                  /*execute a function when someone clicks on the item value (DIV element):*/
                      b.addEventListener("click", function(e) {
                      /*insert the value for the autocomplete text field:*/
                      inp.value = this.getElementsByTagName("input")[0].value;
                      if(all_user){
                          window.location = '/profile_page/'+inp.value;
                      }
                      if(course){
                          let textfield = document.getElementById("Course");
                          textfield.innerHTML = inp.value;
                      }
                      /*close the list of autocompleted values,
                      (or any other open lists of autocompleted values:*/
                      closeAllLists();
                  });
                  a.appendChild(b);
                }
              }
          });
          /*execute a function presses a key on the keyboard:*/
          inp.addEventListener("keydown", function(e) {
              var x = document.getElementById(this.id + "autocomplete-list");
              if (x) x = x.getElementsByTagName("div");
              if (e.keyCode == 40) {
                /*If the arrow DOWN key is pressed,
                increase the currentFocus variable:*/
                currentFocus++;
                /*and and make the current item more visible:*/
                addActive(x);
              } else if (e.keyCode == 38) { //up
                /*If the arrow UP key is pressed,
                decrease the currentFocus variable:*/
                currentFocus--;
                /*and and make the current item more visible:*/
                addActive(x);
              } else if (e.keyCode == 13) {
                /*If the ENTER key is pressed, prevent the form from being submitted,*/
                e.preventDefault();
                if (currentFocus > -1) {
                  /*and simulate a click on the "active" item:*/
                  if (x) x[currentFocus].click();
                }
              }
          });
          function addActive(x) {
            /*a function to classify an item as "active":*/
            if (!x) return false;
            /*start by removing the "active" class on all items:*/
            removeActive(x);
            if (currentFocus >= x.length) currentFocus = 0;
            if (currentFocus < 0) currentFocus = (x.length - 1);
            /*add class "autocomplete-active":*/
            x[currentFocus].classList.add("autocomplete-active");
          }
          function removeActive(x) {
            /*a function to remove the "active" class from all autocomplete items:*/
            for (var i = 0; i < x.length; i++) {
              x[i].classList.remove("autocomplete-active");
            }
          }
          function closeAllLists(elmnt) {
            /*close all autocomplete lists in the document,
            except the one passed as an argument:*/
            var x = document.getElementsByClassName("autocomplete-items");
            for (var i = 0; i < x.length; i++) {
              if (elmnt != x[i] && elmnt != inp) {
              x[i].parentNode.removeChild(x[i]);
            }
          }
        }
        /*execute a function when someone clicks in the document:*/
        document.addEventListener("click", function (e) {
            closeAllLists(e.target);
        });
        }
