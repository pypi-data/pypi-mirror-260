pub mod errors;
pub mod schema;

use errors::ConfigError;
use schema::{AppConfig, ManifestConfig, OptionAppConfig, OptionManifestConfig, ReaderConfig};

use config::{builder::DefaultState, Config, ConfigBuilder};
use log::{debug, error, trace};
use pyo3::exceptions::PyException;
use pyo3::prelude::*;
use serde::Serialize;
use serde_json::Value;
use std::{collections::HashMap, env, sync::OnceLock};
use uuid::Uuid;

/// Global for maximum memory to be used by redis. "TAKEOFF_REDIS_MAX_MEMORY" env var, or 1Gb if not set.
/// For behaviour when reaching the memory limit, see the redis logic in the gateway crate.
pub fn redis_max_memory() -> &'static usize {
    static REDIS_MAX_MEMORY: OnceLock<usize> = OnceLock::new();
    REDIS_MAX_MEMORY.get_or_init(|| {
        let max_memory = env::var("TAKEOFF_REDIS_MAX_MEMORY").unwrap_or(String::from("1000000000"));
        max_memory.parse::<usize>().unwrap()
    })
}

/// Global for maximum size of a prompt in bytes. "TAKEOFF_MAX_PROMPT_STRING_BYTES" env var, or 30kb  if not set.
/// For behaviour when reaching the memory limit, see the redis logic in the gateway crate.
pub fn max_prompt_string_bytes() -> &'static usize {
    static MAX_PROMPT_STRING_BYTES: OnceLock<usize> = OnceLock::new();
    MAX_PROMPT_STRING_BYTES.get_or_init(|| {
        let max_memory =
            env::var("TAKEOFF_MAX_PROMPT_STRING_BYTES").unwrap_or(String::from("30000"));
        max_memory.parse::<usize>().unwrap()
    })
}

// --------------------------------------- Python bindings ----------------------------------------

/// Cast the configuration error to a python error for display by python
impl From<ConfigError> for PyErr {
    fn from(error: ConfigError) -> Self {
        PyErr::new::<PyException, _>(format!("{}", error))
    }
}

/// Read the reader config for reader_id: reader_id from the manifest yaml file.
/// If no such reader is found, return an error to be raised in python
#[pyfunction]
#[pyo3(signature = (path="str", reader_id="str"))]
pub fn read_takeoff_readers_config(path: &str, reader_id: &str) -> PyResult<ReaderConfig> {
    let takeoff_manifest = OptionManifestConfig::read_from_manifest_yaml(path)?;
    match takeoff_manifest.readers_config.get(reader_id) {
        Some(reader_config) => Ok(reader_config.clone()),
        None => Err(ConfigError::InvalidValue(format!(
            "No reader with id {} found in manifest.yaml",
            reader_id
        ))
        .into()),
    }
}

#[pymodule]
fn takeoff_config(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_class::<ReaderConfig>()?;
    m.add_class::<AppConfig>()?;
    m.add_function(wrap_pyfunction!(read_takeoff_readers_config, m)?)?;
    Ok(())
}

// -------------------------------------- Utility Functions ----------------------------------------

/// partially deserialize a struct into a mapping from keys to serde_json Values
pub fn to_hashmap<T: Serialize>(value: T) -> Result<HashMap<String, Value>, ConfigError> {
    let json_value: Value = serde_json::to_value(&value)?;
    if let Value::Object(map) = json_value {
        let hashmap: HashMap<String, Value> = map.into_iter().collect();
        Ok(hashmap)
    } else {
        Err(ConfigError::SerialError(format!(
            "Failed to deserialize {:?} into a hashmap",
            json_value
        )))
    }
}

// ---------------------- TakeoffConfigBuilder used in main of takeoff-gateway ---------------------

/// Used in takeoff gateway, to compose a config from environment variables and yaml file, and then to serialize it for access from readers.
#[derive(Debug, Clone)]
pub struct TakeoffConfigBuilder {
    pub yaml_path: String,
    builder: ConfigBuilder<DefaultState>,
    default_manifest: ManifestConfig,
}

impl TakeoffConfigBuilder {
    /// Create a new config builder
    pub fn new(path: &str) -> Result<Self, ConfigError> {
        let config = TakeoffConfigBuilder {
            yaml_path: path.to_string(),
            builder: Config::builder(),
            default_manifest: ManifestConfig::default(),
        };
        config.add_default_config_to_builder()
    }

    /// Set a single default for the builder.
    fn set_value_as_builder_default(
        mut self,
        key: &str,
        value: Value,
    ) -> Result<Self, ConfigError> {
        match value {
            Value::String(string) => {
                self.builder = self.builder.set_default(key, string).unwrap();
            }
            Value::Number(number) => {
                if !number.is_u64() {
                    return Err(ConfigError::InvalidValue(format!(
                        "Unsupported type in base config: {:?} is not a valid u64",
                        number
                    )));
                }
                self.builder = self.builder.set_default(key, number.as_u64()).unwrap();
            }
            Value::Bool(boolean) => {
                self.builder = self.builder.set_default(key, boolean).unwrap();
            }
            _ => {
                return Err(ConfigError::InvalidValue(format!(
                    "Unsupported type in base config {:?}: {:?}",
                    key, value
                )))
            }
        }
        Ok(self)
    }

    /// Set the default config for the builder from the default_manifest attribute.
    /// These defaults can be overwritten by server config (see set_overwrite_for_server_config) and reader config
    /// (see set_overwrite_for_readers_config) variables.
    /// This function is used as part of the config builder setup
    fn add_default_config_to_builder(mut self) -> Result<Self, ConfigError> {
        // use the base config to set all the Config rs. default values.
        let takeoff_hashmap = to_hashmap(self.default_manifest.clone().server_config)?;
        let readers = self.default_manifest.clone().readers_config;

        // finish deserializing the values in the base config
        for (key, value) in takeoff_hashmap {
            let composite_key = format!("server_config.{}", key);
            self = self.set_value_as_builder_default(composite_key.as_str(), value)?;
        }

        if readers.is_empty() {
            self.builder = self
                .builder
                .set_default("readers_config", HashMap::<String, ReaderConfig>::new())?;
        } else {
            for (reader_id, reader) in readers {
                for (key, value) in to_hashmap(reader)? {
                    let composite_key = format!("readers_config.{}.{}", reader_id, key);
                    self =
                        self.set_value_as_builder_default(composite_key.as_str(), value.clone())?;
                }
            }
        }
        Ok(self)
    }

    fn set_value_as_builder_overwrite(
        mut self,
        key: &str,
        value: Value,
    ) -> Result<Self, ConfigError> {
        match value {
            Value::String(string) => {
                self.builder = self.builder.set_override(key, string).unwrap();
            }
            Value::Number(number) => {
                if !number.is_u64() {
                    return Err(ConfigError::InvalidValue(format!(
                        "Unsupported type in base config: {:?} is not a valid u64",
                        number
                    )));
                }
                self.builder = self.builder.set_override(key, number.as_u64()).unwrap();
            }
            Value::Bool(boolean) => {
                self.builder = self.builder.set_override(key, boolean).unwrap();
            }
            Value::Null => {
                trace!("Skipping null value");
            }
            _ => {
                return Err(ConfigError::InvalidValue(format!(
                    "Unsupported type in base config {:?}: {:?}",
                    key, value
                )))
            }
        }
        Ok(self)
    }

    fn set_overwrite_for_server_config(
        mut self,
        key: String,
        value: Value,
    ) -> Result<Self, ConfigError> {
        let composite_key = format!("server_config.{}", key);
        self = self.set_value_as_builder_overwrite(composite_key.as_str(), value)?;
        Ok(self)
    }

    fn set_overwrite_for_readers_config(
        mut self,
        reader_id: String,
        object: Value,
    ) -> Result<Self, ConfigError> {
        if let Value::Object(map) = object {
            for (key, value) in map {
                let composite_key = format!("readers_config.{}.{}", reader_id, key);
                if let Value::Null = value {
                    trace!("Skipping null value")
                } else {
                    self = self.set_value_as_builder_overwrite(composite_key.as_str(), value)?;
                }
            }
        } else {
            return Err(ConfigError::InvalidValue(String::from("")));
        }
        Ok(self)
    }

    pub fn add_yaml_to_builder(mut self) -> Result<Self, ConfigError> {
        let manifest = match OptionManifestConfig::read_from_manifest_yaml(&self.yaml_path) {
            Ok(manifest) => manifest,
            Err(err) => match err {
                ConfigError::FileNotFound(_) => {
                    debug!(
                        "No yaml file found at: {}! Skipping trying to add to builder.",
                        self.yaml_path
                    );
                    return Ok(self);
                }
                _ => {
                    return Err(err);
                }
            },
        };
        for (key, value) in to_hashmap(manifest.clone().server_config)? {
            self = self.set_overwrite_for_server_config(key, value)?;
        }
        for (reader_id, reader_value) in to_hashmap(manifest.clone().readers_config)? {
            self = self.set_overwrite_for_readers_config(reader_id, reader_value)?;
        }
        Ok(self)
    }

    pub fn add_env_to_builder(mut self) -> Result<Self, ConfigError> {
        // New config builder to grab config set in env vars
        if env::var("TAKEOFF_CONSUMER_GROUP").is_err() {
            trace!("TAKEOFF_CONSUMER_GROUP not set, defaulting to primary");
            env::set_var("TAKEOFF_CONSUMER_GROUP", "primary");
        }
        let mut env_builder = Config::builder();
        env_builder = env_builder.add_source(config::Environment::with_prefix("TAKEOFF"));

        // Overwrite any server config that have been set in env
        match env_builder
            .clone()
            .build()?
            .try_deserialize::<OptionAppConfig>()
        {
            Ok(config) => {
                for (key, value) in to_hashmap(config)? {
                    if let Value::Null = value {
                        trace!("Skipping null value")
                    } else {
                        self = self.set_overwrite_for_server_config(key, value)?;
                    }
                }
            }
            Err(e) => return Err(e.into()),
        }

        // Check to see if the server max batch size has been set in the env vars or the yaml file so far
        // If it has, then use it as a default for the readers.
        let max_batch_size: Option<&str> = self.builder.clone().build()?.get("max_batch_size").ok();

        // set the default consumer group, and the default continuous max batch size (to TAKEOFF_MAX_BATCH_SIZE)
        env_builder = env_builder
            .set_default("consumer_group", "primary")?
            .set_default("max_batch_size", max_batch_size)?;

        // Form readers_config from env vars, if none set or not enough to form a full ReaderConfig default to empty vec
        match env_builder
            .clone()
            .set_default("consumer_group", "primary")?
            .build()?
            .try_deserialize::<ReaderConfig>()
        {
            Ok(reader_config) => {
                // If there is already a reader config set in the yaml file, don't allow env vars to overwrite it, we error and report the conflict.
                if self
                    .builder
                    .clone()
                    .build()?
                    .try_deserialize::<ManifestConfig>()?
                    .readers_config
                    .is_empty()
                {

                    self = self.set_overwrite_for_readers_config(
                        env::var("TAKEOFF_READER_ID").unwrap_or(Uuid::new_v4().to_string()),
                        serde_json::to_value(reader_config)?,
                    )?;
                } else {
                    error!("Reader config configured by yaml and env vars!");
                    return Err(
                        ConfigError::BuilderError(
                            format!(
                                "readers_config already set by yaml file at: {} and trying to overwrite with env vars clashes! Please either remove reader env vars or yaml file.", 
                                self.yaml_path,
                            )
                        )
                    );
                }
            }
            Err(err) => debug!("Couldn't build reader config from env vars, so not attempting to update readers_config, details: {:?}", err)
        };

        Ok(self)
    }

    pub fn yield_config(self) -> Result<ManifestConfig, ConfigError> {
        Ok(self
            .builder
            .clone()
            .build()?
            .try_deserialize::<ManifestConfig>()?)
    }
}

// ----------------- Utility Functions used in takeoff-gateway to read manifest.yaml -----------------

/// Read the server config from the manifest yaml file.
pub fn read_takeoff_app_config(path: &str) -> Result<AppConfig, ConfigError> {
    let takeoff_manifest = ManifestConfig::read_from_manifest_yaml(path)?;
    Ok(takeoff_manifest.server_config)
}

#[cfg(test)]
mod lib_tests {
    use super::*;
    use serde_json::Value;
    use serial_test::serial;
    fn unset_env_vars() {
        for (key, _) in to_hashmap(AppConfig::default()).unwrap() {
            env::remove_var(format!("TAKEOFF_{}", key.to_uppercase()));
        }
        for (key, _) in to_hashmap(ReaderConfig::default()).unwrap() {
            env::remove_var(format!("TAKEOFF_{}", key.to_uppercase()));
        }
    }

    // set the environment variables to the default variables
    fn set_env_vars_from_object<T: Serialize>(object: T) -> Result<(), ConfigError> {
        for (key, value) in to_hashmap(object)? {
            match value {
                Value::String(string) => {
                    env::set_var(format!("TAKEOFF_{}", key.to_uppercase()), string);
                }
                Value::Number(number) => {
                    env::set_var(
                        format!("TAKEOFF_{}", key.to_uppercase()),
                        format!("{:?}", number.as_u64().unwrap()),
                    );
                }
                Value::Bool(boolean) => {
                    env::set_var(
                        format!("TAKEOFF_{}", key.to_uppercase()),
                        format!("{:?}", boolean),
                    );
                }
                _ => {
                    return Err(ConfigError::InvalidValue(format!(
                        "Unsupported type while setting env vars {:?}: {:?}",
                        key, value
                    )))
                }
            }
        }
        Ok(())
    }

    #[test]
    #[serial]
    fn test_build_config_no_overrides() -> Result<(), ConfigError> {
        unset_env_vars();
        // check that TAKEOFF_MAX_BATCH_SIZE isn't set
        println!("{:?}", env::var("TAKEOFF_MAX_BATCH_SIZE"));
        let config = AppConfig::default();
        println!("{:?}", config);
        let manifest = TakeoffConfigBuilder::new("")
            .unwrap()
            .add_env_to_builder()
            .unwrap();
        let manifest = manifest.yield_config().unwrap();
        assert_eq!(config, manifest.server_config);
        assert_eq!(manifest.readers_config, HashMap::new());
        Ok(())
    }

    #[test]
    #[serial]
    fn test_build_config_override_noop() -> Result<(), ConfigError> {
        unset_env_vars();
        let config = AppConfig::default();

        set_env_vars_from_object(config.clone())?;

        let manifest = TakeoffConfigBuilder::new("")
            .unwrap()
            .add_env_to_builder()
            .unwrap();
        let manifest = manifest.yield_config().unwrap();
        assert_eq!(config.clone(), manifest.server_config.clone());
        assert_eq!(manifest.readers_config, HashMap::new());
        Ok(())
    }

    #[test]
    #[serial]
    fn test_build_config_override() -> Result<(), ConfigError> {
        unset_env_vars();

        let overridden_config = AppConfig {
            max_batch_size: 1,
            batch_duration_millis: 1,
            echo: true,
            ..Default::default()
        };

        set_env_vars_from_object(overridden_config.clone())?;

        let manifest = TakeoffConfigBuilder::new("")
            .unwrap()
            .add_env_to_builder()
            .unwrap();
        let manifest = manifest.yield_config().unwrap();
        assert_ne!(manifest.server_config, AppConfig::default());
        assert_eq!(overridden_config, manifest.server_config);
        // No reader config set in env so should be empty
        assert_eq!(manifest.readers_config, HashMap::new());
        Ok(())
    }

    #[test]
    #[serial]
    fn test_env_vars_overwrite_yaml_source() -> Result<(), ConfigError> {
        unset_env_vars();

        let overwrite_env_config = AppConfig {
            max_batch_size: 1,
            batch_duration_millis: 1,
            echo: true,
            ..Default::default()
        };

        set_env_vars_from_object(overwrite_env_config.clone())?;

        let manifest = TakeoffConfigBuilder::new("test.yaml")
            .unwrap()
            .add_yaml_to_builder()
            .unwrap()
            .add_env_to_builder()
            .unwrap();
        let manifest = manifest.yield_config().unwrap();
        let yaml_config = ManifestConfig::read_from_manifest_yaml("test.yaml").unwrap();
        assert_ne!(manifest.server_config.clone(), AppConfig::default());
        assert_eq!(overwrite_env_config, manifest.server_config);
        assert_ne!(yaml_config.server_config, manifest.server_config);
        assert_eq!(yaml_config.readers_config, manifest.readers_config);
        Ok(())
    }

    #[test]
    #[serial]
    fn test_if_readers_set_in_env_vars_and_yaml_it_errors() -> Result<(), ConfigError> {
        unset_env_vars();

        #[derive(Debug, Clone, PartialEq, Serialize)]
        struct OverwriteReaderConfig {
            consumer_group: String,
            device: String,
            model_name: String,
            redis_host: Option<String>,
        }

        let overwrite_env_config = OverwriteReaderConfig {
            consumer_group: "test".to_string(),
            device: "test".to_string(),
            model_name: "test".to_string(),
            redis_host: Some("test".to_string()),
        };

        set_env_vars_from_object(overwrite_env_config)?;

        let builder = TakeoffConfigBuilder::new("test.yaml")
            .unwrap()
            .add_yaml_to_builder()
            .unwrap()
            .add_env_to_builder();
        assert_eq!(
            builder.err().unwrap(),
            ConfigError::BuilderError(
                "readers_config already set by yaml file at: test.yaml and trying to overwrite with env vars clashes! Please either remove reader env vars or yaml file."
                    .to_string()
            )
        );
        Ok(())
    }

    #[test]
    #[serial]
    fn test_that_not_specifying_all_values_in_app_config_yaml_is_fine() -> Result<(), ConfigError> {
        unset_env_vars();

        let manifest = TakeoffConfigBuilder::new("test_incomplete.yaml")
            .unwrap()
            .add_yaml_to_builder()
            .unwrap()
            .add_env_to_builder()
            .unwrap()
            .yield_config()
            .unwrap();
        let yaml_config =
            OptionManifestConfig::read_from_manifest_yaml("test_incomplete.yaml").unwrap();
        let manifest_hashmap = to_hashmap(manifest.server_config.clone()).unwrap();
        assert_ne!(manifest.server_config.clone(), AppConfig::default());
        for (key, value) in to_hashmap(yaml_config.server_config)? {
            if let Value::Null = value {
                println!("Skipping null value")
            } else {
                println!("{}: {}", key, value);
                assert_eq!(manifest_hashmap.get(&key), Some(&value));
            }
        }
        assert_eq!(yaml_config.readers_config, manifest.readers_config);
        Ok(())
    }

    #[test]
    #[serial]
    fn test_incomplete_app_config_env_vars_overwrite_yaml_source() -> Result<(), ConfigError> {
        unset_env_vars();

        #[derive(Debug, Clone, PartialEq, Serialize)]
        struct IncompleteAppConfig {
            max_batch_size: usize,
            batch_duration_millis: usize,
            echo: bool,
        }

        let overwrite_env_config = IncompleteAppConfig {
            max_batch_size: 1,
            batch_duration_millis: 1,
            echo: true,
        };

        set_env_vars_from_object(overwrite_env_config.clone())?;

        let manifest = TakeoffConfigBuilder::new("test.yaml")
            .unwrap()
            .add_yaml_to_builder()
            .unwrap()
            .add_env_to_builder()
            .unwrap();
        let manifest = manifest.yield_config().unwrap();
        let yaml_config = ManifestConfig::read_from_manifest_yaml("test.yaml").unwrap();
        assert_ne!(manifest.server_config.clone(), AppConfig::default());

        let json_object = serde_json::to_value(&overwrite_env_config)?;
        if let Value::Object(map) = json_object {
            let overwrite_hashmap = map.into_iter().collect::<HashMap<String, Value>>();
            let manifest_server_config_hashmap =
                to_hashmap(manifest.server_config.clone()).unwrap();
            for (key, value) in overwrite_hashmap {
                assert_eq!(manifest_server_config_hashmap.get(&key), Some(&value));
            }
        } else {
            panic!("Failed to deserialize {:?} into a hashmap", json_object);
        }

        assert_ne!(yaml_config.server_config, manifest.server_config);
        assert_eq!(yaml_config.readers_config, manifest.readers_config);
        Ok(())
    }

    #[test]
    #[serial]
    fn test_not_setting_consumer_group_in_env_vars_is_ok() -> Result<(), ConfigError> {
        unset_env_vars();

        #[derive(Debug, Clone, PartialEq, Serialize)]
        struct IncompleteReaderConfig {
            model_name: String,
            device: String,
        }

        let overwrite_env_config = IncompleteReaderConfig {
            model_name: "test".to_string(),
            device: "test".to_string(),
        };

        set_env_vars_from_object(overwrite_env_config.clone())?;

        let manifest = TakeoffConfigBuilder::new("non-existent_file.yaml")
            .unwrap()
            .add_yaml_to_builder()
            .unwrap()
            .add_env_to_builder()
            .unwrap();
        let manifest = manifest.yield_config().unwrap();
        assert_ne!(manifest.readers_config.clone(), HashMap::new());

        assert_eq!(manifest.readers_config.len(), 1);
        let reader = manifest.readers_config.values().next().unwrap().clone();
        assert_eq!(
            reader,
            ReaderConfig {
                consumer_group: "primary".to_string(),
                model_name: "test".to_string(),
                device: "test".to_string(),
                ..Default::default()
            }
        );
        Ok(())
    }
}
