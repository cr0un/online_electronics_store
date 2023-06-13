#!/usr/bin/bash
python ./manage.py migrate --check
# shellcheck disable=SC2034
status=$?
# shellcheck disable=SC2050
if [[ status != 0 ]]; then
  python ./manage.py migrate
fi
exec "$@"
