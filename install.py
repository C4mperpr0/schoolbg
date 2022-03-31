import os

with open(f"{os.environ['HOME']}/.profile") as file:
    profile = file.read()
expected_profile = '# ~/.profile: executed by the command interpreter for login shells.\n# This file is not read by bash(1), if ~/.bash_profile or ~/.bash_login\n# exists.\n# see /usr/share/doc/bash/examples/startup-files for examples.\n# the files are located in the bash-doc package.\n\n# the default umask is set in /etc/profile; for setting the umask\n# for ssh logins, install and configure the libpam-umask package.\n#umask 022\n\n# if running bash\nif [ -n "$BASH_VERSION" ]; then\n    # include .bashrc if it exists\n    if [ -f "$HOME/.bashrc" ]; then\n        . "$HOME/.bashrc"\n    fi\nfi\n\n# set PATH so it includes user\'s private bin if it exists\nif [ -d "$HOME/bin" ] ; then\n    PATH="$HOME/bin:$PATH"\nfi\n'

if profile == expected_profile:
    profile = profile.split('\n')
    profile = profile.insert(15, "echo hi\n")
    profile = '\n'.join(profile)
else:
    profile += "\necho hi\n"

with open(f"{os.environ['HOME']}/.profile", "w") as file:
    file.write(profile)
