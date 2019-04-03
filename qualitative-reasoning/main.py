from quantity import Quantity
from quantity_dependency import QuantityDependency
from enums.dependency_type import DependencyType
from enums.space_type import SpaceType
from quantity_space import QuantitySpace
from qualitative_model import QualitativeModel
import utils


# define spaces

# inflow spaces
inflow_zero = QuantitySpace('0')
inflow_plus = QuantitySpace('+')

# outflow spaces
outflow_zero = QuantitySpace('0')
outflow_plus = QuantitySpace('+')
outflow_max = QuantitySpace('max')

# volume spaces
volume_zero = QuantitySpace('0')
volume_plus = QuantitySpace('+')
volume_max = QuantitySpace('max')

# define quantities

sink = Quantity('sink', [])
inflow = Quantity('inflow', [inflow_zero, inflow_plus])
outflow = Quantity('outflow', [outflow_zero, outflow_plus, outflow_max])
volume = Quantity('volume', [volume_zero, volume_plus, volume_max])

quantities = [sink, inflow, outflow, volume]

# define dependencies

inflow_volume_dependency = QuantityDependency(
    DependencyType.PositiveInfluence, inflow, volume)
outflow_volume_dependency = QuantityDependency(
    DependencyType.NegativeInfluence, outflow, volume)
volume_outflow_dependency = QuantityDependency(
    DependencyType.PositiveProportionality, volume, outflow)

inflow_sink_dependency = QuantityDependency(
    DependencyType.Constraint, volume, outflow, volume_max, outflow_max)
outflow_sink_dependency = QuantityDependency(
    DependencyType.Constraint, volume, outflow, volume_zero, outflow_zero)

dependencies = [
    inflow_volume_dependency,
    outflow_volume_dependency,
    volume_outflow_dependency,
    inflow_sink_dependency,
    outflow_sink_dependency
]

qualitative_model = QualitativeModel(quantities, dependencies)
qualitative_model.visualize_states()

# utils.create_representation_graph(
#     quantities,
#     dependencies,
#     font_size=9,
#     font_color='white',
#     node_size=1500)
