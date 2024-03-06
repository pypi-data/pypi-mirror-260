use bstr::Finder;
use pyo3::prelude::*;
use pyo3::types::{PyAny, PyDict, PyFrame, PyList, PyModule};
use pyo3::{PyErr, Python};
use std::collections::HashMap;
use ulid::Ulid;

use super::utils;

#[derive(Debug)]
pub struct PluginProcessor {
    filename_finder: Finder<'static>,
    call_type: String,
    return_type: String,
    subtype: Option<String>,
    call: Option<PyObject>,
    process: Option<PyObject>,
    context: Py<PyDict>,
    frame_ids: HashMap<usize, String>,
}

impl PluginProcessor {
    fn new(plugin_data: &PyDict, context: &PyDict) -> Result<Self, PyErr> {
        let filename: &str = PyAny::get_item(plugin_data, "path_fragment")?.extract()?;
        #[cfg(target_os = "windows")]
        let filename = filename.replace("/", "\\");
        let plugin = Self {
            filename_finder: Finder::new(&filename).into_owned(),
            call_type: PyAny::get_item(plugin_data, "call_type")?.extract()?,
            return_type: PyAny::get_item(plugin_data, "return_type")?.extract()?,
            subtype: match plugin_data
                .get_item("subtype")
                .expect("a string is always a valid dict key")
            {
                Some(subtype) => Some(subtype.extract()?),
                None => None,
            },
            call: match plugin_data
                .get_item("call")
                .expect("a string is always a valid dict key")
            {
                Some(call) => {
                    if call.is_none() {
                        None
                    } else {
                        Some(call.into())
                    }
                }
                None => None,
            },
            process: match plugin_data
                .get_item("process")
                .expect("a string is always a valid dict key")
            {
                Some(process) => {
                    if process.is_none() {
                        None
                    } else {
                        Some(process.into())
                    }
                }
                None => None,
            },
            context: context.into(),
            frame_ids: HashMap::new(),
        };
        Ok(plugin)
    }

    pub fn matches(
        &self,
        py: Python,
        frame: &PyObject,
        event: &str,
        arg: &PyObject,
        filename: &str,
    ) -> Result<bool, PyErr> {
        let filename_matches = self.filename_finder.find(filename).is_some();
        match &self.call {
            None => Ok(filename_matches),
            Some(call) => Ok(filename_matches
                && call
                    .call1(py, (frame, event, arg, &self.context))?
                    .extract(py)?),
        }
    }

    fn frame_id(&mut self, pyframe: &PyFrame, event: &str) -> Option<String> {
        let pyframe_id = pyframe.as_ptr() as usize;
        match event {
            "call" => {
                let frame_id = Ulid::new();
                let frame_id = format!("frm_{}", frame_id.to_string());
                self.frame_ids.insert(pyframe_id, frame_id.clone());
                Some(frame_id)
            }
            "return" => match self.frame_ids.get(&pyframe_id) {
                Some(frame_id) => Some(frame_id.clone()),
                None => {
                    let frame_id = Ulid::new();
                    Some(format!("frm_{}", frame_id.to_string()))
                }
            },
            _ => None,
        }
    }

    pub fn process(
        &mut self,
        py: Python,
        pyframe: &PyFrame,
        event: &str,
        arg: &PyObject,
        call_frames: Vec<(PyObject, String)>,
    ) -> Result<Py<PyDict>, PyErr> {
        let data = PyDict::new(py);
        let frame_id = self.frame_id(pyframe, event);
        data.set_item("frame_id", frame_id.clone())
            .expect("a string is always a valid dict key");
        data.set_item("timestamp", utils::timestamp())
            .expect("a string is always a valid dict key");
        let (thread_name, native_id) = utils::current_thread(py)?;
        data.set_item("thread", thread_name)
            .expect("a string is always a valid dict key");
        data.set_item("thread_native_id", native_id)
            .expect("a string is always a valid dict key");

        let call_site = match utils::user_code_call_site(py, call_frames, frame_id.as_deref())? {
            Some(user_code_call_site) => {
                let call_site = PyDict::new(py);
                call_site
                    .set_item("call_frame_id", user_code_call_site.call_frame_id)
                    .expect("a string is always a valid dict key");
                call_site
                    .set_item("line_number", user_code_call_site.line_number)
                    .expect("a string is always a valid dict key");
                Some(call_site)
            }
            None => None,
        };
        data.set_item("user_code_call_site", call_site)
            .expect("a string is always a valid dict key");

        match event {
            "call" => data
                .set_item("type", &self.call_type)
                .expect("a string is always a valid dict key"),
            "return" => data
                .set_item("type", &self.return_type)
                .expect("a string is always a valid dict key"),
            _ => (),
        }
        if let Some(subtype) = &self.subtype {
            data.set_item("subtype", subtype)
                .expect("a string is always a valid dict key");
        }
        if let Some(process) = &self.process {
            data.update(
                process
                    .call1(py, (pyframe, event, arg, &self.context))?
                    .downcast(py)?,
            )?;
        }
        Ok(data.into())
    }
}

fn load_plugin_data(
    py: Python,
    plugins: &PyList,
    config: &PyDict,
) -> Result<HashMap<String, Vec<PluginProcessor>>, PyErr> {
    let mut processors: HashMap<String, Vec<PluginProcessor>> =
        HashMap::with_capacity(plugins.len());

    for plugin_data in plugins {
        let plugin_data: &PyDict = plugin_data.downcast()?;
        let co_names = PyAny::get_item(plugin_data, "co_names")?;
        let context = match plugin_data
            .get_item("build_context")
            .expect("a string is always a valid dict key")
        {
            Some(build_context) => {
                if build_context.is_none() {
                    PyDict::new(py)
                } else {
                    build_context.call1((config,))?.downcast()?
                }
            }
            None => PyDict::new(py),
        };
        for co_name in co_names.iter()? {
            let co_name: String = co_name?.extract()?;
            let processor = PluginProcessor::new(plugin_data, context)?;
            processors.entry(co_name).or_default().push(processor);
        }
    }
    Ok(processors)
}

pub fn load_plugins(
    py: Python,
    config: &PyDict,
) -> Result<HashMap<String, Vec<PluginProcessor>>, PyErr> {
    let kolo_plugins =
        PyModule::import(py, "kolo.plugins").expect("kolo.plugins should always be importable");
    let load = kolo_plugins
        .getattr("load_plugin_data")
        .expect("load_plugin_data should exist");
    let plugins: &PyList = load
        .call1((config,))
        .expect("load_plugin_data should be callable")
        .downcast()
        .expect("load_plugin_data should return a list");
    load_plugin_data(py, plugins, config)
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::_kolo::utils;
    use pyo3::exceptions::{PyKeyError, PyTypeError, PyValueError};

    fn assert_error_message(py: Python, err: PyErr, expected: &str) {
        let message: &str = err
            .value(py)
            .getattr("args")
            .unwrap()
            .get_item(0)
            .unwrap()
            .extract()
            .unwrap();
        assert_eq!(message, expected);
    }

    fn assert_keyerror(py: Python, context: &PyDict, plugin_data: &PyDict, key: &str) {
        let err = PluginProcessor::new(plugin_data, context).unwrap_err();
        assert!(err.is_instance_of::<PyKeyError>(py));
        assert!(err.value(py).getattr("args").unwrap().eq((key,)).unwrap());
    }

    fn assert_typeerror(py: Python, context: &PyDict, plugin_data: &PyDict, message: &str) {
        let err = PluginProcessor::new(plugin_data, context).unwrap_err();
        assert!(err.is_instance_of::<PyTypeError>(py));
        assert_error_message(py, err, message);
    }

    #[test]
    fn test_new() {
        pyo3::prepare_freethreaded_python();

        Python::with_gil(|py| {
            let context = PyDict::new(py);
            let plugin_data = PyDict::new(py);
            assert_keyerror(py, context, plugin_data, "path_fragment");

            plugin_data.set_item("path_fragment", py.None()).unwrap();
            assert_typeerror(
                py,
                context,
                plugin_data,
                "'NoneType' object cannot be converted to 'PyString'",
            );

            plugin_data.set_item("path_fragment", "kolo").unwrap();
            assert_keyerror(py, context, plugin_data, "call_type");

            plugin_data.set_item("call_type", py.None()).unwrap();
            assert_typeerror(
                py,
                context,
                plugin_data,
                "'NoneType' object cannot be converted to 'PyString'",
            );

            plugin_data.set_item("call_type", "call").unwrap();
            assert_keyerror(py, context, plugin_data, "return_type");

            plugin_data.set_item("return_type", py.None()).unwrap();
            assert_typeerror(
                py,
                context,
                plugin_data,
                "'NoneType' object cannot be converted to 'PyString'",
            );

            plugin_data.set_item("return_type", "return").unwrap();
            let processor = PluginProcessor::new(plugin_data, context).unwrap();
            assert!(processor.context.as_ref(py).eq(context).unwrap());
            assert_eq!(processor.call_type, "call");
            assert_eq!(processor.return_type, "return");
            assert!(processor.subtype.is_none());
            assert!(processor.call.is_none());
            assert!(processor.process.is_none());
            assert!(processor
                .filename_finder
                .find("dev/kolo/middleware.py")
                .is_some());
            assert!(processor
                .filename_finder
                .find("dev/django/middleware.py")
                .is_none());

            plugin_data.set_item("subtype", py.None()).unwrap();
            assert_typeerror(
                py,
                context,
                plugin_data,
                "'NoneType' object cannot be converted to 'PyString'",
            );

            plugin_data.set_item("subtype", "subtype").unwrap();
            let processor = PluginProcessor::new(plugin_data, context).unwrap();
            assert_eq!(processor.subtype.unwrap(), "subtype");

            plugin_data.set_item("call", py.None()).unwrap();
            let processor = PluginProcessor::new(plugin_data, context).unwrap();
            assert!(processor.call.is_none());

            plugin_data.set_item("process", py.None()).unwrap();
            let processor = PluginProcessor::new(plugin_data, context).unwrap();
            assert!(processor.process.is_none());
        })
    }

    #[test]
    fn test_matches() {
        pyo3::prepare_freethreaded_python();

        Python::with_gil(|py| {
            let context = PyDict::new(py);
            let plugin_data = PyDict::new(py);
            plugin_data.set_item("path_fragment", "kolo").unwrap();
            plugin_data.set_item("call_type", "call").unwrap();
            plugin_data.set_item("return_type", "return").unwrap();

            let processor = PluginProcessor::new(plugin_data, context).unwrap();
            let frame = PyModule::from_code(
                py,
                "
import inspect

frame = inspect.currentframe()
                ",
                "kolo/filename.py",
                "module",
            )
            .unwrap()
            .getattr("frame")
            .unwrap();
            let (filename, _) = utils::filename_with_lineno(frame.downcast().unwrap(), py).unwrap();
            let processor_match =
                processor.matches(py, &frame.into_py(py), "call", &py.None(), &filename);
            assert!(processor_match.unwrap());

            let call = PyModule::from_code(
                py,
                "def call(frame, event, arg, context):
                    return event == 'call'
                ",
                "",
                "",
            )
            .unwrap()
            .getattr("call")
            .unwrap();

            plugin_data.set_item("call", call).unwrap();
            let processor = PluginProcessor::new(plugin_data, context).unwrap();
            let processor_match =
                processor.matches(py, &frame.into_py(py), "call", &py.None(), &filename);
            assert!(processor_match.unwrap());
            let processor_match =
                processor.matches(py, &frame.into_py(py), "return", &py.None(), &filename);
            assert!(!processor_match.unwrap());

            let invalid_return_type = PyModule::from_code(
                py,
                "def call(frame, event, arg, context):
                    return 'call'
                ",
                "",
                "",
            )
            .unwrap()
            .getattr("call")
            .unwrap();

            plugin_data.set_item("call", invalid_return_type).unwrap();
            let processor = PluginProcessor::new(plugin_data, context).unwrap();
            let err = processor
                .matches(py, &frame.into_py(py), "call", &py.None(), &filename)
                .unwrap_err();
            assert!(err.is_instance_of::<PyTypeError>(py));
            assert_error_message(py, err, "'str' object cannot be converted to 'PyBool'");

            plugin_data.set_item("call", "invalid_callable").unwrap();
            let processor = PluginProcessor::new(plugin_data, context).unwrap();
            let err = processor
                .matches(py, &frame.into_py(py), "call", &py.None(), &filename)
                .unwrap_err();
            assert!(err.is_instance_of::<PyTypeError>(py));
            assert_error_message(py, err, "'str' object is not callable");
        })
    }

    #[test]
    fn test_process() {
        pyo3::prepare_freethreaded_python();

        Python::with_gil(|py| {
            let context = PyDict::new(py);
            let plugin_data = PyDict::new(py);
            plugin_data.set_item("path_fragment", "kolo").unwrap();
            plugin_data.set_item("call_type", "call").unwrap();
            plugin_data.set_item("return_type", "return").unwrap();

            let mut processor = PluginProcessor::new(plugin_data, context).unwrap();
            let frame = PyModule::from_code(
                py,
                "
import inspect

frame = inspect.currentframe()
                ",
                "kolo/filename.py",
                "module",
            )
            .unwrap()
            .getattr("frame")
            .unwrap()
            .downcast()
            .unwrap();

            let data = processor
                .process(py, frame, "call", &py.None(), vec![])
                .unwrap();
            let data = data.as_ref(py);
            let type_: &str = data.get_item("type").unwrap().unwrap().extract().unwrap();
            assert_eq!(type_, "call");
            data.get_item("thread")
                .unwrap()
                .unwrap()
                .extract::<&str>()
                .unwrap();
            data.get_item("frame_id")
                .unwrap()
                .unwrap()
                .extract::<&str>()
                .unwrap();
            data.get_item("timestamp")
                .unwrap()
                .unwrap()
                .extract::<f64>()
                .unwrap();
            data.get_item("thread_native_id")
                .unwrap()
                .unwrap()
                .extract::<u64>()
                .unwrap();

            let data = processor
                .process(py, frame, "return", &py.None(), vec![])
                .unwrap();
            let data = data.as_ref(py);
            let type_: &str = data.get_item("type").unwrap().unwrap().extract().unwrap();
            assert_eq!(type_, "return");

            let data = processor
                .process(py, frame, "other", &py.None(), vec![])
                .unwrap();
            let data = data.as_ref(py);
            assert!(data.get_item("type").unwrap().is_none());

            plugin_data.set_item("subtype", "rust").unwrap();
            let mut processor = PluginProcessor::new(plugin_data, context).unwrap();
            let data = processor
                .process(py, frame, "return", &py.None(), vec![])
                .unwrap();
            let data = data.as_ref(py);
            let subtype: &str = data
                .get_item("subtype")
                .unwrap()
                .unwrap()
                .extract()
                .unwrap();
            assert_eq!(subtype, "rust");

            let process = PyModule::from_code(
                py,
                "def process(frame, event, arg, context):
                    return {
                        'event': event,
                    }
                ",
                "",
                "",
            )
            .unwrap()
            .getattr("process")
            .unwrap();
            plugin_data.set_item("process", process).unwrap();
            let mut processor = PluginProcessor::new(plugin_data, context).unwrap();
            let data = processor
                .process(py, frame, "call", &py.None(), vec![])
                .unwrap();
            let data = data.as_ref(py);
            let event: &str = data.get_item("event").unwrap().unwrap().extract().unwrap();
            assert_eq!(event, "call");

            let invalid_return_type = PyModule::from_code(
                py,
                "def process(frame, event, arg, context):
                    return 'process'
                ",
                "",
                "",
            )
            .unwrap()
            .getattr("process")
            .unwrap();
            plugin_data
                .set_item("process", invalid_return_type)
                .unwrap();
            let mut processor = PluginProcessor::new(plugin_data, context).unwrap();
            let err = processor
                .process(py, frame, "call", &py.None(), vec![])
                .unwrap_err();
            assert!(err.is_instance_of::<PyTypeError>(py));
            assert_error_message(py, err, "'str' object cannot be converted to 'Mapping'");

            plugin_data.set_item("process", "invalid_callable").unwrap();
            let mut processor = PluginProcessor::new(plugin_data, context).unwrap();
            let err = processor
                .process(py, frame, "call", &py.None(), vec![])
                .unwrap_err();
            assert!(err.is_instance_of::<PyTypeError>(py));
            assert_error_message(py, err, "'str' object is not callable");

            let weird_mapping = PyModule::from_code(
                py,
                "
from collections.abc import Mapping


class WeirdMapping(Mapping):
    def __getitem__(self, key):
        raise ValueError('Weird')

    def __iter__(self):
        raise ValueError('Weird')

    def __len__(self):
        raise ValueError('Weird')


def process(frame, event, arg, context):
    return WeirdMapping()
                ",
                "",
                "",
            )
            .unwrap()
            .getattr("process")
            .unwrap();
            plugin_data.set_item("process", weird_mapping).unwrap();
            let mut processor = PluginProcessor::new(plugin_data, context).unwrap();
            let err = processor
                .process(py, frame, "call", &py.None(), vec![])
                .unwrap_err();
            assert!(err.is_instance_of::<PyValueError>(py));
            assert_error_message(py, err, "Weird");
        })
    }

    #[test]
    fn test_load_plugin_data() {
        pyo3::prepare_freethreaded_python();

        Python::with_gil(|py| {
            let plugins = PyList::empty(py);
            let config = PyDict::new(py);

            let processors = load_plugin_data(py, plugins, config).unwrap();
            assert_eq!(processors.len(), 0);

            let plugins = PyList::new(py, vec![py.None()]);
            let err = load_plugin_data(py, plugins, config).unwrap_err();
            assert!(err.is_instance_of::<PyTypeError>(py));
            assert_error_message(py, err, "'NoneType' object cannot be converted to 'PyDict'");

            let plugin_data = PyDict::new(py);
            let plugins = PyList::new(py, vec![plugin_data]);
            let err = load_plugin_data(py, plugins, config).unwrap_err();
            assert!(err.is_instance_of::<PyKeyError>(py));
            assert_error_message(py, err, "co_names");

            plugin_data.set_item("co_names", py.None()).unwrap();
            let err = load_plugin_data(py, plugins, config).unwrap_err();
            assert!(err.is_instance_of::<PyTypeError>(py));
            assert_error_message(py, err, "'NoneType' object is not iterable");

            plugin_data.set_item("co_names", (py.None(),)).unwrap();
            let err = load_plugin_data(py, plugins, config).unwrap_err();
            assert!(err.is_instance_of::<PyTypeError>(py));
            assert_error_message(
                py,
                err,
                "'NoneType' object cannot be converted to 'PyString'",
            );

            let weird_co_names = PyModule::from_code(
                py,
                "
def weird_gen():
    raise ValueError('Weird')
    yield

weird = weird_gen()
                ",
                "",
                "",
            )
            .unwrap()
            .getattr("weird")
            .unwrap();

            plugin_data.set_item("co_names", weird_co_names).unwrap();
            let err = load_plugin_data(py, plugins, config).unwrap_err();
            assert!(err.is_instance_of::<PyValueError>(py));
            assert_error_message(py, err, "Weird");

            plugin_data.set_item("co_names", ("foo",)).unwrap();
            let err = load_plugin_data(py, plugins, config).unwrap_err();
            assert!(err.is_instance_of::<PyKeyError>(py));
            assert_error_message(py, err, "path_fragment");

            plugin_data.set_item("path_fragment", "kolo").unwrap();
            plugin_data.set_item("call_type", "call_foo").unwrap();
            plugin_data.set_item("return_type", "return_foo").unwrap();

            let processors = load_plugin_data(py, plugins, config).unwrap();
            assert_eq!(processors.len(), 1);

            plugin_data.set_item("build_context", py.None()).unwrap();
            let processors = load_plugin_data(py, plugins, config).unwrap();
            assert_eq!(processors.len(), 1);

            plugin_data
                .set_item("build_context", "invalid callable")
                .unwrap();
            let err = load_plugin_data(py, plugins, config).unwrap_err();
            assert!(err.is_instance_of::<PyTypeError>(py));
            assert_error_message(py, err, "'str' object is not callable");

            let invalid_return_type = PyModule::from_code(
                py,
                "def build_context(config):
                    return 'invalid'
                ",
                "",
                "",
            )
            .unwrap()
            .getattr("build_context")
            .unwrap();
            plugin_data
                .set_item("build_context", invalid_return_type)
                .unwrap();
            let err = load_plugin_data(py, plugins, config).unwrap_err();
            assert!(err.is_instance_of::<PyTypeError>(py));
            assert_error_message(py, err, "'str' object cannot be converted to 'PyDict'");

            let build_context = PyModule::from_code(
                py,
                "def build_context(config):
                    return {'frame_ids': []}
                ",
                "",
                "",
            )
            .unwrap()
            .getattr("build_context")
            .unwrap();
            plugin_data
                .set_item("build_context", build_context)
                .unwrap();
            let processors = load_plugin_data(py, plugins, config).unwrap();
            assert_eq!(processors.len(), 1);
            assert_eq!(processors["foo"].len(), 1);
            assert!(processors["foo"][0]
                .context
                .as_ref(py)
                .get_item("frame_ids")
                .unwrap()
                .unwrap()
                .is_instance_of::<PyList>());
        })
    }

    #[test]
    fn test_load_plugins() {
        pyo3::prepare_freethreaded_python();

        Python::with_gil(|py| {
            let config = PyDict::new(py);
            let processors = load_plugins(py, config).unwrap();
            assert!(!processors.is_empty());
        })
    }
}
