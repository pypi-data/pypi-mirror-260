
from dielectric.constants import *  # imports numpy as np
from dielectric.utils.file_utils import load_config

import logging

# logging.basicConfig(level="DEBUG")
logging.basicConfig(level="INFO")
# logger = logging.getLogger(__name__)
# logger.setLevel(logging.DEBUG)
# logger.setLevel(logging.INFO)


class Ion:
    """class for single ionic species.

    Attributes:
        name (str): ion identifier e.g. K+, Cl-.
        mass (float): bare ionic mass in amu.
        radius (float): hydrodynamic radius of ion.
        D (float): diffusion constant.
        z (float): ionic charge.
        nu (float): stoichiometry of ion in salt.
    """
    def __init__(self, name, mass, radius, z, nu, Lambda=None, D=None):
        self.name = name
        self.mass = mass
        self.radius = radius
        self.Lambda = Lambda
        self.D = D
        self.z = z
        self.nu = nu

    @classmethod
    def from_dict(cls, d):
        """ classmethod to enable constructing an instance from configuration file.

        Args:
            d (dict): dictionary with fields from init.

        Returns:
            instance of Ion class.
        """
        ion = cls(name=d["name"], mass=d["mass"], radius=d["radius"],
                   z=d["z"], nu=d["nu"])
        # for optional parameters, use dict.get method with default value if key does not exist
        ion.Lambda = d.get("Lambda")
        ion.D = d.get("D")           # default value of get method is None by default
        ion.update()
        return ion

    def update(self):
        """update the diffusion constant or the limiting molar conductivity.

        Returns:
           ion: an instance of the Electrolyte class
        """
        factor = N_AVO*E_CHARGE*E_CHARGE / BOLTZ_T
        if self.Lambda is None and self.D is not None:
            self.Lambda = np.abs(self.z) * self.D * factor
        elif self.Lambda is not None and self.D is None:
            self.D = self.Lambda / (np.abs(self.z) * factor)


class Salt:
    """class for single salt, made up of ions.

    Attributes:
        name (str): salt identifier e.g. KCl.
        conc (float): concentration in mmol/l mol/m^3.
        ions (float): list of Ion objects.
        kappa2 (float): square of inverse Debye length due to Salt.
        D_zero (float): average diffusion constant for Salt.
    """
    def __init__(self):
        self.name = None
        self.conc = None
        self.ions = []
        self.kappa2 = None
        self.D_zero = None  # D_zero of salt: sum over ions

    def calc_kappa2(self):
        """calculation of kappa^2 (inverse of Debije length squared).
        """
        self.kappa2 = 0.0
        factor = (np.square(E_CHARGE) * N_AVO) / (EPS_ZW * BOLTZ_T)
        for ion in self.ions:
            self.kappa2 += factor * self.conc * ion.nu * np.square(ion.z)
        # logging.info(f" kappa2: {self.kappa2} kappa: '{self.kappa} Debye_length: {self.Debye_length}")

    def calc_D_zero(self):
        """ calculates D_zero as sum over ions: ``|z_i|*D_i over |z_i|``.
        """
        if self.ions:
            nominator = np.sum(np.abs(ion.z) * ion.D for ion in self.ions)
            denominator = np.sum(np.abs(ion.z) for ion in self.ions)
            self.D_zero = nominator / denominator


class Electrolyte:
    """class for electrolyte consisting of single or multiple salts.

    Attributes:
        config_file (str): configuration file name (``*``.yaml).
        num_salts (int): numer of salts in electrolyte.
        salts (list): list of Salt objects in electrolyte.
        kappa2 (float): inverse of Debye length squared
        kappa (float): inverse of Debye length.
        Debye_length (float): Debye length.
        D_zero (float): average diffusion constant for Salt.
        Dc (float):
        Dn (float):
        Dt (float):
        sigma (float):
        lambda_c2 (float):
        lambda_n2 (float):
    """
    def __init__(self):
        # basic attributes
        self.config_file = None
        self.num_salts = None
        self.salts = []
        # calculated attributes
        self.kappa2 = None
        self.kappa = None
        self.Debye_length = None
        self.D_zero = None         # D_zero of electrolyte: sum over salts
        self.Dc = None
        self.Dn = None
        self.Dt = None             # used for omega << k^2*Dzero
        self.sigma = None          # conductivity: was K1
        self.lambda_c2 = None
        self.lambda_n2 = None

    @classmethod
    def from_yaml(cls, config_yaml: str):
        """ classmethod to enable constructing an instance from configuration file.

        Args:
            config_yaml (str): configuration file name.

        Returns:
            Electrolyte class instance.
        """
        el = cls()
        el.config_file = config_yaml
        d = load_config(el.config_file)
        el.num_salts = len(d["electrolyte"])
        for n in range(el.num_salts):
            ed = d.get("electrolyte")[n]
            salt = Salt()
            salt.name = ed['name']
            salt.conc = ed["conc"]
            num_ions = len(ed["ions"])
            for i in range(num_ions):
                idict = ed.get("ions")[i]
                ion = Ion.from_dict(idict)
                # append by reference, therefore new Ion object in each iteration
                salt.ions.append(ion)
            # append by reference, therefore new Salt object in each iteration
            el.salts.append(salt)
            logging.info(f" salt '{salt.name}' appended to electrolyte")

        el.calc_kappa()
        el.calc_D_zero()
        el.calc_Dc()
        el.calc_Dn_binary()
        el.calc_Dt_binary()
        el.calc_sigma()  # limiting conductivity value
        return el

    def update(self):
        pass

    def calc_kappa(self):
        """calculation of kappa^2, kappa (inverse of Debije length) and Debye length.
        """
        self.kappa2 = 0.0
        self.kappa = 0.0
        self.Debye_length = 0.0
        factor = (np.square(E_CHARGE) * N_AVO) / (EPS_ZW * BOLTZ_T)

        for salt in self.salts:
            for ion in salt.ions:
                self.kappa2 += factor * salt.conc * ion.nu * np.square(ion.z)

        self.kappa = np.sqrt(self.kappa2)  # inverse of the Debije length
        self.Debye_length = np.reciprocal(self.kappa)
        # logging.info(f" kappa2: {self.kappa2} kappa: '{self.kappa} Debye_length: {self.Debye_length}")

    def calc_D_zero(self):
        """ calculates D_zero as sum over ions: ``|z_i|*D_i over |z_i|``.
        """
        if self.salts:
            nominator = sum(np.abs(ion.z) * ion.D for salt in self.salts for ion in salt.ions)
            denominator = sum(np.abs(ion.z) for salt in self.salts for ion in salt.ions)
            self.D_zero = nominator/denominator

    def calc_sigma(self):
        """calculates limiting conductivity value of electrolyte at infinite dilution.
        """
        if self.kappa2 and self.D_zero:
            self.sigma = EPS_ZW * self.kappa2 * self.D_zero  # limiting conductivity value

    def calc_Dc(self):
        """calculates Dc as sum over ions:  ``|z_i| over |z_i|/D_i/``.
        """
        if self.salts:
            denominator = sum(np.abs(ion.z) / ion.D for salt in self.salts for ion in salt.ions)
            nominator = sum(np.abs(ion.z) for salt in self.salts for ion in salt.ions)
            self.Dc = nominator/denominator

    def calc_Dn_binary(self):
        """calculates Dn as sum over ions:  ``|z_i| over |z_i|/D_j.ne.i``.

        See: https://www.geeksforgeeks.org/python-multiply-all-cross-list-element-pairs/
             https://www.geeksforgeeks.org/python-multiply-numbers-list-3-different-ways/
             https://stackoverflow.com/questions/2853212/all-possible-permutations-of-a-set-of-lists-in-python
             https://numpy.org/doc/stable/reference/generated/numpy.outer.html
             https://numpy.org/doc/stable/reference/generated/numpy.einsum.html
        """
        if self.salts:
            z_list = [np.abs(ion.z) for salt in self.salts for ion in salt.ions]
            one_over_D_list = [1.0/ion.D for salt in self.salts for ion in salt.ions]
            out_mat = np.outer(z_list, one_over_D_list)
            np.fill_diagonal(out_mat, 0.0)
            denominator = np.sum(out_mat)
            nominator = np.sum(z_list)
            self.Dn = nominator/denominator

    def calc_Dt_binary(self):
        """calculates Dt as sum over ions:  ``|z_i| over |z_i|/D_j.ne.i``.

        """
        if self.salts:
            z_list = [ion.z for salt in self.salts for ion in salt.ions]
            z_abs_list = [np.abs(ion.z) for salt in self.salts for ion in salt.ions]
            one_over_D_list = [1.0/ion.D for salt in self.salts for ion in salt.ions]

            dpm = sum(one_over_D_list[::2]) - sum(one_over_D_list[1::2])
            nominator = np.product(z_list) * np.square(dpm)

            out_mat = np.outer(z_abs_list, one_over_D_list)
            np.fill_diagonal(out_mat, 0.0)
            denominator = np.sum(z_abs_list) * np.sum(out_mat)
            self.Dt = nominator/denominator
            self.Dt = np.reciprocal(self.Dt)


if __name__ == "__main__":
    from pathlib import Path
    DATADIR = Path(__file__).parent.parent.parent.parent.absolute().joinpath("ImpedanceData")
    e = Electrolyte.from_yaml(str(DATADIR / "Cell_1_KCl_1mM.yaml"))
    print(f"kappa^2: {e.kappa2} [m^2]")

    IVPDIR = Path(__file__).parent.parent.parent.parent.absolute().joinpath("ImpedanceData")
    e2 = Electrolyte.from_yaml(str(IVPDIR / "BaCl2.yaml"))
    for salt in e2.salts:
        print(f"{salt.name}")
    print(f"kappa^2: {e2.kappa2} [m^2]")

