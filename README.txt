Introduction
============

The ``gs.errormesg`` product primarily supplies three `error messages`_. 

It also supplies two base classes: ``gs.errormesg.baseerror.BaseErrorPage``
and the ``gs.errormesg.BaseError`` abstract base class. These classes are
used to handle errors that are provided by the higher-level
products. Examples include the Gone (410) error that is returned when a
person tries to access a hidden post (``gs.group.messages.post``), or the
Bad Request (400) that is returned if the email-verification ID is missing
from a request (``gs.profile.email.verify``).

All the errors conform to the same basic `design`_.

Error Messages
==============

This product supplies the three standard error messages used by
`GroupServer`_: `Not Found (404)`_, `Forbidden (403)`_, or `Unexpected
(500)`_. 

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

Forbidden (403)
---------------

If the user is logged in, and a Forbidden error is raised then this error
is shown. If the user is logged out (anonymous) then he or she is shown the
Login page (``gs.login``).

Unexpected (500)
----------------

The Unexpected Error page is shown when any other exception is
thrown. Often it is triggered by ``assert`` statements. The ``assert``
message will be shown on this page, which is why it is very important that
the messages are human-readable.

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

.. _GroupServer: http://groupserver.org/
.. _A More Useful 404: http://www.alistapart.com/articles/amoreuseful404/
.. _alert text: http://developer.gnome.org/hig-book/stable/windows-alert.html.en#alert-text
