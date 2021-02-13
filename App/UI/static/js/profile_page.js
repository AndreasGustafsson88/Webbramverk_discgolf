function change_menu_icons(active_menu) {
    let menu_elements = document.getElementsByClassName('menu-bar');

    for (let element of menu_elements) {
        if (!element.id.includes(active_menu)) {
            element.style.backgroundColor = '#eee';
        }
        else {
            element.style.backgroundColor = '#fff';
        }
    }

}


function add_post_requests() {
    $('.post').click(function (){
        $.ajax({
            method: 'post',
            url: "/profile_page/accept",
            data: {
                id: id,
                action: this.className,
                request_username: this.id
            },
            success: (data) => {
                if (this.id !== 'image_container') {
                    alert( this.id + ' ' + data)

                    friends[this.id] = "New pal"
                    delete request_list[this.id]

                    show_friends()

                    if (jQuery.isEmptyObject(request_list)) {
                        $('#friend_logo_image')[0].src = menu_friends_picture
                    }
                }
                else {
                    alert(visited_profile_username + ' ' + data)
                }
            },
        })
        $(this).remove()
    });
}


function show_friends(visited_profile, current_user){

    var show_friends = document.getElementById("active_content");
    show_friends.innerHTML = ''

    change_menu_icons('friend')

    var col_search_form = document.createElement("div")
    col_search_form.className = 'col-search-form'
    col_search_form.style.display = 'flex'
    col_search_form.style.justifyContent = 'center'
    col_search_form.style.width = '100%'
    col_search_form.style.height = '50px'

    var form_class = document.createElement("form")
    form_class.className = 'form-inline active-cyan-3 active-cyan-4 center-content'
    form_class.autocomplete = 'off'
    form_class.style.width = '80%'
    form_class.style.maxWidth = '500px'

    var autocompletes = document.createElement("div")
    autocompletes.className = 'autocomplete'
    autocompletes.style.width = '100%'

    var input_class = document.createElement("input")
    input_class.className = 'form-control form-control-m w-100'
    input_class.id = 'user_search'
    input_class.type = 'text'
    input_class.placeholder = 'Search Players'
    input_class.style.marginBottom = '10px'
    input_class.style.marginTop = '10px'
    input_class.style.border = "0"
    input_class.style.borderRadius = "0"
    input_class.style.display = 'flex'
    input_class.style.justifyContent = 'center'
    input_class.style.backgroundColor = '#eee'

    autocompletes.appendChild(input_class)
    form_class.appendChild(autocompletes)
    col_search_form.appendChild(form_class)

    show_friends.appendChild(col_search_form)

    // Check if there are any friend request
    if (!jQuery.isEmptyObject(request_list)) {
        for (let username in request_list) {

            let block_to_insert = document.createElement('div')
            block_to_insert.className= "col-container center-content-h friend_column"
            block_to_insert.style.height = '30px'
            block_to_insert.style.width="100%"

            let friend_name = document.createElement('p');
            friend_name.setAttribute('id', 'friend_name_id')
            friend_name.innerHTML = request_list[username];

            let friend_link = document.createElement("a");
            friend_link.setAttribute("href","/profile_page/" + username);
            friend_link.setAttribute('id', 'friend_link_id');
            friend_link.innerHTML = username;

            let accept_request = document.createElement("img");
            accept_request.setAttribute("type", "image");
            accept_request.setAttribute("id", username);
            accept_request.setAttribute("class", "post accept_request");
            accept_request.setAttribute("src", green_checkmark);
            accept_request.style.height = "25px";
            accept_request.style.width = "30px";
            accept_request.style.marginRight = "10%";

            let decline_request = document.createElement("img");
            decline_request.setAttribute("type", "image");
            decline_request.setAttribute("id", username);
            decline_request.setAttribute("class", "action decline_request");
            decline_request.setAttribute("src", red_cross);
            decline_request.style.height = "25px";
            decline_request.style.width = "30px";

            $('<hr>').appendTo(show_friends)
            block_to_insert.appendChild(friend_name)
            block_to_insert.appendChild(friend_link);
            block_to_insert.appendChild(decline_request);
            block_to_insert.appendChild(accept_request);

            show_friends.appendChild(block_to_insert);
        }
    }

    for(let key in friends){
        var block_to_insert = document.createElement("div");
        block_to_insert.setAttribute("id", key+'1');
        var remove_button = document.createElement("img");
        remove_button.setAttribute("type", "image");
        remove_button.setAttribute("id", key);
        remove_button.setAttribute("class", "action remove");
        remove_button.setAttribute("src", "/assets/img/baseline_delete_black_24dp.png");
        remove_button.style.height="25px"
        remove_button.style.width="25px"
        remove_button.style.marginRight="10%"
        block_to_insert.setAttribute("class", "col-container center-content-h friend_column");
        block_to_insert.style.height="30px"
        block_to_insert.style.width="100%"
        let friend_name = document.createElement('p');
        friend_name.setAttribute('id', 'friend_name_id')
        friend_name.innerHTML = friends[key];
        var friend_link = document.createElement("a");
        friend_link.setAttribute("href","/profile_page/" + key);
        friend_link.setAttribute('id', 'friend_link_id')
        friend_link.innerHTML = key;

        $('<hr>').appendTo(show_friends)
        block_to_insert.appendChild(friend_name)
        block_to_insert.appendChild(friend_link);
        if (visited_profile === current_user) {
            block_to_insert.appendChild(remove_button);
        }

        show_friends.appendChild(block_to_insert);
    }

    $(".action").click(function (){
        $.ajax({
            method: 'delete',
            url: "/profile_page/",
            data: {
                username: this.id,
                action: this.className
            },
            success: (data) => {
                alert(this.id + ' ' + data)

                delete request_list[this.id]

                if (jQuery.isEmptyObject(request_list)) {
                        $('#friend_logo_image')[0].src = menu_friends_picture
                    }
                },
            })
        $(this).parent().remove();
    })

    add_post_requests()
    autocomplete(document.getElementById("user_search"), users, course=false, all_users=true );

}

function show_stats() {
    let active_container = document.getElementById('active_content')
    active_container.innerHTML = ''

    change_menu_icons('stats')

    let outer_cont = document.createElement("div")
    outer_cont.className = 'container-fluid'

    let row = document.createElement("div")
    row.className = 'row'

    let figure_cont = document.createElement("figure")
    figure_cont.className = 'highcharts-figure'
    figure_cont.style.width = '100vw'

    let id_cont = document.createElement("div")
    id_cont.id = 'container'

    figure_cont.appendChild(id_cont)
    row.appendChild(figure_cont)
    outer_cont.appendChild(row)
    active_container.appendChild(outer_cont)

    let outer_button_cont = document.createElement("div")
    outer_button_cont.className = 'cont w100 center-content-h'
    outer_button_cont.style.marginTop = '-20px'

    let inner_button_cont1 = document.createElement("div")
    inner_button_cont1.className = 'cont center-content'
    inner_button_cont1.style.width = '33%'

    let button1 = document.createElement("button")
    button1.className = 'rounds btn btn-blue btn-s w-50 button-text score_buttons font-weight-bold center-content'
    button1.value = '5'
    button1.innerText = '5'
    button1.style.height = '60%'

    inner_button_cont1.appendChild(button1)
    outer_button_cont.appendChild(inner_button_cont1)

    let inner_button_cont2 = document.createElement("div")
    inner_button_cont2.className = 'cont center-content'
    inner_button_cont2.style.width = '33%'

    let button2 = document.createElement("button")
    button2.className = 'rounds btn btn-blue btn-s w-50 button-text score_buttons font-weight-bold center-content'
    button2.value = '20'
    button2.innerText = '20'
    button2.style.height = '60%'

    inner_button_cont2.appendChild(button2)
    outer_button_cont.appendChild(inner_button_cont2)

    let inner_button_cont3 = document.createElement("div")
    inner_button_cont3.className = 'cont center-content'
    inner_button_cont3.style.width = '33%'

    let button3 = document.createElement("button")
    button3.className = 'rounds btn btn-blue btn-s w-50 button-text score_buttons font-weight-bold center-content'
    button3.value = '50'
    button3.innerText = '50'
    button3.style.height = '60%'

    inner_button_cont3.appendChild(button3)
    outer_button_cont.appendChild(inner_button_cont3)

    active_container.appendChild(outer_button_cont)

    let player_history_copy = player_history.slice(Math.max(player_history.length - 20, 0));

    $('.rounds').click(function () {
            let player_history_copy = player_history.slice(Math.max(player_history.length - this.value, 0));
            render_chart(player_history_copy);
        });

    render_chart(player_history_copy)
}

function show_favourites(favorite_courses) {
    let active_contents = $('#active_content')
    active_contents.empty()

    change_menu_icons('favourite')

    let htmls = '<div class="tab-pane text-center gallery" id="favorite_courses" style="width: 100%; margin: 0 auto">' +
        '<p>Gå till courses för att lägga till bana</p><hr>' +
        '<div id="favorite-courses-tag" >'

    for (course of favorite_courses) {
        htmls += `<h5 id="id_courses">${course}</h5><hr>`
    }
    htmls += '</div></div>'

    $(htmls).appendTo(active_contents)
}