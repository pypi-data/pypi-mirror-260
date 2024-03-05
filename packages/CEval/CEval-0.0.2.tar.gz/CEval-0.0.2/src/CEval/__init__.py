"""
`CEval` is a class for evaluating counterfactual explanations.
It calculates the following metrics:
    - Validity
    - Proximity
    - Sparsity
    - Count
    - Diversity
    - Diversity LCC
    - yNN
    - Feasibility
    - kNLN distance
    - Relative distance
    - Redundancy
    - Plausibility
    - Constraint violation
"""

import gower
import pandas as pd
import numpy as np
from sklearn.neighbors import NearestNeighbors
import category_encoders as ce
from scipy.spatial.distance import cdist

class CEval:
    """
    Attributes
    ----------
    explainer_names : list
        a formatted string to print out what the animal says
    label : str
    metric_features: pd.DataFrame
    knn : int
    data : pd.DataFrame
    column_names : list
    comparison_table : pd.DataFrame
    samples : pd.Dataframe
    samples_X : pd.DataFrame
    numeric_names : list
    column_names_X : list
    categorical_names : list
    s_count : int
    encoder : string

    Methods
    -------
    add_explainer(name: str, explanations: pd.DataFrame, exp_type: str, mode='1to1')
        Prints the animals name and what sound it makes

    calculate_validity(exp_df: pd.DataFrame, mode: str)

    calculate_proximity_gower(exp_df: pd.DataFrame, mode: str)

    distance_gower(s: pd.Series, e: pd.Series) -> float

    calculate_proximity(exp_df: pd.DataFrame, mode: str) -> float

    calculate_diversity_lcc(exp_df: pd.DataFrame, mode: str) -> float

    calculate_yNN(exp_df: pd.DataFrame, mode: str)

    calculate_kNLN_distance(exp_df: pd.DataFrame, mode: str)

    calculate_feasibility(exp_df: pd.DataFrame, mode: str)

    calculate_relative_dist(exp_df: pd.DataFrame, mode: str)

    calculate_redundancy(exp_df: pd.DataFrame, mode: str)

    redundancy(s: pd.Series, e: pd.Series) -> int
    """
    def __init__(self, samples: pd.DataFrame, label: str, data=None, model=None, k_nn=5, explainer_name=None, explanations=None, explanation_type=None, explanation_mode='1to1', encoder=None, cdist=None, constraints=None):
        self.explainer_names = []
        self.label = label
        self.metric_features = pd.read_csv('feature_table.csv', index_col=0, delimiter=';')
        self.metrics = self.metric_features.index.values.tolist()
        self.knn = k_nn
        self.data = data
        self.model = model
        self.constraints = constraints

        # Datatype check
        if not type(samples) is pd.core.frame.DataFrame:
            raise TypeError("'samples' must be a DataFrame.")

        self.s_count = len(samples)

        # number of instances check
        if self.s_count > 0:
            # set col names
            self.column_names = samples.columns.values
            self.comparison_table = pd.DataFrame([], columns=self.metrics)
            self.samples = samples
            self.samples_X = samples.drop([label], axis=1)
            self.numeric_names = self.samples_X.select_dtypes(include=np.number).columns.tolist()
            self.column_names_X = self.samples_X.columns.values
            self.categorical_names = self.samples_X.select_dtypes(include=object).columns.tolist()

        else:
            raise Exception("The number of instances must be more than 0.")


        self.set_distance(cdist)


        if self.data is not None:
            self.data_X = data.drop([self.label], axis=1)
            self.data_y = data[self.label]

            self.num_label = len(np.unique(self.data[self.label].values))

            # Encoding
            self.set_encoder(encoder)

            self.data_X_enc = self.encode(self.data_X)
            self.data_enc = self.data_X_enc.copy()
            self.data_enc[self.label] = self.data_y

            self.kNN_model = self.kNN_train(self.knn, self.data_X_enc)


        if explainer_name is not None \
                or explanations is not None \
                or explanation_type is not None:
            self.add_explainer(explainer_name, explanations, explanation_type, explanation_mode)

    def kNN_train(self, k, data):
        return NearestNeighbors(n_neighbors=k).fit(data)

    def kNN(self, kNN_model, row, k, distance=False):
        res = kNN_model.kneighbors(row.values.reshape((1, -1)), k, return_distance=distance)[0]
        if distance:
            return res[0]
        else:
            return res


    def set_distance(self, cdist):

        metrics = { 'braycurtis', 'canberra', 'chebyshev',
                   'jaccard', 'hamming', 'cosine', 'sqeuclidean',
                   'cityblock', 'minkowski', 'euclidean' }
        if cdist in metrics or cdist is None:
            self.dist = cdist
        else:
            raise Exception("Distance metric selection must be one of the followings, None",  ', '.join(metrics))


    def set_encoder(self, enc):
        """
        :param enc: encoder name
        """

        encoders = { 'BackwardDifferenceEncoder': ce.BackwardDifferenceEncoder,
                       'BaseNEncoder': ce.BaseNEncoder,
                       'BinaryEncoder': ce.BinaryEncoder,
                       'CatBoostEncoder': ce.CatBoostEncoder,
                       'CountEncoder': ce.CountEncoder,
                       'GLMMEncoder': ce.GLMMEncoder,
                       'GrayEncoder': ce.GrayEncoder,
                       'HelmertEncoder': ce.HelmertEncoder,
                       'JamesSteinEncoder': ce.JamesSteinEncoder,
                       'LeaveOneOutEncoder': ce.LeaveOneOutEncoder,
                       'MEstimateEncoder': ce.MEstimateEncoder,
                       'OneHotEncoder': ce.OneHotEncoder,
                       'OrdinalEncoder': ce.OrdinalEncoder,
                       'PolynomialEncoder': ce.PolynomialEncoder,
                       'QuantileEncoder': ce.QuantileEncoder,
                       'RankHotEncoder': ce.RankHotEncoder,
                       'SumEncoder': ce.SumEncoder,
                       'TargetEncoder': ce.TargetEncoder,
                       'WOEEncoder': ce.WOEEncoder
                       }

        if enc is None:
            self.encoder = ce.OrdinalEncoder(self.categorical_names).fit(self.data_X, self.data_y)
        elif enc in encoders.keys():
            self.encoder = encoders[ enc ](self.categorical_names).fit(self.data_X, self.data_y)
        else:
            raise Exception("Given encoder is not valid, possible selections: None, ", "', '".join(encoders.keys()))


    def encode(self, x):
        """
        :param x: data to encode
        """
        return self.encoder.transform(x)

    def add_explainer(self, name: str, explanations: pd.DataFrame, exp_type: str, mode='1to1'):
        """
        :param name: Explainer name (str)
        :param explanations: Explanations of samples (pd.DataFrame)
        :param exp_type: Type of explanations (str)
        :param mode: Explanation mode, can be '1to1' or '1toN' (str)
        :return: -
        If mode is '1to1' then explanations must be a DataFrame with the same number of rows as the number of samples.  
        """
        # Datatype check
        if not type(explanations) is pd.core.frame.DataFrame:
            raise TypeError("'explanations' must be a DataFrame.")

        types = [ 'existed-cf',
                  'existed-factual',
                  'generated-cf',
                  'generated-factual' ]

        metrics_map = { 'validity': self.calculate_validity,
                        'proximity': self.calculate_proximity,
                        'proximity_gower': self.calculate_proximity_gower,
                        'sparsity': self.calculate_sparsity,
                        'count': self.calculate_exp_count,
                        'diversity': self.calculate_diversity,
                        'diversity_lcc': self.calculate_diversity_lcc,
                        'yNN': self.calculate_yNN,
                        'feasibility': self.calculate_feasibility,
                        'kNLN_dist': self.calculate_kNLN_distance,
                        'relative_dist': self.calculate_relative_dist,
                        'redundancy': self.calculate_redundancy,
                        'plausibility': self.calculate_plausibility,
                        'constraint_violation': self.constraint_violation,
                        }


        if mode == '1to1':
            if len(explanations) != self.s_count:
                raise Exception("In \'1to1\' mode instance and explanation count must be the same.")

        elif mode == '1toN':
            if 'instance' not in explanations.columns.values:
                raise Exception("In \'1toN\' mode 'instance' feature is required.")

        else:
            raise Exception("Evaluation mode can be only \'1to1\' or \'1toN\'.")

        if exp_type not in types:
            raise ValueError("Explanation type should be one of the followings: " + str(types))

        self.explainer_names.append(name)

        # set the constraints
        c1 = 'existed' if 'existed' in exp_type else 'generated'
        c2 = 'counterfactual' if 'cf' in exp_type else 'factual'
        c3 = mode

        valid_metrics = self.metric_features[self.metric_features[[c1, c2, c3]] != '-' ][[c1, c2, c3]].dropna().index.values

        results = []

        for metric in metrics_map.keys():
            # if it is one to n calculate the same call with others (1,1)(1,2)(2,1)....
            if metric in valid_metrics:
                results.append(metrics_map[metric](explanations, mode))
            else:
                results.append('-')

        self.explainer_names.append(name)

        self.comparison_table = pd.concat([self.comparison_table, pd.DataFrame([results], columns=self.metrics, index=[name])])


    # if the generated or provided explanation case is from another class then 𝑥𝑖
    def calculate_validity(self, exp_df: pd.DataFrame, mode: str):
        """
        :param exp_df:  Explanations of samples (pd.DataFrame)
        :param mode: Explanation mode, can be '1to1' or '1toN' (str)
        :return: Validity score (float).
        """
        if self.model is None or self.data is None:
            return '-'

        def validity(s: pd.Series, e: pd.Series) -> int:
            """
            :param s: A sample to explain (pd.Series)
            :param e: An explanation of s (pd.Series)
            :return: 0 or 1
            """
            t = self.model.predict([e.drop(self.label).values])[0]
            if s[self.label] != e[self.label] and t == e[self.label]:
                return 1
            elif int(s[self.label]) != int(e[self.label]) and int(t) == int(e[self.label]):
                return 1
            else:
                return 0


        samples_enc = self.encode(self.samples_X).reindex()
        samples_enc[self.label] = self.samples[self.label]

        val_count = 0
        if mode == '1to1':
            temp_exp = self.encode(exp_df.drop([self.label], axis=1))
            temp_exp[self.label] = exp_df[self.label]
            for i in range(self.s_count):
                val_count += validity(samples_enc.iloc[i], temp_exp.iloc[i])


        else:
            temp_exp = self.encode(exp_df.drop(['instance',self.label], axis=1))
            temp_exp[self.label] = exp_df[self.label]
            for i in range(self.s_count):
                temp_i_exp = temp_exp[exp_df['instance']==i]
                for j in range(len(temp_i_exp)):
                    val_count += validity(samples_enc.iloc[i], temp_i_exp.iloc[j])

        return round((val_count / len(exp_df)),3)


    def calculate_proximity_gower(self, exp_df: pd.DataFrame, mode: str):
        """
        Calculates average distance score for provided samples and their explanations.
        Uses the Gower distance function
        :param exp_df: Explanations of samples (pd.DataFrame)
        :param mode: Explanation mode, can be '1to1' or '1toN' (str)
        :return: Average distance score (float).
        """
        if self.data is None:
            return '-'

        cum_prox = 0
        exp_df = exp_df.drop([ self.label ], axis=1)

        if mode == '1to1':
            for i in range(self.s_count):
                cum_prox += self.distance_gower(self.samples_X.iloc[i:i+1], exp_df.iloc[i:i+1])

        else:
            for i in range(self.s_count):
                temp_i_exp = exp_df[exp_df['instance']==i].drop(['instance'], axis=1)
                for j in range(len(temp_i_exp)):
                    cum_prox += self.distance_gower(self.samples_X.iloc[i:i+1], temp_i_exp.iloc[j:j+1])

        return round((cum_prox / len(exp_df)),3)

    def distance_gower(self, s: pd.Series, e: pd.Series) -> float:
        """
        Calculates Gower distance between s and e.
        :param s: A sample to explain (pd.Series)
        :param e: An explanation of s (pd.Series)
        :return: Gower distance between s and e (float)
        """
        return gower.gower_matrix(pd.concat([s, e, self.data], axis=1))[0][1]

    def calculate_proximity(self, exp_df: pd.DataFrame, mode: str) -> float:
        """
        Calculates average distance score for provided samples and their explanations.
        Uses the provided distance function
        :param exp_df: Explanations of samples (pd.DataFrame)
        :param mode: Explanation mode, can be '1to1' or '1toN' (str)
        :return: Average distance score (float).
        """
        cum_prox = 0
        exp_df = exp_df.drop([self.label], axis=1)

        if mode == '1to1':
            for i in range(self.s_count):
                cum_prox += self.distance(self.samples_X.iloc[i], exp_df.iloc[i])

        else:
            for i in range(self.s_count):
                temp_i_exp = exp_df[exp_df['instance']==i].drop(['instance'], axis=1)
                for j in range(len(temp_i_exp)):
                    cum_prox += self.distance(self.samples_X.iloc[i], temp_i_exp.iloc[j])

        return round((cum_prox / len(exp_df)),3)

    def distance(self, s: pd.Series, e: pd.Series) -> float:
        """
        Calculate
        :param s: Sample to explain (pd.Series)
        :param e: An explanation of s (pd.Series)
        :return: distance between s and e (float)
        """
        if self.dist is None:
            num_dist = np.linalg.norm(s[self.numeric_names] - e[self.numeric_names])
            cat_dist = 0
            for f in self.categorical_names:
                if s[f] != e[f]:
                    cat_dist += 1

            return num_dist * (len(self.numeric_names)/len(self.column_names_X)) + cat_dist * (len(self.categorical_names)/len(self.column_names_X))
        else:
            # TODO: check hereeeee
            t = cdist(self.encode(s.to_frame().T).values.tolist(), self.encode(e.to_frame().T).values.tolist(), metric=self.dist)[0][0]
            return t


    def calculate_plausibility(self, exp_df: pd.DataFrame, mode: str) -> float:
        """
        Calculates average plausibility score for provided samples and their explanations.
        :param exp_df: Explanations of samples (pd.DataFrame)
        :param mode: Explanation mode, can be '1to1' or '1toN' (str)
        :return: Average plausibility score (float).
        """
        if self.model is None or self.data is None:
            return '-'

        def plausibility(e: pd.Series) -> float:
            """
            Calculates plausibility of an explanation.
            dist(e, NLN(e)) / dist(NLN(e), NUN(NLN(e)))
            :param e: An explanation of s (pd.Series)
            :return: Plausibility score (float)
            """
            nln_e = self.find_NLN(e)
            e_enc = self.encode(e.drop(self.label).to_frame().T).iloc[0]
            nln_ec = nln_e.copy()
            nln_ec[self.label] = self.model.predict([nln_e])[0]

            a = self.distance(e_enc, nln_e)
            b = self.distance(nln_e, self.find_NUN(nln_ec))

            return (1 if b==0 else a/b)

        pls = 0

        if mode == '1to1':
            for i in range(self.s_count):
                pls += plausibility(exp_df.iloc[i])

        else:
            for i in range(self.s_count):
                temp_i_exp = exp_df[exp_df['instance'] == i ].drop(['instance'], axis=1)
                for j in range(len(temp_i_exp)):
                    pls += plausibility(temp_i_exp.iloc[j])

        return round((pls / len(exp_df)), 3)






    def calculate_sparsity(self, exp_df: pd.DataFrame, mode: str) -> float:
        """
        Calculates average Sparsity score for provided samples and their explanations.
        :param exp_df: Explanations of samples (pd.DataFrame)
        :param mode: Explanation mode, can be '1to1' or '1toN' (str)
        :return: Average sparsity score (float).
        """
        cum_spar = 0
        exp_df = exp_df.drop([self.label], axis=1)

        if mode == '1to1':
            for i in range(self.s_count):
                cum_spar += self.sparsity(self.samples_X.iloc[i], exp_df.iloc[i])

        else:
            for i in range(self.s_count):
                temp_i_exp = exp_df[exp_df['instance'] == i].drop(['instance'], axis=1)
                for j in range(len(temp_i_exp)):
                    cum_spar += self.distance_gower(self.samples_X.iloc[i:i+1], temp_i_exp.iloc[j:j+1])

        return round((cum_spar / len(exp_df)),3)

    def sparsity(self, s: pd.Series, e: pd.Series) -> float:
        """
        Calculates sparsity between s and e. (# corrupted features / # features)
        :param s: Sample to explain (pd.Series)
        :param e: An explanation of s (pd.Series)
        :return: Sparsity score (float)
        """
        cnt = 0
        for f in self.column_names_X:
            if s[f] != e[f]:
                cnt += 1
        return cnt / len(self.column_names_X)

    def calculate_exp_count(self, exp_df: pd.DataFrame, mode: str) -> float:
        """
        Calculates average count of explanations for provided samples.
        :param exp_df: Explanations of samples (pd.DataFrame)
        :param mode: Explanation mode, can be '1to1' or '1toN' (str)
        :return: Average explanation count (float).
        """
        return round((len(exp_df) / self.s_count), 3)

    def calculate_diversity(self, exp_df: pd.DataFrame, mode: str) -> float:
        """
        Calculates average diversity for provided samples and their explanations.
        :param exp_df: Explanations of samples (pd.DataFrame)
        :param mode: Explanation mode, can be '1to1' or '1toN' (str)
        :return: Average diversity score (float).
        """
        diversity = 0
        for i in range(self.s_count):
            temp_i_exp = exp_df[exp_df['instance'] == i].drop(['instance',self.label], axis=1)
            # TODO: double check abs()
            diversity += abs(np.linalg.det(gower.gower_matrix(temp_i_exp)))
        return round(diversity/self.s_count,3)

    def calculate_diversity_lcc(self, exp_df: pd.DataFrame, mode: str) -> float:
        """
        Calculates average diversity considering hit classes for provided samples and their explanations.
        Uses calculate_diversity(). (uses coefficient #of hits on classes / # of classes)
        :param exp_df: Explanations of samples (pd.DataFrame)
        :param mode: Explanation mode, can be '1to1' or '1toN' (str)
        :return: Average diversity score (float).
        """
        diversity = self.calculate_diversity(exp_df, mode)
        diversity_lcc = 0
        for i in range(self.s_count):
            temp_i_exp = exp_df[exp_df['instance'] == i].drop(['instance'], axis=1)
            diversity_lcc += len(np.unique(temp_i_exp[self.label].values))
        diversity_lcc = diversity_lcc / ((self.num_label - 1) * self.s_count)
        return diversity_lcc * diversity

    def constraint_violation(self, exp_df: pd.DataFrame, mode: str):
        """
        Calculates average constraint violation score for provided samples and their explanations.
        :param exp_df: Explanations of samples (pd.DataFrame)
        :param mode: Explanation mode, can be '1to1' or '1toN' (str)
        :return: Average constraint violation score distance (float).
        """
        if self.constraints is None or []:
            return '-'

        def violation(s: pd.Series, e: pd.Series) -> int:
            for f in self.constraints:
                if s[f] != e[f]:
                    return 1
            return 0


        cv = 0
        exp_df = exp_df.drop([self.label], axis=1)

        if mode == '1to1':
            for i in range(self.s_count):
                cv += violation(self.samples_X.iloc[ i ], exp_df.iloc[ i ])

        else:
            for i in range(self.s_count):
                temp_i_exp = exp_df[ exp_df['instance'] == i ].drop(['instance'], axis=1)
                for j in range(len(temp_i_exp)):
                    cv += violation(self.samples_X.iloc[i], temp_i_exp.iloc[ j ])

        return round((cv / len(exp_df)), 3)



    def calculate_kNLN_distance(self, exp_df: pd.DataFrame, mode: str):
        """
        Calculates average kNLN distance for provided samples and their explanations.
        :param exp_df: Explanations of samples (pd.DataFrame)
        :param mode: Explanation mode, can be '1to1' or '1toN' (str)
        :return: Average  kNLN distance (float).
        """
        if self.data is None:
            return '-'

        if mode == '1toN':
            exp_df = exp_df.drop(['instance'], axis=1)
        exp_df_X = self.encode(exp_df.drop([self.label], axis=1))

        distance_l = []

        for i in range(len(exp_df)):
            temp_X = self.data_enc[self.data[self.label] == exp_df.iloc[i][self.label]].drop([self.label], axis=1)
            kNN_model = self.kNN_train(self.knn, temp_X)
            distance_l.extend(self.kNN(kNN_model, exp_df_X.iloc[i], True))

        return round(np.mean(distance_l),3)


    def calculate_yNN(self, exp_df: pd.DataFrame, mode: str):
        """
        Calculates average yNN score for provided samples and their explanations.
        :param exp_df: Explanations of samples (pd.DataFrame)
        :param mode: Explanation mode, can be '1to1' or '1toN' (str)
        :return: Average  yNN score (float).
        """
        if self.model is None or self.data is None:
            return '-'

        if mode == '1toN':
            exp_df = exp_df.drop(['instance'], axis=1)

        exp_df_X_enc = self.encode(exp_df.drop([self.label], axis=1))
        yNN = []

        for i in range(len(exp_df)):
            indices = self.kNN(self.kNN_model, exp_df_X_enc.iloc[i], self.knn, False)

            for k in indices:
                yNN.append(int(self.model.predict(self.data_X_enc.iloc[k].values.reshape(1, -1)) == exp_df[self.label][i]))

        return round(np.mean(yNN), 3)


    def calculate_feasibility(self, exp_df: pd.DataFrame, mode: str):
        """
        Calculates average feasibility score for provided samples and their explanations.
        :param exp_df: Explanations of samples (pd.DataFrame)
        :param mode: Explanation mode, can be '1to1' or '1toN' (str)
        :return: Average feasibility score (float).
        """
        if self.data is None:
            return '-'

        if mode == '1toN':
            exp_df = exp_df.drop(['instance'], axis=1)
        exp_df_X = self.encode(exp_df.drop([self.label], axis=1))

        distance_l = []

        for i in range(len(exp_df)):
            distance_l.extend(self.kNN(self.kNN_model, exp_df_X.iloc[i], self.knn, True))

        return round(np.mean(distance_l), 3)


    def find_NUN(self, s: pd.Series) -> pd.Series:
            """
            Finds Nearest Unlike Neighbor (NUN) of s
            :param s: a sample (pd.Series)
            :return: NUN of s (Series)
            """
            temp_X = self.data_X_enc[self.data[self.label] != s[self.label]]

            NLN = self.kNN_train(1,temp_X)

            s = self.encode(s.drop([self.label]).to_frame().T)

            ind = self.kNN(NLN, s, 1, False)[0]

            return temp_X.iloc[ind]

    def find_NLN(self, s: pd.Series) -> pd.Series:
            """
            Finds Nearest Like Neighbor (NLN) of s
            :param s: a sample (pd.Series)
            :return: NLN of s (Series)
            """
            temp_X = self.data_X_enc[self.data[self.label] == s[self.label]]

            NLN = self.kNN_train(1,temp_X)

            s = self.encode(s.drop([self.label]).to_frame().T)

            ind = self.kNN(NLN, s, 1, False)[0]

            return temp_X.iloc[ind]


    def calculate_relative_dist(self, exp_df: pd.DataFrame, mode: str):
        """
        Calculates average relative distance for provided samples and their explanations.
        :param exp_df: Explanations of samples (pd.DataFrame)
        :param mode: Explanation mode, can be '1to1' or '1toN' (str)
        :return: Average relative distance (float) or '-' (str) when background data is not provided.
        """

        def relative_dist(s: pd.Series, e: pd.Series) -> float:
            """
            Calculate relative distance by calculating ratio of dist(s,e)/dist(s,nun(s))
            :param s: A sample to explain (pd.Series)
            :param e: An explanation of s (pd.Series)
            :return: Relative distance of s and e (float)
            """
            nun = self.find_NUN(s)
            s = s.drop([self.label])
            return self.distance(s,e) / self.distance(s,nun)


        if self.data is None:
            return '-'

        cum_rd = 0

        exp_df = exp_df.drop([self.label], axis=1)

        if mode == '1to1':
            for i in range(self.s_count):
                cum_rd += relative_dist(self.samples.iloc[i], exp_df.iloc[i])

        else:
            for i in range(self.s_count):
                temp_i_exp = exp_df[exp_df['instance']==i].drop(['instance'], axis=1)
                for j in range(len(temp_i_exp)):
                    cum_rd += relative_dist(self.samples.iloc[i], temp_i_exp.iloc[j])

        return round((cum_rd / len(exp_df)),3)




    def calculate_redundancy(self, exp_df: pd.DataFrame, mode: str):
        """
        Calculates average redundancy for provided samples and their explanations.
        :param exp_df: Explanations of samples (pd.DataFrame)
        :param mode: Explanation mode, can be '1to1' or '1toN' (str)
        :return: Average redundancy (float) or '-' (str) when model or background data are not provided.
        """
        if self.model is None or self.data is None:
            return '-'

        samples_enc = self.encode(self.samples_X).reindex()
        samples_enc[self.label] = self.samples[self.label]

        red_cnt = []

        if mode == '1to1':
            temp_exp = self.encode(exp_df.drop([self.label], axis=1))
            temp_exp[self.label] = exp_df[self.label]
            for i in range(self.s_count):
                red_cnt.append(self.redundancy(samples_enc.iloc[i], temp_exp.iloc[i]))
        else:
            temp_exp = self.encode(exp_df.drop(['instance',self.label], axis=1))
            temp_exp[self.label] = exp_df[self.label]
            for i in range(self.s_count):
                temp_i_exp = temp_exp[exp_df['instance']==i]
                for j in range(len(temp_i_exp)):
                    red_cnt.append(self.redundancy(samples_enc.iloc[i], temp_i_exp.iloc[j]))

        return round(np.mean(red_cnt),3)


    def redundancy(self, s: pd.Series, e: pd.Series) -> int:
        """
        Calculates redundancy between s and e.
        :param s: A sample explain (pd.Series)
        :param e: An explanation of s (pd.Series)
        :return: redundancy score (int)
        """
        redundancy = 0
        e_label = e[self.label]
        s, e = s.drop(labels=[self.label]).values, e.drop(labels=[self.label]).values

        for col_idx in range(len(e)):
            # if feature is changed
            if s[col_idx] != e[col_idx]:
                temp_cf = np.copy(e)
                temp_cf[col_idx] = s[col_idx]
                # see if change is needed to flip the label
                temp_pred = np.argmax(
                    self.model.predict_proba(temp_cf.reshape((1, -1)))
                )
                if temp_pred == e_label:
                    redundancy += 1
        return redundancy

