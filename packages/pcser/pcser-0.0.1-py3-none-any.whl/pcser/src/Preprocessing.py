__author__ = "Jianfeng Sun"
__version__ = "v1.0"
__copyright__ = "Copyright 2024"
__license__ = "GPL v3.0"
__email__ = "jianfeng.sunmt@gmail.com"
__maintainer__ = "Jianfeng Sun"

import numpy as np
import pandas as pd
from pcser.util.Reader import reader as freader
from pcser.util.Writer import writer as fwriter


class Preprocessing:

    def __init__(
            self,
            data_fpn,
            is_norm=True,
            norm_met='minmax',
            version='extended',
            sv_fp=None,
    ):
        self.freader = freader()
        self.fwriter = fwriter()
        self.data_fpn = data_fpn
        self.is_norm = is_norm
        self.norm_met = norm_met
        self.sv_fp = sv_fp

        self.nanoparticles = [
            'PS',
            'PS-NH2',
            'PS-COOH',
        ]
        self.precoatings = [
            'HuApoA1',
            'MoApoA1',
            'HuClusterin',
            'MoClusterin',
        ]
        self.challenge_systems = [
            'PBS',
            'HuPlasma',
            'C57BL6 MoPlasma',
        ]
        if version == 'extended':
            print('You are using extended sheets.')
            self.sheet_PBS = [
                'PS-PBS',
                'PS-NH2-PBS',
                'PS-COOH-PBS',

                'PS-PBS-HU-3h',
                'PS-NH2-PBS-HU-3h',
                'PS-COOH-PBS-HU-3h',
            ]
        else:
            self.sheet_PBS = [
                'PS-PBS',
                'PS-NH2-PBS',
                'PS-COOH-PBS',
            ]

        self.sheet_challenge = [
            'PS-HuPlasma',
            'PS-NH2-HuPlasma',
            'PS-COOH-HuPlasma',

            'PS-Non Swiss Albino MoPlasma',
            'PS-NH2-Non Swiss AlbinoMoPlasma',
            'PS-COOH-NonSwissAlbino MoPlasma',

            'PS-C57BL6 MoPlasma',
            'PS-NH2-C57BL6 MoPlasma',
            'PS-COOH-C57BL6 MoPlasma',
        ]
        self.sheet_names = self.sheet_PBS + self.sheet_challenge

        if self.is_norm:
            # df['stealth_effect'] = skpreprocessing.normalize([df['stealth_effect'].values])[0]
            print('You have selected the {} normalization method.'.format(self.norm_met))
            if self.norm_met == 'minmax':
                from sklearn.preprocessing import MinMaxScaler
                self.scaler = MinMaxScaler()
            elif self.norm_met == 'std':
                from sklearn.preprocessing import StandardScaler
                self.scaler = StandardScaler()
            elif self.norm_met == 'maxabs':
                from sklearn.preprocessing import MaxAbsScaler
                self.scaler = MaxAbsScaler()
            else:
                from sklearn.preprocessing import MinMaxScaler
                self.scaler = MinMaxScaler()

    def sortout_by_compo(
            self,
    ):
        arr = []
        for sheet_name in self.sheet_names:
            df = self.freader.excel(self.data_fpn, sheet_name=sheet_name, header=0, index_col=False)
            if not df.empty:
                df.index = df['Description'].values
                df = df.drop(['Description'], axis=1).T
                df = df.drop(['Annotation'], axis=0)
                df.index = [sheet_name + '_' + i for i in df.index.values]
                arr.append(df)
        df = pd.concat(arr, axis=0)
        # print(df)
        df = df[df['MFI'].notna()]
        df = df[df['MFI_PBS'].notna()]
        # df['stealth_effect'] = df.apply(lambda x: x['MFI'], axis=1)
        df['stealth_effect'] = df.apply(lambda x: x['MFI_PBS'] - x['MFI'], axis=1)
        # print(df['stealth_effect'])

        if self.is_norm:
            df['stealth_effect'] = np.squeeze(self.scaler.fit_transform(df['stealth_effect'].to_frame()))

        # if self.is_norm:
        #     # df['stealth_effect'] = skpreprocessing.normalize([df['stealth_effect'].values])[0]
        #     if self.norm_met == 'minmax':
        #         from sklearn.preprocessing import MinMaxScaler
        #         scaler = MinMaxScaler()
        #         df['stealth_effect'] = np.squeeze(scaler.fit_transform(df['stealth_effect'].to_frame()))
        #     if self.norm_met == 'std':
        #         from sklearn.preprocessing import StandardScaler
        #         scaler = StandardScaler()
        #         df['stealth_effect'] = np.squeeze(scaler.fit_transform(df['stealth_effect'].to_frame()))
        #     if self.norm_met == 'maxabs':
        #         from sklearn.preprocessing import MaxAbsScaler
        #         scaler = MaxAbsScaler()
        #         df['stealth_effect'] = np.squeeze(scaler.fit_transform(df['stealth_effect'].to_frame()))
        #     print(df['stealth_effect'])
            # df['stealth_effect_recovered'] = scaler.inverse_transform(df['stealth_effect'].to_frame())
            # print(df['stealth_effect_recovered'])

        # eli_arr = [
        #     # 'Apolipoprotein A-I OS=Homo sapiens OX=9606 GN=APOA1 PE=1 SV=1',
        #     # 'Apolipoprotein A-I OS=Mus musculus OX=10090 GN=Apoa1 PE=1 SV=2',
        #     'Clusterin OS=Homo sapiens OX=9606 GN=CLU PE=1 SV=1',
        #     # 'Clusterin OS=Mus musculus OX=10090 GN=Clu PE=1 SV=1',
        # ]
        # df = df[eli_arr + ['Total_quantification'] + ['MFI', 'MFI_PBS'] + ['stealth_effect']]
        # df = df.drop(eli_arr, axis=1)
        df = df.drop(['MFI', 'MFI_PBS'], axis=1)
        df = df.fillna(0)
        # print(df)
        if self.sv_fp:
            self.fwriter.excel(
                df,
                sheet_name='compo',
                sv_fpn=self.sv_fp + 'train_compo.xlsx',
                header=True,
                index=True,
            )
        return self.rename(df)

    def sortout_by_annot(
            self,
    ):
        df_annot = pd.DataFrame()
        for sheet_name in self.sheet_names:
            df = self.freader.excel(self.data_fpn, sheet_name=sheet_name, header=0, index_col=False)
            df_g_tmp = pd.DataFrame()
            if not df.empty:
                df_non_proteomics = df.iloc[-3:]
                # print(df_non_proteomics)
                df_non_proteomics.index = df_non_proteomics['Description'].values
                df_non_proteomics = df_non_proteomics.drop(['Description', 'Annotation', ], axis=1)
                s_cols = df_non_proteomics.columns
                df_non_proteomics.columns = [sheet_name + '_' + u for u in s_cols]
                # print(df_non_proteomics.T)
                df_g = df.groupby(by=['Annotation'])
                g_keys = [*df_g.groups.keys()][1:]
                # print(g_keys)
                for g in g_keys:
                    df_g_ru = df_g.get_group(g)[
                        self.precoatings if sheet_name in self.sheet_PBS else self.precoatings + ['Blank']
                    ]
                    df_g_ru = df_g_ru.sum(axis=0).to_frame().T
                    # df_g_ru.index = [sheet_name + '_' + g]
                    df_g_ru.index = [g]
                    cols = df_g_ru.columns
                    df_g_ru.columns = [sheet_name + '_' + yj for yj in cols]
                    df_g_tmp = pd.concat([df_g_tmp, df_g_ru], axis=0)

                df_g_tmp = pd.concat([df_g_tmp.T, df_non_proteomics.T], axis=1)
                # print(df_g_tmp)
            df_annot = pd.concat([df_annot, df_g_tmp], axis=0)

        df = df_annot

        # eli_arr = [
        #     'Lipoproteins',
        # ]

        df = df[df['MFI'].notna()]
        df = df[df['MFI_PBS'].notna()]
        # df['stealth_effect'] = df.apply(lambda x: x['MFI'], axis=1)
        df['stealth_effect'] = df.apply(lambda x: x['MFI_PBS'] - x['MFI'], axis=1)
        # df = df[eli_arr + ['Total_quantification'] + ['MFI', 'MFI_PBS'] + ['stealth_effect']]

        if self.is_norm:
            df['stealth_effect'] = np.squeeze(self.scaler.fit_transform(df['stealth_effect'].to_frame()))

        # if self.is_norm:
        #     # df['stealth_effect'] = skpreprocessing.normalize([df['stealth_effect'].values])[0]
        #     if self.norm_met == 'minmax':
        #         from sklearn.preprocessing import MinMaxScaler
        #         scaler = MinMaxScaler()
        #         df['stealth_effect'] = np.squeeze(scaler.fit_transform(df['stealth_effect'].to_frame()))
        #     if self.norm_met == 'std':
        #         from sklearn.preprocessing import StandardScaler
        #         scaler = StandardScaler()
        #         df['stealth_effect'] = np.squeeze(scaler.fit_transform(df['stealth_effect'].to_frame()))
        #     if self.norm_met == 'maxabs':
        #         from sklearn.preprocessing import MaxAbsScaler
        #         scaler = MaxAbsScaler()
        #         df['stealth_effect'] = np.squeeze(scaler.fit_transform(df['stealth_effect'].to_frame()))
        #     print(df['stealth_effect'])
            # df['stealth_effect_recovered'] = scaler.inverse_transform(df['stealth_effect'].to_frame())
            # print(df['stealth_effect_recovered'])

        df = df.drop(['MFI', 'MFI_PBS'], axis=1)
        df = df.fillna(0)
        # print(df)
        if self.sv_fp:
            self.fwriter.excel(
                df,
                sheet_name='annot',
                sv_fpn=self.sv_fp + 'train_annot.xlsx',
                header=True,
                index=True,
            )
        return df

    def rename(self, df):
        arr = []
        for i, f in enumerate(df.columns):
            if 'OS=H' in f:
                # arr.append(f.split(' ')[0] + '(H)')
                arr.append(f.split(' ')[0] + '(H)' + str(i))
            elif 'OS=M' in f:
                # arr.append(f.split(' ')[0] + '(M)')
                arr.append(f.split(' ')[0] + '(M)' + str(i))
            else:
                arr.append(f.split(' ')[0])
        df.columns = arr
        return df


if __name__ == "__main__":
    from pcser.path import to

    DEFINE = {
        'data_fpn': to('data/hu_macrophage/Proteomics_07262023.xlsx'),
        # 'data_fpn': to('data/mo_macrophage_264.7/Proteomics_05172023.xlsx'),
    }

    p = Preprocessing(
        data_fpn=DEFINE['data_fpn'],
        is_norm=True,
        norm_met='maxabs', # minmax std maxabs
        version='extended',  # extended old
    )

    # df = p.sortout_by_compo()

    df = p.sortout_by_annot()

    print(df)