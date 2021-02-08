function show_friends(visited_profile, current_user){

    var show_friends = document.getElementById("active_content");
    show_friends.innerHTML = ''

    var col_search_form = document.createElement("div")
    col_search_form.className = 'col-search-form'
    col_search_form.style.display = 'flex'
    col_search_form.style.justifyContent = 'center'
    col_search_form.style.width = '100%'
    col_search_form.style.height = '50px'

    var form_class = document.createElement("form")
    form_class.className = 'form-inline active-cyan-3 active-cyan-4 center-content'
    form_class.autocomplete = 'off'
    form_class.style.width = '100%'
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
    input_class.style.display = 'flex'
    input_class.style.justifyContent = 'center'
    input_class.style.backgroundColor = '#fef9c7'

    autocompletes.appendChild(input_class)
    form_class.appendChild(autocompletes)
    col_search_form.appendChild(form_class)

    show_friends.appendChild(col_search_form)


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
        if (visited_profile === current_user) {
            block_to_insert.appendChild(remove_button);
        }
        show_friends.appendChild(block_to_insert);
    }
    autocomplete(document.getElementById("user_search"), all_users, course=false, all_users=true );
}

function show_stats() {
    let active_container = document.getElementById('active_content')
    active_container.innerHTML = ''

    let active_menu = document.getElementById('stats_menu')
    active_menu.style.backgroundColor = '#2981fd'

    let active_image = document.getElementById('stats_picture')
    active_image.style.filter = 'invert(100%)'

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
    outer_button_cont.style.marginBottom = '15px'

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

    let htmls = '<div class="tab-pane text-center gallery" id="favorite_courses">' +
        '<p>Gå till courses för att lägga till bana</p>' +
        '<div id="favorite-courses-tag" >'

    for (course of favorite_courses) {
        htmls += `<h3 id="id_courses">${course}</h3>`
    }
    htmls += '</div></div>'

    $(htmls).appendTo(active_contents)
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