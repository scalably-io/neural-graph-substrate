"""D2: pins the FLOP convention the preregistration's V1 rule depends on."""
import pytest

from ngs.flops import run_flops, step_flops

N, D = 256, 128


def test_topk_at_k_equals_n_is_exactly_dense():
    assert step_flops("topk", N, D, k=N) == step_flops("dense", N, D)


@pytest.mark.parametrize("k", [2, 4, 8, 16, 64])
def test_topk_saves_matmul_but_pays_selection(k):
    dense, topk = step_flops("dense", N, D), step_flops("topk", N, D, k=k)
    assert dense.matmul - topk.matmul == 2 * N * (N - k) * D      # only aggregation shrinks
    softmax_only = 5 * N * k
    assert topk.nonmatmul == softmax_only + N * N * max(1, (k - 1).bit_length())   # selection is counted, not free


def test_mask_arm_executed_equals_dense_but_useful_is_sparse():
    edges = 4 * N
    executed = step_flops("mask", N, D, edges=edges, count="executed")
    useful = step_flops("mask", N, D, edges=edges, count="useful")
    assert executed.matmul == step_flops("dense", N, D).matmul
    assert useful.matmul < executed.matmul


def test_sdpa_recompute_would_exceed_dense():
    """Review R1 B4: the v0.1 pipeline (scores for top-k, then masked SDPA recomputing QKᵀ
    and a full AV) executes dense + 2N²d; the gather design must not."""
    dense = step_flops("dense", N, D)
    v01_pipeline = dense.matmul + 2 * N * N * D
    assert step_flops("topk", N, D, k=8).matmul < dense.matmul < v01_pipeline


def test_run_flops_scales_linearly_with_steps():
    one = step_flops("topk", N, D, k=8)
    ten = run_flops("topk", N, D, steps=10, k=8)
    assert ten.matmul == 10 * one.matmul and ten.nonmatmul == 10 * one.nonmatmul


def test_entmax_matches_dense_matmul_but_pays_bisection():
    dense, ent = step_flops("dense", N, D), step_flops("entmax", N, D)
    assert ent.matmul == dense.matmul
    assert ent.nonmatmul == dense.nonmatmul + 25 * 4 * N * N


def test_per_step_extras_are_counted():
    plain = step_flops("dense", N, D)
    assert step_flops("dense", N, D, readout_dim=10).matmul == plain.matmul + 2 * N * D * 10
    assert step_flops("dense", N, D, inject=True).matmul == plain.matmul + 2 * N * D * D


def test_bad_arguments_raise():
    with pytest.raises(ValueError):
        step_flops("topk", N, D, k=0)
    with pytest.raises(ValueError):
        step_flops("mask", N, D)
    with pytest.raises(ValueError):
        step_flops("graph", N, D)
