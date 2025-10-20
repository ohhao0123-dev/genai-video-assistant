fn main() {
    let protoc = protoc_bin_vendored::protoc_bin_path().expect("failed to get vendored protoc");
    std::env::set_var("PROTOC", protoc);

    let manifest_dir = std::env::var("CARGO_MANIFEST_DIR").unwrap();
    let proto = format!("{}/proto/assistant.proto", manifest_dir);

    println!("cargo:rerun-if-changed={}", proto);
    println!("cargo:rerun-if-changed={}/proto", manifest_dir);

    tonic_build::configure()
        .compile(&[proto], &[format!("{}/proto", manifest_dir)])
        .expect("compile protos failed");
}
