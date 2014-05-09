import logging
import datetime

import M2Crypto.X509

_logger = logging.getLogger(__name__)

def build_name_from_dict(**kwargs):
    name = M2Crypto.X509.X509_Name()
    for (k, v) in kwargs.items():
        try:
            M2Crypto.X509.X509_Name.nid[k]
        except KeyError as e:
            raise KeyError(k)

        setattr(name, k, v)

    return name

def get_delta_from_validity_phrase(validity_phrase):
    def _translate_years_to_seconds(years):
        now_dt = datetime.datetime.now()
        now_future_dt = now_dt.replace(year=(now_dt.year + years))
        return (now_future_dt - now_dt).total_seconds()

    try:
        validity_y = int(validity_phrase)
    except ValueError:
        if validity_phrase == '':
            raise ValueError("Validity is empty.")
        
        suffix = validity_phrase[-1].lower()
        validity = int(validity_phrase[:-1])

        if suffix == 'y':
            validity_s = _translate_years_to_seconds(validity)
        elif suffix == 'd':
            validity_s = validity * 86400
        elif suffix != 's':
            raise ValueError("Validity suffix [%s] not valid. Please use 's', "
                             "'d', or 'y'.")
    else:
        validity_s = _translate_years_to_seconds(validity_y)

    return datetime.timedelta(seconds=validity_s)
