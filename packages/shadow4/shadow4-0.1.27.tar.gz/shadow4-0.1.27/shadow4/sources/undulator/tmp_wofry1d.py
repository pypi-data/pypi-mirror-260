
#
# Import section
#
import numpy

from syned.beamline.beamline_element import BeamlineElement
from syned.beamline.element_coordinates import ElementCoordinates
from wofry.propagator.propagator import PropagationManager, PropagationElements, PropagationParameters

from wofry.propagator.wavefront1D.generic_wavefront import GenericWavefront1D

from wofryimpl.propagator.propagators1D.fresnel import Fresnel1D
from wofryimpl.propagator.propagators1D.fresnel_convolution import FresnelConvolution1D
from wofryimpl.propagator.propagators1D.fraunhofer import Fraunhofer1D
from wofryimpl.propagator.propagators1D.integral import Integral1D
from wofryimpl.propagator.propagators1D.fresnel_zoom import FresnelZoom1D
from wofryimpl.propagator.propagators1D.fresnel_zoom_scaling_theorem import FresnelZoomScaling1D

from srxraylib.plot.gol import plot, plot_image
plot_from_oe = 0 # set to a large number to avoid plots


##########  SOURCE ##########


#
# create output_wavefront
#
#
from wofryimpl.propagator.util.undulator_coherent_mode_decomposition_1d import UndulatorCoherentModeDecomposition1D
coherent_mode_decomposition = UndulatorCoherentModeDecomposition1D(
    electron_energy=6,
    electron_current=0.2,
    undulator_period=0.025,
    undulator_nperiods=188,
    K=1.68118,
    photon_energy=5666.66, # 5591,
    abscissas_interval=0.00025,
    number_of_points=300,
    distance_to_screen=100,
    magnification_x_forward=100,
    magnification_x_backward=0.01,
    scan_direction='V',
    sigmaxx=3.7e-06,
    sigmaxpxp=1.5e-06,
    useGSMapproximation=False,
    e_energy_dispersion_flag=0,
    e_energy_dispersion_sigma_relative=0.001,
    e_energy_dispersion_interval_in_sigma_units=6,
    e_energy_dispersion_points=11)

# make calculation
coherent_mode_decomposition_results = coherent_mode_decomposition.calculate()

# mode_index = 0
# output_wavefront = coherent_mode_decomposition.get_eigenvector_wavefront(mode_index)

output_wavefront = coherent_mode_decomposition.far_field_wavefront


if plot_from_oe <= 0: plot(output_wavefront.get_abscissas(), output_wavefront.get_intensity(),title='SOURCE')


##########  OPTICAL SYSTEM ##########





##########  OPTICAL ELEMENT NUMBER 1 ##########



input_wavefront = output_wavefront.duplicate()
from syned.beamline.shape import Rectangle
boundary_shape=Rectangle(-0.5, 0.5, -0.5, 0.5)
from wofryimpl.beamline.optical_elements.absorbers.slit import WOSlit1D
optical_element = WOSlit1D(boundary_shape=boundary_shape)

# drift_before 100 m
#
# propagating
#
#
propagation_elements = PropagationElements()
beamline_element = BeamlineElement(optical_element=optical_element,    coordinates=ElementCoordinates(p=-100.000000,    q=0.000000,    angle_radial=numpy.radians(0.000000),    angle_azimuthal=numpy.radians(0.000000)))
propagation_elements.add_beamline_element(beamline_element)
propagation_parameters = PropagationParameters(wavefront=input_wavefront,    propagation_elements = propagation_elements)
#self.set_additional_parameters(propagation_parameters)
#
# propagation_parameters.set_additional_parameters('magnification_x', 30.0)
propagation_parameters.set_additional_parameters('magnification_x', 0.01)
#
propagator = PropagationManager.Instance()
try:
    propagator.add_propagator(FresnelZoom1D())
except:
    pass
output_wavefront = propagator.do_propagation(propagation_parameters=propagation_parameters,    handler_name='FRESNEL_ZOOM_1D')


#
#---- plots -----
#
if plot_from_oe <= 1: plot(output_wavefront.get_abscissas(),output_wavefront.get_intensity(),title='OPTICAL ELEMENT NR 1')