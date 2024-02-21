const wheel = document.getElementById("wheel");
const spinBtn = document.getElementById("spin-btn");
const finalValue = document.getElementById("final-value");

//Object that stores values of minimum and maximum angle for a value
const rotationValues = [
  { minDegree: 0, maxDegree: 30, value: 20 },
  { minDegree: 31, maxDegree: 90, value: 'double the points'},
  { minDegree: 91, maxDegree: 150, value: 40},
  { minDegree: 151, maxDegree: 210, value: 50},
  { minDegree: 211, maxDegree: 270, value:  60},
  { minDegree: 271, maxDegree: 330, value: 'try again' },
  { minDegree: 331, maxDegree: 360, value: 20 },
];
//Size of each piece
const data = [16, 16, 16, 16, 16, 16];
//background color for each piece
var pieColors = [
  "#bbcbdb", "#9ebd9e", "#dd855c", "#f1e8ca","#bbcbdb", "#745151", 
];
//Create chart
let myChart = new Chart(wheel, {
  //Plugin for displaying text on pie chart
  plugins: [ChartDataLabels],
  //Chart Type Pie
  type: "pie",
  data: {
    //Labels(values which are to be displayed on chart)
    labels: ['double', 20, 'try again', 60, 50, 40],
    //Settings for dataset/pie
    datasets: [
      {
        backgroundColor: pieColors,
        data: data,
      },
    ],
  },
  options: {
    //Responsive chart
    responsive: true,
    animation: { duration: 0 },
    plugins: {
      //hide tooltip and legend
      tooltip: false,
      legend: {
        display: false,
      },
      //display labels inside pie chart
      datalabels: {
        color: "#ffffff",
        formatter: (_, context) => context.chart.data.labels[context.dataIndex],
        font: { size: 24 },
      },
    },
  },
});
//display value based on the randomAngle
const valueGenerator = (angleValue) => {
  for (let i of rotationValues) {
    //if the angleValue is between min and max then display it
    if (angleValue >= i.minDegree && angleValue <= i.maxDegree) {
      if(i.value === 'try again'){
        finalValue.innerHTML = `<p>NA VJEN KEQ!</p>`;
      }
      else if(i.value === 'double the points'){
        finalValue.innerHTML = `<p >URIME! JU DYFISHUAT PIKET TUAJA!</p>`;
        point.value = parseInt(point.value * 2);
      }
      else{
      finalValue.innerHTML = `<p>URIME! JU FITUAT : ${i.value} PIKE</p>`;
      point.value = parseInt(point.value) + parseInt(i.value);
    }
      spinBtn.disabled = false;
      break;
    }
  }
};

//Spinner count
let count = 0;
//100 rotations for animation and last rotation for result
let resultValue = 101;
//Start spinning
spinBtn.addEventListener("click", () => {
  spinBtn.disabled = true;
  //Empty final value
  // finalValue.innerHTML = `<p>Good Luck!</p>`;
  //Generate random degrees to stop at
  let randomDegree = Math.floor(Math.random() * (355 - 0 + 1) + 0);
  //Interval for rotation animation
  let rotationInterval = window.setInterval(() => {
    //Set rotation for piechart
    /*
    Initially to make the piechart rotate faster we set resultValue to 101 so it rotates 101 degrees at a time and this reduces by 1 with every count. Eventually on last rotation we rotate by 1 degree at a time.
    */
    myChart.options.rotation = myChart.options.rotation + resultValue;
    //Update chart with new value;
    myChart.update();
    //If rotation>360 reset it back to 0
    if (myChart.options.rotation >= 360) {
      count += 1;
      resultValue -= 5;
      myChart.options.rotation = 0;
    } else if (count > 15 && myChart.options.rotation == randomDegree) {
      valueGenerator(randomDegree);
      clearInterval(rotationInterval);
      count = 0;
      resultValue = 101;
    }
  }, 10);
});



 
// // Display celebration message and create balloons
// const displayCelebration = (value) => {
//   if (value === 'double the points') {
//     finalValue.innerHTML = `<p>Congratulations! You doubled the points!</p>`;
//     createBalloons(5); // Create 5 balloons (adjust the number as needed)
//   } else if (value === 'try again') {
//     finalValue.innerHTML = `<p>Sorry! Better luck next time.</p>`;
//   } else {
//     finalValue.innerHTML = `<p>Value: ${value}</p>`;
//   }
// };

// // Create balloons dynamically
// const createBalloons = (count) => {
//   for (let i = 0; i < count; i++) {
//     const balloon = document.createElement('div');
//     balloon.className = 'balloon';
//     balloon.style.left = `${Math.random() * 100}vw`; // Random horizontal position
//     document.body.appendChild(balloon);
//   }
// };
