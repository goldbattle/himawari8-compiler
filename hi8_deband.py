from skimage import io, filters
import numpy as np
import sys

# ./hi8-deband.py input.png output.png
# Cherrypicked sample before/after: http://basecase.org/2016/1/hi8corr

'''
Himawari-8 has slight noise along scanlines. It seems basically uncorrelated
between rows, and varies smoothly on the scale of about 100 columns.
To correct it, we create a vertically blurred image, vb, which collects
the neighborhood up and down from a given pixel. We assume that similarity
between a pixel and that neighborhood is intrinsic similarity, not noise.

We subtract vb from the input pixel, making vdiff, which represents how
much a pixel varies from its N and S neighbors. Then we blur that horizontally,
to filter out real edges, creating hb.  hb is basically a running average of
how and how much each row has been departing from its neighbor rows (on the
scale defined by the parameter h). We subtract that from the input, and presto.

As far as I've seen, the only artifact this introduces is a slight ringing
that runs E-W near strong N-S contrasts.

To do:
- use edge detection as a mask, so this only applies in low-contrast areas
- check for general numerical validity/stability:
- - would multiplicative rather than additive scaling be better?
- - check that this doesn't damage the histogram too much in practice
'''

# this seems to make it reasonably well-behaved at edges
filtermode = 'reflect'

# Vertical sigma. Too big (5ish) and there will be artifacts near edges;
# too small (0.75ish) and it will undercorrect.
v = 1.25

# Horizontal sigma. Too big (100ish) and it won't adapt fast enough to the
# horizontal variation in noise (undercorrecting); too small (3ish) and it
# will act like a 1-pixel vertical blur.
h = 10

src_path = sys.argv[1]
dst_path = sys.argv[2]

src = io.imread(src_path).astype(np.float32)/255

vb = filters.gaussian_filter(src, (v, 0, 0), mode=filtermode)
vdiff = src - vb
hb = filters.gaussian_filter(vdiff, (0, h, 0), mode=filtermode)
corr = src - hb

dst = np.clip(corr*255, 0, 255).astype(np.uint8)
io.imsave(dst_path, dst)