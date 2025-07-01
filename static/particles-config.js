particlesJS("particles-js", {
  "particles": {
    "number": {
      "value": 40,
      "density": {
        "enable": true,
        "value_area": 800
      }
    },
    "color": { "value": "#a4baff" },
    "shape": {
      "type": "circle",
      "stroke": { "width": 0, "color": "#000" },
      "polygon": { "nb_sides": 5 }
    },
    "opacity": {
      "value": 0.5,
      "random": false
    },
    "size": {
      "value": 6,
      "random": true
    },
    "line_linked": {
      "enable": true,
      "distance": 150,
      "color": "#d3dfff",
      "opacity": 0.4,
      "width": 2
    },
    "move": {
      "enable": true,
      "speed": 0.8,
      "direction": "none",
      "random": false,
      "straight": false,
      "out_mode": "out",
      "bounce": false
    }
  },
  "interactivity": {
    "detect_on": "canvas",
    "events": {
      "onhover": { "enable": true, "mode": "grab" },
      "onclick": { "enable": false },
      "resize": true
    },
    "modes": {
      "grab": {
        "distance": 140,
        "line_linked": { "opacity": 0.4 }
      }
    }
  },
  "retina_detect": true
});
