#![doc = include_str!("../docs/introduction.md")]
#![doc = include_str!("../docs/use_rust.md")]
// # extern crate sophia;
// #![warn(missing_docs)]
// #![doc(html_favicon_url = "https://raw.github.com/MaastrichtU-IDS/knowledge-collaboratory/main/frontend/app/assets/icon.png")]
// #![doc(html_logo_url = "https://raw.github.com/MaastrichtU-IDS/knowledge-collaboratory/main/frontend/app/assets/icon.png")]
// #![doc(issue_tracker_base_url = "https://github.com/vemonet/nanopub-rs/issues/")]
// #![ no_implicit_prelude ]

// https://doc.rust-lang.org/rustdoc/write-documentation/the-doc-attribute.html
// Can't publish because outside of pkg: #![doc = include_str!("../../docs/introduction.md")]

pub mod constants;
pub mod error;
pub mod extract;
pub mod nanopub;
pub mod network;
pub mod profile;
pub mod sign;
pub mod utils;
pub use error::NpError;
/// A module to sign, publish, or check [Nanopublications](https://nanopub.net).
///
/// ## Usage
///
/// ```
/// use std::fs;
/// use nanopub::{Nanopub, NpProfile};
/// use tokio::runtime;
///
/// let private_key = "MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCjY1gsFxmak6SOCouJPuEzHNForkqFhgfHE3aAIAx+Y5q6UDEDM9Q0EksheNffJB4iPqsAfiFpY0ARQY92K5r8P4+a78eu9reYrb2WxZb1qPJmvR7XZ6sN1oHD7dd/EyQoJmQsmOKdrqaLRbzR7tZrf52yvKkwNWXcIVhW8uxe7iUgxiojZpW9srKoK/qFRpaUZSKn7Z/zgtDH9FJkYbBsGPDMqp78Kzt+sJb+U2W+wCSSy34jIUxx6QRbzvn6uexc/emFw/1DU5y7zBudhgC7mVk8vX1gUNKyjZBzlOmRcretrANgffqs5fx/TMHN1xtkA/H1u1IKBfKoyk/xThMLAgMBAAECggEAECuG0GZA3HF8OaqFgMG+W+agOvH04h4Pqv4cHjYNxnxpFcNV9nEssTKWSOvCwYy7hrwZBGV3PQzbjFmmrxVFs20+8yCD7KbyKKQZPVC0zf84bj6NTNgvr6DpGtDxINxuGaMjCt7enqhoRyRRuZ0fj2gD3Wqae/Ds8cpDCefkyMg0TvauHSUj244vGq5nt93txUv1Sa+/8tWZ77Dm0s5a3wUYB2IeAMl5WrO2GMvgzwH+zT+4kvNWg5S0Ze4KE+dG3lSIYZjo99h14LcQS9eALC/VBcAJ6pRXaCTT/TULtcLNeOpoc9Fu25f0yTsDt6Ga5ApliYkb7rDhV+OFrw1sYQKBgQDCE9so+dPg7qbp0cV+lbb7rrV43m5s9Klq0riS7u8m71oTwhmvm6gSLfjzqb8GLrmflCK4lKPDSTdwyvd+2SSmOXySw94zr1Pvc7sHdmMRyA7mH3m+zSOOgyCTTKyhDRCNcRIkysoL+DecDhNo4Fumf71tsqDYogfxpAQhn0re8wKBgQDXhMmmT2oXiMnYHhi2k7CJe3HUqkZgmW4W44SWqKHp0V6sjcHm0N0RT5Hz1BFFUd5Y0ZB3JLcah19myD1kKYCj7xz6oVLb8O7LeAZNlb0FsrtD7NU+Hciywo8qESiA7UYDkU6+hsmxaI01DsttMIdG4lSBbEjA7t4IQC5lyr7xiQKBgQCN87YGJ40Y5ZXCSgOZDepz9hqX2KGOIfnUv2HvXsIfiUwqTXs6HbD18xg3KL4myIBOvywSM+4ABYp+foY+Cpcq2btLIeZhiWjsKIrw71+Q/vIe0YDb1PGf6DsoYhmWBpdHzR9HN+hGjvwlsYny2L9Qbfhgxxmsuf7zeFLpQLijjwKBgH7TD28k8IOk5VKec2CNjKd600OYaA3UfCpP/OhDl/RmVtYoHWDcrBrRvkvEEd2/DZ8qw165Zl7gJs3vK+FTYvYVcfIzGPWA1KU7nkntwewmf3i7V8lT8ZTwVRsmObWU60ySJ8qKuwoBQodki2VX12NpMN1wgWe3qUUlr6gLJU4xAoGAet6nD3QKwk6TTmcGVfSWOzvpaDEzGkXjCLaxLKh9GreM/OE+h5aN2gUoFeQapG5rUwI/7Qq0xiLbRXw+OmfAoV2XKv7iI8DjdIh0F06mlEAwQ/B0CpbqkuuxphIbchtdcz/5ra233r3BMNIqBl3VDDVoJlgHPg9msOTRy13lFqc=";
/// let np_rdf = fs::read_to_string("./tests/resources/simple1-rsa.trig").unwrap();
/// let profile = NpProfile::new(&private_key, "https://orcid.org/0000-0000-0000-0000", "", None).unwrap();
///
/// let signed_np = Nanopub::new(&np_rdf).unwrap().sign(&profile).unwrap();
/// let checked_np = Nanopub::new(&signed_np.get_rdf().unwrap()).unwrap().check();
/// let rt = runtime::Runtime::new().expect("Failed to create Tokio runtime");
/// let published_np = rt.block_on(async {
///   Nanopub::new(&np_rdf).unwrap().publish(Some(&profile), None).await.unwrap()
/// });
/// println!("{}", published_np)
/// ```
pub use nanopub::{create_base_dataset, Nanopub};
pub use profile::NpProfile;
pub use utils::get_np_server;
