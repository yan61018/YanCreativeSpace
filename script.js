const light = document.querySelector(".cursor-light");
const revealItems = document.querySelectorAll(".reveal");
const filters = document.querySelectorAll(".filter");
const projects = document.querySelectorAll(".project-card");
const counters = document.querySelectorAll("[data-count]");
const floaters = document.querySelectorAll(".float-el");
let countersStarted = false;

document.addEventListener("pointermove", (event) => {
  if (!light) return;
  light.style.left = `${event.clientX}px`;
  light.style.top = `${event.clientY}px`;

  const x = (event.clientX / window.innerWidth - 0.5) * 18;
  const y = (event.clientY / window.innerHeight - 0.5) * 18;
  floaters.forEach((item, index) => {
    const depth = (index + 1) * 0.18;
    item.style.marginLeft = `${x * depth}px`;
    item.style.marginTop = `${y * depth}px`;
  });
});

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
