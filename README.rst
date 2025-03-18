===========
Restricción de Listas de Precios por Usuario Portal
===========

.. |badge1| image:: https://img.shields.io/badge/maturity-Stable-brightgreen
    :target: https://odoo-community.org/page/development-status
    :alt: Stable
.. |badge2| image:: https://img.shields.io/badge/licence-AGPL--3-blue.png
    :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
    :alt: License: AGPL-3
.. |badge3| image:: https://onlyone.odoo.com/web/image/website/1/logo/OnlyOne%20Soft?unique=dccda5b
    :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
    :alt: License: AGPL-3

|badge1| |badge2| |badge3| 

This module extends the functionality of Odoo"s Website Sale module to restrict the selectable pricelists for portal users based on the `allowed_pricelist_ids` field assigned to their contact. It allows you to limit the pricelists that portal users can choose in the shop to those with an ID less than or equal to the maximum ID specified in their allowed pricelists.

**Table of contents**

.. contents::
   :local:

Install
=======

To install this module, you need to:

1. Clone or download the module into your Odoo addons directory.
2. Update the Odoo module list from the interface (Apps > Update Apps List).
3. Search for "Restricción de Listas de Precios por Usuario Portal" and click "Install".

Configure
=========

To configure this module, you need to:

1. Go to **Contacts** in Odoo.
2. Open the contact record associated with a portal user.
3. Navigate to the "Configuración del Portal" tab.
4. Add the desired pricelists to the `allowed_pricelist_ids` field (e.g., pricelists with IDs 1, 2, 3).
5. Save the changes.

Usage
=====

1. Log in as a portal user with configured `allowed_pricelist_ids`.
2. Go to the shop page (`/shop`).
3. Verify that only pricelists with IDs less than or equal to the maximum allowed ID (e.g., <= 3) are available in the pricelist dropdown.
4. Attempt to manually select a non-allowed pricelist (e.g., via `/shop/change_pricelist/4`) and confirm it redirects back to the shop without applying the change.

Known issues / Roadmap
======================

* No known issues at this time.
* Future enhancements could include support for more complex pricelist restriction rules (e.g., based on fields other than ID).

Bug Tracker
===========

For bug reports or support, please contact us at:

* Help Contact: `support@onlyone.odoo.com <mailto:support@onlyone.odoo.com>`_

Credits
=======

Authors
~~~~~~~

* Be OnlyOne

Contributors
~~~~~~~~~~~~

* `Be OnlyOne <https://onlyone.odoo.com/>`_
  
  * Matías Bressanello

Maintainers
~~~~~~~~~~~

This module is maintained by Be OnlyOne