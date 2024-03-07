# Thermodynamic data

This folder contains a copy of the experimental thermochemistry data used in the
reaction-network code.

## FREED _(data/freed/compounds.json.gz)_

This is an extraction of the Gibbs free energies of formation data from the FREED Thermodynamic
Database, which is a computer adaptation of the U.S. Bureau of Mines thermodynamic
database and some other exxtra sources.

Reference:

    Morris, Arthur E.; 2019. https://www.thermart.net/freed-thermodynamic-database/

## NIST-JANAF _(data/nist/compounds.json.gz)_

This is a copy of all thermochemical data from the 4th edition of the NIST-JANAF tables,
as gathered from the NIST-JANAF website.

Reference:

    Malcolm W. Chase, J. NIST-JANAF Thermochemical Tables; Fourth edition. Washington, DC: American Chemical Society; New York : American Institute of Physics for the National Institute of Standards and Technology, 1998., 1998.

## FactSage _(data/mu_elements.json)_

This is a copy of the Gibbs energies of elements, as used in FactSage. These are used
according within the `GibbsComputedEntry` class.

Reference:

    Bale, C. W.; Chartrand, P.; Degterov, S. A.; Eriksson, G.; Hack, K.; Ben Mahfoud, R.; Melançon, J.; Pelton, A. D.; Petersen, S. FactSage Thermochemical Software and Databases. Calphad 2002, 26 (2), 189–228. https://doi.org/10.1016/S0364-5916(02)00035-4.
