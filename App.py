from matplotlib import pyplot as plt
from math import pi, sin, cos, fabs, exp, log

# 1. Data: Function that will be quantized
def f(t):
    return exp(-t**2/2)
# 2. Data: Interval beginning
begin = - 2 * pi
# 3. Data: Interval end
end = 2 * pi


# Function for sampling
def sample(signal):
    # I will take 4*len(signal) elements for a good signal presentation
    t = begin
    t_sample = list()
    halfElements = int((len(signal) - 1) / 2)
    # If signal has 201 elements ----> halfElements = 100
    # New halfElements will be 400 now
    stepOfSample =  pi / (4*halfElements)
    sampledSignal = list()
    while t <= end:
        sampledSignal.append(f(t))
        t_sample.append(t)
        t += stepOfSample
    return sampledSignal, t_sample


# Function for quantization
def quantization(sampledSignal, timeOfSample, k):
    # k = number of bits I send
    if k <= 0 or k != int(k):
        print("Error using 'quantization' function.")
        return -1000
    # Δ = Vpp / 2^k
    Vmax = max(sampledSignal)
    Vmin = min(sampledSignal)
    delta = (Vmax - Vmin) / (2**k)
    # Create the levels of quantization
    levels = list()
    level = Vmin
    while level < Vmax:
        levels.append(level + delta/2)
        level += delta
    # For 3 bits and s(t) = sin(t) ----> Vmax = -Vmin = 1 ----> delta = (1-(-1)) / 2^3 = 0.25 ----> levels = [-0.875, -0.625, -0.375, -0.125, 0.125, 0.375, 0.625, 0.875]
    # Now, its time for the values of sampledSignal to be snapped to the numbers contained in the "levels" vector
    quantizedSignal = list()
    for s in sampledSignal:
        minimumDiafora = Vmax - Vmin
        index = 0
        for i in range(len(levels)):
            if fabs(s - levels[i]) < minimumDiafora:
                minimumDiafora = fabs(s - levels[i])
                index = i
        quantizedSignal.append(levels[index])
    timeOfQuantization = timeOfSample
    return quantizedSignal, timeOfQuantization

# *********************************************************************************************************
# ********************************************* MAIN FUNCTION *********************************************
# *********************************************************************************************************

# 1. Create a list with time(t)-coordinates ----> t = [0, pi/100, 2*pi/100, ...., 2*pi-pi/100, 2*pi] with 201 elements
t = list()
i = begin
step = pi / 100
while i <= end:
    t.append(i)
    i += step

# 2. Create the signal I will transmit: s(t) = sin(t)
signal = list()
for time in t:
    signal.append(f(time))
# 3. Create the sampled vector
sampledSignal, timeOfSample = sample(signal)
# 4. Quantization
k = 4
quantizedSignal, timeOfQuantization = quantization(sampledSignal, timeOfSample, k)


plt.plot(t, signal, label='Transmitted Singal s(t)')
# plt.plot(timeOfSample, sampledSignal, label='Sample of: s(t) = sin(t)')
plt.plot(timeOfQuantization, quantizedSignal, label='Quantized Singal if I send ' + str(k) + ' bits')
plt.legend()
plt.show()