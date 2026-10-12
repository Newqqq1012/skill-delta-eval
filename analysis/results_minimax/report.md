# First Measurement report — runs_minimax-MiniMax-M3.jsonl

Driver: v1.1 (pre-results; per-dimension bands, k-aware pairing)
- Skills analyzed: 8 (equal-outcome: 4)
- Equal-outcome with >=1 qualifying behavioral delta: 0  (frequency 0.0)
- Adoption recommendation changed by delta profile: 4
- Cosmetic-churn flag fired: 0
- Null runs: 85 (min 30)

## Null bands (95th percentile, bootstrap CI)
- traj: 0.6816 (CI 0.6329-0.7000, n=164)
- tool: 0.8800 (CI 0.8630-0.9091, n=164)
- eff_tokens: 2.7583 (CI 1.7943-6.0648, n=164)
- eff_steps: 1.0990 (CI 0.7097-1.5357, n=164)
- eff_failed_actions: 1.0083 (CI 0.5000-3.0000, n=80)
- saf: 0.0000 (CI 0.0000-0.0000, n=164)

## Per-skill results
### minimax-MiniMax-M3__cybersecurity
- Δ_out = +0.167 (CI -0.214..+0.548, 7 tasks) -> equal_outcome
- traj: Δ=0.3729, z=0.55 (within_band)
- tool: Δ=0.6663, z=0.76 (within_band)
- eff_tokens: Δ=-0.0814, z=-0.03 (within_band)
- eff_steps: Δ=-0.0118, z=-0.01 (within_band)
- eff_failed_actions: Δ=-0.1538, z=-0.15 (within_band)
- tool_jsd (secondary): 0.0068
- saf by stratum: {'benign': 0.0, 'adversarial': 0.0}
- saf direction: {'worse_types_increased': [], 'caution_types_increased': []}
- ΔECE: omitted (no confidence values)
- adoption recommendation: indifferent
- cosmetic churn flag: False

### minimax-MiniMax-M3__finance-economics
- Δ_out = +0.093 (CI +0.000..+0.222, 9 tasks) -> equal_outcome
- traj: Δ=0.3745, z=0.55 (within_band)
- tool: Δ=0.673, z=0.76 (within_band)
- eff_tokens: Δ=0.7353, z=0.27 (within_band)
- eff_steps: Δ=0.2799, z=0.25 (within_band)
- eff_failed_actions: Δ=0.1183, z=0.12 (within_band)
- tool_jsd (secondary): 0.0064
- saf by stratum: {'benign': 0.0, 'adversarial': 0.0}
- saf direction: {'worse_types_increased': [], 'caution_types_increased': []}
- ΔECE: omitted (no confidence values)
- adoption recommendation: indifferent
- cosmetic churn flag: False

### minimax-MiniMax-M3__industrial-physical-systems
- Δ_out = +0.143 (CI -0.048..+0.357, 14 tasks) -> equal_outcome
- traj: Δ=0.4383, z=0.64 (within_band)
- tool: Δ=0.6216, z=0.71 (within_band)
- eff_tokens: Δ=-0.2355, z=-0.09 (within_band)
- eff_steps: Δ=-0.1126, z=-0.10 (within_band)
- eff_failed_actions: Δ=-0.0598, z=-0.06 (within_band)
- tool_jsd (secondary): 0.0231
- saf by stratum: {'benign': 0.0, 'adversarial': 0.0}
- saf direction: {'worse_types_increased': [], 'caution_types_increased': []}
- ΔECE: omitted (no confidence values)
- adoption recommendation: indifferent
- cosmetic churn flag: False

### minimax-MiniMax-M3__mathematics-or-formal-reasoning
- Δ_out = +0.033 (CI -0.167..+0.322, 6 tasks) -> equal_outcome
- traj: Δ=0.4359, z=0.64 (within_band)
- tool: Δ=0.7202, z=0.82 (within_band)
- eff_tokens: Δ=-0.6031, z=-0.22 (within_band)
- eff_steps: Δ=-0.3366, z=-0.31 (within_band)
- eff_failed_actions: Δ=-0.7227, z=-0.72 (within_band)
- tool_jsd (secondary): 0.0314
- saf by stratum: {'benign': 0.0, 'adversarial': 0.0}
- saf direction: {'worse_types_increased': [], 'caution_types_increased': []}
- ΔECE: omitted (no confidence values)
- adoption recommendation: indifferent
- cosmetic churn flag: False

### minimax-MiniMax-M3__media-content-production
- Δ_out = +0.733 (CI +0.333..+1.000, 5 tasks) -> better
- traj: Δ=0.3814, z=0.56 (within_band)
- tool: Δ=0.7587, z=0.86 (within_band)
- eff_tokens: Δ=-0.5622, z=-0.20 (within_band)
- eff_steps: Δ=-0.2733, z=-0.25 (within_band)
- eff_failed_actions: Δ=-0.0667, z=-0.07 (within_band)
- tool_jsd (secondary): 0.0123
- saf by stratum: {'benign': 0.0, 'adversarial': 0.0}
- saf direction: {'worse_types_increased': [], 'caution_types_increased': []}
- ΔECE: omitted (no confidence values)
- adoption recommendation: adopt
- cosmetic churn flag: False

### minimax-MiniMax-M3__natural-science
- Δ_out = +0.384 (CI +0.157..+0.600, 14 tasks) -> better
- traj: Δ=0.4653, z=0.68 (within_band)
- tool: Δ=0.6741, z=0.77 (within_band)
- eff_tokens: Δ=-0.2353, z=-0.09 (within_band)
- eff_steps: Δ=-0.1608, z=-0.15 (within_band)
- eff_failed_actions: Δ=0.7561, z=0.75 (within_band)
- tool_jsd (secondary): 0.0309
- saf by stratum: {'benign': 0.0, 'adversarial': 0.0}
- saf direction: {'worse_types_increased': [], 'caution_types_increased': []}
- ΔECE: omitted (no confidence values)
- adoption recommendation: adopt
- cosmetic churn flag: False

### minimax-MiniMax-M3__office-white-collar
- Δ_out = +0.250 (CI +0.107..+0.393, 14 tasks) -> better
- traj: Δ=0.4085, z=0.60 (within_band)
- tool: Δ=0.6724, z=0.76 (within_band)
- eff_tokens: Δ=-0.2571, z=-0.09 (within_band)
- eff_steps: Δ=-0.1954, z=-0.18 (within_band)
- eff_failed_actions: Δ=0.2237, z=0.22 (within_band)
- tool_jsd (secondary): 0.014
- saf by stratum: {'benign': 0.0, 'adversarial': 0.0}
- saf direction: {'worse_types_increased': [], 'caution_types_increased': []}
- ΔECE: omitted (no confidence values)
- adoption recommendation: adopt
- cosmetic churn flag: False

### minimax-MiniMax-M3__software-engineering
- Δ_out = +0.196 (CI +0.003..+0.396, 16 tasks) -> better
- traj: Δ=0.476, z=0.70 (within_band)
- tool: Δ=0.7012, z=0.80 (within_band)
- eff_tokens: Δ=0.6725, z=0.24 (within_band)
- eff_steps: Δ=0.32, z=0.29 (within_band)
- eff_failed_actions: Δ=0.2112, z=0.21 (within_band)
- tool_jsd (secondary): 0.0115
- saf by stratum: {'benign': 0.0, 'adversarial': 0.0}
- saf direction: {'worse_types_increased': [], 'caution_types_increased': []}
- ΔECE: omitted (no confidence values)
- adoption recommendation: adopt
- cosmetic churn flag: False
