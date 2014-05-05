Algorithm 1 Obtain a Poisson deviate from a [0, 1)
value
Parameters 0 ≤ x < 1, μ ≥ 0
L ← exp (−μ), k ← 0, prob ← 1
repeat
increment k
prob ← prob ∗ x
until prob > L
return k

