window.particlesJS?.("particles-js", {
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
      type: "polygon",
      stroke: {
        width: 1,
        color: "#5a6fcf"
      },
      polygon: {
        nb_sides: 6
      }
    },
    opacity: {
      value: 0.5,
      random: false,
      anim: {
        enable: false
      }
    },
    size: {
      value: 12,
      random: true,
      anim: {
        enable: false
      }
    },
    line_linked: {
      enable: true,
      distance: 180,
      color: "#6a7dd6",
      opacity: 0.4,
      width: 2
    },
    move: {
      enable: true,
      speed: 1,      // slower speed
      direction: "none",
      random: false,
      straight: false,
      out_mode: "bounce",
      bounce: true,
      attract: {
        enable: false
      }
    }
  },
  interactivity: {
    detect_on: "canvas",
    events: {
      onhover: {
        enable: true,
        mode: "grab"
      },
      onclick: {
        enable: false
      },
      resize: true
    },
    modes: {
      grab: {
        distance: 200,
        line_linked: {
          opacity: 0.7
        }
      }
    }
  },
  retina_detect: true
});
