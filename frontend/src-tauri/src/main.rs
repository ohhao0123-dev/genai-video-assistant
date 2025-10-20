#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

use tonic::transport::Channel;
use serde_json::json;

pub mod assistant {
    tonic::include_proto!("assistant");
}

use assistant::assistant_client::AssistantClient;
use assistant::{QueryRequest, ReportRequest};

async fn get_client() -> Result<AssistantClient<Channel>, String> {
    AssistantClient::connect("http://127.0.0.1:50051")
        .await
        .map_err(|e| e.to_string())
}

#[tauri::command]
async fn process_query(
    video_path: String,
    query: String,
    session_id: String,
) -> Result<serde_json::Value, String> {
    let mut client = get_client().await?;
    let req = QueryRequest {
        video_path,
        query,
        session_id,
    };
    let resp = client
        .process_query(req)
        .await
        .map_err(|e| format!("gRPC 调用失败: {}", e))?
        .into_inner();

    let payload = json!({
        "session_id": resp.session_id,
        "answer": resp.answer,
        "artifacts": resp.artifacts,
        "needs_clarification": resp.needs_clarification,
        "clarification_prompt": resp.clarification_prompt
    });
    Ok(payload)
}

#[tauri::command]
async fn generate_report(session_id: String, fmt: String) -> Result<serde_json::Value, String> {
    let mut client = get_client().await?;
    let req = ReportRequest {
        session_id,
        format: fmt,
    };
    let resp = client
        .generate_report(req)
        .await
        .map_err(|e| format!("gRPC 调用失败: {}", e))?
        .into_inner();

    let payload = json!({
        "session_id": resp.session_id,
        "path": resp.path
    });
    Ok(payload)
}

#[tauri::command]
async fn ping() -> Result<String, String> {
    Ok("pong".into())
}

fn main() {
    tauri::Builder::default()
        .plugin(tauri_plugin_shell::init())
        .invoke_handler(tauri::generate_handler![
            process_query,
            generate_report,
            ping
        ])
        .run(tauri::generate_context!())
        .expect("error while running Tauri application");
}
