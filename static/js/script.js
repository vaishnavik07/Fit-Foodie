document.querySelector(".home").onmousemove = (e) => {
  let x = (window.innerWidth - e.pageX * 2) / 90;
  let y = (window.innerHeight - e.pageY * 2) / 90;

  document.querySelector(
    ".home .home-parallax-img"
  ).style.transform = `translateX(${y}px) translateY(${x}px)`;
};

document.querySelector(".home").onmouseleave = () => {
  document.querySelector(
    ".home .home-parallax-img"
  ).style.transform = `translateX(0px) translateY(0px)`;
};

// toggle menu/navbar script
$('.menu-btn').click(function(){
  $('.navbar .menu').toggleClass("active");
  $('.menu-btn i').toggleClass("active");
});

async function setup() {
  const ctx = document.getElementById('myChart').getContext('2d');
  let chartStatus = Chart.getChart("myChart"); // <canvas> id
      if (chartStatus != undefined) {
      chartStatus.destroy();}
      let myChart = new Chart(ctx, {
        type: 'line',
        data: {
          labels: globalTemps.months,
          datasets: [
            {
              label: 'Exchange Rate',
              data: globalTemps.new_curr,
              fill: false,
              borderColor: 'rgba(18, 18, 114, 1)',
              backgroundColor: 'rgba(18, 18, 114, 0.5)',
              borderWidth: 1
            }
          ]
  
        },
        options: {}
      });
}