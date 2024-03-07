from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from pathlib import Path

import numpy as np
import pandas as pd
import xarray as xr
from tqdm import tqdm


def normalized_NSE(targ, pred, name_ndvi_pred="ndvi_pred", additional_metrics=False):
    """Compute normalized Nash sutcliffe model efficiency of NDVI for one minicube

    The normalized Nash sutcliffe model efficiency scores the predictive skill of a model. It is identical to the most general definition of the coefficient of determination $R^2$.

    We score only on non-cloud observations (determined by the variable `s2_mask` in the target minicube).

    $$$
    nnse = 1 / (2 - nse)
    nse = \frac{\sum_{time} (obs - pred)^2}{\sum_{time} (obs - obsmean)^2}
    $$$

    Further reading:
    - Normalized NSE https://en.wikipedia.org/wiki/Nash%E2%80%93Sutcliffe_model_efficiency_coefficient
    - NDVI https://de.wikipedia.org/wiki/Normalized_Difference_Vegetation_Index

    Args:
        targ (xr.Dataset): target minicube
        pred (xr.Dataset): prediction minicube, contains `name_ndvi_pred` variable with NDVI predictions during the forecasting period.
        name_ndvi_pred (str, optional): Name of the NDVI prediction variable, defaults to `"ndvi_pred"`.
        additional_metrics (boolean, optional): Set to True if want to return more metrics.
    """

    pred_start_idx = len(targ.time.isel(time=slice(4, None, 5))) - len(pred.time)

    nir = targ.s2_B8A.isel(time=slice(4, None, 5)).isel(
        time=slice(pred_start_idx, None)
    )
    red = targ.s2_B04.isel(time=slice(4, None, 5)).isel(
        time=slice(pred_start_idx, None)
    )
    mask = targ.s2_mask.isel(time=slice(4, None, 5)).isel(
        time=slice(pred_start_idx, None)
    )

    targ_ndvi = ((nir - red) / (nir + red + 1e-8)).where(mask == 0, np.NaN)
    pred_ndvi = pred[name_ndvi_pred]

    nnse = 1 / (
        2
        - (
            1
            - (
                ((targ_ndvi - pred_ndvi) ** 2).sum("time")
                / ((targ_ndvi - targ_ndvi.mean("time")) ** 2).sum("time")
            )
        )
    )

    n_obs = (mask == 0).sum("time")

    if additional_metrics:
        bias = targ_ndvi.mean("time") - pred_ndvi.where(mask == 0, np.NaN).mean("time")
        bias_full = targ_ndvi.mean("time") - pred_ndvi.mean("time")
        sigma_targ = targ_ndvi.std("time")
        sigma_pred = pred_ndvi.where(mask == 0, np.NaN).std("time")
        sigma_pred_full = pred_ndvi.std("time")
        beta = bias / (sigma_targ + 1e-8)
        alpha = sigma_pred / (sigma_targ + 1e-8)
        r = xr.corr(targ_ndvi, pred_ndvi, dim="time")
        rmse_0_1 = ((targ_ndvi - pred_ndvi) ** 2).isel(time=slice(1)).mean(
            "time"
        ) ** 0.5
        rmse_0_2 = ((targ_ndvi - pred_ndvi) ** 2).isel(time=slice(2)).mean(
            "time"
        ) ** 0.5
        rmse_0_5 = ((targ_ndvi - pred_ndvi) ** 2).isel(time=slice(5)).mean(
            "time"
        ) ** 0.5
        rmse_0_10 = ((targ_ndvi - pred_ndvi) ** 2).isel(time=slice(10)).mean(
            "time"
        ) ** 0.5
        rmse_0_15 = ((targ_ndvi - pred_ndvi) ** 2).isel(time=slice(15)).mean(
            "time"
        ) ** 0.5
        rmse_0_20 = ((targ_ndvi - pred_ndvi) ** 2).isel(time=slice(20)).mean(
            "time"
        ) ** 0.5
        rmse_5_10 = ((targ_ndvi - pred_ndvi) ** 2).isel(time=slice(5, 10)).mean(
            "time"
        ) ** 0.5
        rmse_10_15 = ((targ_ndvi - pred_ndvi) ** 2).isel(time=slice(10, 15)).mean(
            "time"
        ) ** 0.5
        rmse_15_20 = ((targ_ndvi - pred_ndvi) ** 2).isel(time=slice(15, 20)).mean(
            "time"
        ) ** 0.5
        crmsd = (
            (
                (targ_ndvi - targ_ndvi.mean("time"))
                - (pred_ndvi - pred_ndvi.mean("time"))
            )
            ** 2
        ).mean("time") ** 0.5
        error_sum = (targ_ndvi - pred_ndvi).sum("time")
        df = xr.Dataset(
            {
                "NNSE": nnse,
                "landcover": targ.esawc_lc,
                "n_obs": n_obs,
                "bias": bias,
                "bias_full": bias_full,
                "sigma_targ": sigma_targ,
                "sigma_pred": sigma_pred,
                "sigma_pred_full": sigma_pred_full,
                "beta": beta,
                "alpha": alpha,
                "r": r,
                "rmse_0_1": rmse_0_1,
                "rmse_0_2": rmse_0_2,
                "rmse_0_5": rmse_0_5,
                "rmse_0_10": rmse_0_10,
                "rmse_0_15": rmse_0_15,
                "rmse_0_20": rmse_0_20,
                "rmse_5_10": rmse_5_10,
                "rmse_10_15": rmse_10_15,
                "rmse_15_20": rmse_15_20,
                "crmsd": crmsd,
                "error_sum": error_sum,
            }
        ).to_dataframe()
    else:
        df = xr.Dataset(
            {"NNSE": nnse, "landcover": targ.esawc_lc, "n_obs": n_obs}
        ).to_dataframe()

    return df.drop(columns="sentinel:product_id", errors="ignore")


def score_from_args(args):

    targetfile, predfile, name_ndvi_pred, additional_metrics = args

    targ = xr.open_dataset(targetfile)
    pred = xr.open_dataset(predfile)

    curr_df = normalized_NSE(
        targ, pred, name_ndvi_pred=name_ndvi_pred, additional_metrics=additional_metrics
    )
    curr_df["id"] = targetfile.stem

    return curr_df


def score_over_dataset(
    testset_dir,
    pred_dir,
    name_ndvi_pred="ndvi_pred",
    verbose=True,
    num_workers=1,
    additional_metrics=False,
):
    """Compute normalized Nash sutcliffe model efficiency of NDVI for a full dataset

    Args:
        testset_dir (str): directory under which the target minicubes are stored. e.g. `"data/earthnet2021x/test/"`.
        pred_dir (str): directory under which the predictions are stored. e.g. `"preds/my_model/earthnet2021x-test/"`.
        name_ndvi_pred (str, optional): Name of the NDVI prediction variable, defaults to `"ndvi_pred"`.
        verbose (boolean, optional): Set to false to silence this function.
        num_workers (int, optional): Number of threads to use for scoring. Defaults to 1.
        additional_metrics (boolean, optional): Set to True if want to return more metrics.
    """

    targetfiles = list(Path(testset_dir).glob("**/*.nc"))

    pred_dir = Path(pred_dir)

    predfiles = []
    inputargs = []
    for targetfile in targetfiles:
        cubename = targetfile.name
        region = targetfile.parent.stem

        predfile = pred_dir / region / cubename
        predfiles.append(predfile)
        inputargs.append([targetfile, predfile, name_ndvi_pred, additional_metrics])

    if verbose:
        print(f"scoring {testset_dir} against {pred_dir}")

    with ProcessPoolExecutor(max_workers=num_workers) as pool:
        if verbose:
            dfs = list(tqdm(pool.map(score_from_args, inputargs), total=len(inputargs)))
        else:
            dfs = list(pool.map(score_from_args, inputargs))

    df = pd.concat(dfs).reset_index()

    tree_score = 2 - 1 / df[df.landcover == 10.0].NNSE.mean()
    shrub_score = 2 - 1 / df[df.landcover == 20.0].NNSE.mean()
    grass_score = 2 - 1 / df[df.landcover == 30.0].NNSE.mean()
    crop_score = 2 - 1 / df[df.landcover == 40.0].NNSE.mean()
    swamp_score = 2 - 1 / df[df.landcover == 90.0].NNSE.mean()
    mangroves_score = 2 - 1 / df[df.landcover == 95.0].NNSE.mean()
    moss_score = 2 - 1 / df[df.landcover == 100.0].NNSE.mean()

    veg_score = 2 - 1 / df[df.landcover <= 30.0].NNSE.mean()

    scores = {
        "veg_score": veg_score,
        "tree_score": tree_score,
        "shrub_score": shrub_score,
        "grass_score": grass_score,
        "crop_score": crop_score,
        "swamp_score": swamp_score,
        "mangroves_score": mangroves_score,
        "moss_score": moss_score,
        "all_scores": df,
    }

    if additional_metrics:
        scores["veg_bias"] = df[df.landcover <= 30.0].bias.mean()
        scores["veg_r2"] = ((df[df.landcover <= 30.0].r) ** 2).mean()
        scores["veg_alpha"] = df[df.landcover <= 30.0].alpha.mean()
        scores["veg_beta"] = df[df.landcover <= 30.0].beta.mean()
        scores["veg_rmse_0_1"] = df[df.landcover <= 30.0].rmse_0_1.mean()
        scores["veg_rmse_0_2"] = df[df.landcover <= 30.0].rmse_0_2.mean()
        scores["veg_rmse_0_5"] = df[df.landcover <= 30.0].rmse_0_5.mean()
        scores["veg_rmse_0_10"] = df[df.landcover <= 30.0].rmse_0_10.mean()
        scores["veg_rmse_0_15"] = df[df.landcover <= 30.0].rmse_0_15.mean()
        scores["veg_rmse_0_20"] = df[df.landcover <= 30.0].rmse_0_20.mean()
        scores["veg_rmse_5_10"] = df[df.landcover <= 30.0].rmse_5_10.mean()
        scores["veg_rmse_10_15"] = df[df.landcover <= 30.0].rmse_10_15.mean()
        scores["veg_rmse_15_20"] = df[df.landcover <= 30.0].rmse_15_20.mean()

    if verbose:
        print("Done!")

    return scores
