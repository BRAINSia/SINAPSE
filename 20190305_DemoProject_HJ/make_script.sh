#!/usr/bin/env bash
FILENAME="${1}.sh"
cat > ${FILENAME} << EOF
#!/usr/bin/env bash
# Author: ${USER}
# $(date)
EOF
chmod 754 ${FILENAME}



