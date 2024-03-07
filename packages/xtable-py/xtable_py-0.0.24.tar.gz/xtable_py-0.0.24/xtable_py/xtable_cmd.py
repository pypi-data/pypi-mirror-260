import jpype
import jpype.imports
import jpype.types
from urllib import request
from pathlib import Path


def sync(
    config: Path,
    jars: Path,
    catalog: Path = None,
):
    # Launch the JVM
    jpype.startJVM(classpath=jars / "*")
    run_sync = jpype.JPackage("io").onetable.utilities.RunSync.main

    # call java class
    if catalog:
        run_sync(["--datasetConfig", config, "--icebergCatalogConfig", catalog])

    else:
        run_sync(["--datasetConfig", config])

    # shutdown
    jpype.shutdownJVM()


def setup(jars: Path):
    # vars
    urls = {
        "iceberg-spark-runtime-3.4_2.12-1.4.2.jar": "https://repo1.maven.org/maven2/org/apache/iceberg/iceberg-spark-runtime-3.4_2.12/1.4.2/iceberg-spark-runtime-3.4_2.12-1.4.2.jar",
        "iceberg-aws-bundle-1.4.2.jar": "https://repo1.maven.org/maven2/org/apache/iceberg/iceberg-aws-bundle/1.4.2/iceberg-aws-bundle-1.4.2.jar",
        "utilities-0.1.0-SNAPSHOT-bundled.jar": "https://d1bjpw1aruo86w.cloudfront.net/05eb631ce7f32184ac864b6f1cc81db8/utilities-0.1.0-SNAPSHOT-bundled.jar",
    }

    # download jars
    for jar, url in urls.items():
        if not (jars / jar).exists():
            print(f"Downloading {jar} ...")
            request.urlretrieve(
                url,
                jars / jar,
            )
