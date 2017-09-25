from ThermoPkgs.VaporPressure.interfacePerry import FluidDataPerry,FluidPerryVaporPressure
from ThermoPkgs.VaporPressure.VaporPressure import Perry, Psat
fluido = FluidPerryVaporPressure([31])
fdata = FluidDataPerry(fluido)

a=Perry(fluido, fdata)

print a.computePsat(425.12) # [37.699355118817238]

print Psat(425.12, 31) #37.6993551188

