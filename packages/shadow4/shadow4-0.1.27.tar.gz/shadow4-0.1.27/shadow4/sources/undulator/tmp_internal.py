
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
plot_from_oe = 0 # set to a large number to avoid plots


from pySRU.Simulation import create_simulation
from pySRU.ElectronBeam import ElectronBeam as PysruElectronBeam
from pySRU.MagneticStructureUndulatorPlane import MagneticStructureUndulatorPlane as PysruUndulator
from pySRU.TrajectoryFactory import TRAJECTORY_METHOD_ANALYTIC
from pySRU.RadiationFactory import RADIATION_METHOD_APPROX_FARFIELD

def _calculate_pysru(X,
                     Y,
                     number_of_trajectory_points=20,
                     NPERIODS=188,
                     K=1.681183,
                     LAMBDAU=0.025,
                     E_ENERGY=6.0,
                     INTENSITY=0.2,
                     photon_energy=5591.0,
                     distance=100,
                     ):

    Nb_pts_trajectory = int(number_of_trajectory_points * NPERIODS)

    simulation_test = create_simulation(magnetic_structure=PysruUndulator(
                                        K=K,
                                        period_length=LAMBDAU,
                                        length=LAMBDAU * NPERIODS),
        electron_beam=PysruElectronBeam(
                                        Electron_energy=E_ENERGY,
                                        I_current=INTENSITY),
        magnetic_field=None,
        photon_energy=photon_energy,
        traj_method=TRAJECTORY_METHOD_ANALYTIC,
        Nb_pts_trajectory=Nb_pts_trajectory,  # None,
        rad_method=RADIATION_METHOD_APPROX_FARFIELD,
        initial_condition=None,
        distance=distance,
        X=X,
        Y=Y,
        XY_are_list=True)

    E = simulation_test.electric_field._electrical_field
    return E
    #     tmp_x = E[:, 0].copy()
    #     tmp_y = E[:, 1].copy()
    #     tmp_x.shape = (theta.size, phi.size)
    #     tmp_y.shape = (theta.size, phi.size)
    #
    #     EFIELD_X[ie, :, :] = tmp_x
    #     EFIELD_Y[ie, :, :] = tmp_y
    #
    #     POL_DEG[ie, :, :] = numpy.abs(tmp_x) / (numpy.abs(tmp_x) + numpy.abs(tmp_y))  # SHADOW definition
    # print("Done calculating radiation...")
    # print(">>>>>>>> EFIELD_X: ", EFIELD_X.shape)
    #
    # radiation = numpy.abs(EFIELD_X) ** 2 + numpy.abs(EFIELD_Y) ** 2
    # out = {'radiation': radiation,
    #        'polarization': POL_DEG,
    #        'photon_energy': E,
    #        'theta': theta,
    #        'phi': phi,
    #        'trajectory': None,  # T,
    #        'e_amplitude_sigma': EFIELD_X,  # todo: verify!
    #        'e_amplitude_pi': EFIELD_Y,  # todo: verify!
    #        }

def _propagate_complex_amplitude_from_arrays(
                                            amplitude_flatten,
                                            X_flatten,
                                            Y_flatten,
                                            det_X_flatten=None,
                                            det_Y_flatten=None,
                                            wavelength=1e-10,
                                            propagation_distance=100,
                                            shuffle_interval=0,
                                            ):
    #
    # Fresnel-Kirchhoff integral (neglecting inclination factor)
    #
    if det_X_flatten is None: det_X_flatten = X_flatten
    if det_Y_flatten is None: det_Y_flatten = Y_flatten

    ngood = det_X_flatten.size

    fla_complex_amplitude_propagated = numpy.zeros(ngood, dtype=complex)

    Propagation_distance = numpy.ones_like(X_flatten) * propagation_distance

    wavenumber = 2 * numpy.pi / wavelength

    for i in range(ngood):
        if shuffle_interval == 0:
            rd_x = 0.0
            rd_y = 0.0
        else:
            r = numpy.sqrt(X_flatten**2 + Y_flatten**2)
            interval = (r.max() - r.min()) / r.size
            rd_x = (numpy.random.rand(X_flatten.size) - 0.5) * interval
            rd_y = (numpy.random.rand(Y_flatten.size) - 0.5) * interval



        r = numpy.sqrt( (X_flatten + rd_x - det_X_flatten[i])**2 +
                        (Y_flatten + rd_y - det_Y_flatten[i])**2 +
                        Propagation_distance**2 )

        fla_complex_amplitude_propagated[i] = (amplitude_flatten / r * numpy.exp(1.j * wavenumber *  r)).sum()


    # # added srio@esrf.eu 2018-03-23 to conserve energy - TODO: review method!
    # i0 = numpy.abs(amplitude_flatten)**2
    # i1 = numpy.abs(fla_complex_amplitude_propagated)**2
    # fla_complex_amplitude_propagated *= i0.sum() / i1.sum()

    return fla_complex_amplitude_propagated


if __name__ == "__main__":
    ##########  SOURCE ##########


    #
    # create output_wavefront
    #
    #
    # from wofryimpl.propagator.light_source_pysru import WOPySRULightSource
    # light_source = WOPySRULightSource.initialize_from_keywords(
    #     energy_in_GeV=6,
    #     current=0.2,
    #     K_vertical=1.68118,
    #     period_length=0.025,
    #     number_of_periods=188,
    #     distance=100,
    #     gapH=0.006,
    #     gapV=0.006,
    #     photon_energy=5591,
    #     h_slit_points=100,
    #     v_slit_points=100,
    #     number_of_trajectory_points=2820,
    #     traj_method=1, # 0=TRAJECTORY_METHOD_ANALYTIC, 1=TRAJECTORY_METHOD_ODE
    #     rad_method=2, # 0=RADIATION_METHOD_NEAR_FIELD, 1= RADIATION_METHOD_APPROX, 2=RADIATION_METHOD_APPROX_FARFIELD
    #     )
    #
    # output_wavefront = light_source.get_wavefront()

    # light_source = self.get_light_source()
    # self.wavefront2D = light_source.get_wavefront()

    output_wavefront = GenericWavefront2D.load_h5_file("/users/srio/Oasys/tmp.h5","wfr")

    if plot_from_oe <= 0: plot_image(output_wavefront.get_intensity(),output_wavefront.get_coordinate_x(),output_wavefront.get_coordinate_y(),aspect='auto',title='SOURCE')


    ##########  OPTICAL SYSTEM ##########





    ##########  OPTICAL ELEMENT NUMBER 1 ##########



    input_wavefront = output_wavefront.duplicate()
    from wofryimpl.beamline.optical_elements.ideal_elements.screen import WOScreen

    optical_element = WOScreen()

    # drift_after -100 m
    #
    # propagating
    #
    #
    method = 2 # 0=pysru+wofry, 1=pysru+ad hoc, 2=polar+ad hoc

    if method == 0:
        propagation_elements = PropagationElements()
        beamline_element = BeamlineElement(optical_element=optical_element,    coordinates=ElementCoordinates(p=0.000000,    q=-100.000000,    angle_radial=numpy.radians(0.000000),    angle_azimuthal=numpy.radians(0.000000)))
        propagation_elements.add_beamline_element(beamline_element)
        propagation_parameters = PropagationParameters(wavefront=input_wavefront,    propagation_elements = propagation_elements)
        #self.set_additional_parameters(propagation_parameters)
        #
        propagation_parameters.set_additional_parameters('shuffle_interval', 0)
        propagation_parameters.set_additional_parameters('calculate_grid_only', 1)
        propagation_parameters.set_additional_parameters('magnification_x', 0.025)
        propagation_parameters.set_additional_parameters('magnification_y', 0.025)
        #
        propagator = PropagationManager.Instance()
        try:
            propagator.add_propagator(Integral2D())
        except:
            pass
        output_wavefront = propagator.do_propagation(propagation_parameters=propagation_parameters,    handler_name='INTEGRAL_2D')



        # fla_complex_amplitude_propagated.shape = (x.size, y.size)
        # output_wavefront = GenericWavefront2D.initialize_wavefront_from_arrays(x * 0.025, y * 0.025,
        #                                                                        fla_complex_amplitude_propagated,
        #                                                                        wavelength=wavelength)
        #
        # ---- plots -----
        #
        if plot_from_oe <= 1: plot_image(output_wavefront.get_intensity(), output_wavefront.get_coordinate_x(),
                                         output_wavefront.get_coordinate_y(), aspect='auto', title='OPTICAL ELEMENT NR 1')

        x = output_wavefront.get_coordinate_x()
        y = output_wavefront.get_coordinate_y()
        ii = output_wavefront.get_intensity()
        ii /= ii.max()
        plot(x, ii[:, y.size // 2],
             y, ii[x.size // 2, :],
             legend=['x','y'])
    elif method == 1:
        ca = input_wavefront.get_complex_amplitude()
        x = input_wavefront.get_coordinate_x()
        y = input_wavefront.get_coordinate_y()
        X = numpy.outer(x, numpy.ones_like(y))
        Y = numpy.outer(numpy.ones_like(x), y)
        wavelength = input_wavefront.get_wavelength()
        print(ca.shape, x.shape, y.shape, wavelength)

        # x_axis = x # numpy.concatenate((x, numpy.zeros_like(y)))
        # y_axis = y # numpy.concatenate((numpy.zeros_like(x), y))
        x_axis = numpy.linspace(x.min(), x.max(), 1000)
        y_axis = numpy.linspace(y.min(), y.max(), 1000)
        fla_complex_amplitude_propagated_x_axis = _propagate_complex_amplitude_from_arrays(
            ca.flatten(),
            X.flatten(),
            Y.flatten(),
            det_X_flatten=x_axis * 0.025, #X.flatten() * 0.025,
            det_Y_flatten=y_axis * 0, #Y.flatten() * 0.025,
            wavelength=wavelength,
            propagation_distance=-100)
        fla_complex_amplitude_propagated_y_axis = _propagate_complex_amplitude_from_arrays(
            ca.flatten(),
            X.flatten(),
            Y.flatten(),
            det_X_flatten=x_axis * 0, #X.flatten() * 0.025,
            det_Y_flatten=y_axis * 0.025, #Y.flatten() * 0.025,
            wavelength=wavelength,
            propagation_distance=-100)

        ii_x = numpy.abs(fla_complex_amplitude_propagated_x_axis)**2
        ii_y = numpy.abs(fla_complex_amplitude_propagated_y_axis)**2
        ii_x /= ii_x.max()
        ii_y /= ii_y.max()
        plot(x_axis * 0.025, ii_x,
             y_axis * 0.025, ii_y,
             legend=['x','y'])

        tmp = numpy.zeros((x_axis.size, y_axis.size), dtype=complex)
        tmp[:, y_axis.size // 2] = fla_complex_amplitude_propagated_x_axis
        tmp[x_axis.size // 2, :] = fla_complex_amplitude_propagated_y_axis
        output_wavefront = GenericWavefront2D.initialize_wavefront_from_arrays(x_axis * 0.025, y_axis * 0.025,
                                                                               tmp,
                                                                               wavelength=wavelength)

        #
        # ---- plots -----
        #
        if plot_from_oe <= 1: plot_image(output_wavefront.get_intensity(), output_wavefront.get_coordinate_x(),
                                         output_wavefront.get_coordinate_y(), aspect='auto', title='OPTICAL ELEMENT NR 1')

    elif method == 2:

        ca = input_wavefront.get_complex_amplitude()
        x_in = input_wavefront.get_coordinate_x()
        y_in = input_wavefront.get_coordinate_y()
        print(x_in.min(), x_in.max(), y_in.min(), y_in.max())
        #
        # polar grid
        #
        distance = 100.0
        MAXANGLE = x_in.max() / distance
        NG_T = 101
        NG_P = 11
        theta = numpy.linspace(-MAXANGLE, MAXANGLE, NG_T, dtype=float)
        phi = (numpy.arange(NG_P) / NG_P - 0.5) * numpy.pi

        THETA = numpy.outer(theta, numpy.ones_like(phi))
        PHI = numpy.outer(numpy.ones_like(theta), phi)
        R = distance / numpy.cos(THETA)
        r = R * numpy.sin(THETA)
        xx = r * numpy.cos(PHI)
        yy = r * numpy.sin(PHI)

        E = _calculate_pysru(xx.flatten(),
                              yy.flatten(),
                              )

        tmp_x = E[:, 0].copy()
        tmp_y = E[:, 1].copy()


        intensity = numpy.abs(tmp_x)**2
        intensity.shape = (theta.size, phi.size)

        try:
            plot(THETA, intensity[:,0],
                 THETA, intensity[:, 1],
                 THETA, intensity[:, 2],
                 THETA, intensity[:, 3],
                 THETA, intensity[:, 4],
                 THETA, intensity[:, 5],
                 THETA, intensity[:, 6],
                 THETA, intensity[:, 7],
                 THETA, intensity[:, 8],
                 THETA, intensity[:, 9],
                 THETA, intensity[:, 10],
                 title="source",
                 )
        except:
            pass
        # tmp_x.shape = (theta.size, phi.size)
        # tmp_y.shape = (theta.size, phi.size)



        # X = numpy.outer(x, numpy.ones_like(y))
        # Y = numpy.outer(numpy.ones_like(x), y)
        wavelength = input_wavefront.get_wavelength()
        # print(ca.shape, x.shape, y.shape, wavelength)
        #
        # x_in = numpy.linspace(x_in.min(), x_in.max(), 1000)
        # y_in = numpy.linspace(y_in.min(), y_in.max(), 1000)
        # x_axis = numpy.concatenate((x_in, numpy.zeros_like(y_in)))
        # y_axis = numpy.concatenate((numpy.zeros_like(x_in), y_in))


        x_axis = numpy.linspace(x_in.min(), x_in.max(), 1000)
        y_axis = numpy.linspace(y_in.min(), y_in.max(), 1000)

        print(">>>>>>E, xx.flatten, yy.flatten", tmp_x.shape, xx.flatten().shape, yy.flatten().shape, x_axis.shape, y_axis.shape)
        fla_complex_amplitude_propagated_x_axis = _propagate_complex_amplitude_from_arrays(
            tmp_x,
            xx.flatten(),
            yy.flatten(),
            det_X_flatten=x_axis * 0.025,  # X.flatten() * 0.025,
            det_Y_flatten=y_axis * 0,  # Y.flatten() * 0.025,
            wavelength=wavelength,
            propagation_distance=-distance)

        fla_complex_amplitude_propagated_y_axis = _propagate_complex_amplitude_from_arrays(
            tmp_x,
            xx.flatten(),
            yy.flatten(),
            det_X_flatten=x_axis * 0,  # X.flatten() * 0.025,
            det_Y_flatten=y_axis * 0.025,  # Y.flatten() * 0.025,
            wavelength=wavelength,
            propagation_distance=-distance)

        # area = (x_axis[1] - x_axis[0]) * numpy.abs(x_axis) * 2 * numpy.pi
        # x_norm = 1.0 / (0.025**2 * area)
        # print(x_norm)
        # plot(x_axis * 0.025, x_norm)
        ii_x = numpy.abs(fla_complex_amplitude_propagated_x_axis) ** 2
        ii_y = numpy.abs(fla_complex_amplitude_propagated_y_axis) ** 2
        ii_x /= ii_x.max()
        ii_y /= ii_y.max()
        plot(x_axis * 0.025, ii_x,
             y_axis * 0.025, ii_y,
             legend=['x axis', 'y axis'])


        #
        # plot(x_axis * 0.025, numpy.abs(fla_complex_amplitude_propagated) ** 2,
        #      y_axis * 0.025, numpy.abs(fla_complex_amplitude_propagated) ** 2,
        #      legend=['x', 'y'])
        #

        #
        # tmp = numpy.zeros((x.size, y.size), dtype=complex)
        # tmp[:, y.size // 2] = fla_complex_amplitude_propagated[0:x.size]
        # tmp[x.size // 2, :] = fla_complex_amplitude_propagated[x.size:]
        # output_wavefront = GenericWavefront2D.initialize_wavefront_from_arrays(x * 0.025, y * 0.025,
        #                                                                        tmp,
        #                                                                        wavelength=wavelength)



