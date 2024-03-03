__author__ = "Jianfeng Sun"
__version__ = "v1.0"
__copyright__ = "Copyright 2024"
__license__ = "GPL v3.0"
__email__ = "jianfeng.sunmt@gmail.com"
__maintainer__ = "Jianfeng Sun"

import joblib
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.utils import shuffle
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import KFold
from sklearn.ensemble import RandomForestRegressor
from pcser.src.Importance import Importance as fi
from pcser.util.Reader import reader as freader
from pcser.util.Writer import writer as fwriter
from pcser.src.Preprocessing import Preprocessing as prep


class Model:

    def __init__(
            self,
            data_ref_fpn,
            version='extended',
            is_norm=True,
            norm_met='minmax',
            mode='compo',
            mark='',
            fi_met=None,
            sv_fp=None,
    ):
        self.data_ref_fpn = data_ref_fpn
        self.version = version
        self.is_norm = is_norm
        self.norm_met = norm_met
        self.mode = mode
        self.mark = mark
        self.fi_met = fi_met
        self.sv_fp = sv_fp
        self.prep = prep(
            data_fpn=self.data_ref_fpn,
            version=self.version,
            is_norm=self.is_norm,
            norm_met=self.norm_met,
            sv_fp=self.sv_fp,
        )
        if self.mode == 'compo':
            self.df = self.prep.sortout_by_compo()
        if self.mode == 'annot':
            self.df = self.prep.sortout_by_annot()
        else:
            self.df = self.prep.sortout_by_compo()
        print("Data summary:")
        print("Number of samples: {}".format(self.df.shape[0]))
        print("Number of features: {}".format(self.df.shape[1]))
        self.fi = fi
        self.freader = freader()
        self.fwriter = fwriter()

        sns.set(font="Helvetica")
        sns.set_style("ticks")

    def build_whole(
            self,
            seed=4,
    ):
        df = shuffle(self.df, random_state=seed)
        y = df['stealth_effect'].values
        df = df.drop(['stealth_effect'], axis=1)
        X = df.values
        # print(df)
        # print(X)
        # print(y)

        # import xgboost
        # regr = xgboost.XGBRegressor()
        # regr.fit(X, y)

        regr = RandomForestRegressor(
            random_state=seed,
        )
        regr.fit(X, y)

        if self.fi_met == 'shap':
            df_fi = self.fi(
                X_train=X,
                X_test=X,
                clf=regr,
                feature_names=df.columns,
                sv_fp=self.sv_fp,
            ).shap(
                type=''  # tree
            )
        elif self.fi_met == 'mdi':
            df_fi = self.fi(
                X_train=X,
                X_test=X,
                clf=regr,
                feature_names=df.columns,
                sv_fp=self.sv_fp,
            ).mdi()
        elif self.fi_met == 'pi':
            df_fi = self.fi(
                X_train=X,
                X_test=X,
                clf=regr,
                feature_names=df.columns,
                sv_fp=self.sv_fp,
            ).pi(y=y)
        # from sklearn.model_selection import cross_validate
        # cv_results = cross_validate(regr, X, y, cv=5, return_estimator=True, )
        # print(cv_results['test_score'])
        # rfc_fit = cv_results['estimator']
        # print(rfc_fit)
        return df_fi

    def build_kfold(
            self,
            seed=4,
    ):
        df = shuffle(self.df, random_state=seed)
        y = df['stealth_effect'].values
        # df = df.drop(['Total_quantification'], axis=1)
        df = df.drop(['stealth_effect'], axis=1)
        X = df.values
        # print(df)
        # print(X)
        # print(y)

        # X_b = X[:47]
        # print(X_b)
        # X_cooh = X[47:]
        # print(X_cooh)
        # X = X_b

        arr_mse = []
        arr_r2 = []
        arr_regr = []
        cv = KFold(n_splits=5, shuffle=True, random_state=seed)
        for i, (train_ix, test_ix) in enumerate(cv.split(X)):
            # @@ split data
            print("No.{}-fold".format(i))
            # print("IDs for training: {}".format(train_ix))
            np.random.shuffle(train_ix)
            X_train, X_test = X[train_ix, :], X[test_ix, :]
            y_train, y_test = y[train_ix], y[test_ix]
            # print(X_train.shape)
            regr = RandomForestRegressor(
                # n_estimators=1000,
                max_depth=10,
                random_state=seed,
            )
            regr.fit(X_train, y_train)
            # y_cooh = regr.predict(X_cooh)
            arr_r2.append(regr.score(X_test, y_test))
            arr_mse.append(mean_squared_error(y_test, regr.predict(X_test)))
            arr_regr.append(regr)
            if self.sv_fp:
                joblib.dump(regr, filename=self.sv_fp + 'model/' + 'cv' + str(i) + '.joblib')
            # if regr.score(X_test, y_test) < 0.4:
        print("R2: {}".format(arr_r2))
        # print("No.{}: {} | ".format(i, r2) for i, r2 in enumerate(arr_r2))
        print("===>Average: {}".format(np.mean(arr_r2)))
        print("===>Max: {}".format(np.max(arr_r2)))
        print("MSE: {}".format(arr_mse))
        # print("No.{}: {} | ".format(i, mse) for i, mse in enumerate(arr_mse))
        print("===>Average: {}".format(np.mean(arr_mse)))
        print("===>Max: {}".format(np.max(arr_mse)))

        if self.sv_fp:
            print('Models and training data haven been saved!')
            joblib.dump(
                arr_regr[np.argmax(arr_r2)],
                filename=self.sv_fp + 'model/' + 'best_cv.joblib',
            )
            self.fwriter.generic(
                df=[arr_r2],
                sv_fpn=self.sv_fp + 'r2_kfold_' + self.mode + '_' + self.version + '_' + self.norm_met + '_' + self.mark + '.txt',
                index=True,
                header=True,
            )
            self.fwriter.generic(
                df=[arr_mse],
                sv_fpn=self.sv_fp + 'mse_kfold_' + self.mode + '_' + self.version + '_' + self.norm_met + '_' + self.mark + '.txt',
                index=True,
                header=True,
            )
        print('Models have been built!')
        return arr_regr

    def build_loo(
            self,
            seed=4,
    ):
        """
        Notes
        -----
            Leave-one-out (LOO)

        Returns
        -------

        """
        features = self.df.columns.tolist()
        features.remove('stealth_effect')
        arr = []
        for id, feature in enumerate(features):
            print('No.{}: feature {}'.format(id, feature))
            df = self.df.drop([feature], axis=1)
            print(df.shape)
            # df = shuffle(df)
            df = shuffle(df, random_state=seed)
            y = df['stealth_effect'].values
            df = df.drop(['stealth_effect'], axis=1)
            X = df.values
            arr_mse = []
            arr_r2 = []
            cv = KFold(n_splits=5, shuffle=True, random_state=seed)
            for i, (train_ix, test_ix) in enumerate(cv.split(X)):
                # split data
                np.random.shuffle(train_ix)
                X_train, X_test = X[train_ix, :], X[test_ix, :]
                y_train, y_test = y[train_ix], y[test_ix]
                # print(X_train.shape)
                regr = RandomForestRegressor(
                    # n_estimators=1000,
                    max_depth=10,
                    random_state=seed,
                )
                regr.fit(X_train, y_train)
                arr_r2.append(regr.score(X_test, y_test))
                arr_mse.append(mean_squared_error(y_test, regr.predict(X_test)))
            arr.append(arr_r2)
            print("R2: {}".format(arr_r2))
            print("===>Average: {}".format(np.mean(arr_r2)))
            print("===>Max: {}".format(np.max(arr_r2)))
        df_loo = pd.DataFrame(arr)
        df_loo.index = features
        if self.sv_fp:
            self.fwriter.generic(
                df=df_loo,
                sv_fpn=self.sv_fp + 'r2_loo_' + self.mode + '_' + self.version + '_' + self.norm_met + '_' + self.mark + '.txt',
                index=True,
                header=True,
            )
        return

    def build_with_f_loo(
            self,
            r2_fpn,
            r2_loo_fpn,
            seed=4,
    ):
        """
        Notes
        -----
            Leave-one-out (LOO)

        Returns
        -------

        """
        df_r2 = self.freader.generic(r2_fpn, index_col=0, header=0)
        print(df_r2)
        print(df_r2.max(axis=1))
        df_r2_loo = self.freader.generic(r2_loo_fpn, header=0, index_col=0)
        # print(df_r2_loo)
        print(df_r2_loo.max(axis=1))
        df_increment = df_r2_loo.max(axis=1).apply(lambda x: x - df_r2.max(axis=1).iloc[0])
        print(df_increment)
        df_increment_nega = df_increment[df_increment >= 0].index.tolist()
        print(df_increment_nega)
        df = self.df[df_increment_nega + ['stealth_effect']]
        # print(df)
        df = shuffle(df, random_state=seed)
        y = df['stealth_effect'].values
        df = df.drop(['stealth_effect'], axis=1)
        X = df.values
        cv = KFold(n_splits=5, shuffle=True, random_state=seed)
        arr_r2 = []
        arr_regr = []
        for i, (train_ix, test_ix) in enumerate(cv.split(X)):
            # split data
            X_train, X_test = X[train_ix, :], X[test_ix, :]
            y_train, y_test = y[train_ix], y[test_ix]
            regr = RandomForestRegressor(max_depth=6, random_state=seed)
            regr.fit(X_train, y_train)
            arr_r2.append(regr.score(X_test, y_test))
            arr_regr.append(regr)
            if self.sv_fp:
                joblib.dump(regr, filename=to('data/model/loo_f82/') + 'cv' + str(i) + '.joblib')
        print(arr_r2)
        if self.sv_fp:
            joblib.dump(arr_regr[np.argmax(arr_r2)], filename=to('data/model/loo_f82/') + 'best_cv.joblib')
            self.fwriter.generic(df=[arr_r2], sv_fpn=to('data/r2_loo_f82.txt'), index=True, header=True)
        return

    def evaluate(
            self,
            input_fpn : str,
            sheet_name : str,
            model_fpn: str,
            mfi_ref : float | list = None,
    )-> pd.DataFrame:
        df = self.freader.excel(input_fpn, sheet_name=sheet_name , header=0, index_col='Description')
        df.index.name = None
        spl_names = df.columns.values.tolist()
        if 'Annotation' in spl_names:
            spl_names.remove('Annotation')
        print('You have the samples: {}'.format(spl_names))
        self.df = self.df.drop(['stealth_effect'], axis=1).T
        df = self.df.join(df)[spl_names].T
        df = df.fillna(0)
        # print(df)
        clf = joblib.load(model_fpn)
        df_pred = pd.DataFrame(clf.predict(df.values), columns=['stealth_effect'])
        df_pred.index = spl_names
        if mfi_ref:
            df_pred['MFI'] = mfi_ref - np.squeeze(self.prep.scaler.inverse_transform(df_pred))
        print('PCSER predictions: \n{}'.format(df_pred))
        return df_pred

    def extend(
            self,
            input_fpn: str,
            sheet_name: str,
            model_fpn: str,
            rept_times=5,
            poi='Total_quantification',
            spl_name='PS-PBS-HU-3h_HuApoA1', # PS-PBS_HuApoA1 PS-COOH-C57BL6 MoPlasma_HuApoA1 PS-COOH-NonSwissAlbino MoPlasma_Blank
            mfi_ref: float | list = None,
            poi_increments: float | list = [0, 10, 100, 1000, 10000],
    ) -> pd.DataFrame:
        """
        eli_arr = [
            # 'Apolipoprotein A-I OS=Homo sapiens OX=9606 GN=APOA1 PE=1 SV=1',
            # 'Apolipoprotein E OS=Mus musculus OX=10090 GN=Apoe PE=1 SV=2',
            # 'Apolipoprotein A-I OS=Mus musculus OX=10090 GN=Apoa1 PE=1 SV=2',
            # 'Clusterin OS=Homo sapiens OX=9606 GN=CLU PE=1 SV=1',
            # 'Apolipoprotein A-I OS=Homo sapiens OX=9606 GN=APOA1 PE=1 SV=1',
            'Total_quantification',
            # 'Apolipoprotein E OS=Mus musculus OX=10090 GN=Apoe PE=1 SV=2',
            # 'Integrin beta-3 OS=Mus musculus OX=10090 GN=Itgb3 PE=1 SV=2',
            # 'Vitronectin OS=Mus musculus OX=10090 GN=Vtn PE=1 SV=2',
            # 'Vitronectin OS=Homo sapiens OX=9606 GN=VTN PE=1 SV=1',
        ]
        Parameters
        ----------
        rept_times
        poi
        spl_name

        Returns
        -------

        """
        df = self.freader.excel(input_fpn, sheet_name=sheet_name, header=0, index_col='Description')
        df.index.name = None
        spl_names = df.columns.values.tolist()
        if 'Annotation' in spl_names:
            spl_names.remove('Annotation')
        print('You have the samples: {}'.format(spl_names))
        self.df = self.df.drop(['stealth_effect'], axis=1).T
        df = self.df.join(df)[spl_names].T
        df = df.fillna(0)
        # print(df)

        df = df.loc[spl_name, :].to_frame().T
        # print(df)
        if 'stealth_effect' in df.columns:
            df = df.drop(['stealth_effect'], axis=1)

        feature_names = df.columns
        df = pd.DataFrame(np.repeat(df.values, rept_times, axis=0))
        df.columns = feature_names

        # df[poi] = np.linspace(0, 1, rept_times) * 100
        df[poi] = poi_increments
        clf = joblib.load(model_fpn)
        df_pred = pd.DataFrame(clf.predict(df.values), columns=['stealth_effect'])
        if mfi_ref:
            df_pred['MFI'] = mfi_ref - np.squeeze(self.prep.scaler.inverse_transform(df_pred))
        print('PCSER predictions: \n{}'.format(df_pred))
        return df_pred

    def t(self, x, eli_ref, eli_mark, prot_mark_ids):
        """
        # print(df[prot_mark_ids].sum(axis=1))
        # prot_mark_ids = df.columns.tolist()
        # prot_mark_ids.remove('Total_quantification')
        # prot_mark_ids.remove(poi)
        # # print(len(prot_mark_ids))
        # df.apply(lambda x: self.t(x, eli_ref, poi, prot_mark_ids), axis=1)

        Parameters
        ----------
        x
        eli_ref
        eli_mark
        prot_mark_ids

        Returns
        -------

        """
        for f in prot_mark_ids:
            x[f] = (x[f]/(100-eli_ref))*(100-x[eli_mark])
        return


if __name__ == "__main__":
    from pcser.path import to

    DEFINE = {
        # 'data_ref_fpn': to('data/hu_macrophage/Proteomics_07262023.xlsx'),
        'data_ref_fpn': to('data/hu_macrophage/Proteomics_07262023_rv_C57BL6_spl54.xlsx'),
        # 'data_ref_fpn': to('data/mo_macrophage_264.7/Proteomics_05172023.xlsx'),
        # 'data_ref_fpn': to('data/mo_macrophage_264.7/Proteomics_05262023.xlsx'),
        'sv_fp': to('data/'),
    }

    model = Model(
        data_ref_fpn=DEFINE['data_ref_fpn'],
        version='extended', # extended old
        is_norm=True,
        norm_met='minmax', # minmax std maxabs
        mode='compo', # compo annot
        mark='spl54', # compo annot
        fi_met='pi',  # None shap mdi pi
        sv_fp=to('data/'), # None to('data/')
    )

    # model.build_kfold(
    #     seed=4,
    # )

    # model.build_whole(
    #     seed=4,
    # )

    # model.build_loo(
    #     seed=4,
    # )

    # model.build_with_f_loo(
    #     r2_fpn=to('data/r2_compo-Proteomics_07262023_rv_C57BL6_spl54.txt'),
    #     r2_loo_fpn=to('data/r2_loo_compo-Proteomics_07262023_rv_C57BL6_spl54.txt'),
    # )

    # model.evaluate(
    #     input_fpn=to('data/hu_macrophage/example.xlsx'),
    #     model_fpn=to('data/model/') + 'best_cv.joblib',
    #     sheet_name='a', # a b
    #     # mfi_ref=[10271.33333, 10747, 10303.33333, 9663.333333, 10056],
    #     mfi_ref=[3606.333333, 3606.333333, 3606.333333, 3606.333333],
    # )

    model.extend(
        input_fpn=to('data/hu_macrophage/example.xlsx'),
        sheet_name='a', # a b
        spl_name='HuApoA1', # HuApoA1
        model_fpn=to('data/model/') + 'best_cv.joblib',
        mfi_ref=3606.3,
    )