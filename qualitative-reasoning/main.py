from quantity import Quantity
from quantity_dependency import QuantityDependency
from enums.dependency_type import DependencyType
from enums.space_type import SpaceType
from quantity_space import QuantitySpace
from qualitative_model import QualitativeModel
import utils


# Define possible values

# Inflow possible values
inflow_zero = QuantitySpace('0')
inflow_plus = QuantitySpace('+')

# Outflow possible values
outflow_zero = QuantitySpace('0')
outflow_plus = QuantitySpace('+')
outflow_max = QuantitySpace('max')

# Volume possible values
volume_zero = QuantitySpace('0')
volume_plus = QuantitySpace('+')
volume_max = QuantitySpace('max')

# define quantities

# sink = Quantity('sink', [])
inflow = Quantity('Inflow', [inflow_zero, inflow_plus], ['+', '0', '-'])
outflow = Quantity(
    'Outflow', [outflow_zero, outflow_plus, outflow_max], ['+', '0', '-'])
volume = Quantity(
    'Volume', [volume_zero, volume_plus, volume_max], ['+', '0', '-'])

quantities = [inflow, outflow, volume]

# Define dependencies

# Influences

inflow_volume_dependency = QuantityDependency(
    dependency_type=DependencyType.PositiveInfluence,
    start_quantity=inflow,
    end_quantity=volume)

outflow_volume_dependency = QuantityDependency(
    dependency_type=DependencyType.NegativeInfluence,
    start_quantity=outflow,
    end_quantity=volume)

volume_outflow_dependency = QuantityDependency(
    dependency_type=DependencyType.PositiveProportionality,
    start_quantity=volume,
    end_quantity=outflow)

# Given constraints

inflow_sink_dependency = QuantityDependency(
    dependency_type=DependencyType.Constraint,
    start_quantity=volume,
    end_quantity=outflow,
    start_quantity_values=[volume_max],
    end_quantity_values=[outflow_max])

outflow_sink_dependency = QuantityDependency(
    dependency_type=DependencyType.Constraint,
    start_quantity=volume,
    end_quantity=outflow,
    start_quantity_values=[volume_zero],
    end_quantity_values=[outflow_zero])

# Assumed constraints

in_sink_dependency = QuantityDependency(
    dependency_type=DependencyType.Constraint,
    start_quantity=outflow,
    end_quantity=volume,
    start_quantity_values=[outflow_max],
    end_quantity_values=[volume_max])

out_sink_dependency = QuantityDependency(
    dependency_type=DependencyType.Constraint,
    start_quantity=outflow,
    end_quantity=volume,
    start_quantity_values=[outflow_zero],
    end_quantity_values=[volume_zero])

#if the volume value is 0 the outflow value cannot be 0

volume_outflow_value_dependency = QuantityDependency(
    dependency_type=DependencyType.Constraint,
    start_quantity=volume,
    end_quantity=outflow,
    start_quantity_values=[volume_plus, volume_max],
    end_quantity_values=[outflow_plus, outflow_max])

# if inflow value is 0, volume can not be increasing

inflow_volume_value_dependency = QuantityDependency(
    dependency_type=DependencyType.Constraint,
    start_quantity=inflow,
    end_quantity=volume,
    start_quantity_values=[inflow_zero],
    end_quantity_gradients=['-', '0'])

# if inflow value is 0, outflow can not be increasing

inflow_outflow_value_dependency = QuantityDependency(
    dependency_type=DependencyType.Constraint,
    start_quantity=inflow,
    end_quantity=outflow,
    start_quantity_values=[inflow_zero],
    end_quantity_gradients=['-', '0'])

# if volume is 0, inflow cannot be [+,-]

volume_inflow_value_dependency = QuantityDependency(
    dependency_type=DependencyType.Constraint,
    start_quantity=volume,
    end_quantity=inflow,
    start_quantity_values=[outflow_zero],
    start_quantity_gradients=['0'],
    end_quantity_gradients=['+', '0'])

# group all dependencies together

dependencies = [
    inflow_volume_dependency,
    outflow_volume_dependency,
    volume_outflow_dependency,
    inflow_sink_dependency,
    outflow_sink_dependency,
    inflow_volume_value_dependency,
    inflow_outflow_value_dependency,
    in_sink_dependency,
    out_sink_dependency,
    volume_inflow_value_dependency

    # volume_outflow_value_dependency
]


# Initialize and execute the qualitative model

qualitative_model = QualitativeModel(quantities, dependencies)
qualitative_model.visualize_states()

