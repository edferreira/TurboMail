TurboMail is a multi-threaded mail delivery subsystem and MIME message
generation framework for Python.

TurboMail 3 offers:

 * Simplified creation of complex messages, including rich text, attachments,
   and more.

 * Modular delivery managers including the blocking immediate manager, or the
   two threading managers: on-demand, and polling.

 * Modular back-ends including SMTP and debug (in-memory "storage")

 * Easier debugging when using the debug back-end in concert with the
   immediate manager.

 * A plugin architecture with a sample plugin for altered message encoding.

 * Automatic integration into TurboGears 1.x and Pylons (including TurboGears 2.)

Python includes several standard packages for handling e-mail. These libraries 
are independent of each-other, their documentation is hard-to-follow, and their 
examples are hardly real-world. TurboMail ties these dispersant elements 
together with an elegant and extensible API, freeing you (the developer) from 
drudge-work, strained eyes, and loss of hair, even for the most complicated 
use-cases.

