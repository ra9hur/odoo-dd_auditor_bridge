# D&amp;D Auditor Bridge

Seamless Single Sign-On from Odoo Vendor Bills to the D&amp;D Auditor Web Application.

## Overview

This module adds a **Verify D&amp;D Charges** button to your Vendor Bill (Incoming Invoice) forms in Odoo. Clicking it opens the D&amp;D Auditor Web Application, authenticated securely against your Odoo session via a shared HMAC-signed token. The module is a thin, stateless connector — no data is stored locally in Odoo.

## Features

- One-click **Verify D&amp;D Charges** button on Vendor Bill forms.
- Automated Single Sign-On using an HMAC-SHA256 signed token.
- Per-company admin toggle to enable or disable the integration.
- Configurable App URL and shared HMAC secret.

## Configuration

1. Install the module.
2. Go to **Settings &rarr; General Settings &rarr; D&amp;D Auditor**.
3. Enable the **D&amp;D Auditor Integration** toggle.
4. Set the **App URL** to your D&amp;D Auditor API base URL (e.g. `https://dd-auditor-api.onrender.com`).
5. Enter the **HMAC Secret**. It must match the `ODOO_HMAC_SECRET` configured in the D&amp;D Auditor backend.
6. Save your settings.

## Usage

Open a **Vendor Bill** (Incoming Invoice). In the header, click the **Verify D&amp;D Charges** button. A new tab opens the D&amp;D Auditor application, logged in securely on your behalf.

## Important — Paid Subscription

This module is a **free connector** that requires an active **paid tier subscription** to the **D&amp;D Audit Web Application** in order to function. The Odoo module itself is free, but access to the connected audit service is provided under a separate paid subscription.

## Support

This is a free bridge module. For issues related to the D&amp;D Audit Web Application itself (authentication, subscriptions, analytics), contact the D&amp;D Audit team directly.

## License

LGPL-3
