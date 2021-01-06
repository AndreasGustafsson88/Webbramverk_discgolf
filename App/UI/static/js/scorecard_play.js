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
  console.log(user_name, hole, par, strokes);
  console.log(info);
  info.innerHTML = this.value;
  par_diff = this.value - par;
  player_summary[user_name]['hole'+ hole + '_par'] = par_diff;
  points = parseInt(par) + parseInt(strokes) - this.value + 2;
  player_summary[user_name]['hole'+ hole + '_points'] = points;

  let total_par = document.getElementById(user_name +"_par")
  let total_points = document.getElementById(user_name +"_points")


  let [points_summary, par_summary] = [0, 0]
            for (let v in player_summary[user_name]) {
                if (v.includes("par")) {
                    par_summary += player_summary[user_name][v]
                }
                else if (v.includes("points")) {
                    points_summary += player_summary[user_name][v]
                }
            }


  total_par.innerHTML = par_summary;
  total_points.innerHTML = points_summary;

  console.log(total_points)



}

