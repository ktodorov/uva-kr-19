from quantity import Quantity
from quantity_dependency import QuantityDependency
from enums.dependency_type import DependencyType
from enums.space_type import SpaceType
from quantity_space import QuantitySpace
from qualitative_model import QualitativeModel
import utils


# define spaces

# inflow spaces
inflow_space1 = QuantitySpace('0')
inflow_space2 = QuantitySpace('+')

# outflow spaces
outflow_space1 = QuantitySpace('0')
outflow_space2 = QuantitySpace('+')
outflow_space3 = QuantitySpace('max')

# volume spaces
volume_space1 = QuantitySpace('0')
volume_space2 = QuantitySpace('+')
volume_space3 = QuantitySpace('max')

# define quantities

sink = Quantity('sink', [])
inflow = Quantity('inflow', [inflow_space1, inflow_space2])
outflow = Quantity('outflow', [outflow_space1, outflow_space2, outflow_space3])
volume = Quantity('volume', [volume_space1, volume_space2, volume_space3])

quantities = [sink, inflow, outflow, volume]

# define dependencies

inflow_volume_dependency = QuantityDependency(
    DependencyType.PositiveInfluence, inflow, volume)
outflow_volume_dependency = QuantityDependency(
    DependencyType.NegativeInfluence, outflow, volume)
volume_outflow_dependency = QuantityDependency(
    DependencyType.PositiveProportionality, volume, outflow)

inflow_sink_dependency = QuantityDependency(
    DependencyType.Default, inflow, sink)
outflow_sink_dependency = QuantityDependency(
    DependencyType.Default, outflow, sink)
volume_sink_dependency = QuantityDependency(
    DependencyType.Default, volume, sink)

dependencies = [
    inflow_volume_dependency,
    outflow_volume_dependency,
    volume_outflow_dependency,
    inflow_sink_dependency,
    outflow_sink_dependency,
    volume_sink_dependency
]

qualitative_model = QualitativeModel(quantities, dependencies)
qualitative_model.visualize_states()

# utils.create_representation_graph(
#     quantities,
#     dependencies,
#     font_size=9,
#     font_color='white',
#     node_size=1500)
