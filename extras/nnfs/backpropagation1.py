x = [1.0, -2.0, 3.0] # input values
w = [-3.0, -1.0, 2.0] # weights
b = 1.0 # bias
xw0 = x[0] * w[0]
xw1 = x[1] * w[1]
xw2 = x[2] * w[2]
z = xw0 + xw1 + xw2 + b

# ReLU activation function
y = max(z,0)

# Backward pass
# The derivative from the next layer
dvalue = 1.0
# Derivative of ReLU and the chain rule
drelu_dz = dvalue * (1. if z > 0 else 0.)

# Partial derivatives of the multiplication, the chain rule
dsum_dxw0 = 1
dsum_dxw1 = 1
dsum_dxw2 = 1
dsum_db = 1
drelu_dxw0 = drelu_dz * dsum_dxw0
drelu_dxw1 = drelu_dz * dsum_dxw1
drelu_dxw2 = drelu_dz * dsum_dxw2
drelu_db = drelu_dz * dsum_db
#dsum_dxw0 above means the partial derivative of the sum with respect to the x (input), weighted, for the 0th pair of inputs and weights.

# Partial derivatives of the multiplication, the chain rule
dmul_dx0 = w[0]
dmul_dx1 = w[1]
dmul_dx2 = w[2]
dmul_dw0 = x[0]
dmul_dw1 = x[1]
dmul_dw2 = x[2]
drelu_dx0 = drelu_dxw0 * dmul_dx0
drelu_dw0 = drelu_dxw0 * dmul_dw0
drelu_dx1 = drelu_dxw1 * dmul_dx1
drelu_dw1 = drelu_dxw1 * dmul_dw1
drelu_dx2 = drelu_dxw2 * dmul_dx2
drelu_dw2 = drelu_dxw2 * dmul_dw2

"""
drelu_dx0 = drelu_dxw0 * dmul_dx0

dmul_dx0 = w[0]

drelu_dx0 = drelu_dxw0 * w[0]

drelu_dxw0 = drelu_dz * dsum_dxw0

drelu_dx0 = drelu_dz * dsum_dxw0 * w[0]

dsum_dxw0 = 1

drelu_dx0 = drelu_dz * 1 * w[0] = drelu_dz * w[0]

drelu_dz = dvalue * (1. if z > 0 else 0.)

drelu_dx0 = dvalue * (1. if z > 0 else 0.) * w[0]
"""
dx = [drelu_dx0, drelu_dx1, drelu_dx2] # gradients on inputs
dw = [drelu_dw0, drelu_dw1, drelu_dw2] # gradients on weights
db = drelu_db # gradient on bias...just 1 bias here

print(dx)









