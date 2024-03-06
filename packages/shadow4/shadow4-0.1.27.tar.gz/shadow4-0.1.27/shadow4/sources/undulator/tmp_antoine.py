#
#
#
from shadow4.sources.source_geometrical.source_geometrical import SourceGeometrical

light_source = SourceGeometrical(name='SourceGeometrical', nrays=10000, seed=5676561)
light_source.set_spatial_type_gaussian(sigma_h=4e-05, sigma_v=0.000007)
light_source.set_depth_distribution_off()
light_source.set_angular_distribution_gaussian(sigdix=0.002400, sigdiz=0.001000)
light_source.set_energy_distribution_singleline(860.000000, unit='eV')
light_source.set_polarization(polarization_degree=1.000000, phase_diff=0.000000, coherent_beam=0)
beam = light_source.get_beam()

# optical element number XX
boundary_shape = None

from shadow4.beamline.optical_elements.mirrors.s4_sphere_mirror import S4SphereMirror

optical_element = S4SphereMirror(name='Sphere Mirror', boundary_shape=boundary_shape,
                                 surface_calculation=0, is_cylinder=1, cylinder_direction=0,
                                 convexity=1, radius=1.000000, p_focus=10.950000, q_focus=15.250000,
                                 grazing_angle=0.026180,
                                 f_reflec=0, f_refl=0, file_refl='<none>', refraction_index=0.99999 + 0.001j,
                                 coating_material='Si', coating_density=2.33, coating_roughness=0)

from syned.beamline.element_coordinates import ElementCoordinates

coordinates = ElementCoordinates(p=10.95, q=0, angle_radial=1.54462, angle_azimuthal=1.5708, angle_radial_out=1.54462)
movements = None
from shadow4.beamline.optical_elements.mirrors.s4_sphere_mirror import S4SphereMirrorElement

beamline_element = S4SphereMirrorElement(optical_element=optical_element, coordinates=coordinates, movements=movements,
                                         input_beam=beam)

beam, mirr = beamline_element.trace_beam()

# test plot
if True:
    from srxraylib.plot.gol import plot_scatter

    plot_scatter(beam.get_photon_energy_eV(nolost=1), beam.get_column(23, nolost=1), title='(Intensity,Photon Energy)',
                 plot_histograms=0)
    plot_scatter(1e6 * beam.get_column(1, nolost=1), 1e6 * beam.get_column(3, nolost=1), title='(X,Z) in microns')


########################################################################
import numpy

from shadow4.beamline.optical_elements.mirrors.s4_mirror import S4MirrorElement
from shadow4.beamline.optical_elements.gratings.s4_grating import S4GratingElement

input_beam       = beamline_element.get_input_beam().duplicate()
# input_beam.rays  = input_beam.rays[good_only_cursor]

optical_element  = beamline_element.get_optical_element().duplicate()

v_in = input_beam.get_columns([4, 5, 6])

if   isinstance(beamline_element, S4MirrorElement):  _, normal = optical_element.apply_mirror_reflection(input_beam)
elif isinstance(beamline_element, S4GratingElement): _, normal = optical_element.apply_grating_diffraction(input_beam)

v_out = input_beam.get_columns([4, 5, 6])

angle_in = numpy.arccos(v_in[0,:] * normal[0,:] +
                        v_in[1,:] * normal[1,:] +
                        v_in[2,:] * normal[2,:])

angle_out = numpy.arccos(v_out[0,:] * normal[0,:] +
                         v_out[1,:] * normal[1,:] +
                         v_out[2,:] * normal[2,:])

incidence_angle  = (numpy.pi / 2) - angle_in  # grazing angles
reflection_angle = (numpy.pi / 2) - angle_out # grazing angles
print(numpy.degrees(incidence_angle))
print(numpy.degrees(reflection_angle))