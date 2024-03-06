
#
# Import section
#
import numpy

from syned.beamline.beamline_element import BeamlineElement
from syned.beamline.element_coordinates import ElementCoordinates
from wofry.propagator.propagator import PropagationManager, PropagationElements, PropagationParameters

from wofry.propagator.wavefront2D.generic_wavefront import GenericWavefront2D

from wofryimpl.propagator.propagators2D.fresnel_zoom_xy import FresnelZoomXY2D
from wofryimpl.propagator.propagators2D.fresnel import Fresnel2D
from wofryimpl.propagator.propagators2D.fresnel_convolution import FresnelConvolution2D
from wofryimpl.propagator.propagators2D.fraunhofer import Fraunhofer2D
from wofryimpl.propagator.propagators2D.integral import Integral2D
from wofryimpl.propagator.propagators2D.fresnel_zoom_xy import FresnelZoomXY2D

from srxraylib.plot.gol import plot, plot_image
plot_from_oe = 1 # set to a large number to avoid plots


##########  SOURCE ##########


#
# create output_wavefront
#
#
from orangecontrib.esrf.wofry.util.light_source import WOPySRULightSource # TODO: from wofryimpl...
light_source = WOPySRULightSource.initialize_from_keywords(
    energy_in_GeV=6,
    current=0.2,
    K_vertical=1.68118,
    period_length=0.025,
    number_of_periods=188,
    distance=100,
    gapH=0.006,
    gapV=0.006,
    photon_energy=5591,
    h_slit_points=101,
    v_slit_points=101,)

output_wavefront = light_source.get_wavefront()


if plot_from_oe <= 1000: plot_image(output_wavefront.get_intensity(),output_wavefront.get_coordinate_x(),output_wavefront.get_coordinate_y(),aspect='auto',title='SOURCE')