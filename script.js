const light = document.querySelector(".cursor-light");
const revealItems = document.querySelectorAll(".reveal");
const filters = document.querySelectorAll(".filter");
const projects = document.querySelectorAll(".project-card");
const counters = document.querySelectorAll("[data-count]");
const floaters = document.querySelectorAll(".float-el");
let countersStarted = false;
let lastSparkAt = 0;
const sparkColors = ["#f4bd34", "#f6bfd0", "#8fa45e", "#bcd0e8"];

document.addEventListener("pointermove", (event) => {
  if (!light) return;
  light.style.left = `${event.clientX}px`;
  light.style.top = `${event.clientY}px`;

  if (event.timeStamp - lastSparkAt > 70 && window.matchMedia("(pointer: fine)").matches) {
    createSpark(event.clientX, event.clientY);
    lastSparkAt = event.timeStamp;
  }

  const x = (event.clientX / window.innerWidth - 0.5) * 18;
  const y = (event.clientY / window.innerHeight - 0.5) * 18;
  floaters.forEach((item, index) => {
    const depth = (index + 1) * 0.18;
    item.style.marginLeft = `${x * depth}px`;
    item.style.marginTop = `${y * depth}px`;
  });
});

function createSpark(x, y) {
  const spark = document.createElement("span");
  spark.className = "cursor-spark";
  spark.style.left = `${x + (Math.random() - 0.5) * 18}px`;
  spark.style.top = `${y + (Math.random() - 0.5) * 18}px`;
  spark.style.setProperty("--spark-color", sparkColors[Math.floor(Math.random() * sparkColors.length)]);
  document.body.appendChild(spark);
  spark.addEventListener("animationend", () => spark.remove(), { once: true });
}

const revealObserver = new IntersectionObserver(
  (entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add("is-visible");
      }
    });
  },
  { threshold: 0.16 }
);

revealItems.forEach((item) => revealObserver.observe(item));

filters.forEach((button) => {
  button.addEventListener("click", () => {
    filters.forEach((filter) => filter.classList.remove("active"));
    button.classList.add("active");

    const selected = button.dataset.filter;
    projects.forEach((project) => {
      const shouldShow = selected === "all" || project.dataset.category.includes(selected);
      project.classList.toggle("is-hidden", !shouldShow);
    });
  });
});

document.querySelectorAll(".tilt").forEach((card) => {
  card.addEventListener("pointermove", (event) => {
    const rect = card.getBoundingClientRect();
    const x = event.clientX - rect.left;
    const y = event.clientY - rect.top;
    const rotateY = ((x / rect.width) - 0.5) * 8;
    const rotateX = ((y / rect.height) - 0.5) * -8;
    card.style.transform = `perspective(900px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) translateY(-4px)`;
  });

  card.addEventListener("pointerleave", () => {
    card.style.transform = "";
  });
});

const countObserver = new IntersectionObserver(
  (entries) => {
    entries.forEach((entry) => {
      if (!entry.isIntersecting || countersStarted) return;
      countersStarted = true;
      counters.forEach((counter) => animateCount(counter));
    });
  },
  { threshold: 0.42 }
);

const proofSection = document.querySelector(".proof");
if (proofSection) {
  countObserver.observe(proofSection);
}

function animateCount(counter) {
  const target = Number(counter.dataset.count);
  const duration = 950;
  const startedAt = performance.now();

  function tick(now) {
    const progress = Math.min((now - startedAt) / duration, 1);
    const eased = 1 - Math.pow(1 - progress, 3);
    counter.textContent = Math.round(target * eased);

    if (progress < 1) {
      requestAnimationFrame(tick);
    }
  }

  requestAnimationFrame(tick);
}

const graphicsLightbox = document.querySelector(".graphics-lightbox");
const graphicsCards = document.querySelectorAll(".paper-card");
let lastGraphicsTrigger = null;

function closeGraphicsLightbox() {
  if (!graphicsLightbox) return;
  graphicsLightbox.hidden = true;
  document.body.classList.remove("modal-open");
  if (lastGraphicsTrigger) lastGraphicsTrigger.focus();
}

graphicsCards.forEach((card) => {
  card.addEventListener("click", () => {
    if (!graphicsLightbox) return;
    lastGraphicsTrigger = card;
    const image = graphicsLightbox.querySelector(".graphics-lightbox-media img");
    image.src = card.dataset.image;
    image.alt = card.querySelector("img").alt;
    graphicsLightbox.querySelector("#graphics-lightbox-title").textContent = card.dataset.title;
    graphicsLightbox.querySelector('[data-field="tool"]').textContent = card.dataset.tool;
    graphicsLightbox.querySelector('[data-field="context"]').textContent = card.dataset.context;
    graphicsLightbox.querySelector('[data-field="thought"]').textContent = card.dataset.thought;
    graphicsLightbox.hidden = false;
    document.body.classList.add("modal-open");
    graphicsLightbox.querySelector(".graphics-lightbox-close").focus();
  });
});

if (graphicsLightbox) {
  graphicsLightbox.querySelector(".graphics-lightbox-close").addEventListener("click", closeGraphicsLightbox);
  graphicsLightbox.addEventListener("click", (event) => {
    if (event.target === graphicsLightbox) closeGraphicsLightbox();
  });
  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape" && !graphicsLightbox.hidden) closeGraphicsLightbox();
  });
}
