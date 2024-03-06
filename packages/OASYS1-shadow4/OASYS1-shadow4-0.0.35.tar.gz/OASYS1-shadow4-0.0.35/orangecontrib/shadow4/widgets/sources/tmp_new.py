
# electron beam
from shadow4.sources.s4_electron_beam import S4ElectronBeam
electron_beam = S4ElectronBeam(energy_in_GeV=6,energy_spread=1e-08,current=0.2)
electron_beam.set_sigmas_all(sigma_x=0,sigma_y=0,sigma_xp=0,sigma_yp=0)

# magnetic structure
from shadow4.sources.undulator.s4_undulator_gaussian import S4UndulatorGaussian
source = S4UndulatorGaussian(
    period_length     = 0.02,     # syned Undulator parameter (length in m)
    number_of_periods = 100, # syned Undulator parameter
    photon_energy     = 10000.0, # Photon energy (in eV)
    delta_e           = 0.0, # Photon energy width (in eV)
    ng_e              = 1, # Photon energy scan number of points
    flag_emittance    = 0, # when sampling rays: Use emittance (0=No, 1=Yes)
    flag_energy_spread = 0, # when sampling rays: Use e- energy spread (0=No, 1=Yes)
    harmonic_number    = 1, # harmonic number
    flux_peak          = 1.0, # value to set the flux peak
    )


# light source
from shadow4.sources.undulator.s4_undulator_gaussian_light_source import S4UndulatorGaussianLightSource
light_source = S4UndulatorGaussianLightSource(name='GaussianUndulator', electron_beam=electron_beam, magnetic_structure=source,nrays=50000,seed=5676561)
beam = light_source.get_beam()

# test plot
from srxraylib.plot.gol import plot_scatter
rays = beam.get_rays()
plot_scatter(1e6 * rays[:, 0], 1e6 * rays[:, 2], title='(X,Z) in microns')

print(rays[:, 0].std())
print(rays[:, 2].std())
print(rays[:, 3].std())
print(rays[:, 5].std())