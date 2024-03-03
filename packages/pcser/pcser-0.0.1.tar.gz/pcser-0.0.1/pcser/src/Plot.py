__author__ = "Jianfeng Sun"
__version__ = "v1.0"
__copyright__ = "Copyright 2024"
__license__ = "GPL v3.0"
__email__ = "jianfeng.sunmt@gmail.com"
__maintainer__ = "Jianfeng Sun"

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from pcser.util.Reader import reader as freader
from pcser.util.Writer import writer as fwriter


class Plot:

    def __init__(
            self,
    ):
        self.freader = freader()
        self.fwriter = fwriter()

        self.met_map = {
            'spl54': "Minimum and maximum (54 samples)",
            'spl63': "Minimum and maximum (63 samples)",
            'minmax': "Minimum maximum",
            'std': "Standardization",
            'maxabs': "Maximum absolute",
        }

        sns.set(font="Helvetica")
        sns.set_style("ticks")

    def bar_r2(
            self,
            compo_fpn,
            annot_fpn,
            met='minmax',
            criterion='mse',
    ):
        """
        Examples
        --------
        if criterion == 'r2':
            arr_compo = [0.9629, 0.8251, 0.7757, 0.8435, 0.9498]
            arr_category = [0.8706, 0.8985, 0.8907, 0.7988, 0.6453]
        if criterion == 'mse':
            arr_compo = [0.00021, 0.00243, 0.0079, 0.0010, 0.00084]
            arr_category = [0.0051, 0.00327, 0.00848, 0.00696, 0.003347]

        ax[0].set_ylabel('$R^{2}$ increment (%)')

            def plot_loo(self, train_fpn, train_loo_fpn):
        df_train = self.freader.generic(train_fpn, index_col=0, header=0)
        df_train_loo = self.freader.generic(train_loo_fpn, header=0, index_col=0)
        # print(df_train)
        # print(df_train_loo)
        df_increment = df_train_loo.mean(axis=1).apply(lambda x: (x-df_train.mean(axis=1).iloc[0])*100)
        df_increment_posi = df_increment[df_increment > 0].sort_values(ascending=False)
        df_increment_nega = df_increment[df_increment <= 0].sort_values(ascending=True)
        self.fwriter.excel(df=df_increment, sv_fpn=to('data/plot/loo_f82/all.xlsx'), index=True)
        self.fwriter.excel(df=df_increment_posi, sv_fpn=to('data/plot/loo_f82/posi.xlsx'), index=True)
        self.fwriter.excel(df=df_increment_nega, sv_fpn=to('data/plot/loo_f82/nega.xlsx'), index=True)
        print(df_increment_posi)
        print(df_increment_nega)
        fig, ax = plt.subplots(nrows=3, ncols=1, figsize=(8, 7),)
        ax[0].scatter(
            np.arange(df_increment.shape[0]),
            df_increment.values,
            facecolors='none',
            edgecolors='tab:gray', # tab:brown
            linewidths=2,
            alpha=0.85,
        )
        ax[0].hlines(0, 0, df_increment.shape[0], colors='crimson')
        ax[0].set_title('All')
        ax[0].spines['right'].set_color('none')
        ax[0].spines['top'].set_color('none')

        ax[1].scatter(
            np.arange(df_increment_posi.shape[0]),
            df_increment_posi.values,
            facecolors='none',
            edgecolors='tab:olive',  # tab:brown
            linewidths=2,
            alpha=0.85,
        )
        ax[1].set_title('Increase')
        ax[1].set_ylabel('$R^{2}$ increment (%)')
        ax[1].spines['right'].set_color('none')
        ax[1].spines['top'].set_color('none')

        ax[2].scatter(
            np.arange(df_increment_nega.shape[0]),
            df_increment_nega.values,
            facecolors='none',
            edgecolors='tab:purple',  # tab:brown
            linewidths=2,
            alpha=0.85,
        )
        ax[2].set_title('Decrease')
        ax[2].set_xlabel('No.')
        ax[2].set_ylabel('$R^{2}$ increment (%)')
        ax[2].spines['right'].set_color('none')
        ax[2].spines['top'].set_color('none')

        plt.subplots_adjust(
            hspace=0.3,
            wspace=0.3,
            right=0.99,
            left=0.1,
            bottom=0.08,
            top=0.95,
        )
        plt.show()
        return


        Parameters
        ----------
        compo_fpn
        annot_fpn
        criterion

        Returns
        -------

        """
        arr_5fold = np.arange(5)
        df_compo = self.freader.generic(
            df_fpn=compo_fpn,
            header=0,
        )
        df_annot = self.freader.generic(
            df_fpn=annot_fpn,
            header=0,
        )
        cls = [
            'Protein composition',
            'Protein category',
        ]
        df = pd.DataFrame({
            '5-Fold cross validation': arr_5fold,
            cls[0]: df_compo.T[0].values,
            cls[1]: df_annot.T[0].values,
        })

        df = pd.melt(df, id_vars=['5-Fold cross validation'], value_vars=['Protein composition', 'Protein category'])

        res_sns = sns.catplot(
            data=df,
            x="5-Fold cross validation",
            y="value",
            col="variable",
            kind="bar",
            height=4, aspect=.8,
            palette=sns.color_palette("Set3"),
        )
        axes = res_sns.axes.flatten()
        for i, ax in enumerate(axes):
            ax.set_title(cls[i], fontsize=14)
            ax.set_ylabel('R square' if criterion == 'r2' else 'Mean squared error', fontsize=16)
            ax.set_xlabel("5-Fold cross validation", fontsize=14)
            ax.set_xticks(np.arange(5))
            ax.set_xticklabels(np.arange(5) + 1, fontsize=12)
            for patch in ax.patches:
                current_width = patch.get_width()
                diff = current_width - 0.2
                patch.set_width(0.65)
                patch.set_x(patch.get_x() + diff * .5)
        plt.suptitle(self.met_map[met], size=16)
        plt.tight_layout()
        plt.show()
        return

    def loo_mean(
            self,
            compo_fpn,
            annot_fpn,
    ):
        """
        Examples
        --------
        if criterion == 'r2':
            arr_compo = [0.9629, 0.8251, 0.7757, 0.8435, 0.9498]
            arr_category = [0.8706, 0.8985, 0.8907, 0.7988, 0.6453]
        if criterion == 'mse':
            arr_compo = [0.00021, 0.00243, 0.0079, 0.0010, 0.00084]
            arr_category = [0.0051, 0.00327, 0.00848, 0.00696, 0.003347]

        Parameters
        ----------
        compo_fpn
        annot_fpn
        criterion

        Returns
        -------

        """
        df_compo = self.freader.generic(
            df_fpn=compo_fpn,
            header=0,
        ).mean(axis=1)
        feature_names = df_compo.index
        df_compo.index = np.arange(df_compo.shape[0])
        mean = self.freader.generic(
            df_fpn=annot_fpn,
            header=0,
        ).mean(axis=1).values[0]
        print(df_compo)
        print(mean)
        palette = sns.color_palette('Set3')
        fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(10, 5))
        # fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(5, 5))
        ax.plot(
            df_compo[df_compo >= mean].index,
            df_compo[df_compo >= mean],
            linestyle='none',
            marker='o',
            markerfacecolor='none',
            markeredgewidth=2,
            c=palette[3],
        )
        ax.plot(
            df_compo[df_compo < mean].index,
            df_compo[df_compo < mean],
            linestyle='none',
            marker='o',
            markerfacecolor='none',
            markeredgewidth=2,
            c=palette[0],
        )
        ax.axhline(y=mean, color="black", linestyle="--")

        ax.set_xlabel('Protein composition', fontsize=16)
        ax.set_ylabel('R square', fontsize=18)
        ax.set_xticks(np.arange(len(feature_names)))
        ax.set_xticklabels(
            feature_names,
            # rotation=20,
            # ha='right',
            fontsize=12,
        )

        ax.spines['right'].set_color('none')
        ax.spines['top'].set_color('none')
        ax.spines['bottom'].set_linewidth(2)
        ax.spines['left'].set_linewidth(2)
        ax.tick_params(axis='y', width=2)
        ax.tick_params(axis='x', width=2)
        fig.tight_layout()
        plt.show()
        return

    def bar_fi(
            self,
            df,
            title='',
    ):
        fig, ax = plt.subplots()
        df.plot.barh(
            # xerr=std[:num],
            legend=False,
            color=sns.color_palette('Set3')[4],
            ax=ax,
        )
        ax.set_yticklabels(df.index)
        ax.set_xlabel(title, fontsize=14)

        ax.spines['right'].set_color('none')
        ax.spines['top'].set_color('none')
        ax.spines['bottom'].set_linewidth(2)
        ax.spines['left'].set_linewidth(2)
        ax.tick_params(axis='y', width=2)
        ax.tick_params(axis='x', width=2)
        # ax.legend(frameon=False, fontsize=14)
        fig.tight_layout()
        # fig.subplots_adjust(
        #     top=0.92,
        #     bottom=0.22,
        #     left=0.1,
        #     right=0.6,
        #     # hspace=0.40,
        #     # wspace=0.15,
        # )
        plt.show()
        return


if __name__ == "__main__":
    from pcser.path import to

    p = Plot()

    # p.loo_mean(
    #     compo_fpn=to('data/r2_loo_annot_extended_minmax_spl54.txt'),
    #     annot_fpn=to('data/r2_kfold_annot_extended_minmax_spl54.txt'),
    #     criterion='r2',
    # )

    print(p.bar_r2(
        compo_fpn=to('data/r2_kfold_compo_extended_minmax_spl54.txt'),
        annot_fpn=to('data/r2_kfold_annot_extended_minmax_spl54.txt'),
        criterion='r2',
        met='minmax'
    ))