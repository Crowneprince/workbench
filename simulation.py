# simulation.py

import numpy as np

# Simulation function
def run_freq_sev_simulation(num_obs, freq_dist, sev_dist, freq_params, sev_params):
    # Provide default values for parameters
    lambda_val = freq_params.get('lambda', 10)
    n_val = freq_params.get('n', 10)
    p_val = freq_params.get('p', 0.5)
    mu_val = sev_params.get('mu', 2)
    sigma_val = sev_params.get('sigma', 1)
    alpha_val = sev_params.get('alpha', 3)
    scale_val = sev_params.get('scale', 1)
    a_val = sev_params.get('a', 1)
    shape_val = sev_params.get('shape', 2)

    # Frequency simulation
    if freq_dist == 'poisson':
        freq_sim = np.random.poisson(lam=lambda_val, size=num_obs)
    elif freq_dist == 'binomial':
        freq_sim = np.random.binomial(n=n_val, p=p_val, size=num_obs)
    elif freq_dist == 'nbinomial':
        freq_sim = np.random.negative_binomial(n=n_val, p=1 - p_val, size=num_obs)
    else:
        raise ValueError(f"Unsupported frequency distribution: {freq_dist}")

    # Severity simulation
    sev_sim = []
    for f in freq_sim:
        if sev_dist == 'lognormal':
            sev_sim.append(np.random.lognormal(mean=mu_val, sigma=sigma_val, size=f))
        elif sev_dist == 'pareto':
            sev_sim.append((np.random.pareto(a=alpha_val, size=f) + 1) * scale_val)
        elif sev_dist == 'weibull':
            sev_sim.append(np.random.weibull(a=a_val, size=f) * scale_val)
        elif sev_dist == 'gamma':
            sev_sim.append(np.random.gamma(shape=shape_val, scale=scale_val, size=f))
        elif sev_dist == 'exponential':
            sev_sim.append(np.random.exponential(scale=scale_val, size=f))
        else:
            raise ValueError(f"Unsupported severity distribution: {sev_dist}")

    # Calculate total losses
    total_losses = [np.sum(s) for s in sev_sim]

    return total_losses