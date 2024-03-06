# electron beam
from shadow4.sources.s4_electron_beam import S4ElectronBeam

electron_beam = S4ElectronBeam(energy_in_GeV=1.9, energy_spread=0.001, current=0.4)
electron_beam.set_sigmas_all(sigma_x=3.9e-05, sigma_y=3.1e-05, sigma_xp=3.92e-05, sigma_yp=3.92e-05)

# magnetic structure
from shadow4.sources.wiggler.s4_wiggler import S4Wiggler

source = S4Wiggler(
    magnetic_field_periodic=0,  # 0=external, 1=periodic
    file_with_magnetic_field="https://raw.githubusercontent.com/srio/shadow4/master/examples/sources/BM_multi.b",
    # used only if magnetic_field_periodic=0
    K_vertical=10.0,  # syned Wiggler pars: used only if magnetic_field_periodic=1
    period_length=0.1,  # syned Wiggler pars: used only if magnetic_field_periodic=1
    number_of_periods=10,  # syned Wiggler pars: used only if magnetic_field_periodic=1
    emin=0.4,  # Photon energy scan from energy (in eV)
    emax=0.4,  # Photon energy scan to energy (in eV)
    ng_e=1,  # Photon energy scan number of points for spectrum and internal calculation
    ng_j=501,  # Number of points in electron trajectory (per period) for internal calculation only
    epsi_dx=0.0,  # distance to waist in X [m]
    epsi_dz=0.0,  # distance to waist in Z [m]
    psi_interval_number_of_points=101,  # the number psi (vertical angle) points for internal calculation only
    flag_interpolation=2,  # Use interpolation to sample psi (0=No, 1=Yes)
    flag_emittance=1,  # Use emittance (0=No, 1=Yes)
    shift_x_flag=0,  # 0="No shift", 1="Half excursion", 2="Minimum", 3="Maximum", 4="Value at zero", 5="User value"
    shift_x_value=0.0,  # used only if shift_x_flag=5
    shift_betax_flag=0,  # 0="No shift", 1="Half excursion", 2="Minimum", 3="Maximum", 4="Value at zero", 5="User value"
    shift_betax_value=0.0,  # used only if shift_betax_flag=5
)

# light source
from shadow4.sources.wiggler.s4_wiggler_light_source import S4WigglerLightSource

light_source = S4WigglerLightSource(name='wiggler', electron_beam=electron_beam, magnetic_structure=source, nrays=500,
                                    seed=5676561)
beam = light_source.get_beam()

# test plot
from srxraylib.plot.gol import plot_scatter

rays = beam.get_rays()
plot_scatter(1e6 * rays[:, 0], 1e6 * rays[:, 2], title='(X,Z) in microns')