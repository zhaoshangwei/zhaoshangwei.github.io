/* Retire the legacy offline-first service worker after the academic redesign.
 * Existing readers may still have precache-v1/runtime registered. This worker
 * installs, clears only the old website cache names, then unregisters itself.
 * The portfolio pages no longer register a new service worker.
 */
self.addEventListener("install", event => {
  event.waitUntil(self.skipWaiting());
});
self.addEventListener("activate", event => {
  event.waitUntil(
    Promise.all([
      caches.delete("precache-v1"),
      caches.delete("runtime")
    ]).then(() => self.registration.unregister())
  );
});
