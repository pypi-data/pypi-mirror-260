import jax
import jax.numpy as jnp
import numpy as np
from evosax.experimental.subpops import BatchStrategy, MetaStrategy


def test_batch_strategy():
    rng = jax.random.PRNGKey(0)

    num_dims = 2
    popsize = 100
    num_subpops = 5

    batch_strategy = BatchStrategy(
        strategy_name="CMA_ES",
        num_dims=num_dims,
        popsize=popsize,
        num_subpops=num_subpops,
        strategy_kwargs={"elite_ratio": 0.5},
    )
    es_params = batch_strategy.default_params
    state = batch_strategy.initialize(rng, es_params)
    assert state.mean.shape == (num_subpops, num_dims)

    x, state = batch_strategy.ask(rng, state, es_params)
    assert x.shape == (popsize, num_dims)

    fitness = jnp.zeros(popsize)
    state = batch_strategy.tell(x, fitness, state, es_params)
    assert state.mean.shape == (num_subpops, num_dims)


def test_meta_strategy():
    rng = jax.random.PRNGKey(0)

    num_dims = 2
    popsize = 100
    num_subpops = 10

    meta_strategy = MetaStrategy(
        meta_strategy_name="CMA_ES",
        inner_strategy_name="DE",
        meta_params=["diff_w", "cross_over_rate"],
        num_dims=num_dims,
        popsize=popsize,
        num_subpops=num_subpops,
        meta_strategy_kwargs={"elite_ratio": 0.5},
    )
    meta_es_params = meta_strategy.default_params_meta.replace(
        clip_min=jnp.array([0, 0]), clip_max=jnp.array([2, 1])
    )

    # META: Initialize the meta strategy state
    inner_es_params = meta_strategy.default_params
    meta_state = meta_strategy.initialize_meta(rng, meta_es_params)

    # META: Get altered inner es hyperparams
    inner_es_params, meta_state = meta_strategy.ask_meta(
        rng, meta_state, meta_es_params, inner_es_params
    )
    assert meta_state.mean.shape == (num_dims,)

    # INNER: Initialize the inner batch ES
    state = meta_strategy.initialize(rng, inner_es_params)
    assert state.mean.shape == (num_subpops, num_dims)

    # INNER: Ask for inner candidate params to evaluate on problem
    x, state = meta_strategy.ask(rng, state, inner_es_params)
    assert x.shape == (popsize, num_dims)

    # INNER: Update using pseudo fitness
    fitness = jax.random.normal(rng, (popsize,))
    state = meta_strategy.tell(x, fitness, state, inner_es_params)
    assert state.mean.shape == (num_subpops, num_dims)

    # META: Update the meta strategy
    meta_state = meta_strategy.tell_meta(
        inner_es_params, fitness, meta_state, meta_es_params
    )
    assert meta_state.mean.shape == (num_dims,)


def test_protocol_best_subpop_strategy():
    rng = jax.random.PRNGKey(0)
    batch_strategy = BatchStrategy(
        strategy_name="CMA_ES",
        num_dims=2,
        popsize=100,
        num_subpops=5,
        strategy_kwargs={"elite_ratio": 0.5},
        communication="best_subpop",
    )
    es_params = batch_strategy.default_params
    state = batch_strategy.initialize(rng, es_params)
    assert state.mean.shape == (5, 2)

    x, state = batch_strategy.ask(rng, state, es_params)
    assert x.shape == (100, 2)

    fitness = jnp.ones(100)

    best_ind = np.random.randint(100)
    best_fitness = 0
    fitness = fitness.at[best_ind].set(best_fitness)

    state = batch_strategy.tell(x, fitness, state, es_params)

    assert state.mean.shape == (5, 2)
