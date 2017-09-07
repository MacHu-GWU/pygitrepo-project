This directory includes several bash script to perform some common operation in development.


in Windows
----------
1. Install `Git Bash <https://git-scm.com/downloads>`_ (Git includes git-bash).
2. Install `MinGW <http://www.mingw.org/>`_.
3. Set git-bash is the default application to run ``.sh`` file.


in PyCharm
----------
1. Set up external tools: ``Preference`` -> ``Tools`` -> ``External Tools`` -> ``Add new one`` click ``+`` sign.
2. Config executable: ``Name``: name for this tool, I use ``Run with Bash``, ``Description``: any description text, ``Program``: The executable file (.exe for Windows, usually using git-bash.exe, /bin/bash for MacOS), ``Parameters``: ``$FileName$`` (you can select from macro), ``Working Directory``: ``$FileDir$``, click ``OK``.
3. Assign a Keymap: ``Preference`` -> ``Keymap`` -> Search ``Run with Bash`` -> Add a keymap, I use ``Shift + ```.
4. Try it out: select a file in project view, press Ctrl + Shift + `````.

or you can install `BashSupport <https://plugins.jetbrains.com/plugin/4230-bashsupport>`_.