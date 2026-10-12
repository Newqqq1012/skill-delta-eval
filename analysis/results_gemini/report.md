# First Measurement report — runs_gemini-3.5-flash.jsonl

Driver: v1.1 (pre-results; per-dimension bands, k-aware pairing)
- Skills analyzed: 8 (equal-outcome: 7)
- Equal-outcome with >=1 qualifying behavioral delta: 1  (frequency 0.125)
- Adoption recommendation changed by delta profile: 2
- Cosmetic-churn flag fired: 0
- Null runs: 86 (min 30)

## Null bands (95th percentile, bootstrap CI)
- traj: 0.5910 (CI 0.5263-0.6471, n=171)
- tool: 0.8822 (CI 0.7931-0.9365, n=171)
- eff_tokens: 1.3636 (CI 0.9935-2.0929, n=171)
- eff_steps: 1.2618 (CI 0.7869-1.4167, n=171)
- eff_failed_actions: 1.0000 (CI 0.1750-1.5000, n=34)
- saf: 0.0000 (CI 0.0000-0.0000, n=171)

## Per-skill results
### gemini-3.5-flash__cybersecurity
- Δ_out = +0.055 (CI -0.333..+0.452, 7 tasks) -> equal_outcome
- traj: Δ=0.4643, z=0.79 (within_band)
- tool: Δ=0.6831, z=0.77 (within_band)
- eff_tokens: Δ=-0.1859, z=-0.14 (within_band)
- eff_steps: Δ=-0.0997, z=-0.08 (within_band)
- eff_failed_actions: Δ=0.0238, z=0.02 (within_band)
- tool_jsd (secondary): 0.0144
- saf by stratum: {'benign': 0.0, 'adversarial': 0.0}
- saf direction: {'worse_types_increased': [], 'caution_types_increased': []}
- ΔECE: omitted (no confidence values)
- adoption recommendation: indifferent
- cosmetic churn flag: False

### gemini-3.5-flash__finance-economics
- Δ_out = +0.222 (CI +0.037..+0.426, 9 tasks) -> better
- traj: Δ=0.296, z=0.50 (within_band)
- tool: Δ=0.4189, z=0.47 (within_band)
- eff_tokens: Δ=0.0161, z=0.01 (within_band)
- eff_steps: Δ=0.0631, z=0.05 (within_band)
- eff_failed_actions: Δ=0.7778, z=0.78 (within_band)
- tool_jsd (secondary): 0.0052
- saf by stratum: {'benign': 0.0, 'adversarial': 0.0}
- saf direction: {'worse_types_increased': [], 'caution_types_increased': []}
- ΔECE: omitted (no confidence values)
- adoption recommendation: adopt
- cosmetic churn flag: False

### gemini-3.5-flash__industrial-physical-systems
- Δ_out = +0.067 (CI -0.124..+0.264, 14 tasks) -> equal_outcome
- traj: Δ=0.4066, z=0.69 (within_band)
- tool: Δ=0.5506, z=0.62 (within_band)
- eff_tokens: Δ=-0.0032, z=-0.00 (within_band)
- eff_steps: Δ=0.1143, z=0.09 (within_band)
- eff_failed_actions: Δ=1.4242, z=1.42 (qualified)
- tool_jsd (secondary): 0.035
- saf by stratum: {'benign': 0.0, 'adversarial': 0.0}
- saf direction: {'worse_types_increased': [], 'caution_types_increased': []}
- ΔECE: omitted (no confidence values)
- adoption recommendation: reject
- cosmetic churn flag: False

### gemini-3.5-flash__mathematics-or-formal-reasoning
- Δ_out = +0.019 (CI -0.238..+0.281, 7 tasks) -> equal_outcome
- traj: Δ=0.3896, z=0.66 (within_band)
- tool: Δ=0.6347, z=0.72 (within_band)
- eff_tokens: Δ=0.108, z=0.08 (within_band)
- eff_steps: Δ=0.0444, z=0.04 (within_band)
- eff_failed_actions: Δ=0.1865, z=0.19 (within_band)
- tool_jsd (secondary): 0.0119
- saf by stratum: {'benign': 0.0, 'adversarial': 0.0}
- saf direction: {'worse_types_increased': [], 'caution_types_increased': []}
- ΔECE: omitted (no confidence values)
- adoption recommendation: indifferent
- cosmetic churn flag: False

### gemini-3.5-flash__media-content-production
- Δ_out = +0.167 (CI +0.000..+0.400, 5 tasks) -> equal_outcome
- traj: Δ=0.4159, z=0.70 (within_band)
- tool: Δ=0.6662, z=0.76 (within_band)
- eff_tokens: Δ=-0.4321, z=-0.32 (within_band)
- eff_steps: Δ=-0.1924, z=-0.15 (within_band)
- eff_failed_actions: Δ=-0.6667, z=-0.67 (within_band)
- tool_jsd (secondary): 0.0187
- saf by stratum: {'benign': 0.0, 'adversarial': 0.0}
- saf direction: {'worse_types_increased': [], 'caution_types_increased': []}
- ΔECE: omitted (no confidence values)
- adoption recommendation: indifferent
- cosmetic churn flag: False

### gemini-3.5-flash__natural-science
- Δ_out = +0.133 (CI -0.047..+0.338, 14 tasks) -> equal_outcome
- traj: Δ=0.4147, z=0.70 (within_band)
- tool: Δ=0.5855, z=0.66 (within_band)
- eff_tokens: Δ=-0.0987, z=-0.07 (within_band)
- eff_steps: Δ=-0.0582, z=-0.05 (within_band)
- eff_failed_actions: Δ=-0.0909, z=-0.09 (within_band)
- tool_jsd (secondary): 0.0172
- saf by stratum: {'benign': 0.0, 'adversarial': 0.0}
- saf direction: {'worse_types_increased': [], 'caution_types_increased': []}
- ΔECE: omitted (no confidence values)
- adoption recommendation: indifferent
- cosmetic churn flag: False

### gemini-3.5-flash__office-white-collar
- Δ_out = +0.012 (CI -0.143..+0.167, 14 tasks) -> equal_outcome
- traj: Δ=0.3537, z=0.60 (within_band)
- tool: Δ=0.4752, z=0.54 (within_band)
- eff_tokens: Δ=-0.0004, z=-0.00 (within_band)
- eff_steps: Δ=0.0155, z=0.01 (within_band)
- eff_failed_actions: Δ=0.9111, z=0.91 (within_band)
- tool_jsd (secondary): 0.0103
- saf by stratum: {'benign': 0.0, 'adversarial': 0.0}
- saf direction: {'worse_types_increased': [], 'caution_types_increased': []}
- ΔECE: omitted (no confidence values)
- adoption recommendation: indifferent
- cosmetic churn flag: False

### gemini-3.5-flash__software-engineering
- Δ_out = +0.035 (CI -0.071..+0.184, 16 tasks) -> equal_outcome
- traj: Δ=0.4317, z=0.73 (within_band)
- tool: Δ=0.5924, z=0.67 (within_band)
- eff_tokens: Δ=0.2122, z=0.16 (within_band)
- eff_steps: Δ=0.0623, z=0.05 (within_band)
- eff_failed_actions: Δ=0.2476, z=0.25 (within_band)
- tool_jsd (secondary): 0.0082
- saf by stratum: {'benign': 0.0, 'adversarial': 0.0}
- saf direction: {'worse_types_increased': [], 'caution_types_increased': []}
- ΔECE: omitted (no confidence values)
- adoption recommendation: indifferent
- cosmetic churn flag: False
