load("@npm_angular_bazel//:index.bzl", "ng_module")
#load("//tensorboard/defs:defs.bzl", "tf_ng_web_test_suite", "tf_ts_library")

package(default_visibility = ["//tensorboard:internal"])

licenses(["notice"])  # Apache 2.0

ng_module(
    name = "text_v2",
    srcs = [
        "text_component.ts",
        "text_container.ts",
        "text_module.ts",
    ],
    assets = [
        "text_component.css",
        "text_component.ng.html",
    ],
    deps = [
        "//tensorboard/webapp/plugins:plugin_registry",
        "//tensorboard/webapp/webapp_data_source:http_client",
        "@npm//@angular/common",
        "@npm//@angular/core",
    ],
)

