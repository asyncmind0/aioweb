import os
import csv
import logging
from .model import Nutrient
from aioweb.config import config


def import_sr25_nutr_def(db, loop):
    """
    Columns:
    - Nutr_No  A 3* N Unique 3-digit identifier code for a nutrient. 
    - Units A 7 N Units of measure (mg, g, μg, and so on).
    - Tagname A 20 Y  International Network of Food Data Systems (INFOODS)
        Tagnames.† A unique abbreviation for a nutrient/food
        component developed by INFOODS to aid in the
        interchange of data.
    - NutrDesc A 60 N Name of nutrient/food component.
    - Num_Dec A 1 N Number of decimal places to which a nutrient value is
            rounded.
    - SR_Order N 6 N Used to sort nutrient records in the same order as 
        various reports produced from SR.

    """
    data_path = os.path.join(os.path.dirname(__file__),
                             'data/sr25/NUTR_DEF.txt')
    with open(data_path, 'r', encoding='iso-8859-1') as datafile:
        logger = logging.getLogger("importer")
        reader = csv.reader(datafile, delimiter='^')
        for row in reader:
            row = [col[1:-1] for col in row]
            if not row[2]:
                logger.debug("Skipping: %s" % str(row))
                continue
            nutrient = Nutrient(name=row[3], tag=row[2], unit=row[1],
                                number=row[0], decimal_places=row[4])
            r = loop.run_until_complete(nutrient.save(db))
            assert hasattr(r, 'ok') and r.ok is True
