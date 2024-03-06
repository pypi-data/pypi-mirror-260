"""
Should containe the Gaussian Processes operations


In addition to the feature spaces we should also take into account the average numbers of objects,
e.g. radial number profile (in absolute terms)


"""

import fitsio as fio
import numpy as np
import pandas as pd
import sklearn.neighbors as neighbors
import sklearn.model_selection as modsel
import sklearn.preprocessing as preproc
import sklearn.decomposition as decomp
import copy
import sys
try:
    from collections.abc import Iterable
except ImportError:
    from collections import Iterable
import scipy.interpolate as interp


BADVAL = -9999

ENDIANS = {
    "little": "<",
    "big": ">",
}

import matplotlib as mpl
try:
    import matplotlib.pyplot as plt
except:
    mpl.use("Agg")
    import matplotlib.pyplot as plt

import multiprocessing as mp

from .utils import partition


def get_angle(num, rng):
    angle = rng.uniform(0, np.pi, size=num)
    return angle


def weighted_mean(values, weights):
    average = np.average(values, axis=0, weights=weights)
    return average


def weighted_std(values, weights):
    """
    Return the weighted average and standard deviation.

    values, weights -- Numpy ndarrays with the same shape.
    """
    average = np.average(values, axis=0, weights=weights)
    variance = np.average((values-average)**2, axis=0, weights=weights)
    return np.sqrt(variance)


class BaseContainer(object):

    def __init__(self):
        self.alldata = None
        self.features = None
        self.weights = None

    def construct_features(self, columns, limits=None, logs=None, **kwargs):
        self.columns = columns
        self.limits = limits
        self.logs = logs
        self.features = pd.DataFrame()

        self.inds = np.ones(len(self.alldata), dtype=bool)
        for i, col in enumerate(columns):
            if isinstance(col[1], str):
                res = self.alldata[col[1]]
            else:
                if len(col[1]) == 3:
                    if isinstance(col[1][0], str):
                        col1 = self.alldata[col[1][0]]
                    elif isinstance(col[1][0], (list, tuple)):
                        col1 = self.alldata[col[1][0][0]][:, col[1][0][1]]
                    else:
                        col1 = col[1][0]

                    if isinstance(col[1][1], str):
                        col2 = self.alldata[col[1][1]]
                    elif isinstance(col[1][1], (list, tuple)):
                        col2 = self.alldata[col[1][1][0]][:, col[1][1][1]]
                    else:
                        col2 = col[1][1]

                    if col[1][2] == "-":
                        res = col1 - col2
                    elif col[1][2] == "+":
                        res = col1 + col2
                    elif col[1][2] == "*":
                        res = col1 * col2
                    elif col[1][2] == "/":
                        res = col1 / col2
                    elif col[1][2] == "SQSUM":
                        res = np.sqrt(col1**2. + col2**2.)
                    else:
                        raise KeyError("only + - * / are supported at the moment")

                elif len(col[1]) == 2:
                    res = self.alldata[col[1][0]][:, col[1][1]]
                else:
                    raise KeyError

            self.features[col[0]] = res.astype("float64")
            #
            if limits is not None:
                self.inds &= (self.features[col[0]] > limits[i][0]) & (self.features[col[0]] < limits[i][1])

        self.features = self.features[self.inds]

        try:
            self.weights = self.alldata["WEIGHT"][self.inds]
        except:
            self.weights = pd.Series(data=np.ones(len(self.features)), name="WEIGHT")

        for i, col in enumerate(columns):
            if logs is not None and logs[i]:
              self.features[col[0]] = np.log10(self.features[col[0]])

    def to_dual(self, **kwargs):
        res = DualContainer(self.features.columns, **kwargs)
        res.set_data(self.features, self.weights)
        return res

    def to_kde(self, **kwargs):
        res = KDEContainer(self.features, weights=self.weights)
        return res


class FeatureSpaceContainer(BaseContainer):
    def __init__(self, info):
        """
        This needs to be done first
        """
        BaseContainer.__init__(self)

        self.rcens = info.rcens
        self.redges = info.redges
        self.rareas = info.rareas

        self.survey = info.survey
        self.target = info.target

        self.numprof = info.numprof
        self.samples = info.samples

        self.alldata = pd.concat(self.samples).reset_index(drop=True)

        self.nobj = self.target.nrow

    def surfdens(self, icol=0, scaler=1):
        if self.logs[icol]:
            arr = 10**self.features.values[:, icol]
        else:
            arr = self.features.values[:, icol]
        vals = np.histogram(arr, bins=self.redges, weights=self.weights)[0] / self.nobj / self.rareas * scaler
        return vals

    def downsample(self, nmax=10000, r_key="LOGR", nbins=40, rng=None, **kwargs):
        """Radially balanced downsampling"""

        if rng is None:
            rng = np.random.RandomState()

        rarr = self.features[r_key]
        # rbins = np.sort(rng.uniform(low=rarr.min(), high=rarr.max(), size=nbins+1))
        rbins = np.linspace(rarr.min(), rarr.max(), nbins+1)

        tmp_features = []
        tmp_weights = []
        for i, tmp in enumerate(rbins[:-1]):
            selinds = (self.features[r_key] > rbins[i]) & (self.features[r_key] < rbins[i + 1])
            vals = self.features.loc[selinds]
            ww = self.weights.loc[selinds]

            if len(vals) < nmax:
                tmp_features.append(vals)
                tmp_weights.append(ww)
            else:
                inds = np.arange(len(vals))
                pp = ww / ww.sum()
                chindex = rng.choice(inds, size=nmax, replace=False, p=pp)

                newvals = vals.iloc[chindex]
                newww = ww.iloc[chindex] * len(ww) / nmax

                tmp_features.append(newvals)
                tmp_weights.append(newww)

        features = pd.concat(tmp_features)
        weights = pd.concat(tmp_weights)

        # res = KDEContainer(features.columns, weights=weights)
        res = DualContainer(features.columns, **kwargs)
        res.set_data(features, weights=weights)
        return res


class DeepFeatureContainer(BaseContainer):
    def __init__(self, data):
        BaseContainer.__init__(self)
        self.alldata = data
        self.weights = pd.Series(data=np.ones(len(self.alldata)), name="WEIGHT")

    @classmethod
    def from_file(cls, fname, flagsel=True):

        if ".fit" in fname:
            _deep = fio.read(fname)
        else:
            _deep = pd.read_hdf(fname, key="data").to_records()

        if flagsel:
            inds = _deep["flags"] == 0
            deep = _deep[inds]
        else:
            deep = _deep
        return cls(deep)


class KDEContainer(object):
    _default_subset_sizes = (2000, 5000, 10000)
    _kernel = "tophat"
    _atol = 1e-6
    _rtol = 1e-6
    _breadth_first = False
    _jacobian_matrix = None
    _jacobian_det = None

    def __init__(self, raw_data, weights=None, transform_params=None, seed=None):
        if seed is not None:
            self.rng = np.random.RandomState(seed)
        else:
            self.rng = np.random.RandomState()

        self.data = raw_data
        self.columns = raw_data.columns
        if weights is None:
            self.weights = np.ones(len(raw_data), dtype=float)
        else:
            self.weights = weights.astype(float)
        self.ndim = self.data.shape[1]

    @staticmethod
    def _weight_multiplicator(arr, weights):
        multiplier = np.round(weights)
        newarr = []
        for i in np.arange(len(arr)):
            for j in np.arange(multiplier[i]):
                newarr.append(arr[i])
        newarr = np.vstack(newarr)
        return newarr

    def shuffle(self):
        self.sample(n=None, frac=1.)

    def sample(self, n=None, frac=1.):
        inds = np.arange(len(self.data))

        tab = pd.DataFrame()
        tab["IND"] = inds
        inds = tab.sample(n=n, frac=frac)["IND"].values

        self.data = self.data.iloc[inds].copy().reset_index(drop=True)
        self.weights = self.weights.iloc[inds].copy().reset_index(drop=True)
        # self.xarr = self.xarr.iloc[inds].copy().reset_index(drop=True)
        # self.shape = self.data.shape
    #
    # def set_rmax(self, rmax= 100., rkey="LOGR"):
    #     inds = self.data[rkey] < rmax
    #
        # res = DualContainer(**self.get_meta())
        # res.data = self.data.loc[inds].copy().reset_index(drop=True)
    #     res.weights = self.weights.loc[inds].copy().reset_index(drop=True)
    #     res.xarr = self.xarr.loc[inds].copy().reset_index(drop=True)
    #     res.shape = res.data.shape
    #     return res

    def fit_pca(self):
        """Standardize -> PCA -> Standardize"""

        self.mean1 = weighted_mean(self.data, self.weights)
        _data = self.data - self.mean1
        #
        # Add here a PCA weights pre-burner,
        # draw a subset of 100k rows, then multiplicate them according to weights
        # fit the PCA on theose new rows
        subset = self.select_subset(_data, self.weights, nsample=100000)
        subset = self._weight_multiplicator(subset.values, self.weights)
        self.pca = decomp.PCA()
        self.pca.fit(subset)

        _data = self.pca.transform(_data)
        self.std2 = weighted_std(_data, self.weights)

        rotation_matrix = self.pca.components_
        scale_matrix = np.diag(1. / self.std2)

        # this is the forward transformation from raw data to processed data
        self._jacobian_matrix = np.dot(scale_matrix, rotation_matrix)
        # this is the inverse transformation from processed data to raw data
        self._jacobian_matrix_inv = np.linalg.inv(self._jacobian_matrix)
        # in the KDE we need the Jacobi determinat of the inverse transformation
        self._determinant = np.linalg.det(self._jacobian_matrix_inv)

        self.pca_params = {
            "mean1": self.mean1.copy(),
            "std2": self.std2.copy(),
            "pca": copy.deepcopy(self.pca),
        }

    def pca_transform(self, data):
        _data = data - self.mean1
        _data = self.pca.transform(_data)
        _data /= self.std2
        return _data

    def pca_inverse_transform(self, data):
        _data = data * self.std2
        _data = self.pca.inverse_transform(_data)
        _data = _data + self.mean1
        res = pd.DataFrame(_data, columns=self.columns)
        return res

    def standardize_data(self):
        self.fit_pca()
        self._data = self.pca_transform(self.data)

    def select_subset(self, data, weights, nsample=10000):
        indexes = np.arange(len(data))
        ww = weights / weights.sum()
        inds = self.rng.choice(indexes, size=nsample, p=ww)
        subset = data.iloc[inds]
        return subset

    def construct_kde(self, bandwidth):
        """"""
        self.bandwidth = bandwidth
        self.kde = neighbors.KernelDensity(bandwidth=self.bandwidth, kernel=self._kernel,
                                           atol=self._atol, rtol=self._rtol, breadth_first=self._breadth_first)
        self.kde.fit(self._data, sample_weight=self.weights)

    def random_draw(self, num, rmin=None, rmax=None, rcol="LOGR", mode="data"):
        """draws random samples from KDE maximum radius"""
        _res = self.kde.sample(n_samples=int(num), random_state=self.rng)
        if (rmin is not None) or (rmax is not None):
            if rmin is None:
                rmin = _res.data[rcol].min()

            if rmax is None:
                rmax = _res.data[rcol].max()

            # these are the indexes to replace, not the ones to keep...
            inds = (_res.data[rcol] > rmax) | (_res.data[rcol] < rmin)
            while inds.sum():
                vals = self.kde.sample(n_samples=int(inds.sum()), random_state=self.rng)
                _res[inds, :] = vals
                inds = (_res.data[rcol] > rmax) | (_res.data[rcol] < rmin)

        self.res = self.pca_inverse_transform(_res)
        return self.res

    def score_samples(self, arr):
        """Assuming that arr is in the data format"""

        arr = self.pca_transform(arr)
        res = self.kde.score_samples(arr)
        return res, self._jacobian_det


class GradientKDE(object):
    _stretch_func = []
    _xy_func = []
    _yx_func = []
    settings = None
    def __init__(self, top_scaler=None, rng=None):
        self.top_scaler = top_scaler

        if rng is None:
            self.rng = np.random.RandomState()
        else:
            self.rng = rng

    def set_data(self, data, weights=None):
        self.data = data

        self.weights = weights
        if self.weights is None:
            self.weights = np.ones(len(data))

        if self.top_scaler is None:
            self.top_scaler = {
                "std": self.data.std(axis=0),
                "mean": self.data.mean(axis=0),
            }

        self._top_data = self._standardize(self.data, self.top_scaler)

    def _build_top_kde(self, bandwidth=0.1, kernel="tophat", atol=1e-4, rtol=1e-4, breadth_first=False):
        self.bandwidth = bandwidth
        self.kernel = kernel
        self.atol = atol
        self.rtol = rtol
        self.breadth_first = breadth_first

        self._top_kde = neighbors.KernelDensity(bandwidth=self.bandwidth, atol=self.atol, rtol=self.rtol,
                                           breadth_first=self.breadth_first)
        self._top_kde.fit(self._top_data, sample_weight=self.weights)

    def _build_deep_kde(self):
        self._deep_kde = neighbors.KernelDensity(bandwidth=self.bandwidth, atol=self.atol, rtol=self.rtol,
                                           breadth_first=self.breadth_first)
        self._deep_kde.fit(self._deep_data, sample_weight=self.weights)

    def draw_top_sample(self, nsample=1e6):
        self._top_sample = self._top_kde.sample(n_samples=int(nsample), random_state=self.rng)
        self.top_sample = pd.DataFrame(data=self._top_sample, columns=self.data.columns)
        self.top_sample = self._inverse_standardize(self.top_sample, scaler=self.top_scaler)

    def draw_deep_sample(self, nsample=1e6):
        self._deep_sample_y = self._deep_kde.sample(n_samples=int(nsample), random_state=self.rng)

        self._deep_sample_x = pd.DataFrame()
        columns = list(self._deep_data.columns)
        for i, col in enumerate(columns):
            self._deep_sample_x[col] = self._yx_func[i](self._deep_sample_y[:, i])

        self._deep_sample_x = self._filter_badval(self._deep_sample_x)
        self.deep_sample = self._inverse_standardize(self._deep_sample_x, scaler=self.top_scaler)

    def score(self, sample):

        _deep_sample = self.transform(sample)
        self._deep_log_scores = self._deep_kde.score_samples(_deep_sample.values)

        _jac = self._calc_jacobian(_deep_sample)

        _scores = self._deep_log_scores + np.log(_jac)

        return _scores

    def _calc_jacobian(self, data):
        self.__jac = pd.DataFrame()
        columns = list(self._deep_data.columns)
        for i, col in enumerate(columns):
            self.__jac[col] = 1. / self._dxdy[i](data[col])
        self._tmp = self.__jac

        self._jac = np.abs(np.product(self.__jac.values / self.top_scaler["std"][np.newaxis, :], axis=1))

        # self._jac = np.product(self.__jac.values, axis=1)
        # self._jac = self.__jac.values[:, 0]

        return self._jac

    def transform(self, data):

        _top_data = self._standardize(data, self.top_scaler)

        colnames = list(self.data.columns)
        _deep_data = pd.DataFrame()
        for i, col in enumerate(colnames):
            _deep_data[col] = self._xy_func[i](_top_data[colnames[i]].values)

        return _deep_data

    def inverse_transform(self, deep_data):

        _top_data = pd.DataFrame()
        colnames = list(self.data.columns)
        for i, col in enumerate(colnames):
            _top_data[col] = self._yx_func[i](deep_data[colnames[i]].values)

        _data = self._inverse_standardize(_top_data, self.top_scaler)

        return _data


    def _calc_slices(self, ref_axes=None, nslices=1, nbins=100):
        """Calculates slices"""

        self.ref_axes = ref_axes
        self.nslices = nslices
        self.nbins = nbins
        # pepare slices along reference axes
        self.ref_edges = []
        if self.ref_axes is not None:
            if not isinstance(self.ref_axes, Iterable):
                self.ref_axes = (self.ref_axes,)
            for i, ax in enumerate(self.ref_axes):
                self.ref_edges.append(np.histogram(self._top_sample[:, ax], bins=self.nslices)[1])

        self._slices = []
        self._slices_bin_edges = []
        self._slices_bin_centers = []
        self._ref_in_use = []
        for i in np.arange(self._top_sample.shape[1]):

            col = self._top_sample[:, i]
            cmin = col.min()
            cmax = col.max()
            cbins = np.linspace(cmin, cmax, self.nbins)
            if self.ref_axes is not None:
                _slice = []
                _edge = []
                _cen = []
                _ref = []
                for j, ax in enumerate(self.ref_axes):
                    if i != ax:
                        _ref.append(True)
                        refcol = self._top_sample[:, ax]
                        for k in np.arange(len(self.ref_edges[j]) - 1):
                            ind = (self.ref_edges[j][k] < refcol) & (refcol < self.ref_edges[j][k + 1])
                            vals = col[ind]

                            __slice, __edge = np.histogram(vals, cbins, density=True)
                            _slice.append(__slice)
                            _edge.append(__edge)
                            _cen.append(self._get_bin_cen(__edge))
                    else:
                        _ref.append(False)
                        __slice, __edge = np.histogram(self._top_sample[:, i], cbins, density=True)
                        _slice.append(__slice)
                        _edge.append(__edge)
                        _cen.append(self._get_bin_cen(__edge))

                self._slices.append(_slice)
                self._slices_bin_edges.append(_edge)
                self._slices_bin_centers.append(_cen)
                self._ref_in_use.append(_ref)

            else:
                _slice, _edge = np.histogram(self._top_sample[:, i], cbins, density=True)
                self._slices.append((_slice,))
                self._slices_bin_edges.append((_edge,))
                self._slices_bin_centers.append((self._get_bin_cen(_edge),))
                self._ref_in_use.append((False,))

    def _calc_gradient(self, window_size=None):
        """estimates |f'| along each slice """

        self._gradients = []
        self._gradient_centers = []
        for i, _slice in enumerate(self._slices):
            _grad = []
            _cens = []
            for j, __slice in enumerate(_slice):
                gvals = np.abs(np.diff(__slice))
                if window_size is not None:
                    gvals = self._smooth(gvals, window_size)
                _grad.append(gvals)
                _cens.append((self._slices_bin_centers[i][j][:-1] + np.diff(self._slices_bin_centers[i][j] / 2.)))

            self._gradients.append(_grad)
            self._gradient_centers.append(_cens)

    def _collate_gradients(self, eta=1., tomographic_weights=None):
        self._stretch = []
        self._stretch_centers = []
        self._stretch_func = []
        self.eta = eta

        if tomographic_weights is None:
            if self.ref_axes is not None:
                _tw = []
                for _ in np.arange(len(self.ref_axes)):
                    _tw.append(np.ones(self.nslices))
                self.tomographic_weights = _tw
            else:
                self.tomographic_weights = np.array([1.,])
        else:
            self.tomographic_weights = tomographic_weights

        for i, _grad in enumerate(self._gradients):
            _grad = np.array(_grad).T

            _weigths = []
            if self.ref_axes is not None:
                for j in np.arange(len(self.ref_axes)):
                    if self._ref_in_use[i][j]:
                        _weigths.append(self.tomographic_weights[j])
                    else:
                        _weigths.append([1,])
            else:
                _weigths = np.array([[1.,],])

            _weigths = np.concatenate(_weigths)

            val = np.dot(_grad**2., _weigths[:, np.newaxis]) / _grad.shape[1]

            if np.iterable(self.eta):
                eta = self.eta[i]
            else:
                eta = self.eta
            _stretch = eta * val
            self._stretch.append(_stretch)
            self._stretch_centers.append(self._gradient_centers[i][0])

            xval = self._gradient_centers[i][0]
            yval = _stretch[:, 0]
            self._stretch_func.append(interp.interp1d(xval, yval,
                                                      fill_value=0, bounds_error=False))

    def _calc_deep_data(self, gridpoints=1e4):

        colnames = list(self._top_data.columns)
        self._deep_data = pd.DataFrame()
        self._ycols = []
        self._xcols = []
        self._dydx = []
        self._dxdy = []
        for i in np.arange(self._top_data.shape[1]):
            col = self._top_data[colnames[i]].values
            _xcol = np.linspace(col.min(), col.max(), int(gridpoints))
            self._xcols.append(_xcol)

            x_stretch = self._stretch_func[i](_xcol)

            _ycol = np.zeros(len(_xcol))
            for j in np.arange(len(_xcol)):
                _ycol[j] = _xcol[j] + np.sum(x_stretch[:j])

            func = interp.interp1d(_xcol, _ycol, fill_value=BADVAL, bounds_error=False)
            _tmp_data = func(col)
            _ycol = (_ycol - _tmp_data.mean()) / _tmp_data.std()

            self._ycols.append(_ycol)

            self._xy_func.append(interp.interp1d(_xcol, _ycol, fill_value=BADVAL, bounds_error=False))
            self._yx_func.append(interp.interp1d(_ycol, _xcol, fill_value=BADVAL, bounds_error=False))

            dydx = self._finite_difference(_xcol, _ycol)
            self._dydx.append(interp.interp1d(_xcol, dydx, fill_value=BADVAL, bounds_error=False))

            dxdy = self._finite_difference(_ycol, _xcol)
            self._dxdy.append(interp.interp1d(_ycol, dxdy, fill_value=BADVAL, bounds_error=False))

            self._deep_data[colnames[i]] = self._xy_func[i](self._top_data[colnames[i]].values)

    def build_kde(self, bandwidth=0.1, eta=1., tomographic_weights=None, window_size=5,
                  ref_axes=None, nslices=1, nbins=100, nsample_gradient=1e6,
                  kernel="tophat", atol=1e-4, rtol=1e-4, breadth_first=False, gridpoints=1e4):

        self._build_top_kde(bandwidth=bandwidth, kernel=kernel, atol=atol, rtol=rtol, breadth_first=breadth_first)
        self.draw_top_sample(nsample=nsample_gradient)

        self._calc_slices(ref_axes=ref_axes, nslices=nslices, nbins=nbins)
        self._calc_gradient(window_size=window_size)
        self._collate_gradients(eta=eta, tomographic_weights=tomographic_weights)

        self._calc_deep_data(gridpoints=gridpoints)

        self._build_deep_kde()

    @staticmethod
    def _finite_difference(xcol, ycol):
        derivs = np.zeros(len(xcol))
        for i in np.arange(len(xcol)):
            if i == 0:
                dx = xcol[i + 1] - xcol[i]
                dy = ycol[i + 1] - ycol[i]
                derivs[i] = dy / dx

            elif i == len(ycol) - 1:
                dx = xcol[i] - xcol[i - 1]
                dy = ycol[i] - ycol[i - 1]
                derivs[i] = dy / dx
            else:
                dx = xcol[i + 1] - xcol[i - 1]
                dy = ycol[i + 1] - ycol[i - 1]
                derivs[i] = dy / dx
        return derivs

    @staticmethod
    def _smooth(vals, window_size):
        window = np.ones(window_size)
        window /= window.sum()
        smoothvals = np.convolve(window, vals.copy(), mode="same")
        return smoothvals

    @staticmethod
    def _standardize(data, scaler):
        _data = (data.copy() - scaler["mean"]) / scaler["std"]
        return _data

    @staticmethod
    def _inverse_standardize(data, scaler):
        _data = data.copy() * scaler["std"] + scaler["mean"]
        return _data

    @staticmethod
    def _get_bin_cen(edge):
        cen = edge[:-1] + np.diff(edge) / 2.
        return cen

    @staticmethod
    def _filter_badval(table):
        columns = table.columns
        inds = np.ones(len(table), dtype=bool)
        for i, col in enumerate(columns):
            _ind = np.invert(np.isclose(table[col].values, np.ones(len(table)) * BADVAL))
            inds *= _ind

        return table.copy()[inds]


class DualContainer(object):
    """Contains features in normal and in transformed space"""
    def __init__(self, columns=None, mean=None, sigma=None):
        """
        One column Dataframes can be created by tab[["col"]]
        Parameters
        ----------
        columns
        mean
        sigma
        """
        self.columns = columns
        self.mean = mean
        self.sigma = sigma

    def __getitem__(self, key):
        if self.mode == "xarr":
            return self.xarr[key]
        else:
            return self.data[key]

    def set_mode(self, mode):
        self.mode = mode

    def set_xarr(self, xarr):
        self.xarr = pd.DataFrame(columns=self.columns, data=xarr).reset_index(drop=True)

        self.data = self.xarr * self.sigma + self.mean
        self.weights = pd.Series(np.ones(len(self.data)), name="WEIGHT")
        self.shape = self.data.shape

    def set_data(self, data, weights=None):
        self.columns = data.columns
        self.data = data.reset_index(drop=True)
        self.weights = weights

        if self.weights is None:
            self.weights = pd.Series(np.ones(len(self.data)), name="WEIGHT")
            # self.weights["WEIGHT"] =

        if (self.mean is None) and (self.sigma is None):
            self.mean = np.average(self.data, axis=0, weights=self.weights)
            self.sigma = weighted_std(self.data, weights=self.weights)

        self.xarr = ((self.data - self.mean) / self.sigma)

        self.shape = self.data.shape
        self.mode = "data"

    def transform(self, arr):
        """From Data to Xarr"""

        if not isinstance(arr, pd.DataFrame):
            tab = pd.DataFrame(data=arr, columns=self.columns)
        else:
            tab = arr

        res = (tab - self.mean)/ self.sigma
        return res

    def inverse_transform(self, arr):
        """From Xarr to Data"""

        if not isinstance(arr, pd.DataFrame):
            tab = pd.DataFrame(data=arr, columns=self.columns)
        else:
            tab = arr

        res = tab * self.sigma + self.mean
        return res

    def shuffle(self):
        self.sample(n=None, frac=1.)

    def sample(self, n=None, frac=1.):
        inds = np.arange(len(self.data))

        tab = pd.DataFrame()
        tab["IND"] = inds
        inds = tab.sample(n=n, frac=frac)["IND"].values

        self.data = self.data.iloc[inds].copy().reset_index(drop=True)
        self.weights = self.weights.iloc[inds].copy().reset_index(drop=True)
        self.xarr = self.xarr.iloc[inds].copy().reset_index(drop=True)
        self.shape = self.data.shape

    def set_rmax(self, rmax= 100., rkey="LOGR"):
        inds = self.data[rkey] < rmax

        res = DualContainer(**self.get_meta())
        res.data = self.data.loc[inds].copy().reset_index(drop=True)
        res.weights = self.weights.loc[inds].copy().reset_index(drop=True)
        res.xarr = self.xarr.loc[inds].copy().reset_index(drop=True)
        res.shape = res.data.shape
        return res

    def get_meta(self):
        info = {
            "columns": self.columns,
            "mean": self.mean,
            "sigma": self.sigma,
        }
        return info

    def match_surfdens(self):
        pass


def _add(a, b):
    return a + b

def _subtr(a, b):
    return a - b

_OPERATORS = {
    "+": _add,
    "-": _subtr,
}


class TomographicEyeballer(object):
    def __init__(self, containers, nbins=100, colors=None, labels=None, loc=None):
        self.containers = containers
        self.columns = self.containers[0].columns
        self.nbins = nbins

        self.loc=loc
        self.labels = labels
        self.colors = colors
        if self.colors is None:
            arr = np.linspace(0, 1, len(self.containers))
            self.colors = plt.cm.cool(arr)

    def _get_figure(self):
        num = len(self.columns) - 1
        nrows = int(np.ceil(np.sqrt(num)))
        ncols = int(np.ceil(np.sqrt(num)))
        xsize = 5 * nrows
        ysize = 4 * ncols
        fig, axarr = plt.subplots(nrows=ncols, ncols=nrows, figsize=(xsize, ysize))
        fig.subplots_adjust(wspace=0.3, hspace=0.3)
        faxarr = axarr.flatten()
        for i, ax in enumerate(faxarr):
            #             if i < len(columns):
            #                 faxarr[i].set_title(columns[i])
            if i >= len(self.columns):
                faxarr[i].axis("off")
        return fig, axarr

    def _get_bins(self):
        self.bin_edges = []
        for i, col in enumerate(self.columns):
            xmin = self.containers[0][col].min()
            xmax = self.containers[0][col].max()
            edges = np.linspace(xmin, xmax, self.nbins)
            self.bin_edges.append(edges)

    def plot_marginals(self):
        self._get_bins()
        fig, axarr = self._get_figure()
        faxarr = axarr.flatten()[:len(self.columns)]
        for i, (col, ax) in enumerate(zip(self.columns, faxarr)):
            for j, cont in enumerate(self.containers):

                label = None
                if self.labels is not None:
                    label = self.labels[j]
                ax.hist(cont[col], bins=self.bin_edges[i], density=True, histtype="step",
                        label=label, color=self.colors[j])

            ax.set_xlabel(col)
            ax.set_ylabel("p.d.f")
            ax.grid(ls=":")
            if self.labels is not None:
                ax.legend(loc=self.loc)


class MultiEyeballer(object):
    """
    this needs to be done second
    """
    _radial_splits = np.logspace(np.log10(0.1), np.log10(40), 10)
    _cm_diagrams = (("MAG_R", "COLOR_G_R"), ("MAG_I", "COLOR_R_I"), ("MAG_Z", "COLOR_I_Z"))
    _cc_diagrams = (("COLOR_G_R", "COLOR_R_I"), ("COLOR_R_I", "COLOR_I_Z"))
    _plot_series = ("CC", "CM", "RR")
    _reconstr_mags = {
        "MAG_G": ("COLOR_G_R + COLOR_R_I + MAG_I"),
        "MAG_R": ("COLOR_R_I + MAG_I"),
        "MAG_Z": ("MAG_I - COLOR_I_Z"),
    }

    def __init__(self, container, radial_splits=None, cmap=None):
        """
        Constructs a large set of comparison images

        Density comparisons  and such

        """
        self.container = container
        self.cmap = cmap

        if radial_splits is not None:
            self._radial_splits = radial_splits

    def _get_col(self, label):
        if label in self.container.columns:
            col = self.container[label]
        elif label in self._reconstr_mags:
            tokens = self._reconstr_mags[label].split()
            col = self.container[tokens[0]]
            for i in np.arange(len(tokens) // 2):
                col = _OPERATORS[tokens[i + 1]](col, self.container[tokens[i + 2]])
        else:
            raise KeyError

        return col

    def radial_series(self, label1="MAG_I", label2="COLOR_R_I", rlabel="LOGR",
                      rlog=True, bins=None, fname=None, vmin=1e-3, vmax=None, nbins=60, title=None):

        if rlog:
            rr = 10 ** self.container[rlabel]
        else:
            rr = self.container[rlabel]

        col1 = self._get_col(label1)
        col2 = self._get_col(label2)

        ww = self.container.weights

        if bins is None:
            bins = (np.linspace(col1.min(), col1.max(), nbins),
                    np.linspace(col2.min(), col2.max(), nbins))

        num = len(self._radial_splits) - 1
        nrows = int(np.ceil(np.sqrt(num)))
        ncols = int(np.round(np.sqrt(num)))
        xsize = 4 * nrows
        ysize = 3 * ncols

        fig, axarr = plt.subplots(nrows=ncols, ncols=nrows, figsize=(xsize, ysize))
        faxarr = axarr.flatten()

        if title is not None:
            fig.text(0.125, 0.9, title, fontsize=14)

        for axs in axarr:
            axs[0].set_ylabel(label2)

        for axs in axarr[-1]:
            axs.set_xlabel(label1)

        for i, ax in enumerate(faxarr):
            ind = (rr > self._radial_splits[i]) & (rr < self._radial_splits[i + 1])
            if i == 0 and vmax is None:
                tmp = np.histogram2d(col1[ind], col2[ind], weights=ww[ind], bins=bins, normed=True)[0]
                vmax = 1 * tmp.max()
            ax.hist2d(col1[ind], col2[ind], weights=ww[ind], bins=bins, cmap=self.cmap,
                      norm=mpl.colors.LogNorm(), normed=True, vmax=vmax, vmin=vmin)
            ax.grid(ls=":")

            ax.text(0.05, 0.87,
                    "$R\in[{:.2f};{:.2f})$".format(self._radial_splits[i], self._radial_splits[i + 1]),
                    transform=ax.transAxes)

        if fname is not None:
            fig.savefig(fname, dpi=300, bbox_inches="tight")
        return fig, axarr

    def set_info(self, radial_splits=None, cm_diagrams=None, cc_diagrams=None, plot_series=None,
                 reconstr_mags=None):

        if radial_splits is not None:
            self._radial_splits = radial_splits
        if cc_diagrams is not None:
            self._cc_diagrams = cc_diagrams
        if cm_diagrams is not None:
            self._cm_diagrams = cm_diagrams
        if plot_series is not None:
            self._plot_series = plot_series
        if reconstr_mags is not None:
            self._reconstr_mags = reconstr_mags

    def corner(self, rbin=None, rlabel="LOGR", rlog=True, clognorm=True, bins=None, nbins=60,
               fname=None, vmin=None, vmax=None, title=None):
        # This should be one radial bin, or if None, then all



        if rbin is not None:
            if rlog:
                rr = 10 ** self.container[rlabel]
            else:
                rr = self.container[rlabel]
            rind = (rr > self._radial_splits[rbin]) & (rr < self._radial_splits[rbin + 1])
        else:
            rind = np.ones(len(self.container.data), dtype=bool)

        columns = list(self.container.columns)
        if bins is None:
            bins = []
            for col in columns:
                bins.append(np.linspace(self.container[col].min(),
                                        self.container[col].max(), nbins))

        nrows = len(columns)
        ncols = len(columns)
        xsize = 2.5 * nrows
        ysize = 2.5 * ncols

        fig, axarr = plt.subplots(nrows=nrows, ncols=nrows, figsize=(xsize, ysize))
        fig.subplots_adjust(wspace=0.1, hspace=0.1)
        faxarr = axarr.flatten()

        if title is not None:
            fig.text(0.125, 0.9, title, fontsize=14)

        # blocking upper triangle
        for i in np.arange(nrows):
            for j in np.arange(ncols):
                if j < i:
                    norm = mpl.colors.Normalize()
                    if clognorm:
                        norm = mpl.colors.LogNorm()

                    axarr[i, j].hist2d(self.container[columns[j]][rind],
                                       self.container[columns[i]][rind],
                                       weights=self.container.weights[rind],
                                       bins=(bins[j], bins[i]), cmap=self.cmap,
                                       norm=norm, normed=True, vmax=vmax, vmin=vmin)
                    axarr[i, j].grid(ls=":")
                if i == j:
                    axarr[i, j].hist(self.container[columns[i]][rind], bins=bins[i],
                                     weights=self.container.weights[rind],
                                     histtype="step", density=True)
                    axarr[i, j].grid(ls=":")
                if j > i:
                    axarr[i, j].axis("off")
                if i < nrows - 1:
                    axarr[i, j].set_xticklabels([])
                if j > 0:
                    axarr[i, j].set_yticklabels([])
                if j == 0 and i > 0:
                    axarr[i, j].set_ylabel(columns[i])
                if i == nrows - 1:
                    axarr[i, j].set_xlabel(columns[j])

        if fname is not None:
            fig.savefig(fname, dpi=300, bbox_inches="tight")
        return fig, axarr

    def diffplot(self, fsc1, fsc2):
        # TODO this needs implemented in the end...

        #         this should be almost like the the other but some tweaking with the color scales
        pass

    def get_corner_bins(self, nbins=60):
        # corner bins
        self.corner_bins = []
        columns = list(self.container.columns)
        for col in columns:
            self.corner_bins.append(np.linspace(self.container[col].min(),
                                                self.container[col].max(), nbins))
        return self.corner_bins

    def plot_radial_ensemble(self, fname_root, cm=True, cc=True, radial=True, nbins=60, vmax=None, vmin=None,
                             cm_bins=None, cc_bins=None, corner_bins=None, title=None, suffix=""):
        """loop through a set of predefined diagrams"""

        # c-m diagrams
        if cm:
            for cm in self._cm_diagrams:
                fname = fname_root + "_cm_" + cm[0] + "_" + cm[1] + suffix + ".png"
                print(fname)
                self.radial_series(label1=cm[0], label2=cm[1], fname=fname,
                                   nbins=nbins, vmax=vmax, bins=cm_bins, title=title)

        # c-c diagrams
        if cc:
            for cc in self._cc_diagrams:
                fname = fname_root + "_cc_" + cc[0] + "_" + cc[1] + suffix + ".png"
                print(fname)
                self.radial_series(label1=cc[0], label2=cc[1], fname=fname,
                                   nbins=nbins, vmax=vmax, bins=cc_bins, title=title)

        # all -radial bin
        if radial:
            fname = fname_root + "_corner_all" + suffix + ".png"
            print(fname)
            self.corner(fname=fname, nbins=nbins, vmax=vmax, bins=corner_bins, title=title, vmin=vmin)

            # radial bins
            for rbin in np.arange(len(self._radial_splits) - 1):
                fname = fname_root + "_corner_rbin{:02d}".format(rbin) + suffix + ".png"
                print(fname)
                self.corner(rbin=rbin, fname=fname, nbins=nbins, vmax=vmax, bins=corner_bins, title=title, vmin=vmin)


# This is just a standard function
class NaiveKDE(object):
    def __init__(self, container, rng=None):
        """
        This is just the packaged version of the KDE
        It assumes that the data to be density estimated is int he .xarr attribute of the DualContainer...
        """
        self.container = container
        self.kde = None

        if rng is None:
            self.rng = np.random.RandomState()
        else:
            self.rng = rng
    def train(self, bandwidth=0.2, kernel="tophat", atol=1e-6, rtol=1e-6, breadth_first=False, **kwargs):
            """train the emulator"""
            self.bandwidth = bandwidth
            self.kwargs = kwargs
            self.kde = neighbors.KernelDensity(bandwidth=self.bandwidth, kernel=kernel,
                                               atol=atol, rtol=rtol, breadth_first=breadth_first, **kwargs)
            self.kde.fit(self.container.xarr, sample_weight=self.container.weights)

    def draw(self, num, rmin=None, rmax=None, rcol="LOGR", mode="data"):
        """draws random samples from KDE maximum radius"""
        self.res = DualContainer(**self.container.get_meta())
        _res = self.kde.sample(n_samples=int(num), random_state=self.rng)
        self.res.set_xarr(_res)

        if (rmin is not None) or (rmax is not None):
            if rmin is None:
                rmin = self.res.data[rcol].min()

            if rmax is None:
                rmax = self.res.data[rcol].max()

            # these are the indexes to replace, not the ones to keep...
            inds = (self.res.data[rcol] > rmax) | (self.res.data[rcol] < rmin)
            while inds.sum():
            # print(inds.sum())
                vals = self.kde.sample(n_samples=int(inds.sum()), random_state=self.rng)
                _res[inds, :] = vals
                self.res.set_xarr(_res)
                inds = (self.res.data[rcol] > rmax) | (self.res.data[rcol] < rmin)

        self.res.set_mode(mode)
        return self.res

    def score_samples(self, arr):
        """Assuming that arr is in the data format"""

        arr = self.container.transform(arr)
        res = self.kde.score_samples(arr)
        return res

    # def to_dict(self):
    #
    #
    #     # Memory view of training data cannot be pickled and is not strictly necessary
    #     _state = list(self.kde.tree_.__getstate__())
    #     sample_weights = copy.deepcopy(np.array(_state[-1]))
    #
    #
    #     # we have to change the state so that it can be pickled, it will be reconustructed later
    #     state = copy.deepcopy(_state[:-1])
    #     state.append(None)
    #
    #     self.kde.tree_.__setstate__(state)
    #     res = {
    #         "bandwidth": self.bandwidth,
    #         "container_meta": self.container.get_meta(),
    #         "kde": copy.deepcopy(self.kde),
    #         "sample_weights": sample_weights,
    #     }
    #     # we have to reset the original state
    #     self.kde.tree_.__setstate__(_state)
    #     # print(res["sample_weights"])
    #     # print(np.array(self.kde.tree_.__getstate__()[-1]))
    #     return res
    #
    # @classmethod
    # def from_dict(cls, info):
    #     container = DualContainer(**info["container_meta"])
    #     res = cls(container)
    #     res.kde = info["kde"]
    #     _state = list(res.kde.tree_.__getstate__())
    #     _state[-1] = info["sample_weights"]
    #     # _state[-2] = neighbors.dist_metrics.EuclideanDistance()
    #     res.kde.tree_.__setstate__(_state)
    #     return res

##########################################################################

def construct_wide_container(dataloader, settings, nbins=100, nmax=5000):
    fsc = FeatureSpaceContainer(dataloader)
    fsc.construct_features(**settings)
    # cont = fsc.to_dual(r_normalize=r_normalize)
    cont_small = fsc.downsample(nbins=nbins, nmax=nmax,)
    cont_small.shuffle()
    settings = copy.copy(settings)
    settings.update({"container": cont_small})
    return settings


def construct_wide_kde(settings):
    cont = settings["container"]
    emu = GradientKDE()
    emu.set_data(cont.data, cont.weights)
    emu.build_kde(**settings["emulator"])
    return emu


def construct_deep_container(fname, settings, frac=1.):
    fsc = DeepFeatureContainer.from_file(fname)
    fsc.construct_features(**settings)
    cont = fsc.to_dual()
    cont.sample(frac=frac)
    settings = copy.copy(settings)
    settings.update({"container": cont})
    return settings

def construct_deep_kde(settings):
    cont = settings["container"]
    emu = GradientKDE()
    emu.set_data(cont.data, cont.weights)
    emu.build_kde(**settings["emulator"])
    return emu

##########################################################################


# def make_infodicts(wcr_settings, wr_settings, dc_settings, dsmc_settings,
#                    nsamples, cols, nchunks):
#
#     dsmc_emu =  construct_deep_kde(dsmc_settings)
#     wr_emu = construct_deep_kde(wr_settings)
#
#     dsmc_emu.draw_deep_sample(nsample=nsamples)
#     wr_emu.draw_deep_sample(nsample=nsamples)
#
#     sample = pd.merge(dsmc_emu.deep_sample, wr_emu.deep_sample, left_index=True, right_index=True)
#     sample_inds = partition(list(sample.index), nchunks)
#
#     infodicts = []
#     for i in np.arange(nchunks):
#         subsample = sample.loc[sample_inds[i]]
#
#         info = {
#             "sample": subsample,
#             "dc_settings": dc_settings,
#             "wr_settings": wr_settings,
#             "wcr_settings": wcr_settings,
#             "cols": cols,
#         }
#         infodicts.append(info)
#     return sample, infodicts

def make_naive_infodicts(wcr_cont, wr_cont, dc_cont, dsmc_cont,
                         nsamples, cols, nchunks, bandwidth=0.1,
                         rmin=None, rmax=None, rcol="LOGR"):

    dsmc_emu = NaiveKDE(dsmc_cont)
    dsmc_emu.train(bandwidth=bandwidth)
    wr_emu = NaiveKDE(wr_cont)
    wr_emu.train(bandwidth=bandwidth)

    dsmc_emu.draw(nsamples)
    wr_emu.draw(nsamples, rmin=rmin, rmax=rmax, rcol=rcol)
    sample = pd.merge(dsmc_emu.res.data, wr_emu.res.data, left_index=True, right_index=True)
    sample_inds = partition(list(sample.index), nchunks)

    infodicts = []
    for i in np.arange(nchunks):
        subsample = sample.loc[sample_inds[i]]

        info = {
            "sample": subsample,
            "dc_cont": dc_cont,
            "wr_cont": wr_cont,
            "wcr_cont": wcr_cont,
            "cols": cols,
            "bandwidth": bandwidth,
        }
        infodicts.append(info)
    return sample, infodicts


# def make_infodicts_legacy(wcr, wr, dc, dsmc, nsamples, cols, nchunks=30, bandwidth=0.2, sample_rmax=5,
#                    atol=1e-4, rtol=1e-4):
#     wr_emu = FeatureEmulator(wr)
#     wr_emu.train(kernel="tophat", bandwidth=bandwidth, atol=atol, rtol=rtol)
#
#     dsmc_emu = FeatureEmulator(dsmc)
#     dsmc_emu.train(kernel="tophat", bandwidth=bandwidth, atol=atol, rtol=rtol)
#
#     _sample = dsmc_emu.draw(num=nsamples)
#
#     rvals = wr_emu.draw(num=nsamples, rmax=sample_rmax)
#     sample = pd.merge(_sample.data, rvals.data, left_index=True, right_index=True)
#     sample_inds = partition(list(sample.index), nchunks)
#
#     infodicts = []
#     for i in np.arange(nchunks):
#         subsample = sample.loc[sample_inds[i]]
#
#         info = {
#             "sample": subsample,
#             "dc_cont": dc,
#             "wr_cont": wr,
#             "wcr_cont": wcr,
#             "cols": cols,
#             "bandwidth": bandwidth,
#             "atol": atol,
#             "rtol": rtol,
#         }
#         infodicts.append(info)
#     return sample, infodicts


def run_scores(infodicts):
    pool = mp.Pool(processes=len(infodicts))
    try:
        pp = pool.map_async(calc_scores, infodicts)
        # the results here should be a list of score values
        result = pp.get(86400)  # apparently this counters a bug in the exception passing in python.subprocess...
    except KeyboardInterrupt:
        print("Caught KeyboardInterrupt, terminating workers")
        pool.terminate()
        pool.join()
    else:
        pool.close()
        pool.join()

    dc_scores = []
    wr_scores = []
    wcr_scores = []
    for res in result:
        dc_scores.append(res[0])
        wr_scores.append(res[1])
        wcr_scores.append(res[2])

    dc_scores = np.concatenate(dc_scores)
    wr_scores = np.concatenate(wr_scores)
    wcr_scores = np.concatenate(wcr_scores)

    return dc_scores, wr_scores, wcr_scores


def calc_scores(info):
    dc_score, wr_score, wcr_score = [], [], []
    try:
        sample = info["sample"]

        dc_emu = NaiveKDE(info["dc_cont"])
        dc_emu.train(bandwidth=info["bandwidth"])
        wr_emu = NaiveKDE(info["wr_cont"])
        wr_emu.train(bandwidth=info["bandwidth"])
        wcr_emu = NaiveKDE(info["wcr_cont"])
        wcr_emu.train(bandwidth=info["bandwidth"])

        dc_score = dc_emu.score_samples(sample[info["cols"]["cols_dc"]])
        wr_score = wr_emu.score_samples(sample[info["cols"]["cols_wr"]])
        wcr_score = wcr_emu.score_samples(sample[info["cols"]["cols_wcr"]])

        # dc_emu = construct_deep_kde(info["dc_settings"])
        # wr_emu = construct_deep_kde(info["wr_settings"])
        # wcr_emu = construct_deep_kde(info["wcr_settings"])
        #
        # dc_score = dc_emu.score(sample[info["cols"]["cols_dc"]])
        # wr_score = wr_emu.score(sample[info["cols"]["cols_wr"]])
        # wcr_score = wcr_emu.score(sample[info["cols"]["cols_wcr"]])

    except KeyboardInterrupt:
        pass

    return dc_score, wr_score, wcr_score


def to_buffer(arr):
    mp_arr = mp.Array("d", arr.flatten(), lock=False)
    return mp_arr, arr.shape


def from_buffer(mp_arr, shape):
    arr = np.frombuffer(mp_arr, dtype="d").reshape(shape)
    return arr


class KFoldValidator(object):
    """
    TODO validation package,

    Should automate splitting base data into training and test
    """
    def __init__(self, container, cv=5, param_grid=None, extra_params=None, score_train=False):
        self.container = container
        self.cv = cv

        self.param_grid = param_grid
        self.param_list = list(modsel.ParameterGrid(param_grid))
        if extra_params is None:
            self.extra_params = {}
        else:
            self.extra_params = extra_params

        # self.mp_xarr, self.mp_xarr_shape = to_buffer(self.container.xarr.values)
        # self.mp_w, self.mp_w_shape = to_buffer(self.container.weights.values)

        self._calc_split()

        self.result = None
        self.scores = None
        self.score_train = score_train

    def _calc_split(self):
        # TODO replace this with something that balances weights...

        inds = np.arange(len(self.container.data))
        # ww = self.container.weights

        kfold = modsel.KFold(n_splits=self.cv)
        self.splits = list(kfold.split(inds))

    def _get_infodicts(self):
        """
        Splits the dataset into a set of dictionaries dispathable to subprocesses
        """

        infodicts = []
        for i, params in enumerate(self.param_list):
            for j, split in enumerate(self.splits):
                info = {
                    "id": (i,j),
                    "split": split,
                    "params": params,
                    "extra_params": self.extra_params,
                    "xarr": self.container.xarr,
                    "w": self.container.weights,
                    "score_train": self.score_train,
                    # "meta": self.container.get_meta(),
                    # "mp_xarr": self.mp_xarr,
                    # "mp_xarr_shape": self.mp_xarr_shape,
                    # "mp_w": self.mp_w,
                    # "mp_w_shape": self.mp_w_shape,
                }
                infodicts.append(info)

        return infodicts

    def run(self, nprocess=1):

        self.infodicts = self._get_infodicts()

        if nprocess > len(self.infodicts):
            nprocess = len(self.infodicts)
        info_chunks = partition(self.infodicts, nprocess)

        pool = mp.Pool(processes=nprocess)
        try:
            pp = pool.map_async(_run_validation_chunks, info_chunks)
            # the results here should be a list of score values
            self.result = pp.get(86400)  # apparently this counters a bug in the exception passing in python.subprocess...
        except KeyboardInterrupt:
            print("Caught KeyboardInterrupt, terminating workers")
            pool.terminate()
            pool.join()
        else:
            pool.close()
            pool.join()

        self.train_scores = []
        self.test_scores = []
        for res in self.result:
            if self.score_train:
                self.train_scores.append(res[0])
            self.test_scores.append(res[1])

        if self.score_train:
            self.train_scores = np.concatenate(self.train_scores).reshape((len(self.param_list), self.cv))
        self.test_scores = np.concatenate(self.test_scores).reshape((len(self.param_list), self.cv))


def _run_validation_chunks(infodicts):

    train_scores = []
    test_scores = []

    train_allscores = []
    test_allscores = []
    try:
        for info in infodicts:
            kdes = KDEScorer(info)
            kdes.train()
            if info["score_train"]:
                train_score, tmp = kdes.score(on="train")
                train_scores.append(train_score)
                train_allscores.append(tmp)
            #
            test_score, tmp = kdes.score(on="test")
            test_scores.append(test_score)
            test_allscores.append(tmp)

    except KeyboardInterrupt:
            pass

    return train_scores, test_scores, (train_allscores, test_allscores)
    # return


INFVAL = -16  # this is the value we replace -inf with, effectively a surrogate for log(0), an obvious approximation...
def force_finite(arr):
    inds = np.invert(np.isfinite(arr))
    arr[inds] = INFVAL
    return arr


def ring_area(r1, r2):
    val = np.pi * (r2**2. - r1**2.)
    return val


class KDEScorer(object):
    def __init__(self, info):
        # self.xarr = from_buffer(info["mp_xarr"], info["mp_xarr_shape"])
        # self.weights = from_buffer(info["mp_w"], info["mp_w_shape"])
        self.xarr = info["xarr"]
        self.weights = info["w"]

        self.train_inds = info["split"][0]
        self.test_inds = info["split"][1]

        self.params = info["params"]
        self.params.update(info["extra_params"])

        self.kde = neighbors.KernelDensity(**self.params)

    def train(self):
        self.kde.fit(self.xarr.values[self.train_inds, :], sample_weight=self.weights.values[self.train_inds])

    def score(self, on="test"):
        if on == "test":
            index = self.test_inds
        elif on == "train":
            index = self.train_inds
        else:
            raise KeyError

        raw_scores = self.kde.score_samples(self.xarr.values[index, :])
        scores = force_finite(raw_scores)

        # this does not inlcude weights, but is OK as we don't want result skewed by the high weight limb...
        res = scores.sum() / len(scores)

        return res, scores


def get_nearest(val, arr):
    res = []
    for tmp in val:
        res.append(np.argmin((tmp - arr)**2.))
    return np.array(res)


class CompositeDraw(object):
    def __init__(self, wemu, demu, ipivot=22.4, whistsize=1e6, icutmin=22, chunksize=1e5, rng=None):
        self.wemu = wemu
        self.demu = demu
        self.ipivot = ipivot
        self.whistsize = whistsize
        self.icutmin = icutmin
        self.chunksize = int(chunksize)

        self._mkref()
        if rng is not None:
            self.rng = rng
        else:
            self.rng = np.random.RandomState()

    def _mkref(self):
        self.ibins = np.linspace(13, 30, 500)
        self.icens = self.ibins[:-1] + np.diff(self.ibins) / 2.

        wsamples = self.wemu.draw(self.whistsize)

        self.wip = np.histogram(wsamples.data["MAG_I"], weights=wsamples.weights, bins=self.ibins, density=True)[0]
        self.dip = np.histogram(self.demu.container.data["MAG_I"], weights=self.demu.container.weights, bins=self.ibins, density=True)[0]

        iscale = np.argmin((self.icens - self.ipivot) ** 2.)
        self.ifactor = self.wip[iscale] / self.dip[iscale]
        self.refcurve = self.dip * self.ifactor

        self.dip0 = np.zeros(len(self.icens))
        ii = self.icens <= self.ipivot
        self.dip0[ii] = self.wip[ii]
        ii = self.icens > self.ipivot
        self.dip0[ii] = self.dip[ii] * self.ifactor

        self.fracdeep = np.sum(self.dip0) / np.sum(self.wip) - 1.

    def draw(self, wide_samples_to_draw):

        self.wide_samples_to_draw = int(wide_samples_to_draw)
        self.deep_samples_to_draw = int(self.wide_samples_to_draw * self.fracdeep)


        wide = self.wemu.draw(self.wide_samples_to_draw)
        wide.set_mode("data")
        deep = self._deepdraw()
        deep.set_mode("data")

        joint = DualContainer()
        joint.set_data(pd.concat((wide.data, deep.data), sort=False).reset_index(drop=True))
        joint.set_mode("data")

        return joint, wide, deep

    def _deepdraw(self):

        chunks = []
        nobjs = 0
        while nobjs < self.deep_samples_to_draw:

            dsamples = self.demu.draw(self.chunksize)
            dsamples.set_mode("data")
            rands = self.rng.uniform(size=len(dsamples.data))
            inodes = get_nearest(dsamples["MAG_I"], self.icens)

            refvals = self.refcurve[inodes]
            wvals = self.wip[inodes]
            bools = (rands * refvals > wvals) & (dsamples["MAG_I"] > self.icutmin)

            chunks.append(dsamples.data[bools])
            nobjs += bools.sum()
        chunks = pd.concat(chunks)
        chunks = chunks.iloc[:self.deep_samples_to_draw].copy()

        tmp = self.wemu.draw(self.deep_samples_to_draw)
        chunks["LOGR"] = tmp.data["LOGR"].values
        chunks = chunks.reset_index(drop=True)
        cols = [chunks.columns[-1], ] + list(chunks.columns[:-1])
        # print(cols)
        chunks = chunks[cols]

        res = DualContainer()
        res.set_data(chunks)
        return res

