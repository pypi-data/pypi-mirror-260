Changelog
=========

All notable changes to this project will be documented in this file.

The format is based on `Keep a Changelog`_,
and this project adheres to `Semantic Versioning`_.

Unreleased
----------

This version requires AlekSIS-Core 3.0. It is incompatible with any previous
version.

Removed
~~~~~~~

* Legacy menu integration for AlekSIS-Core pre-3.0


Added
~~~~~

* Support for SPA in AlekSIS-Core 3.0

Fixed
-----

* Replace usage of deprecated `ugettext_lazy` with `gettext_lazy`.

`1.2`_ - 2022-03-20
-------------------

Added
-----

* Update django-payments to 1.0
* Update invoice if person changes

Changed
-------

* Always set person on Invoice objects

`1.1.1`_ - 2022-03-15
---------------------

Fixed
~~~~~

* Fixed VAT display in totals table

`1.1`_ - 2022-03-15
---------------------

Added
~~~~~

* Allow changing the payment variant under certain conditions

Fixed
~~~~~

* Add a missing dependency for Sofort payments

Changed
~~~~~~~

* Purchased items are expected to list net prices

`1.0.2`_ - 2022-03-14
---------------------

Fixed
~~~~~

* Migration was missing

`1.0.1`_ - 2022-03-14
--------------------

Fixed
~~~~~

* Remove NOT NULL constraint from for_object in Invoice
* Fix return value of get_purchased_items in manual invoicing

Changed
~~~~~~~

* Billing address is auto-filled from related person

`1.0`_
------

Added
~~~~~

* Initial release.


.. _Keep a Changelog: https://keepachangelog.com/en/1.0.0/
.. _Semantic Versioning: https://semver.org/spec/v2.0.0.html


.. _1.0: https://edugit.org/AlekSIS/onboarding//AlekSIS-App-Tezor/-/tags/1.0
.. _1.0.1: https://edugit.org/AlekSIS/onboarding//AlekSIS-App-Tezor/-/tags/1.0.1
.. _1.0.2: https://edugit.org/AlekSIS/onboarding//AlekSIS-App-Tezor/-/tags/1.0.2
.. _1.1: https://edugit.org/AlekSIS/onboarding//AlekSIS-App-Tezor/-/tags/1.1
.. _1.1.1: https://edugit.org/AlekSIS/onboarding//AlekSIS-App-Tezor/-/tags/1.1.1
.. _1.2 https://edugit.org/AlekSIS/onboarding//AlekSIS-App-Tezor/-/tags/1.2
