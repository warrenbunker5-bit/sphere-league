// Bump VERSION on every release so phones pick up the new build.
const VERSION = 'v35';
const CACHE = 'sphere-league-' + VERSION;
const CORE = ['./', './index.html', './manifest.webmanifest', './icons/icon-192.png', './icons/icon-512.png', './art/ball.png', './art/ball_glow.png', './art/sphere_interior.jpg', './art/sphere_backdrop.jpg', './art/portraits.jpg', './art/portraits_jersey.png', './art/swimmer_human.png', './art/rig/human/rig.json', './art/rig/human/head.png', './art/rig/human/head_sleep.png', './art/rig/human/torso.png', './art/rig/human/pelvis.png', './art/rig/human/upper_arm.png', './art/rig/human/forearm.png', './art/rig/human/fist.png', './art/rig/human/thigh.png', './art/rig/human/shin.png', './art/swimmer_human_jersey.png', './art/swimmer_vanguard.png', './art/swimmer_vanguard_jersey.png', './art/swimmer_amphibian.png', './art/swimmer_amphibian_jersey.png', './art/swimmer_dragonfly.png', './art/swimmer_dragonfly_jersey.png', './art/swimmer_river_otter.png', './art/swimmer_river_otter_jersey.png', './art/swimmer_anaconda.png', './art/swimmer_anaconda_jersey.png', './art/swimmer_piranha.png', './art/swimmer_piranha_jersey.png', './art/swimmer_river_predator.png', './art/swimmer_river_predator_jersey.png', './art/swimmer_axolotl.png', './art/swimmer_axolotl_jersey.png', './art/swimmer_human_f.png', './art/swimmer_human_f_jersey.png', './art/swimmer_synthari_m.png', './art/swimmer_synthari_m_jersey.png', './art/swimmer_synthari_f.png', './art/swimmer_synthari_f_jersey.png', './art/swimmer_octarine.png', './art/swimmer_octarine_jersey.png', './art/swimmer_mantae.png', './art/swimmer_mantae_jersey.png', './art/swimmer_cartilagin.png', './art/swimmer_cartilagin_jersey.png', './art/swimmer_crustal.png', './art/swimmer_crustal_jersey.png', './art/swimmer_tree_frog.png', './art/swimmer_tree_frog_jersey.png', './art/swimmer_angler.png', './art/swimmer_angler_jersey.png', './art/swimmer_trench.png', './art/swimmer_trench_jersey.png', './art/icon_poison.png', './art/icon_sleep.png', './art/icon_hex.png', './art/icon_fire.png', './art/icon_swirl.png', './art/icon_ice.png', './art/icon_mirage.png', './art/icon_anchor.png', './art/icon_drain.png', './art/icon_shield.png', './art/crest_lakewood_riptide.png', './art/crest_mile_high_currents.png', './art/crest_boulder_breakers.png', './art/crest_aurora_anglers.png', './art/crest_durango_divers.png', './art/crest_pikes_peak_undertow.png'];

self.addEventListener('install', e => {
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(CORE)));
});
self.addEventListener('message', e => { if (e.data === 'skipWaiting') self.skipWaiting(); });
self.addEventListener('activate', e => {
  e.waitUntil(caches.keys().then(ks => Promise.all(ks.filter(k => k !== CACHE).map(k => caches.delete(k))))
    .then(() => self.clients.claim()));
});
self.addEventListener('fetch', e => {
  if (e.request.method !== 'GET') return;
  const url = new URL(e.request.url);
  if (url.origin === location.origin && e.request.mode === 'navigate') {
    // Game page: network first so updates show up, cache when offline.
    e.respondWith(fetch(e.request).then(r => { const cp = r.clone(); caches.open(CACHE).then(c => c.put('./index.html', cp)); return r; })
      .catch(() => caches.match('./index.html')));
    return;
  }
  // Everything else (icons, fonts): cache first, then network.
  e.respondWith(caches.match(e.request).then(hit => hit || fetch(e.request).then(r => {
    if (r.ok || r.type === 'opaque') { const cp = r.clone(); caches.open(CACHE).then(c => c.put(e.request, cp)); }
    return r;
  })));
});
