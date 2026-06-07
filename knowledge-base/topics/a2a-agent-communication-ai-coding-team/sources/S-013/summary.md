# Semantic Kernel Agent Framework

Semantic Kernel Agent Framework | Microsoft Learn (function () { try { var state = JSON.parse(localStorage.getItem('atlas-layout-preferences') || '{}'); var view = state["docs-layout-persistence"] || {}; var excludesKey = ""; var blocked = {}; if (excludesKey) { var exclusions = JSON.parse(localStorage.getItem('atlas-layout-exclusions') || '{}'); if (Object.prototype.hasOwnProperty.call(exclusions, excludesKey)) { var scoped = exclusions[excludesKey]; if (scoped) { if (typeof scoped === 'object') blocked = scoped; } } } var html = document.documentElement; for (var c in view) { if (Object.prototype.hasOwnProperty.call(blocked, c)) continue; if (view[c]) html.classList.add(c); else html.classList.remove(c); } } catch (e) {} })();; var msDocs = { "environment": { "accessLevel": "online", "azurePortalHostname": "portal.azure.com", "reviewFeatures": false, "supportLevel": "production", "systemContent": true, "siteName": "learn", "legacyHosting": false }, "data": { "contentLocale": "en-us", "contentDir": "ltr", "userLocale": "en-us", "userDir": "ltr", "pageTemplate": "Conceptual", "layoutStateStorageKey": "docs-layout-persistence", "brand": "", "context": {}, "standardFeedback": false,

## Limitations

- This is an initial machine-generated extraction and must be reviewed by an agent.
