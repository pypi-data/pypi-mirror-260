use crate::validators::PyDataType;
use baskerville::{
    csv::{Terminator, Trim},
    infer_csv_with_options, CsvInput, DataType, InferOptions,
};
use pyo3::exceptions::{PyException, PyValueError};
use pyo3::prelude::*;

use crate::field::PyField;

fn as_byte(value: &str) -> PyResult<u8> {
    if value.len() != 1 {
        Err(PyValueError::new_err("value is not one character"))
    } else {
        Ok(value.as_bytes()[0])
    }
}

fn as_terminator(value: &str) -> PyResult<Terminator> {
    match value {
        "CRLF" => Ok(Terminator::CRLF),
        any => Ok(Terminator::Any(as_byte(any)?)),
    }
}

fn as_trim(value: Option<&str>) -> PyResult<Trim> {
    match value {
        Some(value) => match value {
            "headers" => Ok(Trim::Headers),
            "fields" => Ok(Trim::Fields),
            "all" => Ok(Trim::All),
            _ => Err(PyValueError::new_err("value is not a valid trim")),
        },
        None => Ok(Trim::None),
    }
}

/// Infers types from the file in the path given.
///
/// Args:
///     path (str): Path to the csv file.
///     data_types (typing.Optional[list[typing.Union[baskerville.Text, baskerville.Literal, baskerville.Integer, baskerville.Float, baskerville.Unique, baskerville.Date, baskerville.Time, baskerville.DateTime, typing.Callable[[str], bool]]]]):
///                What data type validators to use to infer. See :doc:`validators`.
///     null_validator (typing.Optional[typing.Union[baskerville.Text, baskerville.Literal, baskerville.Integer, baskerville.Float, baskerville.Unique, baskerville.Date, baskerville.Time, baskerville.DateTime, typing.Callable[[str], bool]]]):
///                    A validator to use to identify nullable values. See :doc:`validators`.
///     has_headers(bool): Whether the first line of the csv file is headers. If ``True``, then these
///                        are used as the column names
///     flexible(bool): Whether rows can have varying number of columns. If ``False``, then all
///                     rows must have the same number of columns or an error is thrown.
///     delimiter(str): The csv delimiter. A single character string.
///     escape(typing.Optional[str]): The escape character to use. By default, none is used.
///     quote(str): The csv quote character. A single character string.
///     quoting(bool): Whether to use quoting when reading the file.
///     trim(typing.Optional[typing.Literal["headers", "fields", "all"]]): Trim whitespace from
///         headers, fields, or all records.
///     terminator(typing.Union[typing.Literal["CRLF"], str]): Specify the record terminator.
///         The default is CRLF, which treats \\r, \\n or \\r\\n as a single record terminator.
///
/// Returns:
///     list[Field]: The inferred :class:`Field` s.
///
/// Example:
///     .. admonition:: ``mascots.csv``
///
///         .. code-block::
///     
///             Name,LOC,Species
///             Ferris,42,Crab
///             Corro,7,Urchin
///
///     >>> import baskerville # doctest: +SKIP
///     >>> fields = baskerville.infer_csv("mascots.csv") # doctest: +SKIP
///     >>> print(baskerville.display_fields(fields)) # doctest: +SKIP
///     ╭──────┬─────────┬─────────╮
///     │ Name │ LOC     │ Species │
///     ├──────┼─────────┼─────────┤
///     │ Text │ Integer │ Text    │
///     │      │ Float   │         │
///     │      │ Text    │         │
///     ╰──────┴─────────┴─────────╯
#[pyfunction]
#[pyo3(
    name = "infer_csv",
    signature=(
        path,
        data_types=None,
        null_validator=None,
        has_headers=true,
        flexible=false,
        delimiter=",",
        escape=None,
        quote="\"",
        quoting=true,
        trim=None,
        terminator="CRLF",
    )
)]
#[allow(clippy::too_many_arguments)]
pub fn infer_csv_py(
    path: &str,
    data_types: Option<Vec<PyDataType>>,
    null_validator: Option<PyDataType>,
    has_headers: bool,
    flexible: bool,
    delimiter: &str,
    escape: Option<&str>,
    quote: &str,
    quoting: bool,
    trim: Option<&str>,
    terminator: &str,
) -> PyResult<Vec<PyField>> {
    let default = InferOptions::default();
    let fields = infer_csv_with_options(
        CsvInput::Path(path),
        &mut InferOptions {
            data_types: data_types.map_or(default.data_types, |data_types| {
                data_types.into_iter().map(DataType::from).collect()
            }),
            null_validator: null_validator.map_or(default.null_validator, DataType::from),
            has_headers,
            flexible,
            delimiter: as_byte(delimiter)?,
            escape: escape.map(as_byte).transpose()?,
            quote: as_byte(quote)?,
            quoting,
            trim: as_trim(trim)?,
            terminator: as_terminator(terminator)?,
        },
    )
    // TODO: more comprehensive error handling
    //       e.g: we might want to alert to try flexible=True
    .map_err(|e| PyException::new_err(e.to_string()))?;
    Ok(fields.0.into_iter().map(PyField::from).collect())
}
