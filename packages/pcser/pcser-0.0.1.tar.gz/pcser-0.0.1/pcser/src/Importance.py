__author__ = "Jianfeng Sun"
__version__ = "v1.0"
__copyright__ = "Copyright 2024"
__license__ = "GPL v3.0"
__email__ = "jianfeng.sunmt@gmail.com"
__maintainer__ = "Jianfeng Sun"

import shap
import numpy as np
import pandas as pd
import seaborn as sns
from pcser.src.Plot import Plot
from pcser.util.Reader import reader as freader
from pcser.util.Writer import writer as fwriter


class Importance:

    def __init__(
            self,
            X_train,
            X_test,
            clf,
            feature_names=None,
            mark='',
            sv_fp=None,
    ):
        self.X_train = X_train
        self.X_test = X_test
        self.feature_names = feature_names

        self.df_train = pd.DataFrame(self.X_train, columns=self.feature_names)
        self.df_test = pd.DataFrame(self.X_test, columns=self.feature_names)

        self.clf = clf

        self.mark = mark
        self.sv_fp = sv_fp

        self.plot = Plot()
        self.freader = freader()
        self.fwriter = fwriter()

        sns.set(font="Helvetica")
        sns.set_style("ticks")

    def shap(
            self,
            type='tree',
    ) -> str:
        shap.initjs()
        if type == 'tree':
            explainer = shap.TreeExplainer(self.clf)
            shap_values = explainer.shap_values(self.df_test)
        else:
            explainer = shap.Explainer(self.clf, self.df_train)
            shap_values = explainer(self.df_test)
        # print(shap_values.feature_names)
        # clustering = shap.utils.hclust(self.df_train, y)
        print()
        shap.plots.bar(shap_values, )
        print()
        shap.summary_plot(shap_values, self.X_test)
        # shap.dependence_plot("Total_quantification", shap_values, self.X_test)
        print()
        shap.waterfall_plot(shap_values[0])
        print()
        shap.plots.scatter(shap_values[:, "Total_quantification"])
        print()
        shap.plots.heatmap(shap_values)
        return 'Finished'

    def mdi(
            self,
            num=10,
    ) -> pd.DataFrame:
        """
        Mean Decrease in Impurity

        Parameters
        ----------
        X_train
        X_test
        clf

        Returns
        -------

        """
        fi_values = self.clf.feature_importances_
        std = np.std([tree.feature_importances_ for tree in self.clf.estimators_], axis=0)
        # print(std)
        df_fi = pd.Series(
            fi_values,
            index=self.feature_names,
        ).sort_values(ascending=False).to_frame().rename(columns={0: 'importance'})
        # print(df_fi)
        self.plot.bar_fi(
            df=df_fi.iloc[:num, :],
            title='Mean decrease in impurity',
        )
        if self.sv_fp:
            self.fwriter.excel(df=df_fi, sv_fpn=self.sv_fp + 'mdi_' + self.mark + '.xlsx', header=True)
        return df_fi

    def pi(
            self,
            y,
            num=10,
    ) -> pd.DataFrame:
        """
        Permutation feature importance


        Returns
        -------

        """
        from sklearn.inspection import permutation_importance

        result = permutation_importance(
            self.clf,
            self.X_train,
            y,
            n_repeats=10,
            random_state=42,
            n_jobs=2,
        )

        fi_values = result.importances_mean
        std = np.std([tree.feature_importances_ for tree in self.clf.estimators_], axis=0)
        # print(std)

        df_fi = pd.Series(
            fi_values,
            index=self.feature_names,
        ).sort_values(ascending=False).to_frame().rename(columns={0: 'importance'})
        # print(df_fi)
        self.plot.bar_fi(
            df=df_fi.iloc[:num, :],
            title='Permutation importance',
        )
        if self.sv_fp:
            self.fwriter.excel(df=df_fi, sv_fpn=self.sv_fp + 'pi_' + self.mark + '.xlsx', header=True)
        return df_fi