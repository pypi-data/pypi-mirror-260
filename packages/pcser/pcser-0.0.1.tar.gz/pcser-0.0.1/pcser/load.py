__version__ = "v1.0"
__copyright__ = "Copyright 2024"
__license__ = "MIT"
__developer__ = "Jianfeng Sun"
__maintainer__ = "Jianfeng Sun"
__email__ = "jianfeng.sunmt@gmail.com"

from typing import List

import pandas as pd

from pcser.src.Model import Model as pcsermodel
from pcser.src.Preprocessing import Preprocessing as prep
from pcser.src.Plot import Plot


def data_ref_compo(
        data_ref_fpn,
        sv_fp,
        is_norm=True,
        norm_met='minmax',
        version='extended',
) -> pd.DataFrame:
    dataparser = prep(
        data_fpn=data_ref_fpn,
        version=version,
        is_norm=is_norm,
        norm_met=norm_met,
        sv_fp=sv_fp,
    )
    return dataparser.sortout_by_compo()


def data_ref_annot(
        data_ref_fpn,
        sv_fp,
        is_norm=True,
        norm_met='minmax',
        version='extended',
) -> pd.DataFrame:
    dataparser = prep(
        data_fpn=data_ref_fpn,
        version=version,
        is_norm=is_norm,
        norm_met=norm_met,
        sv_fp=sv_fp,
    )
    return dataparser.sortout_by_annot()


def train(
        data_ref_fpn,
        sv_fp,
        mark='',
        mode='compo',
        is_norm=True,
        norm_met='minmax',
        seed=4,
        version='extended',
) -> List:
    return pcsermodel(
        data_ref_fpn=data_ref_fpn,
        version=version,
        is_norm=is_norm,
        norm_met=norm_met,
        mode=mode,
        mark=mark,
        sv_fp=sv_fp,
    ).build_kfold(
        seed=seed,
    )


def feature_contribution(
        data_ref_fpn,
        fi_met,
        sv_fp,
        mark='',
        mode='compo',
        is_norm=True,
        norm_met='minmax',
        seed=4,
        version='extended',
) -> str:
    return pcsermodel(
        data_ref_fpn=data_ref_fpn,
        version=version,
        is_norm=is_norm,
        norm_met=norm_met,
        mode=mode,
        mark=mark,
        fi_met=fi_met,
        sv_fp=sv_fp,
    ).build_whole(
        seed=seed,
    )


def evaluate(
        data_ref_fpn,
        sv_fp,
        input_fpn,
        model_fpn,
        sheet_name,
        mfi_ref=None,
        mark='',
        mode='compo',
        is_norm=True,
        norm_met='minmax',
        version='extended',
) -> pd.DataFrame:
    return pcsermodel(
        data_ref_fpn=data_ref_fpn,
        version=version,
        is_norm=is_norm,
        norm_met=norm_met,
        mode=mode,
        mark=mark,
        sv_fp=sv_fp,
    ).evaluate(
        input_fpn=input_fpn,
        model_fpn=model_fpn,
        sheet_name=sheet_name,
        mfi_ref=mfi_ref,
    )


def extend(
        data_ref_fpn,
        input_fpn,
        model_fpn,
        sheet_name,
        rept_times,
        poi,
        spl_name,
        poi_increments,

        sv_fp=None,
        mfi_ref=None,
        mark='',
        mode='compo',
        is_norm=True,
        norm_met='minmax',
        version='extended',
) -> pd.DataFrame:
    return pcsermodel(
        data_ref_fpn=data_ref_fpn,
        version=version,
        is_norm=is_norm,
        norm_met=norm_met,
        mode=mode,
        mark=mark,
        sv_fp=sv_fp,
    ).extend(
        input_fpn=input_fpn,
        model_fpn=model_fpn,
        sheet_name=sheet_name,
        mfi_ref=mfi_ref,
        rept_times=rept_times,
        poi=poi,
        spl_name=spl_name,
        poi_increments=poi_increments,
    )


def plot_res(
        compo_fpn,
        annot_fpn,
        met,
        criterion,
):
    Plot().bar_r2(
        compo_fpn=compo_fpn,
        annot_fpn=annot_fpn,
        met=met,
        criterion=criterion,
    )
    return 'Finished'


if __name__ == "__main__":
    from pcser.path import to

    # df_compo = data_ref_compo(
    #     data_ref_fpn=to('data/hu_macrophage/Proteomics_07262023_rv_C57BL6_spl54.xlsx'),
    #     sv_fp=to('data/'),  # None to('data/')
    #     is_norm=True,
    #     norm_met='minmax',  # minmax std maxabs
    #     version='extended',  # e
    # )
    # print(df_compo)

    # df_annot = data_ref_annot(
    #     data_ref_fpn=to('data/hu_macrophage/Proteomics_07262023_rv_C57BL6_spl54.xlsx'),
    #     sv_fp=to('data/'),  # None to('data/')
    #     is_norm=True,
    #     norm_met='minmax',  # minmax std maxabs
    #     version='extended',  # e
    # )
    # print(df_annot)

    # train(
    #     data_ref_fpn=to('data/hu_macrophage/Proteomics_07262023_rv_C57BL6_spl54.xlsx'),
    #     sv_fp=to('data/'),  # None to('data/')
    #     is_norm=True,
    #     norm_met='minmax',  # minmax std maxabs
    #     mode='compo',  # compo annot
    #     mark='spl54',  # spl54 spl63
    #     seed=4,
    #     version='extended',  # extended old
    # )

    # feature_contribution(
    #     data_ref_fpn=to('data/hu_macrophage/Proteomics_07262023_rv_C57BL6_spl54.xlsx'),
    #     fi_met='mdi',  # None shap mdi pi
    #     sv_fp=to('data/'),  # None to('data/')
    #     is_norm=True,
    #     norm_met='minmax',  # minmax std maxabs
    #     mode='compo',  # compo annot
    #     mark='spl54',  # spl54 spl63
    #     seed=4,
    #     version='extended',  # extended old
    # )

    # evaluate(
    #     data_ref_fpn=to('data/hu_macrophage/Proteomics_07262023_rv_C57BL6_spl54.xlsx'),
    #     input_fpn=to('data/hu_macrophage/example.xlsx'),
    #     model_fpn=to('data/model/') + 'best_cv.joblib',
    #     sheet_name='a', # a b
    #     # mfi_ref=[10271.33333, 10747, 10303.33333, 9663.333333, 10056],
    #     mfi_ref=[3606.333333, 3606.333333, 3606.333333, 3606.333333],
    #
    #     sv_fp=to('data/'),  # None to('data/')
    #     is_norm=True,
    #     norm_met='minmax',  # minmax std maxabs
    #     mode='compo',  # compo annot
    #     mark='spl54',  # spl54 spl63
    #     version='extended',  # extended old
    # )

    # extend(
    #     data_ref_fpn=to('data/hu_macrophage/Proteomics_07262023_rv_C57BL6_spl54.xlsx'),
    #     input_fpn=to('data/hu_macrophage/example.xlsx'),
    #     model_fpn=to('data/model/') + 'best_cv.joblib',
    #     sheet_name='a',  # a b
    #     spl_name='HuApoA1',  # HuApoA1
    #     mfi_ref=3606.3,
    #
    #     rept_times=5,
    #     poi='Total_quantification',
    #     poi_increments=[0, 10, 100, 1000, 10000],
    #
    #     sv_fp=to('data/'),  # None to('data/')
    #     is_norm=True,
    #     norm_met='minmax',  # minmax std maxabs
    #     mode='compo',  # compo annot
    #     mark='spl54',  # spl54 spl63
    #     version='extended',  # extended old
    # )

    # plot_res(
    #     compo_fpn=to('data/r2_kfold_compo_extended_minmax_spl54.txt'),
    #     annot_fpn=to('data/r2_kfold_annot_extended_minmax_spl54.txt'),
    #     criterion='r2',
    #     met='minmax'
    # )
