from .axelrod import Axelrod
from .centola import Centola
from .klemm import Klemm
from .expandable_model import MultilayerAxelrod, MultilayerCentola, MultilayerKlemm
from .evolution_algorithm import EvolutionAlgorithm


__version__ = 1
__all__ = ["evolution_algorithm", "axelrod", "centola", "expandable_model", "klemm"]
