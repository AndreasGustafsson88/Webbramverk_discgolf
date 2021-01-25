var swiper = new Swiper('.swiper-container', {
    on: {
        slideChange: () => {
            if (player_summary['active']){
                console.log(player_summary['active'])
                if ((JSON.stringify(check_round['players']) === JSON.stringify(player_summary['players']))) {
                }
                else {
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
    renderBullet: function (index, className) {
      return '<span class="' + className + '">' + (index + 1) + '</span>';
    },
  },
});


function set_info_bg_color(info, par_diff) {
    if (par_diff === -1){
        info.style.backgroundColor = '#CCFF99'
    }
    else if (par_diff === -2){
        info.style.backgroundColor = '#80FF00'
    }
    else if (par_diff < -2){
        info.style.backgroundColor = '#FFFF66'
    }
    else if (par_diff === 0){
        info.style.backgroundColor = ''
    }
    else if (par_diff === 1){
        info.style.backgroundColor = '#FF9999'
    }
    else if (par_diff === 2){
        info.style.backgroundColor = '#FF6666'
    }
    else if (par_diff > 2) {
        info.style.backgroundColor = '#FF3333'
    }
}

function update_result() {
  let par_diff, points;
  let user_name, hole, par, strokes;
  [user_name, hole, par, strokes] = this.getAttribute("id").split("_");
  let info = document.getElementById(user_name + hole);
  info.innerHTML = this.value;
  par_diff = this.value - par;
  set_info_bg_color(info, par_diff)
  points = parseInt(par) + parseInt(strokes) - this.value + 2;

  for (let player of player_summary['players']) {
      if (player['user_name'] === user_name) {
          player['stats']['hole'+ hole + '_par'] = par_diff;
          player['stats']['hole'+ hole + '_points'] = points;
          player['stats']['hole'+ hole + '_throws'] = this.value;

          let total_par = document.getElementById(user_name +"_par")
          let total_points = document.getElementById(user_name +"_points")
          let [points_summary, par_summary] = [0, 0]

          for (let v in player['stats']) {
            if (v.includes("par")) {
                if (typeof player['stats'][v] === 'string'){
                    par_summary += 0
                }
                else {
                    par_summary += player['stats'][v]
                }

                }
                else if (v.includes("points")) {
                    if (typeof player['stats'][v] === 'string'){
                        points_summary += 0
                    }
                    else {
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
    for (let player of player_summary['players']){
        for (let key in player['stats']) {
            if (typeof player['stats'][key] === "string" && key.includes('par')) {
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
            data: {p_summary: JSON.stringify(player_summary)},

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
    [user_name, hole, par, strokes] = element.getAttribute("id").split("_");
    let info = document.getElementById(user_name + hole);

    if (element.value !== "") {

        info.innerHTML = element.value;
        par_diff = element.value - par;
        set_info_bg_color(info, par_diff)

        points = parseInt(par) + parseInt(strokes) - element.value + 2;

        for (let player of player_summary['players']) {

            if (player['user_name'] === user_name) {
                player['stats']['hole'+ hole + '_par'] = par_diff;
                player['stats']['hole'+ hole + '_points'] = points;
                player['stats']['hole'+ hole + '_throws'] = element.value;

                let total_par = document.getElementById(user_name +"_par")
                let total_points = document.getElementById(user_name +"_points")
                let [points_summary, par_summary] = [0, 0]

                for (let v in player['stats']) {
                    if (v.includes("par")) {
                        if (typeof player['stats'][v] === 'string'){
                            par_summary += 0
                        }
                        else {
                            par_summary += player['stats'][v]
                        }
                    }

                    else if (v.includes("points")) {
                        if (typeof player['stats'][v] === 'string'){
                            points_summary += 0
                        }
                        else {
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
        url: '/scorecard/incomplete',
        data: {
            p_summary: JSON.stringify(player_summary)
        },
        success: (data) => {
            alert(data)
            location.replace('/scorecard/incomplete')
        }
    });
}