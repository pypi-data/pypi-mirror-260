# WebCase Jet Sidebar Customization

**WebCase Jet Sidebar Customization** offers a flexible and powerful customization system for the Django admin interface sidebar, allowing administrators to configure the order, custom names, positioning, and view mode (compact or expanded) of sidebar items for the current user.

This package is perfect for those looking to enhance the usability and efficiency of their admin panel, providing custom settings for each sidebar item based on user needs and preferences.

## Installation

To get started with **WebCase Jet Sidebar Customization**, follow these steps:

Install the package using pip:

```sh
pip install wc-django-jet-sidebar
```

Add `wcd_jet_sidebar` to your `settings.py`:

```python
INSTALLED_APPS += [
  'wcd_jet_sidebar',
]
```

To integrate with your project, replace the inheritance of your admin interface templates:

In `/markup/templates/admin/base_site.html` and `/markup/templates/rosetta/base.html` files, replace:

```html
{% extends "admin/base.html" %}
```

With:

```html
{% extends "wcd_jet_sidebar/base.html" %}
```

## Enjoy!

You are now ready to use **WebCase Jet Sidebar Customization** to customize and optimize your Django admin interface. Personalize your sidebar effortlessly and conveniently, making your work more productive and enjoyable.