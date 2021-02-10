var swiper = new Swiper('.swiper-container', {
    on: {
        slideChange: () => {
            if (player_summary['active']) {
                if ((JSON.stringify(check_round['players']) === JSON.stringify(player_summary['players']))) {} else {
                    check_round = JSON.parse(JSON.stringify(player_summary))
                    swipe_save()
                }
            }
        }
    },
    autoHeight: true,
    pagination: {
        el: '.swiper-pagination',
        clickable: true,
        renderBullet: function(index, className) {
            if (player_summary['multi'] === 1 && index === player_summary['course_holes'][0]) {
                return '<span class="' + className + '">' + 'S' + '</span>';
            } else if (player_summary['multi'] === 2 && index === (player_summary['course_holes'][0] * 2)) {
                return '<span class="' + className + '">' + 'S' + '</span>';
            } else {
                return '<span class="' + className + '">' + (index + 1) + '</span>';
            }

        },
    },
});

$(window).resize(() => {
    swiper.update()
})

function set_info_bg_color(info, par_diff, value) {
    if (par_diff === -1) {
        info.style.backgroundColor = '#c7fdbc'
    } else if (parseInt(value) === 1) {
        info.style.backgroundColor = '#ffe870'
    } else if (par_diff === -2) {
        info.style.backgroundColor = '#98fc81'
    } else if (par_diff < -2) {
        info.style.backgroundColor = '#75ff70'
    } else if (par_diff === 0) {
        info.style.backgroundColor = ''
    } else if (par_diff === 1) {
        info.style.backgroundColor = '#f8a3a3'
    } else if (par_diff === 2) {
        info.style.backgroundColor = '#f66a6a'
    } else if (par_diff > 2) {
        info.style.backgroundColor = '#f84444'
    }
}

function update_result() {
    let par_diff, points;
    let user_name, hole, par, strokes;
    [user_name, hole, par, strokes] = this.getAttribute("id").split("|");
    let info = document.getElementById(user_name + hole);
    info.innerHTML = $(this).val();
    par_diff = this.value - par;
    set_info_bg_color(info, par_diff, this.value)
    points = parseInt(par) + parseInt(strokes) - this.value + 2;

    if (points < 0) {
        points = 0;
    }

    for (let player of player_summary['players']) {
        if (player['user_name'] === user_name) {
            player['stats']['hole' + hole + '_par'] = par_diff;
            player['stats']['hole' + hole + '_points'] = points;
            player['stats']['hole' + hole + '_throws'] = this.value;

            let total_par = document.getElementById(user_name + "_par")
            let total_points = document.getElementById(user_name + "_points")
            let [points_summary, par_summary] = [0, 0]

            for (let v in player['stats']) {
                if (v.includes("par")) {
                    if (typeof player['stats'][v] === 'string') {
                        par_summary += 0
                    } else {
                        par_summary += player['stats'][v]
                    }

                } else if (v.includes("points")) {
                    if (typeof player['stats'][v] === 'string') {
                        points_summary += 0
                    } else {
                        points_summary += player['stats'][v]
                    }
                }
            }

            total_par.innerHTML = par_summary;
            total_points.innerHTML = points_summary;
        }
    }
}

function complete_round() {
    for (let player of player_summary['players']) {
        for (let key in player['stats']) {
            if (player['stats'][key] === "" && key.includes('throws') || player['stats'][key] === "0" && key.includes('throws')) {
                return false;
            }
        }
    }
    return true;
}

function submit_scorecards() {

    if (complete_round()) {
        player_summary['active'] = false

        $('#submit_button').hide()

        $.ajax({
            method: 'post',
            url: '/scorecard/play',
            data: {
                p_summary: JSON.stringify(player_summary)
            },

            success: (data) => {
                alert(data)
                location.replace(redirect_url)
            }
        });
    }
}


function save_scorecards() {

    $.ajax({
        method: 'post',
        url: '/scorecard/play',
        data: {
            p_summary: JSON.stringify(player_summary)
        },
        success: (data) => {
            alert(data)
            location.replace(redirect_url)
        }
    })
}

function swipe_save() {

    $.ajax({
        method: 'post',
        url: '/scorecard/play',
        data: {
            p_summary: JSON.stringify(player_summary)
        },
    })
}

function load_summary(element) {
    // Revisit this function
    let par_diff, points;
    let user_name, hole, par, strokes;
    [user_name, hole, par, strokes] = element.getAttribute("id").split("|");
    let info = document.getElementById(user_name + hole);

    if (element.value !== "") {

        info.innerHTML = element.value;
        par_diff = element.value - par;
        set_info_bg_color(info, par_diff)

        points = parseInt(par) + parseInt(strokes) - element.value + 2;

        if (points < 0) {
            points = 0;
        }

        for (let player of player_summary['players']) {

            if (player['user_name'] === user_name) {
                player['stats']['hole' + hole + '_par'] = par_diff;
                player['stats']['hole' + hole + '_points'] = points;
                player['stats']['hole' + hole + '_throws'] = element.value;

                let total_par = document.getElementById(user_name + "_par")
                let total_points = document.getElementById(user_name + "_points")
                let [points_summary, par_summary] = [0, 0]

                for (let v in player['stats']) {
                    if (v.includes("par")) {
                        if (typeof player['stats'][v] === 'string') {
                            par_summary += 0
                        } else {
                            par_summary += player['stats'][v]
                        }
                    } else if (v.includes("points")) {
                        if (typeof player['stats'][v] === 'string') {
                            points_summary += 0
                        } else {
                            points_summary += player['stats'][v]
                        }
                    }
                }
                total_par.innerHTML = par_summary;
                total_points.innerHTML = points_summary;
            }
        }
    }
}

function delete_scorecards() {
    $.ajax({
        method: 'delete',
        url: '/scorecard/play',
        data: {
            p_summary: JSON.stringify(player_summary),
            action: 'delete_scorecard'
        },
        success: (data) => {
            alert(data)
            location.replace(redirect_url)
        }
    });
}

let check_round = JSON.parse(JSON.stringify(player_summary));
var elements = document.getElementsByClassName("throws-input");
for (let i = 0; i < elements.length; i++) {
    elements[i].addEventListener("input", update_result)
    load_summary(elements[i])
}
