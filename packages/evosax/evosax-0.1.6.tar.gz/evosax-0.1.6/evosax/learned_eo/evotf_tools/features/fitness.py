import functools
from typing import Tuple
import chex
from flax import struct
import jax
import jax.numpy as jnp
from evosax.strategies.des import get_des_weights
from evosax.strategies.snes import get_snes_weights
from evosax.core.fitness import (
    centered_rank_trafo,
    z_score_trafo,
    compute_l2_norm,
    range_norm_trafo,
)


@struct.dataclass
class FitnessFeaturesState:
    best_fitness: float


class FitnessFeaturizer(object):
    def __init__(
        self,
        popsize: int,
        num_dims: int,
        seq_len: int,
        improved_best: bool = False,
        z_score: bool = False,
        norm_diff_best: bool = False,
        norm_range: bool = False,
        snes_weights: bool = False,
        des_weights: bool = False,
        w_decay: float = 0.0,
        maximize: bool = False,
        verbose: bool = False,
    ):
        self.popsize = popsize
        self.num_dims = num_dims
        self.seq_len = seq_len
        self.improved_best = improved_best
        self.z_score = z_score
        self.norm_diff_best = norm_diff_best
        self.norm_range = norm_range
        self.snes_weights = snes_weights
        self.des_weights = des_weights
        self.w_decay = w_decay
        self.maximize = maximize
        self.verbose = verbose

        if self.verbose:
            print(
                f"Fitness Features / Batch shape: {self.num_features} / {self.example_batch_shape}"
            )
            print("[BASE] Centered ranks in [-0.5, 0.5]")
            print(f"[{self.improved_best}] Improved best fitness -> f < f_best")
            print(f"[{self.z_score}] Z-score normalization -> (f-f_mu)/f_sigma")
            print(
                f"[{self.norm_diff_best}] Normalized difference to best -> (f-f_best) in [-1, 1]"
            )
            print(f"[{self.norm_range}] Normalized fitness -> f in [-1, 1]")
            print(f"[{self.snes_weights}] SNES weights")
            print(f"[{self.des_weights}] DES weights")
            print(f"[{self.w_decay}] Scaled Weight Norm")

    @functools.partial(jax.jit, static_argnums=0)
    def featurize(
        self, x: chex.Array, fitness: chex.Array, state: FitnessFeaturesState
    ) -> Tuple[chex.Array, FitnessFeaturesState]:
        fitness = jax.lax.select(self.maximize, -1 * fitness, fitness)
        fit_out = centered_rank_trafo(fitness).reshape(-1, 1)

        if self.improved_best:
            fit_improve = ((fitness < state.best_fitness) * 1.0).reshape(-1, 1)
            fit_out = jnp.concatenate([fit_out, fit_improve], axis=1)

        if self.z_score:
            fit_zs = z_score_trafo(fitness).reshape(-1, 1)
            fit_out = jnp.concatenate([fit_out, fit_zs], axis=1)

        if self.norm_diff_best:
            fit_best = get_norm_diff_best(fitness, state.best_fitness).reshape(-1, 1)
            fit_out = jnp.concatenate([fit_out, fit_best], axis=1)

        if self.norm_range:
            fit_norm = range_norm_trafo(fitness, -0.5, 0.5).reshape(-1, 1)
            fit_out = jnp.concatenate([fit_out, fit_norm], axis=1)

        if self.snes_weights:
            fit_snes = get_snes_weights(fitness.shape[0])[fitness.argsort()].reshape(
                -1, 1
            )
            fit_out = jnp.concatenate([fit_out, fit_snes], axis=1)

        if self.des_weights:
            fit_des = get_des_weights(fitness.shape[0])[fitness.argsort()].reshape(
                -1, 1
            )
            fit_out = jnp.concatenate([fit_out, fit_des], axis=1)

        if self.w_decay:
            fit_wnorm = compute_l2_norm(x).reshape(-1, 1)
            fit_out = jnp.concatenate([fit_out, fit_wnorm], axis=1)

        best_fitness = update_best_fitness(fitness, state.best_fitness, self.maximize)
        return fit_out, FitnessFeaturesState(best_fitness=best_fitness)

    @functools.partial(jax.jit, static_argnums=0)
    def initialize(self) -> FitnessFeaturesState:
        return FitnessFeaturesState(best_fitness=jnp.finfo(jnp.float32).max)

    @property
    def num_features(self) -> int:
        return (
            1
            + self.improved_best
            + self.z_score
            + self.norm_diff_best
            + self.norm_range
            + self.snes_weights
            + self.des_weights
            + (self.w_decay > 0.0)
        )

    @property
    def example_batch_shape(self) -> Tuple[int, ...]:
        return (
            1,  # batchsize
            self.seq_len,  # timesteps
            self.popsize,  # popsize
            self.num_features,
        )


def update_best_fitness(
    fitness: chex.Array, best_fitness: float, maximize: bool = False
) -> chex.Array:
    fitness_min = jax.lax.select(maximize, -1 * fitness, fitness)
    best_fit_min = jax.lax.select(maximize, -1 * best_fitness, best_fitness)
    best_in_gen = jnp.argmin(fitness_min)
    best_in_gen_fit = fitness_min[best_in_gen]
    replace_fit = best_in_gen_fit < best_fit_min
    best_fitness = jax.lax.select(replace_fit, best_in_gen_fit, best_fit_min)
    best_fitness = jax.lax.select(maximize, -1 * best_fitness, best_fitness)
    return best_fitness


def get_norm_diff_best(fitness: chex.Array, best_fitness: float) -> chex.Array:
    fitness = jnp.clip(fitness, -1e10, 1e10)
    diff_best = fitness - best_fitness
    return jnp.clip(
        diff_best / (jnp.nanmax(diff_best) - jnp.nanmin(diff_best) + 1e-10),
        -1,
        1,
    )
