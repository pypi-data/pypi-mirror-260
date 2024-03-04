from sklearn.neural_network import MLPClassifier
import numpy as np
from mlfriends import RobustEllipsoidRegion


def filter_points(root, pointpile, ellipsoid_region):
    """Find all stored points, live or dead, that are within ellipsoid."""
    ids_inside = ellipsoid_region.inside_ellipsoid(pointpile.us)
    N = ids_inside.sum()
    found_i = 0
    found_us = pointpile.us[ids_inside,:]
    found_Ls = np.empty((N,))
    open_nodes = list(root.children)
    while len(open_nodes) > 0:
        n = open_nodes.pop(0)
        if ids_inside[n.id]:
            found_Ls[found_i] = n.value
            found_i += 1
        open_nodes += n.children
    assert found_i == N
    return found_us, found_Ls

# use viz_callback to build a neural network
# enable vectorization and set ndraw_min high.

class NeuralFilter(RobustEllipsoidRegion):
    def __init__(self, sampler, viz_callback, prob_cutoff, num_networks=4,
            neural_network_kwargs={}, verbose=True):

        default_neural_network_kwargs = dict(
            hidden_layer_sizes=(100, 50, 20), alpha=0, learning_rate_init=1e-2,
            max_iter=10000, tol=0, n_iter_no_change=10)
        default_neural_network_kwargs.update(neural_network_kwargs)
        self.neural_network_kwargs = default_neural_network_kwargs

        self.sampler = sampler
        self.viz_callback = viz_callback
        self.num_networks = num_networks
        self.prob_cutoff = prob_cutoff
        self.verbose = verbose
        self.networks = []

    def train(self, points, region, transformLayer):
        # get all stored/pile points within ellipsoid
        if self.verbose:
            print("training: getting data...")
        us, Ls = filter_points(self.sampler.root, self.sampler.pointpile, region)
        # transform to a whitened space with ellipsoid
        ts = transformLayer.transform(us)
        # then train neural network classifier to distinguish rejected from live points
        # classification training data:
        inside_class = (Ls > self.sampler.Lmin) * 1
        self.networks = []
        for i in range(self.num_networks):
            if self.verbose:
                print("training[%d/%d] with %d/%d samples ..." % (i+1, self.num_networks, inside_class.sum(), len(inside_class)))
            network = MLPClassifier(**self.neural_network_kwargs)
            network.fit(ts, inside_class)
            self.networks.append((transformLayer, network))

    def viz_callback(self, points, info, region, transformLayer, **kwargs):
        self.train(points=points, region=region, transformLayer=transformLayer)
        return self.viz_callback(points=points, info=info, transformLayer=transformLayer, **kwargs)

    def inside(self, us):
        proba = [network.predict_proba(layer.transform(us))[:,1]
            for layer, network in self.networks]
        mean_proba = np.mean(proba, axis=1)
        std_proba = np.std(proba, axis=1).mean()
        is_inside = mean_proba > self.prob_cutoff
        if self.verbose:
            print("prediction frac=%.3f%% mean[prob]=%.3f, std[cross-NN]=%.3f" % (is_inside.mean() * 100, mean_proba.mean(), std_proba))
        
        return is_inside

    def sample_from_boundingbox(self, nsamples=100):
        """Draw uniformly sampled points from MLFriends region.

        Draws uniformly from bounding box around region.

        Parameters as described in *sample()*.
        """
        N, ndim = self.u.shape
        # draw from unit cube in prior space
        u = np.random.uniform(size=(nsamples, ndim))
        wmask = self.inside(u)
        return u[wmask,:]

    def sample_from_transformed_boundingbox(self, nsamples=100):
        """Draw uniformly sampled points from MLFriends region.

        Draws uniformly from bounding box around region (in whitened space).

        Parameters as described in *sample()*.
        """
        N, ndim = self.u.shape
        # draw from rectangle in transformed space
        v = np.random.uniform(self.bbox_lo - self.maxradiussq, self.bbox_hi + self.maxradiussq, size=(nsamples, ndim))

        # check if inside unit cube
        w = self.transformLayer.untransform(v)
        wmask = np.logical_and(w > 0, w < 1).all(axis=1)
        wmask[wmask] = self.inside(w[wmask])

        return w[wmask,:]

    def sample_from_wrapping_ellipsoid(self, nsamples=100):
        """Draw uniformly sampled points from MLFriends region.

        Draws uniformly from wrapping ellipsoid and filters with region.

        Parameters as described in ``sample()``.
        """
        N, ndim = self.u.shape
        # draw from rectangle in transformed space

        z = np.random.normal(size=(nsamples, ndim))
        assert ((z**2).sum(axis=1) > 0).all(), (z**2).sum(axis=1)
        z /= ((z**2).sum(axis=1)**0.5).reshape((nsamples, 1))
        assert self.enlarge > 0, self.enlarge
        u = z * self.enlarge**0.5 * np.random.uniform(size=(nsamples, 1))**(1./ndim)

        w = self.ellipsoid_center + np.dot(u, self.ellipsoid_axes_T)
        #assert self.inside_ellipsoid(w).all()

        wmask = np.logical_and(w > 0, w < 1).all(axis=1)
        wmask[wmask] = self.inside(w[wmask])
        return w[wmask,:]
