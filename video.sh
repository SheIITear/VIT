#!/bin/bash

python <(cat <<EOF
import sys
import time
fps = 30; time_per_frame = 2.0 / fps
buf = ''; frame = 0; next_frame = 0
begin = time.time()
try:
  for i, line in enumerate(sys.stdin):
    if i % 32 == 0:
      frame += 1
      sys.stdout.write(buf); buf = ''
      elapsed = time.time() - begin
      repose = (frame * time_per_frame) - elapsed
      if repose > 0.0:
        time.sleep(repose)
      next_frame = elapsed / time_per_frame
    if frame >= next_frame:
      buf += line
except KeyboardInterrupt:
  pass
EOF
) < <(cat /dev/shm/out)
