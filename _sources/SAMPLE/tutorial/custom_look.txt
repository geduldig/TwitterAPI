.. _custom_look:


******************************************
Customizing the look and feel of the site
******************************************

The `sphinx <http://sphinx.pocoo.org/>`_ site itself looks better than
the sites created with the default css, so here we'll invoke T. S. Eliot's
maxim "Talent imitates, but genius steals" and grab their css
and part of their layout.  As before, you can either get the required
files :file:`_static/default.css`, :file:`_templates/layout.html` and
:file:`_static/logo.png` from the website or git (see
:ref:`fetching-the-data`).  Since I did a git clone before, I will
just copy the stuff I need from there::

    home:~/tmp/sampledoc> cp ../sampledoc_tut/_static/default.css _static/
    home:~/tmp/sampledoc> cp ../sampledoc_tut/_templates/layout.html _templates/
    home:~/tmp/sampledoc> cp ../sampledoc_tut/_static/logo.png _static/
    home:~/tmp/sampledoc> ls _static/ _templates/
    _static/:
    basic_screenshot.png	default.css		logo.png

    _templates/:
    layout.html

Sphinx will automatically pick up the css and layout html files since
we put them in the default places with the default names, but we have
to manually include the logo in our :file:`layout.html`.  Let's take a
look at the layout file: the first part puts a horizontal navigation
bar at the top of our page, like you see on the `sphinx
<http://sphinx.pocoo.org>`_ and `matplotlib
<http://matplotlib.sourceforge.net/>`_ sites, the second part includes
a logo that when we click on it will take us `home` and the last part
moves the vertical navigation panels to the right side of the page::

    {% extends "!layout.html" %}


    {% block rootrellink %}
            <li><a href="{{ pathto('index') }}">home</a>|&nbsp;</li>
            <li><a href="{{ pathto('search') }}">search</a>|&nbsp;</li>
           <li><a href="{{ pathto('contents') }}">documentation </a> &raquo;</li>
    {% endblock %}


    {% block relbar1 %}

    <div style="background-color: white; text-align: left; padding: 10px 10px 15px 15px">
    <a href="{{ pathto('index') }}"><img src="{{
    pathto("_static/logo.png", 1) }}" border="0" alt="sampledoc"/></a>
    </div>
    {{ super() }}
    {% endblock %}

    {# put the sidebar before the body #}
    {% block sidebar1 %}{{ sidebar() }}{% endblock %}
    {% block sidebar2 %}{% endblock %}

Once you rebuild the site with a ``make html`` and reload the page in your browser, you should see a fancier site that looks like this

.. image:: _static/fancy_screenshot.png
