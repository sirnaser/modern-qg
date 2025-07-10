particlesJS("particles-js", {
  particles: {
    number: {
      value: 50,
      density: {
        enable: true,
        value_area: 800
      }
    },
    color: {
      value: "#3f51b5"
    },
    shape: {
      type: "circle"
    },
    opacity: {
      value: 0.4,
      random: false
    },
    size: {
      value: 6,
      random: true
    },
    line_linked: {
      enable: true,
      distance: 150,
      color: "#3f51b5",
      opacity: 0.25,
      width: 2
    },
    move: {
      enable: true,
      speed: 1.2,
      direction: "none",
      random: false,
      straight: false,
      out_mode: "out"
    }
  },
  interactivity: {
    detect_on: "canvas",
    events: {
      onhover: {
        enable: true,
        mode: "repulse"
      },
      onclick: {
        enable: false
      },
      resize: true
    },
    modes: {
      repulse: {
        distance: 100,
        duration: 0.4
      }
    }
  },
  retina_detect: true
});
