import json
from decimal import Decimal as D  # noqa: N817

from .calculate import Zscore
from .constant import REPO_DIR, WHO_TABLES
from .extract_value import LmsBoxCox
from .table import Table
TABLE_REPO = REPO_DIR / 'tables'
GROWTH_CHART = {}


def setup_tables():
    for t in WHO_TABLES:
        table_name, _, _ = t.split('.')[0].rpartition('_')
        table = Table(TABLE_REPO / t)
        table.load_table()
        table.add_value()
        new_table = table.append_value()
        GROWTH_CHART[table_name] = new_table


setup_tables()


def z_score_calculation(lms_box_cox: LmsBoxCox) -> float:
    lms_box_cox.get_file_name_from_data()
    lms_box_cox.get_lms_value(GROWTH_CHART)
    skew, median, coff, measurement = lms_box_cox.resolve_lms_value()
    z_score_value = Zscore(skew, median, coff, measurement).z_score_measurement()
    return z_score_value


def z_score_wfa(weight: str, age_in_days: str, sex: str) -> int:
    """z-score for weight for age"""

    lms_box_cox = LmsBoxCox('wfa', weight=weight, muac=None, age_in_days=age_in_days, sex=sex, height=None)
    return z_score_calculation(lms_box_cox)


def z_score_wfh(weight: str, age_in_days: str, sex: str, height: str) -> int:
    """z-score for weight for height"""

    if D(age_in_days) <= 731:
        return z_score_wfl(weight, age_in_days, sex, height)
    lms_box_cox = LmsBoxCox('wfh', weight=weight, muac=None, age_in_days=age_in_days, sex=sex, height=height)
    return z_score_calculation(lms_box_cox)


def z_score_wfl(weight: str, age_in_days: str, sex: str, height: str) -> int:
    """z-score for weight for length"""
    if D(age_in_days) > 731:
        return z_score_wfh(weight, age_in_days, sex, height)
    lms_box_cox = LmsBoxCox('wfl', weight=weight, muac=None, age_in_days=age_in_days, sex=sex, height=height)
    return z_score_calculation(lms_box_cox)


def z_score_lhfa(age_in_days: str, sex: str, height: str) -> int:
    """z-score for length/height for age"""
    lms_box_cox = LmsBoxCox('lhfa', weight=None, muac=None, age_in_days=age_in_days, sex=sex, height=height)
    return z_score_calculation(lms_box_cox)


def z_score_with_class(weight: str, muac: str, age_in_days: str, sex: str, height: str):
    wfa = z_score_wfa(weight=weight, age_in_days=age_in_days, sex=sex)
    if wfa < -3:
        class_wfa = 'Severely Under-weight'
    elif -3 <= wfa < -2:
        class_wfa = 'Moderately Under-weight'
    else:
        class_wfa = 'Healthy'

    wfl = z_score_wfl(weight=weight, age_in_days=age_in_days, sex=sex, height=height)
    if wfl < -3:
        class_wfl_zscore = "SAM"
    elif -3 <= wfl < -2:
        class_wfl_zscore = "MAM"
    else:
        class_wfl_zscore = "Healthy"

    lhfa = z_score_lhfa(age_in_days=age_in_days, sex=sex, height=height)
    if lhfa < -3:
        class_lhfa = 'Severely Stunted'
    elif -3 <= lhfa < -2:
        class_lhfa = 'Moderately Stunted'
    else:
        class_lhfa = 'Healthy'

    if D(muac) < 11.5:
        class_wfl_muac = "SAM"
    elif D(muac) < 12.5:
        class_wfl_muac = "MAM"
    else:
        class_wfl_muac = "Healthy"

    return json.dumps({'Z_score_WFA': wfa, 'Class_WFA': class_wfa, 'Z_score_WFH' if D(age_in_days) > 24 else
                       'Z_score_WFL': wfl, 'Class_WFH' if D(age_in_days) > 24 else 'Class_WFL': class_wfl_zscore,
                       'Z_score_HFA': lhfa, 'Class_HFA': class_lhfa, 'Class_Wasting_MUAC': class_wfl_muac})

    