Introduction
============

The ``gs.errormesg`` product primarily supplies two `error messages`_ for
GroupServer_.

It also supplies two base classes: ``gs.errormesg.baseerror.BaseErrorPage``
and the ``gs.errormesg.BaseError`` abstract base class. These classes are
used to handle errors that are provided by the higher-level
products. Examples include 

* The Gone (410) error that is returned when a person tries to access a
  hidden post (``gs.group.messages.post``)

* The Bad Request (400) that is returned if the email-verification ID is
  missing from a request (``gs.profile.email.verify``).

* The Forbidden (403) error that is handled by the ``gs.login`` system. 

All the errors in conform to the same basic design_.

Error Messages
==============

This product supplies the two standard error messages: `Not Found (404)`_,
and `Unexpected (500)`_. There are two versions of each of these
messages. One supports `infrae.wsgi`_; it has the advantage of keeping the
URL that caused the error static, but it requires WSGI to be used as a
front-end to Zope. The other provides the error pages when WSGI is not
used. The ``Products.GroupServer.groupserver.GroupserverSite`` class
catches the errors and instantiates to the Not Found or Unexpected pages as
appropriate.

Not Found (404)
---------------

The 404 page was inspired by the article `A More Useful 404`_ on A List
Apart. The ``NotFound`` class examines the ``HTTP_REFERER`` header of the
request, to determine the referring sytstem. The page then makes a
suggestion based on the referrer.

================  =============================================================
Referrer          Suggestion
================  =============================================================
A search engine   Wait for the link to be corrected.
An external site  Contact the referring site to fix the link.
Internal          Email support on the current site.
A direct link     Check what was typed, or if the link was broken over a line.
================  =============================================================

Unexpected (500)
----------------

The Unexpected Error page is shown when an exception other than Not Found
is thrown. The last line of the Python traceback is shown on this page, and
in the email to Support. The traceback is described as "technical
information", to mitigate problems caused by the confusing data being shown
to non-technical participants.

Going to ``/fail`` will trigger an assertion error, which can be used to
test the Unexpected page.

Design
======

The design behind the error messages is based on the `alert text`_ rules
from the GNOME Human Interface Guidelines.

* The page title provides the basic information.
* The body provides more detail of the issue, and a suggestion of what to do.
* Links are provided to carry out the suggestion.

Generally the suggestion is to email support. We, as designers, will know
far more about the error and what is needed in the email to support than
any group member. So it is the job of our error pages to *write* the email
to support, by setting the ``body`` of the ``mailto``::

  mailto:support@example.com?Subject=Error Name&body=Hello,

* The ``Subject`` should never contain dynamic text, because it is useful
  to have all the related errors in one topic in the support group. The
  subject should follow the page title.
* The body-text should be written as if it was sent from the user (as it
  will be).
* If additional information is needed from the group member (such as what
  he or she was trying to do when the error occurred) then ellipsis
  (``...``) are added at the *end* of the text, before any technical
  information.
* If technical information is supplied (such as by a 500 error) then it
  should be placed at the *bottom* of the email, following the disclaimer
  ``This technical information may help you fix the error:``

Finally, some technical information should be provided on the page. This
will make debugging easier (which is important as we will see our error
pages more than anyone else). This information is placed at the bottom of
the page in a ``<div>`` element with the ``technical`` ID. 

Resources
=========

- Code repository: https://source.iopen.net/groupserver/gs.errormesg
- Questions and comments to http://groupserver.org/groups/development
- Report bugs at https://redmine.iopen.net/projects/groupserver

.. _GroupServer: http://groupserver.org/
.. _A More Useful 404: http://www.alistapart.com/articles/amoreuseful404/
.. _alert text: http://developer.gnome.org/hig-book/stable/windows-alert.html.en#alert-text
.. _infrae.wsgi: http://pypi.python.org/pypi/infrae.wsgi
