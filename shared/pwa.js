/* Rejestracja PWA także przy bezpośrednim wejściu do produktu. */
if ('serviceWorker' in navigator && window.isSecureContext && /^https?:$/.test(location.protocol)) {
  navigator.serviceWorker.register('./sw.js').catch(error => console.warn('KODOWIT PWA:', error));
}
