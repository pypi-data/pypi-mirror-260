import logging
import subprocess
from itertools import chain
from typing import List, Optional, Tuple, Union
import pathlib
import matplotlib.backends.backend_pdf
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import tmtoolkit
from gensim import corpora, matutils, utils
from gensim.models import basemodel
from gensim.utils import check_output, revdict
from scipy import sparse
import math
import joblib
import ray
import anndata


def loglikelihood(nzw, ndz, alpha, eta):
    D = ndz.shape[0]
    n_topics = ndz.shape[1]
    vocab_size = nzw.shape[1]

    const_prior = (n_topics * math.lgamma(alpha) - math.lgamma(alpha * n_topics)) * D
    const_ll = (
        vocab_size * math.lgamma(eta) - math.lgamma(eta * vocab_size)
    ) * n_topics

    # calculate log p(w|z)
    topic_ll = 0
    for k in range(n_topics):
        sum = eta * vocab_size
        for w in range(vocab_size):
            if nzw[k, w] > 0:
                topic_ll = math.lgamma(nzw[k, w] + eta)
                sum += nzw[k, w]
        topic_ll -= math.lgamma(sum)

    # calculate log p(z)
    doc_ll = 0
    for d in range(D):
        sum = alpha * n_topics
        for k in range(n_topics):
            if ndz[d, k] > 0:
                doc_ll = math.lgamma(ndz[d, k] + alpha)
                sum += ndz[d, k]
        doc_ll -= math.lgamma(sum)

    ll = doc_ll - const_prior + topic_ll - const_ll
    return ll


def convert_input(corpus, id2word, output_dir):
    """
    Convert corpus to Mallet format and save it to a temporary text file.

    Parameters
    ----------
    corpus : iterable of iterable of (int, int)
    Collection of texts in BoW format.
    infer : bool, optional
    serialize_corpus : bool, optional
    """
    output_dir = pathlib.Path(output_dir)
    txt_path = output_dir / "corpus.txt"
    mallet_path = output_dir / "corpus.mallet"
    with utils.open(txt_path, "wb") as fout:
        for docno, doc in enumerate(corpus):
            tokens = chain.from_iterable(
                [id2word[tokenid]] * int(cnt) for tokenid, cnt in doc
            )
            fout.write(utils.to_utf8("%s 0 %s\n" % (docno, " ".join(tokens))))

    cmd = (
        "mallet import-file --preserve-case --keep-sequence "
        '--remove-stopwords --token-regex "\\S+" --input %s --output %s'
    )
    cmd = cmd % (txt_path, mallet_path)
    check_output(args=cmd, shell=True)
    txt_path.unlink()

    # dump id2word to a file
    id2word_path = output_dir / "id2word"
    joblib.dump(id2word, id2word_path)
    return mallet_path, id2word_path


class CistopicLDAModel:
    """
    cisTopic LDA model class

    :class:`cistopicLdaModel` contains model quality metrics (model coherence (adaptation from Mimno et al., 2011), log-likelihood (Griffiths and Steyvers, 2004), density-based (Cao Juan et al., 2009) and divergence-based (Arun et al., 2010)), topic quality metrics (coherence, marginal distribution and total number of assignments), cell-topic and topic-region distribution, model parameters and model dimensions.

    Parameters
    ----------
    metrics: pd.DataFrame
        :class:`pd.DataFrame` containing model quality metrics, including model coherence (adaptation from Mimno et al., 2011), log-likelihood and density and divergence-based methods (Cao Juan et al., 2009; Arun et al., 2010).
    coherence: pd.DataFrame
        :class:`pd.DataFrame` containing the coherence of each topic (Mimno et al., 2011).
    marginal_distribution: pd.DataFrame
        :class:`pd.DataFrame` containing the marginal distribution for each topic. It can be interpreted as the importance of each topic for the whole corpus.
    topic_ass: pd.DataFrame
        :class:`pd.DataFrame` containing the total number of assignments per topic.
    cell_topic: pd.DataFrame
        :class:`pd.DataFrame` containing the topic cell distributions, with cells as columns, topics as rows and the probability of each topic in each cell as values.
    topic_region: pd.DataFrame
        :class:`pd.DataFrame` containing the topic cell distributions, with topics as columns, regions as rows and the probability of each region in each topic as values.
    parameters: pd.DataFrame
        :class:`pd.DataFrame` containing parameters used for the model.
    n_cells: int
        Number of cells in the model.https://www.google.com/maps/place/The+Home+Depot/data=!4m7!3m6!1s0x89e378259073c585:0xf1c58d25004b2b2d!8m2!3d42.3620232!4d-71.1560237!16s%2Fg%2F1tp1ztzr!19sChIJhcVzkCV444kRLStLACWNxfE?authuser=0&hl=en&rclk=1
    n_regions: int
        Number of regions in the model.
    n_topic: int
        Number of topics in the model.

    References
    ----------
    Mimno, D., Wallach, H., Talley, E., Leenders, M., & McCallum, A. (2011). Optimizing semantic coherence in topic models. In Proceedings of the 2011 Conference on Empirical Methods in Natural Language Processing (pp. 262-272).

    Griffiths, T. L., & Steyvers, M. (2004). Finding scientific topics. Proceedings of the National academy of Sciences, 101(suppl 1), 5228-5235.

    Cao, J., Xia, T., Li, J., Zhang, Y., & Tang, S. (2009). A density-based method for adaptive LDA model selection. Neurocomputing, 72(7-9), 1775-1781.

    Arun, R., Suresh, V., Madhavan, C. V., & Murthy, M. N. (2010). On finding the natural number of topics with latent dirichlet allocation: Some observations. In Pacific-Asia conference on knowledge discovery and data mining (pp. 391-402). Springer, Berlin, Heidelberg.
    """

    def __init__(
        self,
        metrics: pd.DataFrame,
        coherence: pd.DataFrame,
        marg_topic: pd.DataFrame,
        topic_ass: pd.DataFrame,
        cell_topic: pd.DataFrame,
        topic_region: pd.DataFrame,
        parameters: pd.DataFrame,
    ):
        self.metrics = metrics
        self.coherence = coherence
        self.marg_topic = marg_topic
        self.topic_ass = topic_ass
        self.cell_topic = cell_topic
        self.cell_topic_harmony = []
        self.topic_region = topic_region
        self.parameters = parameters
        self.n_cells = cell_topic.shape[1]
        self.n_regions = topic_region.shape[0]
        self.n_topic = cell_topic.shape[0]

    def __str__(self):
        descr = f"CistopicLDAModel with {self.n_topic} topics and n_cells × n_regions = {self.n_cells} × {self.n_regions}"
        return descr


class LDAMallet(utils.SaveLoad, basemodel.BaseTopicModel):
    def __init__(
        self,
        num_topics: int,
        corpus_mallet_path: str,
        id2word_path: str,
        output_dir: str,
        alpha: Optional[float] = 50,
        eta: Optional[float] = 0.1,
        n_cpu: Optional[int] = 1,
        optimize_interval: Optional[int] = 0,
        iterations: Optional[int] = 150,
        topic_threshold: Optional[float] = 0.0,
        random_seed: Optional[int] = 555,
    ):
        """
        Wrapper class to run LDA models with Mallet.

        This class has been adapted from gensim (https://github.com/RaRe-Technologies/gensim/blob/27bbb7015dc6bbe02e00bb1853e7952ac13e7fe0/gensim/models/wrappers/ldamallet.py).

        Parameters
        ----------
        num_topics: int
            The number of topics to use in the model.
        corpus_mallet_path: str
            Path to the corpus in Mallet format.
        id2word_path: str
            Path to the id2word dictionary.
        output_dir: str
            Path to save the model.
        alpha: float, optional
            alpha value for mallet train-topics. Default: 50.
        eta: float, optional
            beta value for mallet train-topics. Default: 0.1.
        n_cpu : int, optional
            Number of threads that will be used for training. Default: 1.
        optimize_interval : int, optional
            Optimize hyperparameters every `optimize_interval` iterations (sometimes leads to Java exception 0 to switch off hyperparameter optimization). Default: 0.
        iterations : int, optional
            Number of training iterations. Default: 150.
        topic_threshold : float, optional
            Threshold of the probability above which we consider a topic. Default: 0.0.
        random_seed: int, optional
            Random seed to ensure consistent results, if 0 - use system clock. Default: 555.
        """
        self.corpus_mallet_path = corpus_mallet_path
        self.id2word_path = id2word_path
        self.id2word = joblib.load(id2word_path)

        self.num_terms = 0 if not self.id2word else 1 + max(self.id2word.keys())
        if self.num_terms == 0:
            raise ValueError("Cannot compute LDA over an empty collection (no terms)")

        self.num_topics = num_topics

        self.topic_threshold = topic_threshold
        self.alpha = alpha
        self.eta = eta

        # get temp_dir with prefix
        self.n_cpu = n_cpu
        self.optimize_interval = optimize_interval
        self.iterations = iterations
        self.random_seed = random_seed

        # path
        self.output_dir = pathlib.Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.state_path = self.output_dir / "state.mallet.gz"
        self.doctopics_path = self.output_dir / "doctopics.txt"
        self.inferencer_path = self.output_dir / "inferencer.mallet"
        self.topickeys_path = self.output_dir / "topickeys.txt"

        self.train()

    def train(self):
        """
        Train Mallet LDA.

        Parameters
        ----------
        corpus : iterable of iterable of (int, int)
            Corpus in BoW format
        reuse_corpus: bool, optional
            Whether to reuse the mallet corpus in the tmp directory. Default: False
        """
        cmd = (
            "mallet train-topics --input %s --num-topics %s  --alpha %s --beta %s --optimize-interval %s "
            "--num-threads %s --output-state %s --output-doc-topics %s --output-topic-keys %s "
            "--num-iterations %s --inferencer-filename %s --doc-topics-threshold %s  --random-seed %s"
        )

        cmd = cmd % (
            self.corpus_mallet_path,
            self.num_topics,
            self.alpha,
            self.eta,
            self.optimize_interval,
            int(self.n_cpu * 1.5),
            self.state_path,
            self.doctopics_path,
            self.topickeys_path,
            self.iterations,
            self.inferencer_path,
            self.topic_threshold,
            str(self.random_seed),
        )
        cmd = cmd.split()
        try:
            subprocess.check_output(args=cmd, shell=False, stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError as e:
            raise RuntimeError(
                "command '{}' return with error (code {}): {}".format(
                    e.cmd, e.returncode, e.output
                )
            )
        self.word_topics = self.load_word_topics()
        self.wordtopics = self.word_topics

    def load_word_topics(self):
        """
        Load words X topics matrix from :meth:`gensim.models.wrappers.LDAMallet.LDAMallet.fstate` file.

        Returns
        -------
        np.ndarray
            Matrix words X topics.
        """
        logger = logging.getLogger("LDAMalletWrapper")
        logger.info("loading assigned topics from %s", self.state_path)
        word_topics = np.zeros((self.num_topics, self.num_terms), dtype=np.float64)
        if hasattr(self.id2word, "token2id"):
            word2id = self.id2word.token2id
        else:
            word2id = revdict(self.id2word)

        with utils.open(self.state_path, "rb") as fin:
            _ = next(fin)  # header
            self.alpha = np.fromiter(next(fin).split()[2:], dtype=float)
            assert (
                len(self.alpha) == self.num_topics
            ), "Mismatch between MALLET vs. requested topics"
            _ = next(fin)  # noqa:F841 beta
            for _, line in enumerate(fin):
                line = utils.to_unicode(line)
                *_, token, topic = line.split(" ")
                if token not in word2id:
                    continue
                tokenid = word2id[token]
                word_topics[int(topic), tokenid] += 1.0
        return word_topics

    def get_topics(self):
        """
        Get topics X words matrix.

        Returns
        -------
        np.ndarray
            Topics X words matrix, shape `num_topics` x `vocabulary_size`.
        """
        topics = self.word_topics
        return topics / topics.sum(axis=1)[:, None]


def run_lda_mallet(
    data: Union[anndata.AnnData, pd.DataFrame],
    output_dir,
    n_topics: List[int],
    n_iter: Optional[int] = 500,
    random_state: Optional[int] = 555,
    alpha: Optional[float] = 50,
    eta: Optional[float] = 0.1,
    top_topics_coh: Optional[int] = 5,
    mallet_cpu = 4,
):
    """
    Run Latent Dirichlet Allocation per model as implemented in Mallet (McCallum, 2002).

    Parameters
    ----------
    data: Union[anndata.AnnData, pd.DataFrame]
        Data matrix containing cells as rows and regions as columns.
        If an anndata.AnnData is provided, the data matrix will be extracted from data.X.T.
        If a pd.DataFrame is provided, the data matrix will be extracted from data.values.T.
    n_topics: list of int
        A list containing the number of topics to use in each model.
    n_iter: int, optional
        Number of iterations for which the Gibbs sampler will be run. Default: 150.
    random_state: int, optional
        Random seed to initialize the models. Default: 555.
    alpha: float, optional
        Scalar value indicating the symmetric Dirichlet hyperparameter for topic proportions. Default: 50.
    eta: float, optional
        Scalar value indicating the symmetric Dirichlet hyperparameter for topic multinomials. Default: 0.1.
    top_topics_coh: int, optional
        Number of topics to use to calculate the model coherence. For each model,
        the coherence will be calculated as the average of the top coherence values. Default: 5.
    mallet_cpu: int, optional
        Number of threads for each malles train-topics call. Default: 4.

    Return
    ------
    list of :class:`CistopicLDAModel`
        A list with cisTopic LDA models.

    References
    ----------
    McCallum, A. K. (2002). Mallet: A machine learning for language toolkit. http://mallet.cs.umass.edu.
    """
    output_dir = pathlib.Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # binary_matrix is a matrix containing cells as columns and regions as rows, following the cisTopic format
    if isinstance(data, anndata.AnnData):
        binary_matrix = data.X.T
        cell_names = data.obs_names
        region_names = data.var_names
    elif isinstance(data, pd.DataFrame):
        binary_matrix = data.values.T
        cell_names = data.index
        region_names = data.columns
    else:
        raise ValueError("data has to be an anndata.AnnData or a pd.DataFrame")

    if isinstance(binary_matrix, np.ndarray):
        binary_matrix = sparse.csc_matrix(binary_matrix)
    elif sparse.issparse(binary_matrix):
        binary_matrix = binary_matrix.tocsc()
    else:
        raise ValueError(
            "binary_matrix has to be a numpy.ndarray or a sparse.csr_matrix"
        )

    corpus = matutils.Sparse2Corpus(binary_matrix)
    names_dict = {x: str(x) for x in range(len(region_names))}
    id2word = corpora.Dictionary.from_corpus(corpus, names_dict)
    corpus_mallet_path, id2word_path = convert_input(
        corpus=corpus, id2word=id2word, output_dir=output_dir
    )

    @ray.remote(num_cpus=mallet_cpu)
    def _remote_run_cgs_model_mallet(*args, kwargs):
        return run_cgs_model_mallet(*args, **kwargs)

    # save the corpus to disk and call mallet in parallel
    binary_matrix_remote = ray.put(binary_matrix)
    futures = [
        _remote_run_cgs_model_mallet.remote(
            binary_matrix=binary_matrix_remote,
            corpus_mallet_path=corpus_mallet_path,
            id2word_path=id2word_path,
            output_dir=output_dir / f"model{n_topic}",
            n_topics=n_topic,
            cell_names=cell_names,
            region_names=region_names,
            n_iter=n_iter,
            random_state=random_state,
            alpha=alpha,
            eta=eta,
            top_topics_coh=top_topics_coh,
            cpu=mallet_cpu,
        )
        for n_topic in n_topics
    ]
    model_list = ray.get(futures)

    # delete mallet and id2word files
    corpus_mallet_path.unlink()
    id2word_path.unlink()
    return model_list

def run_cgs_model_mallet(
    binary_matrix: sparse.csr_matrix,
    corpus_mallet_path: str,
    id2word_path: str,
    output_dir: str,
    n_topics: List[int],
    cell_names: List[str],
    region_names: List[str],
    n_iter: Optional[int] = 500,
    random_state: Optional[int] = 555,
    alpha: Optional[float] = 50,
    eta: Optional[float] = 0.1,
    top_topics_coh: Optional[int] = 5,
    cpu=4,
):
    """
    Run Latent Dirichlet Allocation in a model as implemented in Mallet (McCallum, 2002).

    Parameters
    ----------
    binary_matrix: sparse.csr_matrix
        Binary sparse matrix containing cells as columns, regions as rows, and 1 if a regions is considered accesible on a cell (otherwise, 0).
    corpus_mallet_path: str
        Path to the corpus in Mallet format.
    id2word_path: str
        Path to the id2word dictionary.
    output_dir: str
        Path to save the model.
    n_topics: list of int
        A list containing the number of topics to use in each model.
    cell_names: list of str
        List containing cell names as ordered in the binary matrix columns.
    region_names: list of str
        List containing region names as ordered in the binary matrix rows.
    n_iter: int, optional
        Number of iterations for which the Gibbs sampler will be run. Default: 150.
    random_state: int, optional
        Random seed to initialize the models. Default: 555.
    alpha: float, optional
        Scalar value indicating the symmetric Dirichlet hyperparameter for topic proportions. Default: 50.
    eta: float, optional
        Scalar value indicating the symmetric Dirichlet hyperparameter for topic multinomials. Default: 0.1.
    top_topics_coh: int, optional
        Number of topics to use to calculate the model coherence. For each model, the coherence will be calculated as the average of the top coherence values. Default: 5.
    cpu: int, optional
        Number of threads that will be used for training. Default: 4.
            
    Return
    ------
    CistopicLDAModel
        A cisTopic LDA model.

    References
    ----------
    McCallum, A. K. (2002). Mallet: A machine learning for language toolkit. http://mallet.cs.umass.edu.
    """
    output_dir = pathlib.Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Running model
    model = LDAMallet(
        num_topics=n_topics,
        corpus_mallet_path=corpus_mallet_path,
        id2word_path=id2word_path,
        output_dir=output_dir,
        alpha=alpha,
        eta=eta,
        n_cpu=cpu,
        optimize_interval=0,
        iterations=n_iter,
        topic_threshold=0.0,
        random_seed=random_state,
    )

    # Get distributions
    topic_word = model.get_topics()
    doc_topic = (
        pd.read_csv(model.doctopics_path, header=None, sep="\t").iloc[:, 2:].to_numpy()
    )

    # Model evaluation
    cell_cov = np.asarray(binary_matrix.sum(axis=0)).astype(float)
    arun_2010 = tmtoolkit.topicmod.evaluate.metric_arun_2010(
        topic_word, doc_topic, cell_cov
    )
    cao_juan_2009 = tmtoolkit.topicmod.evaluate.metric_cao_juan_2009(topic_word)
    mimno_2011 = tmtoolkit.topicmod.evaluate.metric_coherence_mimno_2011(
        topic_word,
        dtm=binary_matrix.transpose(),
        top_n=20,
        eps=1e-12,
        normalize=True,
        return_mean=False,
    )
    topic_word_assig = model.word_topics
    doc_topic_assig = (doc_topic.T * (cell_cov)).T
    ll = loglikelihood(topic_word_assig, doc_topic_assig, alpha, eta)

    # Organize data
    if len(mimno_2011) <= top_topics_coh:
        metrics = pd.DataFrame(
            [arun_2010, cao_juan_2009, np.mean(mimno_2011), ll],
            index=["Arun_2010", "Cao_Juan_2009", "Mimno_2011", "loglikelihood"],
            columns=["Metric"],
        ).transpose()
    else:
        metrics = pd.DataFrame(
            [
                arun_2010,
                cao_juan_2009,
                np.mean(
                    mimno_2011[
                        np.argpartition(mimno_2011, -top_topics_coh)[-top_topics_coh:]
                    ]
                ),
                ll,
            ],
            index=["Arun_2010", "Cao_Juan_2009", "Mimno_2011", "loglikelihood"],
            columns=["Metric"],
        ).transpose()
    coherence = pd.DataFrame(
        [range(1, n_topics + 1), mimno_2011], index=["Topic", "Mimno_2011"]
    ).transpose()
    marg_topic = pd.DataFrame(
        [
            range(1, n_topics + 1),
            tmtoolkit.topicmod.model_stats.marginal_topic_distrib(doc_topic, cell_cov),
        ],
        index=["Topic", "Marg_Topic"],
    ).transpose()
    topic_ass = pd.DataFrame.from_records(
        [
            range(1, n_topics + 1),
            list(chain.from_iterable(model.word_topics.sum(axis=1)[:, None])),
        ],
        index=["Topic", "Assignments"],
    ).transpose()
    cell_topic = pd.DataFrame.from_records(
        doc_topic,
        index=cell_names,
        columns=["Topic" + str(i) for i in range(1, n_topics + 1)],
    ).transpose()
    topic_region = pd.DataFrame.from_records(
        topic_word,
        columns=region_names,
        index=["Topic" + str(i) for i in range(1, n_topics + 1)],
    ).transpose()
    parameters = pd.DataFrame(
        [
            "Mallet",
            n_topics,
            n_iter,
            random_state,
            alpha,
            eta,
            top_topics_coh,
        ],
        index=[
            "package",
            "n_topics",
            "n_iter",
            "random_state",
            "alpha",
            "eta",
            "top_topics_coh",
        ],
        columns=["Parameter"],
    )
    # Create object
    model = CistopicLDAModel(
        metrics, coherence, marg_topic, topic_ass, cell_topic, topic_region, parameters
    )
    # save model
    joblib.dump(model, output_dir / "model.lib")
    return model


def subset_list(target_list, index_list):
    X = list(map(target_list.__getitem__, index_list))
    return X


def evaluate_models(
    models: List["CistopicLDAModel"],
    select_model: Optional[int] = None,
    return_model: Optional[bool] = True,
    metrics: Optional[str] = [
        "Minmo_2011",
        "loglikelihood",
        "Cao_Juan_2009",
        "Arun_2010",
    ],
    min_topics_coh: Optional[int] = 5,
    plot: Optional[bool] = True,
    figsize: Optional[Tuple[float, float]] = (6.4, 4.8),
    plot_metrics: Optional[bool] = False,
    save: Optional[str] = None,
):
    """
    Model selection based on model quality metrics (model coherence (adaptation from Mimno et al., 2011), log-likelihood (Griffiths and Steyvers, 2004), density-based (Cao Juan et al., 2009) and divergence-based (Arun et al., 2010)).

    Parameters
    ----------
    models: list of :class:`CistopicLDAModel`
        A list containing cisTopic LDA models, as returned from run_cgs_models or run_cgs_modelsMallet.
    selected_model: int, optional
        Integer indicating the number of topics of the selected model. If not provided, the best model will be selected automatically based on the model quality metrics. Default: None.
    return_model: bool, optional
        Whether to return the selected model as :class:`CistopicLDAModel`
    metrics: list of str
        Metrics to use for plotting and model selection:
            Minmo_2011: Uses the average model coherence as calculated by Mimno et al (2011). In order to reduce the impact of the number of topics, we calculate the average coherence based on the top selected average values. The better the model, the higher coherence.
            log-likelihood: Uses the log-likelihood in the last iteration as calculated by Griffiths and Steyvers (2004). The better the model, the higher the log-likelihood.
            Arun_2010: Uses a divergence-based metric as in Arun et al (2010) using the topic-region distribution, the cell-topic distribution and the cell coverage. The better the model, the lower the metric.
            Cao_Juan_2009: Uses a density-based metric as in Cao Juan et al (2009) using the topic-region distribution. The better the model, the lower the metric.
        Default: all metrics.
    min_topics_coh: int, optional
        Minimum number of topics on a topic to use its coherence for model selection. Default: 5.
    plot: bool, optional
        Whether to return plot to the console. Default: True.
    figsize: tuple, optional
                Size of the figure. Default: (6.4, 4.8)
    plot_metrics: bool, optional
        Whether to plot metrics independently. Default: False.
    save: str, optional
        Output file to save plot. Default: None.

    Return
    ------
    plot
        Plot with the combined metrics in which the best model should have high values for all metrics (Arun_2010 and Cao_Juan_2011 are inversed).

    References
    ----------
    Mimno, D., Wallach, H., Talley, E., Leenders, M., & McCallum, A. (2011). Optimizing semantic coherence in topic models. In Proceedings of the 2011 Conference on Empirical Methods in Natural Language Processing (pp. 262-272).

    Griffiths, T. L., & Steyvers, M. (2004). Finding scientific topics. Proceedings of the National academy of Sciences, 101(suppl 1), 5228-5235

    Cao, J., Xia, T., Li, J., Zhang, Y., & Tang, S. (2009). A density-based method for adaptive LDA model selection. Neurocomputing, 72(7-9), 1775-1781.

    Arun, R., Suresh, V., Madhavan, C. V., & Murthy, M. N. (2010). On finding the natural number of topics with latent dirichlet allocation: Some observations. In Pacific-Asia conference on knowledge discovery and data mining (pp. 391-402). Springer, Berlin, Heidelberg.
    """
    models = [models[i] for i in np.argsort([m.n_topic for m in models])]
    all_topics = sorted([models[x].n_topic for x in range(0, len(models))])
    metrics_dict = {}
    fig = plt.figure(figsize=figsize)
    if "Minmo_2011" in metrics:
        in_index = [
            i for i in range(len(all_topics)) if all_topics[i] >= min_topics_coh
        ]
    if "Arun_2010" in metrics:
        arun_2010 = [
            models[index].metrics.loc["Metric", "Arun_2010"]
            for index in range(0, len(all_topics))
        ]
        arun_2010_negative = [-x for x in arun_2010]
        arun_2010_rescale = (arun_2010_negative - min(arun_2010_negative)) / (
            max(arun_2010_negative) - min(arun_2010_negative)
        )
        if "Minmo_2011" in metrics:
            metrics_dict["Arun_2010"] = np.array(
                subset_list(arun_2010_rescale, in_index)
            )
        else:
            metrics_dict["Arun_2010"] = arun_2010_rescale
        plt.plot(
            all_topics,
            arun_2010_rescale,
            linestyle="--",
            marker="o",
            label="Inv_Arun_2010",
        )

    if "Cao_Juan_2009" in metrics:
        Cao_Juan_2009 = [
            models[index].metrics.loc["Metric", "Cao_Juan_2009"]
            for index in range(0, len(all_topics))
        ]
        Cao_Juan_2009_negative = [-x for x in Cao_Juan_2009]
        Cao_Juan_2009_rescale = (
            Cao_Juan_2009_negative - min(Cao_Juan_2009_negative)
        ) / (max(Cao_Juan_2009_negative) - min(Cao_Juan_2009_negative))
        if "Minmo_2011" in metrics:
            metrics_dict["Cao_Juan_2009"] = np.array(
                subset_list(Cao_Juan_2009_rescale, in_index)
            )
        else:
            metrics_dict["Cao_Juan_2009"] = Cao_Juan_2009_rescale
        plt.plot(
            all_topics,
            Cao_Juan_2009_rescale,
            linestyle="--",
            marker="o",
            label="Inv_Cao_Juan_2009",
        )

    if "Minmo_2011" in metrics:
        Mimno_2011 = [
            models[index].metrics.loc["Metric", "Mimno_2011"]
            for index in range(0, len(all_topics))
        ]
        Mimno_2011 = subset_list(Mimno_2011, in_index)
        Mimno_2011_all_topics = subset_list(all_topics, in_index)
        Mimno_2011_rescale = (Mimno_2011 - min(Mimno_2011)) / (
            max(Mimno_2011) - min(Mimno_2011)
        )
        metrics_dict["Minmo_2011"] = np.array(Mimno_2011_rescale)
        plt.plot(
            Mimno_2011_all_topics,
            Mimno_2011_rescale,
            linestyle="--",
            marker="o",
            label="Mimno_2011",
        )

    if "loglikelihood" in metrics:
        loglikelihood = [
            models[index].metrics.loc["Metric", "loglikelihood"]
            for index in range(0, len(all_topics))
        ]
        loglikelihood_rescale = (loglikelihood - min(loglikelihood)) / (
            max(loglikelihood) - min(loglikelihood)
        )
        if "Minmo_2011" in metrics:
            metrics_dict["loglikelihood"] = np.array(
                subset_list(loglikelihood_rescale, in_index)
            )
        else:
            metrics_dict["loglikelihood"] = loglikelihood_rescale
        plt.plot(
            all_topics,
            loglikelihood_rescale,
            linestyle="--",
            marker="o",
            label="Loglikelihood",
        )

    if select_model is None:
        combined_metric = sum(metrics_dict.values())
        if "Minmo_2011" in metrics:
            best_model = Mimno_2011_all_topics[
                combined_metric.tolist().index(max(combined_metric))
            ]
        else:
            best_model = all_topics[
                combined_metric.tolist().index(max(combined_metric))
            ]
    else:
        combined_metric = None
        best_model = select_model

    plt.axvline(best_model, linestyle="--", color="grey")
    plt.xlabel("Number of topics\nOptimal number of topics: " + str(best_model))
    plt.ylabel("Rescaled metric")
    plt.legend(bbox_to_anchor=(1.04, 1), loc="upper left")
    if save is not None:
        pdf = matplotlib.backends.backend_pdf.PdfPages(save)
        pdf.savefig(fig, bbox_inches="tight")
    if plot is True:
        plt.show()
    else:
        plt.close(fig)

    if plot_metrics:
        if "Arun_2010" in metrics:
            fig = plt.figure()
            plt.plot(all_topics, arun_2010, linestyle="--", marker="o")
            plt.axvline(best_model, linestyle="--", color="grey")
            plt.title("Arun_2010 - Minimize")
            if save is not None:
                pdf.savefig(fig)
            plt.show()

        if "Cao_Juan_2009" in metrics:
            fig = plt.figure()
            plt.plot(all_topics, Cao_Juan_2009, linestyle="--", marker="o")
            plt.axvline(best_model, linestyle="--", color="grey")
            plt.title("Cao_Juan_2009 - Minimize")
            if save is not None:
                pdf.savefig(fig)
            plt.show()
        if "Minmo_2011" in metrics:
            fig = plt.figure()
            plt.plot(Mimno_2011_all_topics, Mimno_2011, linestyle="--", marker="o")
            plt.axvline(best_model, linestyle="--", color="grey")
            plt.title("Mimno_2011 - Maximize")
            if save is not None:
                pdf.savefig(fig)
            plt.show()

        if "loglikelihood" in metrics:
            fig = plt.figure()
            plt.plot(all_topics, loglikelihood, linestyle="--", marker="o")
            plt.axvline(best_model, linestyle="--", color="grey")
            plt.title("Loglikelihood - Maximize")
            if save is not None:
                pdf.savefig(fig)
            plt.show()

    if save is not None:
        pdf.close()

    if return_model:
        return models[all_topics.index(best_model)]


def _norm_topics(x):
    """
    Smooth topic-region distributions.
    """
    return x * (np.log(x + 1e-100) - np.sum(np.log(x + 1e-100)) / len(x))


def _smooth_topics_f(topic_region):
    """
    Smooth topic-region distributions.

    Parameters
    ---------
    topic_region: `class::pd.DataFrame`
            A pandas dataframe with topic-region distributions (with topics as columns and regions as rows)

    Return
    ---------
    pd.DataFrame
    """
    topic_region_np = np.apply_along_axis(_norm_topics, 1, topic_region.values)
    topic_region = pd.DataFrame(
        topic_region_np, index=topic_region.index, columns=topic_region.columns
    )
    return topic_region


def _threshold_otsu(array, nbins=100):
    """
    Apply Otsu threshold on topic-region distributions [Otsu, 1979].

    Parameters
    ---------
    array: `class::np.array`
            Array containing the region values for the topic to be binarized.
    nbins: int
            Number of bins to use in the binarization histogram

    Return
    ---------
    float
            Binarization threshold.

    Reference
    ---------
    Otsu, N., 1979. A threshold selection method from gray-level histograms. IEEE transactions on systems, man, and
    cybernetics, 9(1), pp.62-66.
    """
    hist, bin_centers = _histogram(array, nbins)
    hist = hist.astype(float)
    # Class probabilities for all possible thresholds
    weight1 = np.cumsum(hist)
    weight2 = np.cumsum(hist[::-1])[::-1]
    # Class means for all possible thresholds
    mean1 = np.cumsum(hist * bin_centers) / weight1
    mean2 = (np.cumsum((hist * bin_centers)[::-1]) / weight2[::-1])[::-1]
    # Clip ends to align class 1 and class 2 variables:
    # The last value of ``weight1``/``mean1`` should pair with zero values in
    # ``weight2``/``mean2``, which do not exist.
    variance12 = weight1[:-1] * weight2[1:] * (mean1[:-1] - mean2[1:]) ** 2
    idx = np.argmax(variance12)
    threshold = bin_centers[:-1][idx]
    return threshold


def _histogram(array, nbins=100):
    """
    Draw histogram from distribution and identify centers.

    Parameters
    ---------
    array: `class::np.array`
            Scores distribution
    nbins: int
            Number of bins to use in the histogram

    Return
    ---------
    float
            Histogram values and bin centers.
    """
    array = array.ravel().flatten()
    hist, bin_edges = np.histogram(array, bins=nbins, range=None)
    bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2.0
    return hist, bin_centers


def binarize_topics(
    topic_dist: pd.DataFrame,
    nbins: Optional[int] = 100,
):
    """
    Binarize topic distributions.

    Parameters
    ---------
    nbins: int, optional
        Number of bins to use in the histogram used for otsu, yen and li thresholding. Default: 100

    Return
    ---------
    dict
        A dictionary containing a pd.DataFrame with the selected regions with region names as indexes and a topic score
        column.

    References
    ---------
    Otsu, N., 1979. A threshold selection method from gray-level histograms. IEEE transactions on systems, man, and
    cybernetics, 9(1), pp.62-66.
    Yen, J.C., Chang, F.J. and Chang, S., 1995. A new criterion for automatic multilevel thresholding. IEEE Transactions on
    Image Processing, 4(3), pp.370-378.
    Li, C.H. and Lee, C.K., 1993. Minimum cross entropy thresholding. Pattern recognition, 26(4), pp.617-625.
    Van de Sande, B., Flerin, C., Davie, K., De Waegeneer, M., Hulselmans, G., Aibar, S., Seurinck, R., Saelens, W., Cannoodt, R.,
    Rouchon, Q. and Verbeiren, T., 2020. A scalable SCENIC workflow for single-cell gene regulatory network analysis. Nature Protocols,
    15(7), pp.2247-2276.
    """
    # smooth topics:
    topic_dist = _smooth_topics_f(topic_dist)

    binarized_topics = {}

    for i in range(topic_dist.shape[1]):
        l = np.asarray(topic_dist.iloc[:, i])
        l_norm = (l - np.min(l)) / np.ptp(l)

        thr = _threshold_otsu(l_norm, nbins=nbins)
        binarized_topics["Topic" + str(i + 1)] = pd.DataFrame(
            topic_dist.iloc[l_norm > thr, i]
        )

    # binary empty df
    binarized_df = pd.DataFrame(
        np.zeros(shape=topic_dist.shape, dtype=bool),
        index=topic_dist.index,
        columns=topic_dist.columns,
    )
    for k, v in binarized_topics.items():
        binarized_df.loc[v.index, k] = True
    return binarized_df
