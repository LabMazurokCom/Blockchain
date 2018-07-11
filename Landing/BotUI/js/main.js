class Plotter {

}

let currency_to_usd = {
  'btc': 6370,
  'ltc': 80,
  'bch': 707.8,
  'usd': 1,
  'xrp': 0.45,
  'dash': 220.0,
  'eth': 445.0
}


function myplot(time, pdata) {
  let plot = document.createElement('div');
  let plottingData = [];
  let layouts = [];
  console.log([...Array(time.length).keys()])
  for (let key in pdata) {
    plottingData.push({
      x: time, //[...Array(time.length).keys()],
      y: pdata[key],
      type: 'lines+markers',
      name: key != 'usd' ? key + ', in usd equivalent' : key
    })
  }

  let layout = {
    margin: {
      l: 50,
      b: 50,
      t: 5,
      r: 20
    },
    title: false,
    width: 1000,
    height: 600,
    autoscale: false,
    xaxis: {
      type: 'category',
      title: 'time',
      titlefont: {
        size: 10
      },
      tickfont: {
        size: 10
      }
    },
    yaxis: {
      title: 'balance, usd',
      titlefont: {
        size: 10
      },
      tickfont: {
        size: 10
      }
    },
    showlegend: true,
    legend: {
      x: 300,
      y: 1
    }
  };


  Plotly.plot('plot', plottingData, layout).catch(console.log);
  // Plotly.plot(plot, plottingData, layout).then(
  //   function(gd) {
  //     return Plotly.toImage(gd, {
  //       format: "svg",
  //       height: 600,
  //       width: 1000
  //     }).then(
  //       function(url) {
  //         let img_jpg = document.getElementById("jpg-export");
  //         img_jpg.src = url;
  //       }
  //     )
  //   }).catch(e => console.log(e));
}

// let file = 'balances.txt';

function format_date(date) {
  return date.getHours() + ':' + date.getMinutes() + ':' + date.getSeconds();
}

function prepare_csv(text) {

  console.log(text);
  let data = text.split('\n').map((x) => {
    let tmp = x.split('|');
    if (tmp[1] != 'Balances') return null;
    try {
      tmp[5] = JSON.parse(tmp[5].replace(/'/g, '"'));

    } catch (e) {
      console.log(e);
      console.log(tmp[5]);
      return null;
    }
    return [format_date(new Date(tmp[0])), tmp[5]];
  }).filter(x => x !== null);

  for (let i = 1; i < data.length; i++) {
    for (let exch in data[i][1]) {
      for (let curr in data[i][1][exch]) {
        if (data[i][1][exch][curr] == -1) {
          data[i][1][exch][curr] = data[i - 1][1][exch][curr];
        }
      }
    }
  }

  data = data.map(x => {
    let acc = {};
    for (let exch in x[1]) {
      for (let curr in x[1][exch]) {
        if (curr in acc) {
          acc[curr] += +x[1][exch][curr];
        } else {
          acc[curr] = +x[1][exch][curr];
        }
      }
    }
    return [x[0], acc];
  });

  return data;

}

function prepare_json(text) {
  let data = text.split('\n').map(x => {
    console.log(x);
    let tmp = 0;
    try {
      tmp = JSON.parse(x.replace(/'/g, '"'));
    } catch (e) {
      console.log(e);
      return null;
    }
    return [format_date(new Date(tmp['timestamp'])), tmp['data']];
  }).filter(x => x !== null);
  console.log(data);

  for (let i = 1; i < data.length; i++) {
    for (let exch in data[i][1]) {
      for (let curr in data[i][1][exch]) {
        if (data[i][1][exch][curr] == -1) {
          data[i][1][exch][curr] = data[i - 1][1][exch][curr];
        }
      }
    }
  }

  data = data.map(x => {
    let acc = {};
    for (let exch in x[1]) {
      for (let curr in x[1][exch]) {
        if (curr in acc) {
          acc[curr] += +x[1][exch][curr];
        } else {
          acc[curr] = +x[1][exch][curr];
        }
      }
    }
    return [x[0], acc];
  });
  return data;
}


function get_lines(pdata, number_of_records) {
  let data = pdata.slice(Math.max(pdata.length - number_of_records, 0), pdata.length);
  console.log(data);

  let points = {};
  let time = [];
  for (let i = 0; i < data.length; i++) {
    time.push(data[i][0]);
    for (key in data[i][1]) {
      if (key in points) {
        points[key].push(data[i][1][key] * currency_to_usd[key]);
      } else {
        points[key] = [data[i][1][key] * currency_to_usd[key]];
      }
    }
  }
  console.log(time, points);
  return [time, points];
}


function process_file(file, prepare_data) {
  $.get(file, function(text) {
    let data = prepare_data(text);
    let [time, lines] = get_lines(data, 20);
    myplot(time, lines);
  });
}
