use crate::errors::{ConfigError, ValidationError, ValidationErrorType, Where};
use config::ValueKind;
use homedir::get_my_home;
use log::debug;
use pyo3::{prelude::*, types::PyDict};
use serde::{Deserialize, Serialize};
use serde_json::Value;
use std::{collections::HashMap, fs, io::Write};
use url::Url;
use utoipa::ToSchema;

#[pyclass]
#[derive(Debug, Clone, Default, Deserialize, Serialize, PartialEq)]
pub struct OptionManifestConfig {
    pub server_config: OptionAppConfig,
    pub readers_config: HashMap<String, ReaderConfig>,
}
impl OptionManifestConfig {
    pub fn read_from_manifest_yaml(path: &str) -> Result<Self, ConfigError> {
        let file =
            fs::read_to_string(path).map_err(|_| ConfigError::FileNotFound(path.to_string()))?;
        let raw_yaml: HashMap<String, OptionManifestConfig> = serde_yaml::from_str(&file)?;
        // Added prefix takeoff to yaml for easier writing/reading
        raw_yaml
            .get("takeoff")
            .ok_or(ConfigError::SerialError(
                "No takeoff key found in manifest".to_string(),
            ))
            .map(|x| x.clone())
    }
}

#[pyclass]
#[derive(Debug, Clone, Default, Deserialize, Serialize, PartialEq)]
pub struct ManifestConfig {
    pub server_config: AppConfig,
    pub readers_config: HashMap<String, ReaderConfig>,
}

impl ManifestConfig {
    pub fn read_from_manifest_yaml(path: &str) -> Result<Self, ConfigError> {
        let file =
            fs::read_to_string(path).map_err(|_| ConfigError::FileNotFound(path.to_string()))?;
        let raw_yaml: HashMap<String, ManifestConfig> = serde_yaml::from_str(&file)?;
        // Added prefix takeoff to yaml for easier writing/reading
        raw_yaml
            .get("takeoff")
            .ok_or(ConfigError::SerialError(
                "No takeoff key found in manifest".to_string(),
            ))
            .map(|x| x.clone())
    }

    pub fn write_manifest_to_yaml(&self, path: &str) -> Result<(), ConfigError> {
        fs::remove_file(path).unwrap_or(debug!("No file to remove at path {}", path));
        let mut file = std::fs::OpenOptions::new()
            .write(true)
            .create(true)
            .open(path)
            .map_err(|_| ConfigError::FileNotFound(path.to_string()))?;

        // Added prefix takeoff to yaml for easier writing/reading
        let yaml = serde_yaml::to_string(&HashMap::from([("takeoff", self.clone())]))?;
        file.write_all(yaml.as_bytes())
            .map_err(|e| ConfigError::WriteError(e.to_string()))?;
        Ok(())
    }
}

#[derive(Debug, Clone, Default, Deserialize, Serialize, Eq, PartialEq, ToSchema)]
pub struct OptionAppConfig {
    pub max_batch_size: Option<usize>,
    pub batch_duration_millis: Option<u64>,
    pub echo: Option<bool>,
    pub port: Option<u16>,
    pub enable_metrics: Option<bool>,
    pub heartbeat_check_interval: Option<u64>,
    pub launch_management_server: Option<bool>,
    pub launch_vertex_server: Option<bool>,
    pub launch_sagemaker_server: Option<bool>,
    pub launch_openai_server: Option<bool>,
    pub management_port: Option<u16>,
    pub vertex_port: Option<u16>,
    pub repository_path: Option<String>,
    pub body_size_limit_bytes: Option<usize>,
    pub openai_port: Option<u16>,
    pub allow_remote_images: Option<bool>,
}

/// The app configuration
// IF YOU ADD A FIELD, MAKE SURE TO ADD IT TO OptionAppConfig as well!
#[pyclass]
#[derive(Debug, Clone, Deserialize, Serialize, Eq, PartialEq, ToSchema)]
#[schema(default = json!(AppConfig::default()))]
pub struct AppConfig {
    pub max_batch_size: usize,
    pub batch_duration_millis: u64,
    pub echo: bool,
    pub port: u16,
    pub enable_metrics: bool,
    pub heartbeat_check_interval: u64,
    pub launch_management_server: bool,
    pub launch_vertex_server: bool,
    pub launch_sagemaker_server: bool,
    pub launch_openai_server: bool,
    pub management_port: u16,
    pub vertex_port: u16,
    pub repository_path: String,
    pub body_size_limit_bytes: usize,
    pub openai_port: u16,
    pub allow_remote_images: bool,
}

impl Default for AppConfig {
    fn default() -> Self {
        // This expect is annoying but necessary: its statically a valid url.
        let mut url = Url::parse("file://").expect("Unreachable error");

        // These expects are also annoying but necessary: we know that we have a valid home directory.
        let repository_dir = get_my_home()
            .expect("Couldnt get home directory")
            .expect("Couldnt get home directory")
            .join("artefacts/");

        // Should be able to create the artefacts directory.
        fs::create_dir_all(&repository_dir).expect("Couldnt create artefacts directory");

        url.set_path(&repository_dir.to_string_lossy());

        let repository_path = url.to_string();
        Self {
            max_batch_size: 8,
            batch_duration_millis: 100,
            echo: false,
            port: 3000,
            enable_metrics: true,
            heartbeat_check_interval: 1,
            launch_management_server: true,
            launch_vertex_server: true,
            launch_sagemaker_server: true,
            launch_openai_server: true,
            management_port: 3001,
            vertex_port: 3002,
            repository_path,
            body_size_limit_bytes: 1024 * 1024 * 2, // default 2mb
            openai_port: 3003,
            allow_remote_images: false, // default to false: for security reasons
        }
    }
}

#[pyclass]
#[pyo3(dict)]
#[derive(Debug, Default, Clone, Deserialize, Serialize, PartialEq, ToSchema)]
pub struct ReaderConfig {
    #[pyo3(get)]
    pub model_name: String,
    #[pyo3(get)]
    pub device: String,
    #[pyo3(get)]
    pub consumer_group: String,
    #[pyo3(get)]
    pub redis_host: Option<String>,
    #[pyo3(get)]
    pub access_token: Option<String>,
    #[pyo3(get)]
    pub log_level: Option<String>,
    #[pyo3(get)]
    pub disable_continuous_generation: Option<bool>,
    // old backends commands that we will map to jf commands:
    #[pyo3(get)]
    pub backend: Option<String>,
    #[pyo3(get)]
    pub cuda_visible_devices: Option<String>,

    // command we should probably remove
    #[pyo3(get)]
    pub max_batch_size: Option<u64>,
    #[pyo3(get)]
    pub assistant_model_name: Option<String>,

    // necessary jf commands:
    #[pyo3(get)]
    pub tensor_parallel: Option<u32>,
    #[pyo3(get)]
    pub quant_type: Option<String>,
    #[pyo3(get)]
    pub max_sequence_length: Option<u32>,
    #[pyo3(get)]
    pub nvlink_unavailable: Option<u32>,

    // jf dev commands
    #[pyo3(get)]
    pub disable_static: Option<u32>,
    #[pyo3(get)]
    pub disable_cuda_graph: Option<u32>,
    #[pyo3(get)]
    pub cuda_graph_cache_capacity: Option<u32>,
}

impl From<ReaderConfig> for ValueKind {
    fn from(reader_config: ReaderConfig) -> Self {
        let json_value = serde_json::json!(reader_config);
        let hashmap: HashMap<String, config::Value> = serde_json::from_value(json_value).unwrap();
        ValueKind::Table(hashmap)
    }
}

#[pymethods]
impl ReaderConfig {
    #[new]
    #[pyo3(signature = (**kwargs))]
    fn new(kwargs: Option<&PyDict>) -> PyResult<Self> {
        if let Some(kwargs) = kwargs {
            let mut model_name = String::new();
            let mut device = String::new();
            let mut consumer_group = String::new();
            let mut log_level = None;
            let mut cuda_visible_devices = None;
            let mut max_batch_size = None;
            let mut tensor_parallel = None;
            let mut max_sequence_length = None;

            for (key, value) in kwargs {
                match key.to_string().as_str() {
                    "model_name" => model_name = value.extract()?,
                    "device" => device = value.extract()?,
                    "consumer_group" => consumer_group = value.extract()?,
                    "log_level" => log_level = Some(value.extract()?),
                    "cuda_visible_devices" => cuda_visible_devices = value.extract()?,
                    "max_batch_size" => max_batch_size = value.extract()?,
                    "tensor_parallel" => tensor_parallel = value.extract()?,
                    "max_sequence_length" => max_sequence_length = value.extract()?,
                    _ => {}
                }
            }

            if model_name == String::new() {
                return Err(PyErr::new::<pyo3::exceptions::PyTypeError, _>(
                    "model_name cannot be empty".to_string(),
                ));
            }
            if device != "cpu" && device != "cuda" {
                return Err(PyErr::new::<pyo3::exceptions::PyTypeError, _>(
                    "device must be either 'cpu' or 'cuda'".to_string(),
                ));
            }

            Ok(Self {
                model_name,
                device,
                consumer_group,
                log_level,
                cuda_visible_devices,
                max_batch_size,
                tensor_parallel,
                max_sequence_length,
                ..Default::default()
            })
        } else {
            Ok(Self::default())
        }
    }

    pub fn dict_without_optionals(&self, py: Python) -> PyResult<PyObject> {
        let py_obj = PyDict::new(py);

        let json_value = serde_json::json!(self);
        let mut hashmap: HashMap<String, Value> = serde_json::from_value(json_value).unwrap();

        // Remove Cuda Visible Devices as is set by rust and so doesn't need to be accessed in reader.
        hashmap.remove("cuda_visible_devices");

        for (key, value) in hashmap {
            match value {
                Value::String(s) => {
                    py_obj.set_item(key, s)?;
                }
                Value::Number(n) => {
                    if n.is_u64() {
                        py_obj.set_item(key, n.as_u64().unwrap())?;
                    } else {
                        return Err(PyErr::new::<pyo3::exceptions::PyTypeError, _>(format!(
                            "Invalid number type for key {}",
                            key
                        )));
                    }
                }
                Value::Bool(b) => {
                    py_obj.set_item(key, b)?;
                }
                Value::Null => {
                    debug!("Null value for key {} not added to dict", key);
                }
                _ => {
                    return Err(PyErr::new::<pyo3::exceptions::PyTypeError, _>(format!(
                        "Invalid value {} for key {}",
                        value, key
                    )));
                }
            }
        }

        Ok(py_obj.to_object(py))
    }

    pub fn validate(&self) -> Result<(), ConfigError> {
        let mut errs: Vec<ValidationError> = vec![];

        if self.device == *"cpu" && self.tensor_parallel.is_some() {
            errs.push(ValidationError {
                field: Where::Field(String::from("tensor_parallel")),
                error_type: ValidationErrorType::Invalid(
                    "tensor_parallel is not supported on cpu".to_string(),
                ),
            });
        }

        // Check that device is either cpu or cuda
        if self.device != *"cpu" && self.device != *"cuda" {
            errs.push(ValidationError {
                field: Where::Field(String::from("device")),
                error_type: ValidationErrorType::Invalid(
                    "device must be either 'cpu' or 'cuda'".to_string(),
                ),
            });
        }

        // If backend is multigpu and cuda_visible_devices is set must be a power of 2
        if let Some(backend) = self.backend.clone() {
            if backend == *"multigpu" {
                if let Some(cuda_visible_devices) = self.cuda_visible_devices.clone() {
                    let n = cuda_visible_devices.split(',').collect::<Vec<&str>>();
                    if n.len() & (n.len() - 1) != 0 {
                        errs.push(ValidationError {
                            field: Where::Field(String::from("cuda_visible_devices")),
                            error_type: ValidationErrorType::Invalid(
                                "cuda_visible_devices must be a power of 2 for multigpu backend"
                                    .to_string(),
                            ),
                        });
                    }
                }
            }
        }

        // Check that the cuda_visible_devices is a comma separated string of integers
        if let Some(cuda_visible_devices) = self.cuda_visible_devices.clone() {
            let cuda_list = cuda_visible_devices.split(',');
            for device in cuda_list {
                if device.parse::<u32>().is_err() {
                    errs.push(
                        ValidationError {
                            field: Where::Field(String::from("cuda_visible_devices")),
                            error_type: ValidationErrorType::Invalid("cuda_visible_devices must be a comma separated string of integers like '0,1'".to_string()),
                        }
                    );
                    break;
                }
            }
        }

        // Return any errors
        if !errs.is_empty() {
            Err(ConfigError::ValidationErrors(errs))
        } else {
            Ok(())
        }
    }

    pub fn add_to_manifest_yaml(&self, path: &str, reader_id: String) -> Result<(), ConfigError> {
        let mut manifest_config = ManifestConfig::read_from_manifest_yaml(path)?;
        manifest_config
            .readers_config
            .insert(reader_id, self.clone());
        manifest_config.write_manifest_to_yaml(path)?;
        Ok(())
    }
}

pub fn remove_from_manifest_yaml(path: &str, reader_id: String) -> Result<(), ConfigError> {
    let mut manifest_config = ManifestConfig::read_from_manifest_yaml(path)?;
    manifest_config.readers_config.remove(&reader_id);
    manifest_config.write_manifest_to_yaml(path)?;
    Ok(())
}

#[cfg(test)]
mod schema_test {
    use super::*;
    use crate::TakeoffConfigBuilder;
    use std::fs;

    fn delete_file(path: &str) {
        fs::remove_file(path).unwrap_or(());
    }

    #[test]
    fn test_read_yaml_to_manifest_config() {
        ManifestConfig::read_from_manifest_yaml("test.yaml").unwrap();
    }

    #[test]
    fn test_write_yaml_to_file() {
        let path = "test_write_1.yaml";
        delete_file(path);
        let manifest_config = ManifestConfig::default();
        manifest_config.write_manifest_to_yaml(path).unwrap();
        let read_manifest_config = ManifestConfig::read_from_manifest_yaml(path).unwrap();
        assert_eq!(read_manifest_config, manifest_config);
        delete_file(path);
    }

    #[test]
    fn test_adding_reader_to_manifest() {
        let path = "test_write_2.yaml";
        delete_file(path);
        let initial_manifest = ManifestConfig::default();
        initial_manifest.write_manifest_to_yaml(path).unwrap();
        let reader_config = ReaderConfig {
            model_name: "test".to_string(),
            device: "cpu".to_string(),
            consumer_group: "primary".to_string(),
            redis_host: Some("redis".to_string()),
            backend: Some("backend".to_string()),
            log_level: None,
            cuda_visible_devices: None,
            disable_continuous_generation: None,
            max_batch_size: None,
            assistant_model_name: None,
            ..Default::default()
        };
        reader_config
            .add_to_manifest_yaml(path, "reader_new".to_string())
            .unwrap();
        let new_manifest = ManifestConfig::read_from_manifest_yaml(path).unwrap();
        assert_ne!(new_manifest, initial_manifest);
        assert_ne!(new_manifest.readers_config, initial_manifest.readers_config);
        assert_eq!(new_manifest.server_config, initial_manifest.server_config);

        assert_eq!(
            new_manifest.readers_config.get("reader_new").unwrap(),
            &reader_config
        );

        delete_file(path);
    }

    #[test]
    fn test_removing_reader_from_manifest() {
        let path = "test_write_3.yaml";
        delete_file(path);
        let initial_manifest = ManifestConfig {
            server_config: AppConfig::default(),
            readers_config: HashMap::from([
                (
                    "reader1".to_string(),
                    ReaderConfig {
                        model_name: "test".to_string(),
                        device: "cpu".to_string(),
                        consumer_group: "primary".to_string(),
                        redis_host: Some("redis".to_string()),
                        backend: Some("backend".to_string()),
                        ..Default::default()
                    },
                ),
                (
                    "reader2".to_string(),
                    ReaderConfig {
                        model_name: "test2".to_string(),
                        device: "cpu".to_string(),
                        consumer_group: "primary".to_string(),
                        redis_host: Some("redis".to_string()),
                        backend: Some("backend".to_string()),
                        ..Default::default()
                    },
                ),
            ]),
        };
        initial_manifest.write_manifest_to_yaml(path).unwrap();
        remove_from_manifest_yaml(path, "reader1".to_string()).unwrap();
        let new_manifest = ManifestConfig::read_from_manifest_yaml(path).unwrap();
        assert_ne!(new_manifest, initial_manifest);
        assert_ne!(new_manifest.readers_config, initial_manifest.readers_config);
        assert_eq!(new_manifest.server_config, initial_manifest.server_config);

        assert!(new_manifest.readers_config.get("reader1").is_none());
        assert!(new_manifest.readers_config.get("reader2").is_some());

        delete_file(path);
    }

    #[test]
    fn test_adding_multiple_readers_to_manifest() {
        let path = "test_write_4.yaml";
        let reader_ids = vec!["reader_1", "reader_2", "reader_3"];
        delete_file(path);
        let initial_manifest = TakeoffConfigBuilder::new("")
            .unwrap()
            .yield_config()
            .unwrap();
        initial_manifest.write_manifest_to_yaml(path).unwrap();

        let reader_config = ReaderConfig {
            model_name: "test".to_string(),
            device: "cpu".to_string(),
            consumer_group: "primary".to_string(),
            redis_host: Some("redis".to_string()),
            backend: Some("backend".to_string()),
            ..Default::default()
        };

        for id in reader_ids.clone() {
            reader_config
                .add_to_manifest_yaml(path, id.to_string())
                .unwrap();
        }

        let new_manifest = ManifestConfig::read_from_manifest_yaml(path).unwrap();
        assert_ne!(new_manifest, initial_manifest);
        assert_ne!(new_manifest.readers_config, initial_manifest.readers_config);
        assert_eq!(new_manifest.server_config, initial_manifest.server_config);
        for id in reader_ids {
            assert_eq!(new_manifest.readers_config.get(id).unwrap(), &reader_config);
        }

        delete_file(path);
    }
}
