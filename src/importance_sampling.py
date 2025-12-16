import numpy as np
from pathlib import Path

def IS_SH_azi_SH_uniform(
    random_seed: int,
    name_prefix: str,
    n_samples: int,
    alpha: float,
    beta: float,
    proposal_SH_azi_low: float,
    proposal_SH_low: float,
    show_summary: bool = True
    ):

    # set up path
    base_path = Path('..')

    np.random.seed(random_seed)
    # name_prefix = '251023'
    # Parameters
    # n_samples = 90
    # alpha = 0.9
    # beta = 0.9

    # --- Target distributions ---
    # SH_azi ~ U(300, 320)
    target_SH_azi_low, target_SH_azi_high = 300, 320
    # proposal_SH_azi_low = 319
    p_SH_azi = 1/(target_SH_azi_high - target_SH_azi_low)

    # SH ~ U(16.2, 19.8)
    SH_base = 18
    target_SH_low, target_SH_high = SH_base * 0.9, SH_base * 1.1 # U(16.2,19.8)
    # proposal_SH_low = 18 * 1.05
    p_SH = 1/(target_SH_high - target_SH_low)

    # --- Proposal mixture components ---
    # SH_azi: 0.2 U(300,310) + 0.8 U(310,320)
    u1 = np.random.rand(n_samples)
    u1_quantile = np.quantile(u1,alpha)
    samples_SH_azi = np.empty(n_samples)
    samples_SH_azi[u1 > u1_quantile] = np.random.uniform(target_SH_azi_low, proposal_SH_azi_low, size=(u1 > u1_quantile).sum())
    samples_SH_azi[u1 <= u1_quantile] = np.random.uniform(proposal_SH_azi_low, target_SH_azi_high, size=(u1 <= u1_quantile).sum())
    q_SH_azi = np.where((samples_SH_azi >= proposal_SH_azi_low) & (samples_SH_azi < target_SH_azi_high), 
                alpha / (target_SH_azi_high-target_SH_azi_low), 
                (1 - alpha) / target_SH_azi_high-target_SH_azi_low)


    # SH: 0.2 U(16.2,17) + 0.8 U(17,19.8)
    u2 = np.random.rand(n_samples)
    u2_quantile = np.quantile(u2,beta)
    samples_SH = np.empty(n_samples)
    samples_SH[u2 > u2_quantile] = np.random.uniform(target_SH_low, proposal_SH_low, size=(u2 > u2_quantile).sum())
    samples_SH[u2 <= u2_quantile] = np.random.uniform(proposal_SH_low, target_SH_high, size=(u2 <= u2_quantile).sum())
    q_SH = np.where((samples_SH >= proposal_SH_low) & (samples_SH < target_SH_high), 
            beta / (target_SH_high-target_SH_low), 
            (1 - beta) / (target_SH_high-target_SH_low))

    # --- Importance weights ---
    # Since the two variables are independent, total weight = (p_SH_azi * p_SH) / (q_SH_azi*q_SH)
    weights = (p_SH_azi * p_SH) / (q_SH_azi * q_SH)
    weights /= np.sum(weights)

    # combine into a 2D array, note SH is turned into negative for CMG sign convention
    importance_sampling = np.column_stack((samples_SH_azi,q_SH_azi,-samples_SH,q_SH,weights))

    header_string = 'SH_azi_deg,q_SH_azi,SH_MPa/km,q_SH,weights'
    np.savetxt(base_path/'results'/'sim_files'/f'{name_prefix}_importance_sampling.csv',importance_sampling,delimiter=',',fmt='%.4f',header=header_string,comments='')
    
    if show_summary:
        print('SH_azi')
        print(f'Target distribution: U[{target_SH_azi_low}, {target_SH_azi_high}], {n_samples} samples')
        print(f'Proposal distribution: {(1-alpha):.1f} * U[{target_SH_azi_low}, {proposal_SH_azi_low}] + {alpha} * U[{proposal_SH_azi_low}])')
        print(f'Importance samples min: {np.min(samples_SH_azi):.2f}, max: {np.max(samples_SH_azi):.2f}, number of alpha samples: {np.sum(importance_sampling[:,0] > proposal_SH_azi_low)}')
        print('SH')
        print(f'Target distribution: U[{target_SH_low}, {target_SH_high}], {n_samples} samples')
        print(f'Proposal distribution: {(1-beta):.1f} * U[{target_SH_low}, {proposal_SH_low:.2f}] + {beta} * U[{proposal_SH_low:.2f}, {target_SH_high}]')
        print(f'Importance samples min: {np.min(samples_SH):.2f}, max: {np.max(samples_SH):.2f}, number of beta samples: {np.sum(importance_sampling[:,2] < -proposal_SH_low)}')