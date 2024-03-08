use std::fs;
use takeoff_config::schema::{AppConfig, ReaderConfig};
use utoipa::OpenApi;

fn gen_my_openapi() -> String {
    #[derive(OpenApi)]
    #[openapi(components(schemas(AppConfig, ReaderConfig)))]
    struct ApiDoc;

    ApiDoc::openapi().to_pretty_json().unwrap()
}

fn main() {
    let doc = gen_my_openapi();
    fs::write(
        "../../hermes/external/docs_container/docs/openapi_docs/takeoff_config.json",
        doc,
    )
    .unwrap();
}
