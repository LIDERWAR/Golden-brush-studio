/* ==============================================================================
   GB STUDIO — Force Dark Architecture Theme
   ============================================================================== */
(function() {
    try {
        localStorage.setItem('jazzmin-theme-mode', 'dark');
        document.documentElement.setAttribute('data-bs-theme', 'dark');
    } catch (e) {
        // Storage access may be restricted in private browsing
    }
})();
