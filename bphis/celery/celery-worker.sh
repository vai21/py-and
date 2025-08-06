set -o errexit
set -o nounset

celery -A celerypyand worker -l info --pool=solo
