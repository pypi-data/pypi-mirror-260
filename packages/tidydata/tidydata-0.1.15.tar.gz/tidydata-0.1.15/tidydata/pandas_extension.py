import pandas as pd
from pandas.api.types import (
    is_any_real_numeric_dtype,
    is_integer_dtype,
    is_string_dtype,
    is_bool_dtype,
    is_numeric_dtype,
    is_datetime64_any_dtype,
    is_float_dtype
)
from typeguard import typechecked
from typing import Optional, Literal, Any, List
import re
from pandas._libs.missing import NAType
from numpy import log, log10, log2


@pd.api.extensions.register_series_accessor("bools")
class BooleanAccessor:
    def __init__(self, pandas_obj):
        self._validate(pandas_obj)
        self._obj = pandas_obj

    def _validate(self, obj):
        if not is_bool_dtype(obj) or obj.dtype.name != "bool[pyarrow]":
            raise TypeError(f"Not a boolean series with dtype name 'bool[pyarrow]'.")

    def to_dummy(self, fill_value: Optional[bool] = None):
        bool_ss = self._obj
        if fill_value is not None:
            bool_ss = bool_ss.fillna(fill_value)

        return (
            bool_ss.astype(object).replace({True: 1, False: 0}).astype("int64[pyarrow]")
        )

    def to_cats(
        self,
        true: str = "Yes",
        false: str = "No",
        fill_value: Optional[bool] = None,
        ordered: bool = True,
    ):
        bool_ss = self._obj
        if fill_value is not None:
            bool_ss = bool_ss.fillna(fill_value)

        return (
            bool_ss.astype(object)
            .replace({True: true, False: false})
            .astype(pd.CategoricalDtype([false, true], ordered=ordered))
        )

    def _or(self, other: pd.Series, skipna: bool = True):
        if not is_bool_dtype(other):
            raise TypeError(f"Not a boolean series in 'other': {other}.")

        xor_ss = (self._obj | other).fillna(False)
        if skipna:
            both_nas = self._obj.isna() & other.isna()
            return xor_ss.mask(both_nas, pd.NA)
        else:
            any_nas = self._obj.isna() | other.isna()
            return xor_ss.mask(any_nas, pd.NA)


@pd.api.extensions.register_series_accessor("cats")
class CategoricalAccessor:
    def __init__(self, pandas_obj):
        self._validate(pandas_obj)
        self._obj = pandas_obj

    def _validate(self, obj):
        if not isinstance(obj.dtype, pd.CategoricalDtype):
            raise TypeError(f"Not a Categorical series.")

    def to_dummy(
        self, true: List[str] | str | pd.Series, fill_value: Optional[Any] = None
    ):
        cat_ss = self._obj
        cat_codes = cat_ss.cat.categories

        if fill_value is not None:
            if fill_value not in cat_codes:
                raise ValueError(
                    f"Value in 'fill_value' is not in existing categories."
                )
            else:
                cat_ss = cat_ss.fillna(fill_value)

        if isinstance(true, pd.Series) and not is_bool_dtype(true):
            raise TypeError(f"Value in 'true' is not a boolean series: {true}.")

        if isinstance(true, pd.Series):
            fill_true = true.fillna(False)
            return (
                self._obj.astype(object)
                .where(fill_true, 0)
                .mask(fill_true, 1)
                .where(true.notna(), pd.NA)
                .astype("int64[pyarrow]")
            )
        else:
            if isinstance(true, str):
                true = [true]
            repls = {cat: 1 if cat in set(true) else 0 for cat in cat_codes}
            return cat_ss.astype(object).replace(repls).astype("int64[pyarrow]")

    def to_bool(
        self, true: List[str] | str | pd.Series, fill_value: Optional[Any] = None
    ):
        return self._obj.cats.to_dummy(true, fill_value).astype("bool[pyarrow]")


@pd.api.extensions.register_series_accessor("combs")
class CombineAccessor:
    def __init__(self, pandas_obj):
        self._obj = pandas_obj

    def _max(self, other: pd.Series, skipna: bool = False):
        return pd.concat((self._obj, other), axis=1).max(axis=1, skipna=skipna)

    def _min(self, other: pd.Series, skipna: bool = False):
        return pd.concat((self._obj, other), axis=1).min(axis=1, skipna=skipna)

    def _if(self, other: pd.Series, cond: pd.Series, skipna: bool = False):
        fill_cond = cond.fillna(False)
        mask_cond = (
            fill_cond | self._obj.isna() if skipna else fill_cond & self._obj.notna()
        )
        return self._obj.mask(mask_cond, other)


@pd.api.extensions.register_series_accessor("strs")
class StringAccessor:
    def __init__(self, pandas_obj):
        self._validate(pandas_obj)
        self._obj = pandas_obj

    def _validate(self, obj):
        if obj.dtype.name != "string":
            raise TypeError(f"Not a string series with dtype name 'string'.")

    def to_numeric(self, coerce: bool = False):
        errors = "coerce" if coerce else "raise"
        return pd.to_numeric(self._obj, errors=errors, dtype_backend="pyarrow")

    def cat(
        self, other: str | pd.Series, sep: str = "", fill_value: Optional[str] = None
    ):
        ss = self._obj.fillna(fill_value) if fill_value is not None else self._obj

        if isinstance(other, str):
            return ss + sep + other
        else:
            return ss.str.cat(other, sep=sep, na_rep=fill_value)


@pd.api.extensions.register_series_accessor("ints")
class IntegerAccessor:
    def __init__(self, pandas_obj):
        self._validate(pandas_obj)
        self._obj = pandas_obj

    def _validate(self, obj):
        if not is_integer_dtype(obj):
            raise TypeError(f"Not a integer series: {obj}.")

    def to_string(self):
        return self._obj.astype("string[pyarrow]")

    def log(self, base: Literal["e"] = "e"):
        log_funcs = {"e": log, "10": log10, "2": log2}
        return (
            self._obj.astype("float64")
            .transform(log_funcs[base])
            .astype("float64[pyarrow]")
        )



@pd.api.extensions.register_series_accessor("floats")
class IntegerAccessor:
    def __init__(self, pandas_obj):
        self._validate(pandas_obj)
        self._obj = pandas_obj

    def _validate(self, obj):
        if not is_float_dtype(obj):
            raise TypeError(f"Not a float series: {obj}.")
        
    def log(self, base: Literal["e"] = "e"):
        log_funcs = {"e": log, "10": log10, "2": log2}
        return (
            self._obj.astype("float64")
            .transform(log_funcs[base])
            .astype("float64[pyarrow]")
        )

@pd.api.extensions.register_series_accessor("econ")
class EconomicsAccessor:
    def __init__(self, pandas_obj):
        self._obj = pandas_obj
        self._educ10_cn = {
            "No formal education illiterate": 1,
            "Did not finish primary school but capable of reading and/or writing": 2,
            "Sishu": 3,
            "Elementary school": 6,
            "Middle school": 9,
            "High school": 12,
            "Vocational school": 12,
            "Two/Three Year College/Associate degree": 15,
            "Four Year College/Bachelor's degree": 16,
            "Post-graduated(Master/PhD)": 19,
        }
        self._educ_system = {"cn10": self._educ10_cn}

    def to_educ_year(self, system: Optional[Literal["cn10"]] = "cn10"):
        ss = self._obj
        if not isinstance(
            ss.dtype, pd.CategoricalDtype
        ) and not ss.dtype.name.startswith("dictionary"):
            raise TypeError(f"Not a categorical or dictionary series: {ss}.")

        if ss.dtype.name.startswith("dictionary"):
            ss = ss.astype("category")

        if set(ss.cat.categories) != set(self._educ_system[system].keys()):
            raise ValueError(
                f"Categories Mismatch: categories from series can not match the categoeies of 'cn10'."
            )

        return (
            ss.astype(object)
            .replace(self._educ_system[system])
            .astype("int64[pyarrow]")
        )
