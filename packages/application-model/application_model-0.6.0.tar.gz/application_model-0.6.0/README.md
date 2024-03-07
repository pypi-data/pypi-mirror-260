# Application Model

`application_model` package generate application score for new customers.

Training details:
1. **Cohorts**: from 2022-01 to 2023-04
2. **Target**: over60mob6
3. **Features set**: Ume, Bvs-Income, Bvs-P5 and Bvs-P5-Subscores

More details in [Documentation](https://scudraservicos.github.io/application_model/)

## Installation

[PyPI Package](https://pypi.org/project/application_model/)

```bash
$ pip install application_model
```

## How to use

`generate_application_score` function can be used to generate the application score as follows:

```python
import json
from application_model.application_model import generate_application_score

payload = """
    {
       "ume-profession":"COSTUREIRA",
       "ume-zipcode":69059192.0,
       "ume-age_on_application":63.0,
       "ume-segment":"Móveis",
       "ume-retailer":"apa-moveis",
       "ume-state":"AMAZONAS",
       "bvsIncome-CLASSRENDAV2":6.0,
       "bvsIncome-RendaPresumida":1700.0,
       "bvsP5-Score":0.3009,
       "bvsSubP5-Fintechs":0.4499,
       "bvsSubP5-CartaoCredito":0.3950,
       "bvsSubP5-CreditoPessoal":0.4589,
       "bvsSubP5-VAR_MoveisEletrodomesticos":0.3379,
       "bvsSubP5-VAR_VestuarioAcessorios":0.2430,
       "bvsSubP5-FinancialmentoVeiculos":0.4199
    }
"""

# the payload needs to be casted to json format 
payload_json = json.loads(payload)

# get the score from the payload
score = generate_application_score(payload_json)
```

## Data source

Origin of Ume's attributes

1. **ume-profession**: Ume profession model colected during the customer application. 
2. **ume-zipcode**: Zipcode in numerical format.
3. **ume-age_on_application**: Customer age.
4. **ume-segment**: Data extracted from column `name` in table `prd-ume-data.prd_datastore_public.retailer_categories`.
5. **ume-retailer**: Data extracted from column `name` in table `tabela prd-ume-data.prd_datastore_public.retailers`.
6. **ume-state**: Full name in upper case (e.g. PARÁ).

The Bvs's attributes are extracted from BVS API. Bellow are the instructions that map the payload names to real names.

1. **bvsIncome-CLASSRENDAV2**: `CLASSRENDAV2`
2. **bvsIncome-RendaPresumida**: `RNDRPRPNMMESPFLGBREGV2`
3. **bvsP5-Score**: `SCRCRDPNM06MPFLGBCLFALLV5`
4. **bvsSubP5-Fintechs**: `SCRCRDPNM06MPFLGBCLFBCDV2`
5. **bvsSubP5-CartaoCredito**: `SCRCRDPNMCCRPFLGBCLFBVSV3`
6. **bvsSubP5-CreditoPessoal**: `SCRCRDPNMCRPPFLGBCLFBVSV3`
7. **bvsSubP5-VAR_MoveisEletrodomesticos**: `SCRCRDPNMVARPFLGBCLFBVSV3`
8. **bvsSubP5-VAR_VestuarioAcessorios**: `SCRCRDPNMVARPFLGBCLFBVSV2`
9. **bvsSubP5-FinancialmentoVeiculos**: `SCRCRDPNMVEIPFLGBCLFBVSV3`

## License

`application_model` was created by Wesllen Sousa Lima in Ume corporation. It is licensed under the terms of the Proprietary license.

## Credits

`application_model` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).
