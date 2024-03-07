"""Class for Mixture.

Mixture class is the top class, but may serve as a constituent for itself.
"""

from typing import Union, TypeAlias

from .substance import Substance
from .element import Element
from .molecule import Molecule


Constituent: TypeAlias = Union["Mixture", Molecule, Element]

class Mixture(Substance):
    """A substance made of elements, molecules or other mixtures.

    A molecule shares its properties with its parent class `Substance`.
    Furthermore, it is possible to calculate the density of a mixture, as long
    as all its constituents have a specified density.
    """

    # override
    @classmethod
    def _get_allowed_constituents(cls):
        return (Mixture, Molecule, Element)
    
    def __init__(self, name: str, composition: dict[Constituent, float], mode: str = "_legacy", **kwargs) -> None:
        """Constructor of mixture.
        
        Args:
            name:
                Descriptive name.
            composition:
                Dictionary that maps a constituent of the mixture to its
                fraction. The fractions are physically interpreted according
                to the given mode. Values are normalsied and don't need to add
                up to unity.
            mode:
                Fractions in the composition can be interpreted as atomic,
                weight or volumetric fractions. Volumetric is only valid, if
                all constituents have a density. The default value allows
                inputs as before v1.1.0, where positive fractions refer to
                atomic and negative fractions to weight.
            **kwargs:
                Keyword arguments to override values.
        
        Keyword Args:
            M (float):
                Set molar mass.
            rho (float):
                Set density.
            symbol (str):
                Short symbol.
            data (dict[str, float]):
                Dictionary with additional data to store or use for mean values
                in mixtures.

        Raises:
            ValueError:
                If non-valid constructor mode or given constituent is not a
                substance.
        """

        super().__init__(name=name, composition=composition, mode=mode, **kwargs)

        if self._rho == 0.0:
            self._rho = self._calc_rho()


    # ########
    # Quantity Calculation
    # ########

    def _calc_rho(self) -> float:
        r"""Calculates average density.
        
        The mean of all constituent densities, weighted by their volume fraction:
            $$\overline{\rho} = \sum_i \phi_i \cdot \rho_i$$
        Returns zero if calculation is not possible.
        """
        try:
            return self.rule_of_mixtures("volume", "density")
        except:
            return 0.0
        
    def rule_of_mixtures(self, mode: str, quantity: str, inverse: bool = False) -> float:
        r"""Calculates average quantity value for a mixture.

        Average value is either calculated via general rule of mixtures:
            $$\overline{\psi} = \sum_i f_i \cdot \psi_i$$
        or if selected via the inverse rule of mixtures:
            $$\overline{\psi} = \left( \sum_i \frac{f_i}{\psi_i} \right)^{-1}$$
        
        Args:
            mode:
                Composition fractions used for weighting. Possible fraction
                modes are `atomic`/`mole`, `weight` or `volume` Volumetric 
                fractions are only valid, if all constituents have a density.
            quantity:
                Quantity, which should be calculated as average.
            inverse:
                Use inverse rule of mixtures.

        Returns:
            Calculated mean value.

        Raises:
            ValueError:
                If a constituent contains a zero value for relevant quantities
                or fraction mode is unknown.
            KeyError:
                If a constituent does not contain the key (and thus data) for
                the selected quantity.
        """

        # get composition in selected mode
        if mode in {"atomic", "at", "mole", "mol"}:
            composition = self._composition
        elif mode in {"weight", "wt"}:
            if all(constituent.M > 0 for constituent in self._composition.keys()):
                composition = self.get_composition_in_wt()
            else:
                raise ValueError("One of the constituents contains zero-values for molar mass.")
        elif mode in {"volume", "vol"}:
            if all((constituent.M > 0 and constituent.rho > 0) for constituent in self._composition.keys()):
                composition = self.get_composition_in_vol()
            else:
                raise ValueError("One of the constituents contains zero-values for molar mass or density.")
        else:
            raise ValueError(f"Unknown fraction mode \"{mode}\".")
        
        # extract fractions
        fractions = composition.values()

        # extract quantities
        if quantity == "density" or quantity == "rho":
            quantities = [constituent.rho for constituent in composition.keys()]
        else:
            try:
                quantities = [constituent.data[quantity] for constituent in composition.keys()]
            except KeyError:
                raise KeyError("One of the constituents does not contain values for the selected quantity.")

        # check if all quantities are non-zero
        if any(quantity == 0 for quantity in quantities):
            raise ValueError("One of the constituents contains zero-values for the selected quantity.")
        
        if inverse:
            return self._inverse_rule_of_mixtures(fractions, quantities)
        else:
            return self._general_rule_of_mixtures(fractions, quantities)    

    @staticmethod
    def _general_rule_of_mixtures(fractions: list[float], quantities: list[float]) -> float:
        r"""Calculates average value for a quantity.

        Weighted average of quantities with given fractions:
            $$\overline{\psi} = \sum_i f_i \cdot \psi_i$$

        Args:
            fractions:
                List with fractions of each constituent.
            quantities:
                List with quantity values of each constituent.
        """
        return sum(fraction*quantity for fraction, quantity in zip(fractions, quantities))

    @staticmethod
    def _inverse_rule_of_mixtures(fractions: list[float], quantities: list[float]) -> float:
        r"""Calculates average value for a quantity.

        Inverse of weighted average of quantities with given fractions:
            $$\overline{\psi} = \left( \sum_i \frac{f_i}{\psi_i} \right)^{-1}$$
        
        Args:
            fractions:
                List with fractions of each constituent.
            quantities:
                List with quantity values of each constituent.
        """
        return sum(fraction/quantity for fraction, quantity in zip(fractions, quantities))**-1