import numpy as np
import torch
from numpy import linalg as npLA
from scipy import linalg as sciLA


class LA_Tools:

    def __init__(self, engine: str = "torch") -> None:
        self.engine = engine
        assert engine in [
            "torch",
            "numpy",
            "scipy",
        ], """
        Please select a valid computing engine... the options are:
        "torch", "numpy", "scipy"
        """

    @staticmethod
    def state_ordering(evecs_old, evecs_new, round=8, **kwargs):
        # Essentially a matrix of the fidelities: |<phi|psi>|
        overlap = np.round(abs(evecs_old @ evecs_new.T), round)
        # calculate trace distance
        # for o in overlap:
        #     for _o in o:
        #         if (_o>1):
        #             print('OVERLAP BIGGER THAN 1', _o)
        # dist = abs(1-overlap)/step**2
        # ordering = np.array([dist[i,:].argmin() for i in range(len(evecs_old))])  #python
        # ordering = np.argmin(dist,axis=1) #numpy
        ordering = np.argmax(overlap, axis=1)  # numpy
        return ordering

    @staticmethod
    def order_eig(evals, evecs, **kwargs):
        order = np.argsort(evals)
        evecs_ordered = evecs[order, :]
        evals_ordered = evals[order]
        return evals_ordered, evecs_ordered

    def diagonalize_batch(self, matrix_array, round=10, **kwargs):
        if self.engine == "numpy":
            w, v = npLA.eigh(matrix_array)
        elif self.engine == "scipy":
            w, v = sciLA.eigh(matrix_array)
        elif self.engine == "torch":
            w, v = torch.linalg.eigh(torch.from_numpy(matrix_array))
            w = w.numpy()
            v = v.numpy()
        evals_batch = np.round(w, round)
        evecs_batch = np.round(np.transpose(v, [0, 2, 1]), round)
        return evals_batch, evecs_batch

    def diagonalize(self, matrix, order=False, normalize=False, round=10, **kwargs):
        if self.engine == "numpy":
            w, v = npLA.eigh(matrix)
        elif self.engine == "scipy":
            w, v = sciLA.eigh(matrix)
        elif self.engine == "torch":
            w, v = torch.linalg.eigh(torch.from_numpy(matrix))
            w = w.numpy()
            v = v.numpy()
        evals = np.round(w, round)
        evecs = np.round(v.T, round)
        if normalize:
            for i, evec in enumerate(evecs):
                evecs[i] /= evec @ evec
        if order:
            idx_order = np.argsort(evals)
            evecs = evecs[idx_order, :]
            evals = evals[idx_order]
        return evals, evecs
