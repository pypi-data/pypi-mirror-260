behave-django-steps
===
[![Coverage Status](https://coveralls.io/repos/github/BillSchumacher/behave-django-steps/badge.svg?branch=main)](https://coveralls.io/github/BillSchumacher/behave-django-steps?branch=main)

Reduce boilerplate in your behave steps for Django.

Features
---

Authentication Steps: [authentication.feature](tests%2Facceptance%2Ffeatures%2Fauthentication.feature)

Authorization Steps: [authorization.feature](tests%2Facceptance%2Ffeatures%2Fauthorization.feature)

Model Steps: [models.feature](tests%2Facceptance%2Ffeatures%2Fmodels.feature)

Performance Steps: [queries.feature](tests%2Facceptance%2Ffeatures%2Fqueries.feature)

Request Steps: [requests.feature](tests%2Facceptance%2Ffeatures%2Frequests.feature)


Caveats
---

When loading `auth.Permission` fixtures you must consider that Django
automatically creates basic permissions for models.

If you're trying to load custom permissions after writing the `Permission.json` fixture
you need to delete the default permissions from the fixture, or json.loads it and filter
on only your custom permissions.

Because the permission was already created by Django, if you try to load it
you will get an `IntegrityError`.
