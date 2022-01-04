/**Creates the service worker and implements its strategies. */

import {
  registerRoute,
  setCatchHandler,
  setDefaultHandler,
} from "workbox-routing";
import {
  NetworkFirst,
  StaleWhileRevalidate,
  CacheFirst,
  NetworkOnly,
} from "workbox-strategies";
import { CacheableResponsePlugin } from "workbox-cacheable-response";
import { ExpirationPlugin } from "workbox-expiration";

const FALLBACK_URI = "/offline/";

const STATIC_PAGES: string[] = [];
const NETWORK_ONLY_PAGES = [
  `checkout`,
  "change-password",
  "logout",
  "login",
  "register",
  "password"
];

self.addEventListener("install", async (event: any) => {
  event.waitUntil(
    caches.open("static_pages").then((cache) => cache.add(FALLBACK_URI))
  );
});

/**Implement stale while revalidate strategy for static pages. */
registerRoute(
  ({ request }) => {
    return (
      request.mode === "navigate" &&
      STATIC_PAGES.some((path) => request.url.search(path) >= 0)
    );
  },
  new StaleWhileRevalidate({
    cacheName: "static_pages",
    plugins: [
      new CacheableResponsePlugin({
        statuses: [200],
      }),
    ],
  })
);

/**Implement network only strategy. */
registerRoute(({ request }) => {
  return (
    request.mode === "navigate" &&
    NETWORK_ONLY_PAGES.some((path) => request.url.search(path) >= 0)
  );
}, new NetworkOnly());

// This code is left in in case we want to include dynamic pages.
// /**Treat other HTMLs as dynamic pages. */
// registerRoute(
//   ({ request }) => {
//     return (
//       request.mode === "navigate" &&
//       STATIC_PAGES.every((path) => request.url.search(path) === -1) &&
//       NETWORK_ONLY_PAGES.every((path) => request.url.search(path) === -1)
//     );
//   },
//   new NetworkFirst({
//     cacheName: "dynamic_pages",
//     plugins: [
//       new CacheableResponsePlugin({
//         statuses: [200],
//       }),
//     ],
//   })
// );

// Cache CSS, JS, and Web Worker requests with a Stale While Revalidate strategy
registerRoute(
  // Check to see if the request's destination is style for stylesheets, script for JavaScript, or worker for web worker
  ({ request }) =>
    request.destination === "style" ||
    request.destination === "script" ||
    request.destination === "worker",
  // Use a Stale While Revalidate caching strategy
  new StaleWhileRevalidate({
    // Put all cached files in a cache named 'assets'
    cacheName: "assets",
    plugins: [
      // Ensure that only requests that result in a 200 status are cached
      new CacheableResponsePlugin({
        statuses: [200],
      }),
    ],
  })
);

// Cache images with a Cache First strategy
registerRoute(
  // Check to see if the request's destination is style for an image
  ({ request }) => request.destination === "image",
  // Use a Cache First caching strategy
  new CacheFirst({
    // Put all cached files in a cache named 'images'
    cacheName: "images",
    plugins: [
      // Ensure that only requests that result in a 200 status are cached
      new CacheableResponsePlugin({
        statuses: [200],
      }),
      // Don't cache more than 50 items, and expire them after 30 days
      new ExpirationPlugin({
        maxEntries: 50,
        maxAgeSeconds: 60 * 60 * 24 * 30, // 30 Days
      }),
    ],
  })
);

// Cache Google Fonts with a stale-while-revalidate strategy, with
// a maximum number of entries.
registerRoute(
  ({ url }) =>
    url.origin === "https://fonts.googleapis.com" ||
    url.origin === "https://fonts.gstatic.com",
  new StaleWhileRevalidate({
    cacheName: "google-fonts",
    plugins: [new ExpirationPlugin({ maxEntries: 20 })],
  })
);

// Use a stale-while-revalidate strategy for all other requests.
//@ts-ignore
setDefaultHandler(new NetworkFirst());

// Fallback
//@ts-ignore
setCatchHandler(({ event }) => {
  if (event.request.destination === "document") {
    return caches.match(FALLBACK_URI);
  } else {
    return Response.error();
  }
});
