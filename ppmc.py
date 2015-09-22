import math

k = 3 # context size
#msg = open('test-input.txt', 'r').read()
msg = 'Prediction by partial matching'

bits = list()
table = [dict() for i in range(k+2)] # {-1, ..., k}
escape = '<$>'
output = '%s, %.5f'

# -1 table, default ctx is ''
table[0][''] = dict()
for i in range(2**8):
  table[0][''][chr(i)] = 1

def predict(c, ctx, s, impossible):
  if ctx in table[s+1]:
    cp = table[s+1][ctx].copy()
    for key in impossible:
      if key in cp:
        cp.pop(key)
    distinct = 0 if s == -1 else len(cp.keys())
    csum = sum(cp.values())
    if c in cp:
      prob = float(cp[c]) / float(distinct + csum)
      bits.append(- math.log(prob,2))
      print output % ("' '" if c == ' ' else c, prob)
    else:
      if csum > 0:
        prob = float(distinct) / float(distinct + csum)
        bits.append(- math.log(prob,2))
        print output % (escape, prob)
      predict(c, ctx[1:], s-1, impossible + cp.keys())
  else:
    predict(c, ctx[1:], s-1, impossible)

def update(c, ctx):
  for i in range(0,len(ctx)+1):
    pre = ctx[i:]
    s = len(pre)
    if pre not in table[s+1]:
      table[s+1][pre] = dict()
    if c not in table[s+1][pre]:
      table[s+1][pre][c] = 0
    table[s+1][pre][c] += 1

for i in range(len(msg)):
  c = msg[i]
  start = i - k if i > k else 0
  context = msg[start:i]
  predict(c, context, len(context), [])
  update(c, context)

print 'Total bits:', sum(bits)
