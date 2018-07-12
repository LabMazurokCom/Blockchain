const PROGRESS_BAR_TEMPLATE =
  //   `
  // <div class="progress">
  //   <div id = "progress_bar{id}" class="progress-bar progress-bar-info" role="progressbar" aria-valuenow="70"
  //     aria-valuemin="0" aria-valuemax="100" style="width:0%" onload = "console.log('i am in progressbar'), update_progress_bar(document.getElementById('progress_bar{id}'))">
  //       0% Complete (info)
  //   </div>
  // </div>
  // `
  // `
  // <video class= 'load' muted autoplay loop id="dlvid">
  //   <source src="video/load_video.mp4" type="video/mp4">
  // </video>
  // `
  `
<div >
<img class = 'load' src ='img/UnitedSmartBinturong.gif'/>
</div>
`;


const TIMEOUT = 15000; // in milliseconds

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}


function prepare_progress_bar(elem, id_num) {
  elem.class = 'progress';
  elem.innerHTML = formatObj(PROGRESS_BAR_TEMPLATE, {
    'id': id_num
  });
}


function update_progress_bar(elem) {
  let update_times = 100;
  let delay = 15000 / update_times;
  let time = 0;
  console.log("i am here in update bar function");
  setInterval(() => {
    time = time + delay;
    elem.style.width = ((time / TIMEOUT) * 100).toFixed(0) + '%';
    elem.value = elem.style.width + ' Complete';
  }, delay);
}


function formatObj(str, dict) {
  let res = str.slice();
  console.log("i am in format");
  for (let key in dict) {
    res = res.replace(new RegExp('(\\{' + key + '\\})', 'g'), dict[key]);
  }
  return res;
}

// <div class="progress">
//   <div class="progress-bar progress-bar-danger" role="progressbar" aria-valuenow="70"
//   aria-valuemin="0" aria-valuemax="100" style="width:70%">
//     70% Complete (danger)
//   </div>
// </div>
