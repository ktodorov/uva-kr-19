from quantity import Quantity
from quantity_dependency import QuantityDependency
from dependency_type import DependencyType
import utils

sink = Quantity('sink')
inflow = Quantity('inflow')
outflow = Quantity('outflow')
volume = Quantity('volume')

inflow_volume_dependency = QuantityDependency(DependencyType.PositiveInfluence, inflow, volume)
outflow_volume_dependency = QuantityDependency(DependencyType.NegativeInfluence, outflow, volume)
volume_outflow_dependency = QuantityDependency(DependencyType.PositiveProportionality, volume, outflow)

inflow_sink_dependency = QuantityDependency(DependencyType.Default, inflow, sink)
outflow_sink_dependency = QuantityDependency(DependencyType.Default, outflow, sink)
volume_sink_dependency = QuantityDependency(DependencyType.Default, volume, sink)

quantities = [sink, inflow, outflow, volume]
dependencies = [inflow_volume_dependency, outflow_volume_dependency, volume_outflow_dependency, inflow_sink_dependency, outflow_sink_dependency, volume_sink_dependency]

utils.create_representation_graph(
    quantities,
    dependencies, 
    font_size = 9,
    font_color = 'white', 
    node_size = 1500)