use config::ConfigError as ExternalConfigError;
use core::fmt::Display;
use serde::{Deserialize, Serialize};
use std::error::Error;
use utoipa::ToSchema;

#[derive(Debug, Deserialize, Serialize, Clone, ToSchema, PartialEq, Eq)]
pub enum ValidationErrorType {
    RequiredMissing,
    Invalid(String),
}

#[derive(Debug, Deserialize, Serialize, Clone, ToSchema, PartialEq, Eq)]
pub enum Where {
    All,
    Field(String),
}

#[derive(Debug, Deserialize, Serialize, Clone, ToSchema, PartialEq, Eq)]
pub struct ValidationError {
    pub field: Where,
    pub error_type: ValidationErrorType,
}

impl ValidationError {}

#[derive(Debug, Clone, Deserialize, Serialize, ToSchema, PartialEq, Eq)]
pub enum ConfigError {
    #[schema(example = "Missing Config: TAKEOFF_MODEL_NAME not set")]
    MissingConfig(String),
    #[schema(example = "Invalid Value: Unsupported type in base config: port is not a valid u64")]
    InvalidValue(String),
    #[schema(example = "File Not Found on path: /path/to/file")]
    FileNotFound(String),
    #[schema(example = "Error with Config Builder: ...")]
    BuilderError(String),
    #[schema(example = "Error Serializing/Deserializing: ...")]
    SerialError(String),
    #[schema(
        example = "Validation Errors: [ValidationError { field: Field(\"server_config\"), error_type: RequiredMissing }, ValidationError { field: Field(\"reader_config\"), error_type: RequiredMissing }]"
    )]
    ValidationErrors(Vec<ValidationError>),
    #[schema(example = "Error Writing to file: ...")]
    WriteError(String),
}

impl Display for ConfigError {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            ConfigError::MissingConfig(err) => {
                write!(f, "Missing Config: {}", err)
            }
            ConfigError::InvalidValue(err) => {
                write!(f, "Invalid Value: {}", err)
            }
            ConfigError::FileNotFound(path) => {
                write!(f, "File Not Found on path: {}", path)
            }
            ConfigError::SerialError(err) => {
                write!(f, "Error Error Serializing/Deserializing:: {}", err)
            }
            ConfigError::BuilderError(err) => {
                write!(f, "Error with Config Builder: {}", err)
            }
            ConfigError::ValidationErrors(errs) => {
                write!(f, "Validation Errors: {:?}", errs)
            }
            ConfigError::WriteError(err) => {
                write!(f, "Error Writing to file: {}", err)
            }
        }
    }
}

impl Error for ConfigError {}

impl From<ExternalConfigError> for ConfigError {
    fn from(err: ExternalConfigError) -> Self {
        ConfigError::BuilderError(err.to_string())
    }
}

impl From<serde_json::Error> for ConfigError {
    fn from(err: serde_json::Error) -> Self {
        ConfigError::SerialError(err.to_string())
    }
}

impl From<serde_yaml::Error> for ConfigError {
    fn from(err: serde_yaml::Error) -> Self {
        ConfigError::SerialError(err.to_string())
    }
}
