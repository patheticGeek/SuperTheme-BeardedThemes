/* Bearded Themes — site behaviour: variant switching, copy buttons, tabs. */

const VARIANTS = {
  diamond: {
    ident: 'BeardedDiamond',
    slug: 'black-and-diamond',
    idLower: 'beardeddiamond',
    name: 'Black & Diamond',
    accent: '#11B7D4',
    accentSoft: '#63ddf2',
  },
  gold: {
    ident: 'BeardedGold',
    slug: 'black-and-gold',
    idLower: 'beardedgold',
    name: 'Black & Gold',
    accent: '#c7910c',
    accentSoft: '#f4c54f',
  },
  emerald: {
    ident: 'BeardedEmerald',
    slug: 'black-and-emerald',
    idLower: 'beardedemerald',
    name: 'Black & Emerald',
    accent: '#38c7bd',
    accentSoft: '#90e0da',
  },
};

/* Shared across every variant -- only the accent differs. */
const BASE_SWATCHES = [
  ['Background', '#111418'],
  ['Surface', '#161a1f'],
  ['Titlebar', '#060708'],
  ['Terminal', '#0f1215'],
  ['Foreground', '#bec6d0'],
  ['Muted', '#a0acbb'],
  ['Border', '#3b4654'],
  ['Green', '#00a884'],
  ['Yellow', '#c7910c'],
  ['Red', '#e35535'],
  ['Magenta', '#d46ec0'],
];

const root = document.documentElement;

function applyVariant(key) {
  const v = VARIANTS[key];
  if (!v) return;

  root.dataset.variant = key;
  root.style.setProperty('--accent', v.accent);
  root.style.setProperty('--accent-soft', v.accentSoft);

  document.querySelectorAll('.switcher button').forEach((b) => {
    b.setAttribute('aria-checked', String(b.dataset.variant === key));
  });

  document.querySelectorAll('.v-ident').forEach((el) => { el.textContent = v.ident; });
  document.querySelectorAll('.v-slug').forEach((el) => { el.textContent = v.slug; });
  document.querySelectorAll('.v-id').forEach((el) => { el.textContent = v.idLower; });

  setText('live-ident', v.ident);
  setText('live-slug', v.slug);
  setText('live-id', `org.kde.${v.idLower}.desktop`);
  setText('win-title', `${v.ident} — ~/Projects`);

  renderSwatches(v);
}

function setText(id, text) {
  const el = document.getElementById(id);
  if (el) el.textContent = text;
}

function renderSwatches(v) {
  const host = document.getElementById('swatches');
  if (!host) return;
  const entries = [['Accent', v.accent], ...BASE_SWATCHES];
  host.innerHTML = entries
    .map(
      ([name, hex]) => `
      <div class="swatch">
        <div class="chip" style="background:${hex}"></div>
        <span class="name">${name}</span>
        <span class="hex">${hex.toUpperCase()}</span>
      </div>`
    )
    .join('');
}

document.querySelectorAll('.switcher button').forEach((btn) => {
  btn.addEventListener('click', () => applyVariant(btn.dataset.variant));
});

/* --- copy buttons -------------------------------------------------------- */

document.querySelectorAll('.copy').forEach((btn) => {
  btn.addEventListener('click', async () => {
    const target = document.querySelector(btn.dataset.copy);
    if (!target) return;
    try {
      await navigator.clipboard.writeText(target.textContent.trim());
    } catch {
      return; /* clipboard blocked (insecure context, denied permission) */
    }
    const label = btn.querySelector('span');
    const original = label.textContent;
    label.textContent = 'Copied';
    btn.classList.add('done');
    setTimeout(() => {
      label.textContent = original;
      btn.classList.remove('done');
    }, 1600);
  });
});

/* --- tabs ---------------------------------------------------------------- */

const tabButtons = [...document.querySelectorAll('.tab-btns button')];
tabButtons.forEach((btn) => {
  btn.addEventListener('click', () => {
    tabButtons.forEach((b) => {
      const selected = b === btn;
      b.setAttribute('aria-selected', String(selected));
      document.getElementById(b.getAttribute('aria-controls')).hidden = !selected;
    });
  });
});

/* --- nav border on scroll ------------------------------------------------ */

const nav = document.querySelector('.nav');
const onScroll = () => nav.classList.toggle('scrolled', window.scrollY > 8);
window.addEventListener('scroll', onScroll, { passive: true });
onScroll();

/* --- reveal sections as they come into view ------------------------------ */

const revealables = document.querySelectorAll('.section, .variants');
if ('IntersectionObserver' in window) {
  const io = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add('in');
          io.unobserve(entry.target);
        }
      });
    },
    { rootMargin: '0px 0px -12% 0px' }
  );
  revealables.forEach((el) => {
    el.classList.add('reveal');
    io.observe(el);
  });
}

applyVariant('emerald');
