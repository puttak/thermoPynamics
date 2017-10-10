# thermoPynamics

This is a implementation of some thermodynamics models. 
There's a integrated component database.
The models were programmed in a very reusable way. (See example)

They can calculate: fugacity coefficient, compressibility factor, residual enthalpy.

-Calculations:

1 - Calculation of Hydrates Formation Pressure. (Erickson 1983) [hydrates]

2 - Calculation of JT cooling effect. [JTcooling]

3 - Hydrate limits to gas expansion through a valve [ExpansionHydLimit]

-ThermoPkgs:

1 - SRK EoS (Z, fug. coef., residual enthalpy)

2 - IDEAL (Ideal Gas Cp computation )

3 - PR EoS (Z, fug. coef., residual enthalpy)

4 - UNIFAC (act. coef.)

References:

Critical properties - Perry's Chemical Engineers Handbook, 8th edition.

UNIFAC parameters - http://www.ddbst.com/published-parameters-unifac.html

D. Y. Peng, D. B. Robinson, “A new two-constant equation of state”, Industrial & Engineering Chemistry Fundamentals, 1976, 15: 59-64.
Boukouvalas, C.; Spiliots, N.; Coutsikos, P.; Tzouvaras, N.; Tassios, D. Prediction of Vapor-Liquid Equilibrium with the LCVM Model: a Linear Combination of the Vidal and Michelsen Mixing Rules Coupled with the Original UNIFAC and the t-mPR Equation of State. Fluid Phase Equilib. 1994, 92, 75.

Fredenslund, A.; Jones, R. L.; Prausnitz, J. M. Group-Contribution Estimation of Activity Coefficients in Nonideal Liquid Mixtures. Alche J. v. 21, p. 1086-1099, 1975.
 
SOAVE, G. Equilibrium Constants from a Modified Redlich-Kwong Equation of State. Chemical Engineering Science, v. 27, p. 1197-1203, 1972. 
 
