var swiper = new Swiper('.swiper-container', {
  pagination: {
    el: '.swiper-pagination',
    clickable: true,
    renderBullet: function (index, className) {
      return '<span class="' + className + '">' + (index + 1) + '</span>';
    },
  },
});



function update_result() {
  let par_diff, points;
  let user_name, hole, par, strokes;
  [user_name, hole, par, strokes] = this.getAttribute("id").split("_");
  let info = document.getElementById(user_name + hole);
  info.innerHTML = this.value;
  par_diff = this.value - par;
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
                par_summary += player['stats'][v]
                }
                else if (v.includes("points")) {
                    points_summary += player['stats'][v]
                }
            }

          total_par.innerHTML = par_summary;
          total_points.innerHTML = points_summary;
      }
  }
  console.log(player_summary)

}

function submit_scorecards() {
    player_summary['status'] = 'complete'

    $.ajax({
        method: 'post',
        url: '/scorecard/play',
        data: {
            p_summary: JSON.stringify(player_summary)
        },
        success: (data) => {
            alert(data)
            // location.replace('/scorecard')
    }
    })
}


function save_scorecards() {

    player_summary['status'] = 'incomplete'

    $.ajax({
    method: 'post',
    url: '/scorecard/play',
    data: {
        p_summary: JSON.stringify(player_summary)
    },
    success: (data) => {
        alert(data)
        // location.replace('/scorecard')
    }
    })
}