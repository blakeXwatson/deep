#!/bin/bash
if [ ! $(ls /bin|grep deep) ]; then sleep 0; else echo "/bin/deep already exists"; exit; fi
if [ ! $(whoami|grep root) ]; then echo "run as root"; exit; fi
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
deep_src="#/bin/bash\ndir=$DIR\npython \$dir/deep.py \$@\n"
echo -e $deep_src>./deep.sh
ln ./deep.sh /bin/deep

